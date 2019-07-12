from IPython.core.display import HTML, Markdown
import ipywidgets as widgets
import subprocess
import json
import os.path

class DemoCatalog:

    def __init__(self, config_file):
        self.config_file = config_file
        with open(config_file, "r") as config:
            self.conf = json.load(config)
            config.close()
        with open(self.conf['css']) as css:
            self.css = css.read()
            css.close()

    def ShowRepositoryControls(self):
        url, status, lastCheck, fullstatus = self.GetStatus()
        msgs = self.conf['status']['messages']
        if int(status) == 0:
            c = 'uptodate'
        elif int(status) == 1:
            c = 'behind'
        elif int(status) == 2:
            c = 'ahead'
        else:
            c = 'unable'
        v = msgs[c].format(time=lastCheck)

        display(HTML(self.css))

        w_url = widgets.HTML(value=("{remote}: {remote_url}").format(remote=msgs['remote'], remote_url=url))
        w_time = widgets.HTML(value=("{time}: {lastCheck}").format(time=msgs['lastCheck'], lastCheck=lastCheck))
        w_git = widgets.HTML(value=("{gitsaid}: {gitline}").format(gitsaid=msgs['gitsaid'], gitline=fullstatus))
        w_hint = widgets.HTML(value=msgs['foreword'])
        w_refresh=widgets.Button(description=self.conf['status']['button'])
        w_info=widgets.VBox([w_refresh, w_hint, w_url, w_time, w_git])
        w_acc=widgets.Accordion(children=[w_info], selected_index=None)
        w_acc.set_title(0, v)
        w_acc.add_class(c)
        display(w_acc)
        
        self.refreshButton = w_refresh
        self.refreshButton.on_click(self.RefreshRepository)

    def ShowCatalog(self):
        self.ShowIntro()
        self.ShowListOfDemos()
        
    def ShowIntro(self):
        if (self.conf['intro']):
            with open("README.md", "r") as readme:
                cont=readme.read()
                readme.close()
            display(Markdown(cont))

    def ShowListOfDemos(self):
        data = "## "+self.conf['list']['header']+"\n"
        for lab in self.conf['list']['labs']:
            lab_dir=os.path.dirname(lab)
            with open(lab_dir+"/README.md", "r") as readme:
                cont=readme.read()
                readme.close()
                data += cont
            data += "  "  # forces a newline
            title = cont[0]
            data += "\n<a href='"+lab+"' target='_blank' class='big-jupyter-button'>"+self.conf['list']['messages']['goto']+": "+lab+"</a>\n"
        display(Markdown(data))

    def GetStatus(self):
        cmd = self.conf['status']['serverSideStatusScript']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output,_ = p.communicate()
        data = output.decode().split("\n")
        return data[0], data[1], data[2], data[3]
        
    def RefreshRepository(self, evt):
        self.refreshButton.disabled = True
        cmd = self.conf['status']['serverSideRefreshScript']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output,_ = p.communicate()
        display(HTML(self.conf['status']['reloadCode']))

    def Anchor(self, name):
        display(HTML("<a class='"+name+"'></a>"))

    def Autorun(self, name):
        display(HTML("<script>"+
                     "function ClickRunGenerate() {"+
                     "  var code_cells = document.getElementsByClassName('code_cell');"+
                     "  if (code_cells.length > 0) {"+
                     "    var i;"+
                     "    for (i = 0; i < code_cells.length; i++) {"+
                     "      var anch = code_cells[i].getElementsByClassName('"+name+"');"+
                     "      if (anch.length > 0) {"+
                     "        var rtc = code_cells[i].getElementsByClassName('run_this_cell');"+
                     "        if (rtc.length > 0) {"+
                     "          var j;"+
                     "          for (j = 0; j < rtc.length; j++) {"+
                     "            rtc[j].click();"+
                     "          }"+
                     "        }"+
                     "      }"+
                     "    }"+
                     "  }"+
                     "  if ("+self.conf['status']['autorunInterval']+" > 0) {"+
                     "    setTimeout(ClickRunGenerate, "+self.conf['status']['autorunInterval']+");"+
                     "  }"+
                     "}"+
                     "setTimeout(ClickRunGenerate, "+self.conf['status']['autorunFirstDelay']+");"+
                     "</script>"))

    def ToggleCode(self):
        display(HTML("<script>"+
                     "codeShow=true;"+
                     "function CodeToggle() {"+
                     "  if (codeShow) {"+
                     "    $('div.input').hide();"+
                     "  } else {"+
                     "    $('div.input').show();"+
                     "  }"+
                     "  codeShow = !codeShow;"+
                     "}"+
                     "$( document ).ready(CodeToggle);"+
                     "</script>"+
                     "<form action='javascript:CodeToggle()'><input type='submit' value='"+self.conf['messages']['toggle']+"'></form>"))
