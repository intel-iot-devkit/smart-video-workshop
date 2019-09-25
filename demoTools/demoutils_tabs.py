from IPython.core.display import HTML
import threading
from IPython.display import display, Image
import ipywidgets as widgets
from ipywidgets import Layout
import time
import queue
import subprocess
import datetime
import matplotlib
import matplotlib.pyplot as plt
import os 
import warnings
import json
import random
import io
import urllib, base64
import urllib.parse

def progressUpdate(file_name, time_diff, frame_count, video_len):
        progress = round(100*(frame_count/video_len), 1)
        remaining_time = round((time_diff/frame_count)*(video_len-frame_count), 1)
        estimated_time = round((time_diff/frame_count)*video_len, 1)
        with  open(file_name, "w") as progress_file:
            progress_file.write(str(progress)+'\n')
            progress_file.write(str(remaining_time)+'\n')
            progress_file.write(str(estimated_time)+'\n')
    
class Demo:

	def __init__(self, config):
		container_list = []
		self.command = config["job"]["command"] if "command" in config["job"] else ""
		self.output_type = config["job"]["output_type"]
		self.results_path = config["job"]["results_path"]
		if "results_defines" in config["job"]:
			self.results_defines = config["job"]["results_defines"]
			self.command = self.command.replace(self.results_defines, self.results_path)
		self.progress_list = config["job"]["progress_indicators"] if "progress_indicators" in config["job"] else None
		if "plots" in config["job"]:
			self.plot = config["job"]["plots"]
			self.plot_button = widgets.Button(description='Plot results' , disabled=True, button_style='info')
			self.plot_img = widgets.HTML('')
			container_list = [self.plot_button, self.plot_img]
		else:
			self.plot = None
		self.status = widgets.HTML("No jobs submitted yet")
		self.submit = widgets.Button(description='Submit', disabled=False, button_style='info')
		self.submit.disabled = False if "inputs" in config else True
		self.input_ = []
		self.jobDict = {}
		self.tab = widgets.Tab()
		self.tab.children = []
		self.display_tab = False
		data=config["inputs"] if "inputs" in config else []
		self.container = widgets.VBox([self.status, self.tab]+container_list)


	                  
		for item in data:
			for key, val in item.items():
				dict_ = {}
				name = key
				dict_['name'] = key
				if val['type'] == "select":
					list_ = []
					for x in val['options']:
						list_.append(x['name'])
					widget = widgets.Select(options=list_, description='', disabled=False, rows=len(list_), layout = Layout(width='fixed'))
					dict_["options"] = val["options"]
				elif val['type'] == "text":
					widget = widgets.Text(value=val['default'], description="", layout = Layout(width='100%'), disabled=False)
				dict_['widget'] = widget
				dict_['type'] = val["type"]
				dict_['defines'] = val['defines'] 
				dict_['title'] = widgets.Label(val['display_name'])
				self.input_.append(dict_)

	def submitJob(self, command): 
		self.command = command
		for widget in self.input_:

			value = widget["widget"].value
			if widget["type"] == "select":
				try:
					defines_dict = next(item for item in widget["options"] if item['name'] == value)
				except:
					self.status.value = "<span style='color:red'>&#9888;</span> Job submission failed, Invalid selection"
					return

				if 'defines' in defines_dict:
					for key2, val2 in defines_dict['defines'].items():
						command = command.replace(key2, val2)
				elif "dummy" in defines_dict and defines_dict["dummy"] == "True":
					self.status.value = "<span style='color:red'>&#9888;</span> Job submission failed, {}".format(defines_dict['name'])
					return
			else:	
				for item in widget['defines']:
					command = command.replace(item, value) 
		if not command in self.jobDict.keys():
			self.jobDict[command] = {}
			self.jobDict[command]['box_id'] = None
		elif self.jobStillRunning(command):
			self.status.value = "<span style='color:red'>&#10008;</span> Unable to submit: another job with the same arguments is still running"
			return

		p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		output,_ = p.communicate()
		jobid = output.decode("utf-8").rstrip()
		if jobid != "":
			self.status.value = "<span style='color:green'>&#10004;</span> Job submitted, job ID: {jobid}".format(jobid=jobid)
		else:
			self.status.value = "<span style='color:red'>&#9888;</span> Job submission failed"
			return

		self.jobDict[command]['jobid'] = jobid 
		std_path = self.results_path+jobid
		if not os.path.isdir(std_path):
			os.makedirs(std_path, exist_ok=True)
		command2 = "qalter -o {outpath} -e {errorpath} {jobid}".format(outpath=std_path+"/stdout", errorpath=std_path+"/stderr", jobid=jobid)
		p2 = subprocess.Popen(command2, stdout=subprocess.PIPE, shell=True)
		output2,_ = p2.communicate()
		self.jobDict[command]['selector'] = {}
		for item in self.input_:
			self.jobDict[command]['selector'][item['title'].value] = item['widget'].value
		self.jobDict[command]['output_path'] = self.results_path+jobid
		self.outputDisplay(jobid, command, 0, 100)
		if self.plot:
			self.plot_button.on_click(self.summaryPlot)

	def displayUI(self):
		n_widgets = []
		for widget in self.input_:
			n_widgets.append(widgets.VBox([widget['title'], widget['widget']]))
		UI = widgets.VBox(n_widgets)
		display(UI)		
		if not self.submit.disabled:
			display(self.submit)
		display(self.container)

		def on_value_change(change):
			controller = next(widget for widget in self.input_ if widget['widget'].description == change['owner'].description) 
			selected = next( option for option in controller['options'] if option['name'] == change['new'])
			for key, val in selected['controls'].items():
				controlled = next(widget for widget in self.input_ if widget['name'] == key)
				controlled['widget'].options = val

		for widget in self.input_:
			if widget['type'] == 'select':
				for item in widget['options']:
					observer = True if 'controls' in item else False
				widget['observer'] = observer
			if 'observer' in widget and widget['observer']:
				widget['widget'].observe(on_value_change, 'value') 
		def wrapSubmit(event):
			self.submitJob(self.command)
				
		self.submit.on_click(self.submitJob)

	def outputDisplay(self, jobid, command, min_, max_):
		'''
		Progress indicator reads first line in the file "path" 
		jobid: id of the job submitted
		command: qsub command 
		min_: min_ value for the progress bar
		max_: max value in the progress bar
		'''
		progress_info = []
		progress_wid = []
		path = self.results_path+jobid
		style = {'description_width': 'initial'}
		title = widgets.HTML("")
		if self.progress_list:
			for item in self.progress_list:
				progress_info.append(path+'/'+item['file_name'])
				progress_wid.append(widgets.FloatProgress(value=min_, min=min_, max=max_, description=item["title"], bar_style='info', orientation='horizontal', style=style))
				progress_wid.append(widgets.HTML(value='...waiting to start', placeholder='0', description='', style=style))  #Estimated time
				progress_wid.append(widgets.HTML(value='', placeholder='0', description='', style=style))			#Remaining time

			for name in progress_info:
				f = open(name, "w")
				f.close()
		def _work():
			box_layout = widgets.Layout(display='flex', flex_flow='column', align_items='stretch', border='ridge', width='100%', height='')
			frame_layout = widgets.Layout(display='flex', flex_flow='column', align_items='stretch', border='', width='100%', height='')
			table = '''<table><style type="text/css" scoped>td{ padding:5px; border: 1px solid #9e9e9e; line-height:1.2em;}td:first-child{font-weight:bold;}</style><tbody>'''
			for item in self.input_:
				table += '''<tr><td>{name}</td><td>{value}</td></tr>'''.format(name=item['title'].value, value=item['widget'].value)
			table += '''<tr><td>Submission command</td><td>{command}</td></tr>'''.format(command=command)
			table += '''</tbody></table>'''
			title = widgets.HTML(value = '''{table}'''.format(table=table))
			op_display_button = widgets.Button(description='Display output', disabled=True, button_style='info')
			op_display = widgets.HTML(value='')
			widget_list = [title]+progress_wid+[op_display_button, op_display]

			if self.jobDict[command]['box_id'] == None:
				frame = widgets.HBox(widget_list, layout=frame_layout)
				cur_tabs = list(self.tab.children)
				cur_tabs.append(frame)
				self.tab.children = tuple(cur_tabs)
				self.tab.set_title(str(len(self.tab.children)-1),  '{jobid}'.format(jobid=jobid))
				frame_id = len(self.tab.children)-1
				self.jobDict[command]['box_id'] = frame_id
				self.tab.selected_index = frame_id
			else:
				frame_id = self.jobDict[command]['box_id']
				frame = self.tab.children[frame_id]
				#output.value = ""
				op_display_button.disabled=True
				frame.children = widget_list
				self.tab.set_title(str(frame_id), '{jobid}'.format(jobid=jobid.split(".")[0]))
				self.tab.selected_index = frame_id
			#if not self.display_tab: 
				#display(self.tab)
			#	if self.plot:
			#		display(self.plot_button)
			#		display(self.plot_img)
			#	self.display_tab = True
			# progress
			id_ = 0
			self.tab.set_title(str(frame_id), 'Queued: {jobid}'.format(jobid=jobid.split(".")[0]))
			cmd = "qstat | grep "+jobid
			running = False
			while not running:
				p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
				output,_ = p.communicate()
				stat = output.decode("utf-8").rsplit()
				running = True if stat[4]=='R' else False
 
			self.tab.set_title(str(frame_id), 'Running: {jobid}'.format(jobid=jobid.split(".")[0]))
			for output_file in progress_info: 
				progress_bar =  progress_wid[id_]
				est_time =  progress_wid[id_+1]
				remain_time =  progress_wid[id_+2]
				last_status = 0.0
				remain_val = '0'
				est_val = '0'
				while last_status < 100:
					if os.path.isfile(output_file):
						with open(output_file, "r") as fh:
							line1 = fh.readline() 	#Progress 
							line2 = fh.readline()  	#Remaining time
							line3 = fh.readline()  	#Estimated total time
							if line1 and line2 and line3:
								last_status = float(line1)
								remain_val = line2
								est_val = line3
							progress_bar.value = last_status
							if remain_val > '0':
								remain_time.value = 'Remaining: {} seconds'.format(remain_val)
								est_time.value = 'Total estimated: {} seconds'.format(est_val) 
							else:
								remain_time.value = '...waiting to start' 
					else:
						cmd = ['ls']
						p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
						output,_ = p.communicate()
					time.sleep(0.1)
				remain_time.value = 'Done' 
				os.remove(output_file)
				id_ += 3

			while self.jobStillRunning(command):
				time.sleep(0.1) 
			if self.plot:
				self.plot_button.disabled=False
			self.tab.set_title(str(frame_id), 'Done: {jobid}'.format(jobid=jobid.split(".")[0]))
			op_display_button.disabled=False
			def wrapHTML(event):
				op_display.value = self.outputHTML(path)

			op_display_button.on_click(wrapHTML)

		thread = threading.Thread(target=_work, args=())
		thread.start()
		time.sleep(0.1)

	def jobStillRunning (self, command):
		''' Input: command
			Return: True if job still running, false if job terminated
		'''
		cmd = 'qstat '+self.jobDict[command]['jobid']
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		output,_ = p.communicate()
		return output.decode("utf-8").rstrip() != ''

	def outputHTML(self, result_path):
		'''
		device: tuple of edge and accelerator
		'''
		op_list = []
		stats = result_path+'/stats.json'
		for file_ in os.listdir(result_path):
			if file_.endswith(self.output_type):
				op_list.append(result_path+'/'+file_)
		if os.path.isfile(stats):
			with open(stats) as f:
				data = json.load(f)
			time = data['time']
			frames = data['frame']
			stats_line = "<p>{frames} frames processed in {time} seconds</p>".format(frames=frames, time=time)
		else:
			stats_line = ""
		string = ""
		height = '480' if len(op_list) == 1 else '240'
		if self.output_type == ".mp4":
			for x in op_list:
				string += "<video alt=\"\" controls autoplay height=\"{height}\"><source src=\"{op}\" type=\"video/mp4\" /></video>".format(op=x, height=height)
		elif self.output_type == ".png":
			for x in op_list:
				string += "<img src='{img}' width='783' height='{height}'>".format(img=x, height=height)
		elif self.output_type == ".txt":
			for x in op_list:
				with open(x, 'r') as f:
					string += str(f.readlines())

		return '''<h2></h2>
    				{stats_line}
    				{op}
    				'''.format(op=string, stats_line=stats_line)
					

	def summaryPlot(self, event):
		''' Bar plot input:
		   x_axis: label of the x axis
		   y_axis: label of the y axis
		   title: title of the graph
		'''
		
		warnings.filterwarnings('ignore')
		clr = 'xkcd:blue'
		html = '''<html><body>'''
		for item in self.plot: 
			fig = plt.figure(figsize=(15, 5))
			title = item['title']
			type = item['type']
			y_axis = item['ylabel'] if 'ylabel' in item else None 
			x_axis = item['xlabel'] if 'xlabel' in item else None 
			selector = item['selector'] if 'selector' in item else None
			plt.title(title , fontsize=20, color='black', fontweight='bold')
			plt.ylabel(y_axis, fontsize=16, color=clr)
			plt.xlabel(x_axis, fontsize=16, color=clr)
			val = []
			arch = {}
			diff = 0

			for key, val in self.jobDict.items():
				job = self.jobDict[key]
				path = os.path.join(val['output_path'], 'stats.json')
				label = {"selector" : val['selector'][selector]} if selector else {"selector" : val["jobid"]}
				if os.path.isfile(path) and not self.jobStillRunning(key):
					with open(path, "r") as f:
						data = json.load(f)
					value = float(data[item["type"]])
					for key2, val2 in label.items():
						arch[val2] = round(value, 2)

			if len(arch) <= 9:
				rotation=0
				align="center"
			else:
				rotation=45
				align="right"
			plt.xticks(fontsize=16, rotation=rotation, rotation_mode='anchor', horizontalalignment=align)
			plt.yticks(fontsize=16)
			if len(arch) != 0:
				# set offset
				max_val = max(arch.values()) 
				offset = max_val/100
				plt.ylim(top=(max_val+10*offset))
				for dev, val in arch.items():
					y = val+offset
					plt.text(diff, y, val, fontsize=14, multialignment="center",horizontalalignment="center", verticalalignment="bottom",  color='black')
					diff += 1
					plt.bar(dev, val, width=0.5, align='center', label = dev, color=clr)
				imgdata = io.BytesIO()
				plt.tight_layout()
				fig.savefig(imgdata, format='png')
				html += '''<img src="data:image/png;base64,{}"/>'''.format(base64.encodebytes(imgdata.getvalue()).decode()) 
				plt.close()
			else:
				plt.close()
		html += '''</body></html>'''
		self.plot_img.value = html
