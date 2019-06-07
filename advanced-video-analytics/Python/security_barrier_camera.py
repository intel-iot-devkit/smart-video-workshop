#!/usr/bin/env python
"""
 Copyright (c) 2019 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from __future__ import print_function
import sys
import os
from argparse import ArgumentParser
import cv2
import numpy as np
import time
import logging as log
from  openvino.inference_engine import IENetwork, IEPlugin


def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", help="Path to an .xml file with a trained model.", required=True, type=str)
    parser.add_argument("-m_va", "--model_va", help="Path to an .xml file with a trained model.",  type=str, default=None )
    parser.add_argument("-m_lpr", "--model_lpr", help="Path to an .xml file with a trained model.",  default=None ,type=str )
    parser.add_argument("-i", "--input",
                        help="Path to video file or image. 'cam' for capturing video stream from camera", required=True,
                        type=str)
    parser.add_argument("-l", "--cpu_extension",
                        help="MKLDNN (CPU)-targeted custom layers.Absolute path to a shared library with the kernels "
                             "impl.", type=str, default=None)
    parser.add_argument("-pp", "--plugin_dir", help="Path to a plugin folder", type=str, default=None)
    parser.add_argument("-d", "--device",
                        help="Specify the target device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. Demo "
                             "will look for a suitable plugin for device specified (CPU by default)", default="CPU",
                        type=str)
    parser.add_argument("-d_va", "--device_va",
                        help="Specify the target device for Vehicle Attributes (CPU, GPU, FPGA, MYRIAD, or HETERO).(CPU by default)", default="CPU",
                        type=str)
    parser.add_argument("-d_lpr", "--device_lpr",
                        help="Specify the target device for License Plate Recognition (CPU, GPU, FPGA, MYRIAD, or HETERO).(CPU by default)", default="CPU",
                        type=str)
    parser.add_argument("--labels", help="Labels mapping file", default=None, type=str)
    parser.add_argument("-pt", "--prob_threshold", help="Probability threshold for detections filtering",
                        default=0.5, type=float)
    parser.add_argument("-ni", "--ni_required", help="n infer request message",default=1, type=int)
    parser.add_argument("-pc", "--perf_counts", help="Report performance counters", default=False, action="store_true")

    return parser


colors = ["white", "gray", "yellow", "red", "green", "blue", "black"]
types  = ["car", "van", "truck", "bus"]
items  = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
          "<Anhui>", "<Beijing>", "<Chongqing>", "<Fujian>",
          "<Gansu>", "<Guangdong>", "<Guangxi>", "<Guizhou>",
          "<Hainan>", "<Hebei>", "<Heilongjiang>", "<Henan>",
          "<HongKong>", "<Hubei>", "<Hunan>", "<InnerMongolia>",
          "<Jiangsu>", "<Jiangxi>", "<Jilin>", "<Liaoning>",
          "<Macau>", "<Ningxia>", "<Qinghai>", "<Shaanxi>",
          "<Shandong>", "<Shanghai>", "<Shanxi>", "<Sichuan>",
          "<Tianjin>", "<Tibet>", "<Xinjiang>", "<Yunnan>",
          "<Zhejiang>", "<police>",
          "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
          "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
          "U", "V", "W", "X", "Y", "Z"]
maxSequenceSizePerPlate = 88

def load_model(feature,model_xml,device,plugin_dirs,input_key_length,output_key_length,cpu_extension):

    model_bin = os.path.splitext(model_xml)[0] + ".bin"

    log.info("Initializing plugin for {} device...".format(device))
    plugin = IEPlugin(device, plugin_dirs)

    log.info("Loading network files for {}".format(feature))
    if cpu_extension and 'CPU' in device:
        plugin.add_cpu_extension(cpu_extension)
    else:
        plugin.set_config({"PERF_COUNT":"YES"})

    net = IENetwork(model=model_xml, weights=model_bin)

    if plugin.device == "CPU":
        supported_layers = plugin.get_supported_layers(net)
        not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        if len(not_supported_layers) != 0:
            log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      format(plugin.device, ', '.join(not_supported_layers)))
            log.error("Please try to specify cpu extensions library path in demo's command line parameters using -l "
                      "or --cpu_extension command line argument")
            sys.exit(1)
    
    log.info("Checking {} network inputs".format(feature))
    assert len(net.inputs.keys()) == input_key_length, "Demo supports only single input topologies"
    log.info("Checking {} network outputs".format(feature))
    assert len(net.outputs) == output_key_length, "Demo supports only single output topologies"
    return plugin,net


def main():
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
    args = build_argparser().parse_args()
    va_enabled=False
    lpr_enabled=False

    #Make sure only one IEPlugin was created for one type of device
    plugin,net = load_model("Vehicle Detection",args.model,args.device,args.plugin_dir,1,1,args.cpu_extension)    
    
    if args.model and args.model_va:
        plugin_va,va_net = load_model("Vehicle Attribute Detection",args.model_va,args.device_va,args.plugin_dir,1,2,args.cpu_extension)
        if args.device == args.device_va:
            plugin_va = plugin
            if args.model and args.model_lpr:
                plugin_lpr,lpr_net=load_model("License Plate Recognition",args.model_lpr,args.device_lpr,args.plugin_dir,2,1,args.cpu_extension)
                if args.device == args.device_lpr:                    
                    plugin_lpr = plugin

                    
        elif args.model and args.model_lpr:
            plugin_lpr,lpr_net=load_model("License Plate Recognition",args.model_lpr,args.device_lpr,args.plugin_dir,2,1,args.cpu_extension)
            if args.device_va == args.device_lpr:
                plugin_lpr = plugin_va
            elif args.device == args.device_lpr:    
                plugin_lpr = plugin                    
                                        

    elif args.model and args.model_lpr:
        plugin_lpr,lpr_net=load_model("License Plate Recognition",args.model_lpr,args.device_lpr,args.plugin_dir,2,1,args.cpu_extension)
        if args.device == args.device_lpr:
            plugin_lpr = plugin

            
                
    
    #Vehicle Detection
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    log.info("Loading IR to the plugin...")

    exec_net = plugin.load(network=net, num_requests=2)
    n, c, h, w = net.inputs[input_blob].shape
    del net
    
    #For Vehicle Attribute Detection
    if args.model and args.model_va :
        va_enabled=True
        va_input_blob=next(iter(va_net.inputs))
        va_out_blob=next(iter(va_net.outputs))
        va_exec_net = plugin_va.load(network=va_net, num_requests=2)
        n_va,c_va,h_va,w_va = va_net.inputs[va_input_blob].shape
        del va_net
        
    #For License Plate Recognition   
    if args.model and args.model_lpr:
        lpr_enabled=True
        lpr_input_data_blob=next(iter(lpr_net.inputs))
        lpr_seqBlob=next(iter(lpr_net.inputs))
        lpr_out_blob = next(iter(lpr_net.outputs))
        lpr_seqBlob=[[0.0]]
        for i in range(1,maxSequenceSizePerPlate):
            lpr_seqBlob[0].append(1.0)

        lpr_exec_net = plugin_lpr.load(network=lpr_net, num_requests=2)
        n_lpr,c_lpr,h_lpr,w_lpr =lpr_net.inputs['data'].shape
        del lpr_net


    if args.input == 'cam':
        input_stream = 0
    else:
        input_stream = args.input
        assert os.path.isfile(args.input), "Specified input file doesn't exist"
    if args.labels:
        with open(args.labels, 'r') as f:
            labels_map = [x.strip() for x in f]
    else:
        labels_map = None

    log.info("Starting inference ...")
    log.info("To stop the demo execution press Esc button")
    render_time = 0
    lpr_det_time=0
    va_det_time=0
    framecount=0
    
    while True:
        img=cv2.imread(input_stream)
        initial_w = img.shape[1]
        initial_h = img.shape[0]
        framecount+=1
        inf_start = time.time()
    
        in_frame = cv2.resize(img, (w, h))
        in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        in_frame = in_frame.reshape((n, c, h, w))
        exec_net.start_async(request_id=0, inputs={input_blob: in_frame})
        infer_status = exec_net.requests[0].wait()
        if infer_status == 0:
            inf_end = time.time()
            det_time = inf_end - inf_start

            # Parse detection results of the current request
            res = exec_net.requests[0].outputs[out_blob]
            
            for obj in res[0][0]:
                # Draw only objects when probability more than specified threshold
                if obj[2] > args.prob_threshold:
                    xmin = int(obj[3] * initial_w)
                    ymin = int(obj[4] * initial_h)
                    xmax = int(obj[5] * initial_w)
                    ymax = int(obj[6] * initial_h)
                    class_id = int(obj[1])
                    
                    # Draw box and label\class_id
                    color = (min(class_id * 12.5, 255), min(class_id * 7, 255), min(class_id * 5, 255))
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0,255,0), 2)
                    clippedRect=img[ymin:ymax, xmin:xmax]
                    det_label = labels_map[class_id] if labels_map else str(class_id)
                    # For vehicle attribute recognition
                    if det_label == '1' and va_enabled:
                        va_inf_start = time.time()
                        in_frame = cv2.resize(clippedRect, (w_va, h_va))
                        in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
                        in_frame = in_frame.reshape((n_va, c_va, h_va, w_va))
                        va_exec_net.start_async(request_id=0, inputs={va_input_blob: in_frame})
                        va_infer_status= va_exec_net.requests[0].wait()
                        va_inf_end = time.time()
                        va_det_time=va_inf_end-va_inf_start
                        colorsValues= va_exec_net.requests[0].outputs['color']
                        typesValues= va_exec_net.requests[0].outputs['type']
                        color_id=colorsValues.argmax()
                        type_id=typesValues.argmax()
                        cv2.putText(img, colors[color_id] , (xmin+2, ymin +15),cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,0,0), 1, cv2.LINE_AA)
                        cv2.putText(img, types[type_id] , (xmin+2, ymin+30),cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,0,0), 1, cv2.LINE_AA)
                    #For lpr recognition
                    elif det_label == '2' and lpr_enabled:
                        lpr_inf_start = time.time()
                        in_frame=cv2.resize(clippedRect,(w_lpr,h_lpr))
                        in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
                        in_frame = in_frame.reshape((n_lpr, c_lpr, h_lpr, w_lpr))
                        lpr_exec_net.start_async(request_id=0, inputs={'data': in_frame, 'seq_ind': (lpr_seqBlob[0][1])})
                        status=lpr_exec_net.requests[0].wait(-1)
                        lpr_inf_end = time.time()
                        lpr_det_time = lpr_inf_end - lpr_inf_start
                        lpr_res=lpr_exec_net.requests[0].outputs[lpr_out_blob]
                        result=""
                        for i in range(0,lpr_res.size):
                            if lpr_res[0][i] != -1:
                                 result+=items[int(lpr_res[0][i])]
                            else:
                                cv2.putText(img, result , (xmin, ymin +50),cv2.FONT_HERSHEY_COMPLEX, 0.6, (0,0,255), 1, cv2.LINE_AA)
                                break

            #Inference Statistics  
            inf_time_message = "Time for processing 1 stream (nireq ={}): {:.3f} ms ({} fps)".format(args.ni_required,(det_time * 1000),int(1/det_time))
            render_time_message = "Rendering time ({}): {:.3f} ms".format(args.device,render_time * 1000)
            vehicle_detection_time="Vehicle detection time ({}) : {:.3f} ms ({} fps)".format(args.device,(det_time*1000),int(1/(det_time)/framecount))
            if va_det_time :
                vehicle_attrib_time_message="Vehicle Attribs time({}) : {:.3f} ms ({} fps)".format(args.device_va,(va_det_time*1000),int(1/(va_det_time)/framecount))
                cv2.putText(img, vehicle_attrib_time_message, (0, 60), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
            if lpr_det_time :
                lpr_time_message="Lpr recognition time({}) : {:.2f} ms ({} fps)".format(args.device_lpr,(lpr_det_time*1000),int(1/(lpr_det_time)/framecount))
                cv2.putText(img, lpr_time_message, (0, 80), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
            cv2.putText(img, inf_time_message, (0, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1,cv2.LINE_AA)
            cv2.putText(img, vehicle_detection_time, (0, 40), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1,cv2.LINE_AA)

            cv2.imshow("Detection Results", img)
 
 
            key = cv2.waitKey(0)
            if key == 27:
                break
    if args.perf_counts:        
        perf_counts=exec_net.requests[0].get_perf_counts()
        print("performance counts:\n")
        total=0
        for layer, stats in perf_counts.items():
            total+=stats['real_time']
            print ("{:<40} {:<15} {:<10} {:<15} {:<8} {:<5} {:<5} {:<5} {:<10} {:<15}".format(layer, stats['status'], 'layerType:', stats['layer_type'], 'realTime:', stats['real_time'], 'cpu:', stats['cpu_time'],'execType:', stats['exec_type'] ))
        print ("{:<20} {:<7} {:<20}".format('TotalTime:',total ,'microseconds'))
    log.info("Execution successful")
              
    del exec_net
    del plugin
    cv2.destroyAllWindows()
if __name__ == '__main__':
    sys.exit(main() or 0)
