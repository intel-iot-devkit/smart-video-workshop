#!/usr/bin/env python
"""
 Copyright (c) 2018 Intel Corporation

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
import time
import numpy as np
import math
import logging as log
from PIL import Image
from openvino.inference_engine import IENetwork, IEPlugin
CV_PI=3.1415926535897932384626433832795

def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", help="Path to an .xml file with a trained model.", required=True, type=str)
    parser.add_argument("-m_ag", "--ag_model", help="Path to an .xml file with a trained model.", default=None, type=str)
    parser.add_argument("-m_hp", "--hp_model", help="Path to an .xml file with a trained model.", default=None, type=str)
    parser.add_argument("-m_em", "--em_model", help="Path to an .xml file with a trained model.", default=None, type=str)
    parser.add_argument("-m_lm", "--lm_model", help="Path to an .xml file with a trained model.", default=None, type=str)
    parser.add_argument("-pc", "--perf_counts", help="Report performance counters", default=False, action="store_true")
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
    parser.add_argument("-d_ag", "--device_ag",
                        help="Target device for Age/Gender Recognition network (CPU, GPU, FPGA, or MYRIAD). The demo will look for a suitable plugin for a specified device. (CPU by default)", default="CPU",
                        type=str)
    parser.add_argument("-d_hp", "--device_hp",
                        help="Target device for Head Pose Estimation network (CPU, GPU, FPGA, or MYRIAD). The demo will look for a suitable plugin for a specified device. (CPU by default)", default="CPU",
                        type=str)
    parser.add_argument("-d_em", "--device_em",
                        help="Target device for Emotions Recognition network (CPU, GPU, FPGA, or MYRIAD). The demo will look for a suitable plugin for a specified device.(CPU by default)", default="CPU",
                        type=str)
    parser.add_argument("-d_lm", "--device_lm",
                        help="Target device for Facial Landmarks Estimation network (CPU, GPU, FPGA, or MYRIAD). The demo will look for a suitable plugin for device specified.(CPU by default)", default="CPU",
                        type=str)
    
    parser.add_argument("--labels", help="Labels mapping file", default=None, type=str)
    parser.add_argument("-pt", "--prob_threshold", help="Probability threshold for detections filtering",
                        default=0.5, type=float)
    parser.add_argument("-no_show", "--no_show", help="do not show processed video",
                        default=False, action="store_true")
    parser.add_argument("-r", "--raw", help="raw_output_message",
                        default=False, action="store_true")
    return parser

emotions = ["neutral", "happy", "sad", "surprise", "anger"]

def drawAxes(pitch,yaw,roll,cpoint,frame):

    pitch *= CV_PI/180.0	
    yaw *= CV_PI/180.0
    roll *= CV_PI/180.0

    yawMatrix = np.matrix([[math.cos(yaw), 0, -math.sin(yaw)], [0, 1, 0], [math.sin(yaw), 0, math.cos(yaw)]])                    
    pitchMatrix = np.matrix([[1, 0, 0],[0, math.cos(pitch), -math.sin(pitch)], [0, math.sin(pitch), math.cos(pitch)]])
    rollMatrix = np.matrix([[math.cos(roll), -math.sin(roll), 0],[math.sin(roll), math.cos(roll), 0], [0, 0, 1]])                    

    #Rotational Matrix
    R = yawMatrix * pitchMatrix * rollMatrix
    rows=frame.shape[0]
    cols=frame.shape[1]

    cameraMatrix=np.zeros((3,3), dtype=np.float32)
    cameraMatrix[0][0]= 950.0
    cameraMatrix[0][2]= cols/2
    cameraMatrix[1][0]= 950.0
    cameraMatrix[1][1]= rows/2
    cameraMatrix[2][1]= 1
   
    xAxis=np.zeros((3,1), dtype=np.float32)
    xAxis[0]=50
    xAxis[1]=0
    xAxis[2]=0

    yAxis=np.zeros((3,1), dtype=np.float32)
    yAxis[0]=0
    yAxis[1]=-50
    yAxis[2]=0
    
    zAxis=np.zeros((3,1), dtype=np.float32)
    zAxis[0]=0
    zAxis[1]=0
    zAxis[2]=-50
                   
    zAxis1=np.zeros((3,1), dtype=np.float32)
    zAxis1[0]=0
    zAxis1[1]=0
    zAxis1[2]=50

    o=np.zeros((3,1), dtype=np.float32)
    o[2]=cameraMatrix[0][0]

    xAxis=R*xAxis+o
    yAxis=R*yAxis+o
    zAxis=R*zAxis+o
    zAxis1=R*zAxis1+o

    p2x=int((xAxis[0]/xAxis[2]*cameraMatrix[0][0])+cpoint[0])
    p2y=int((xAxis[1]/xAxis[2]*cameraMatrix[1][0])+cpoint[1])
    cv2.line(frame,(cpoint[0],cpoint[1]),(p2x,p2y),(0,0,255),2)

    p2x=int((yAxis[0]/yAxis[2]*cameraMatrix[0][0])+cpoint[0])
    p2y=int((yAxis[1]/yAxis[2]*cameraMatrix[1][0])+cpoint[1])
    cv2.line(frame,(cpoint[0],cpoint[1]),(p2x,p2y),(0,255,0),2)

    p1x=int((zAxis1[0]/zAxis1[2]*cameraMatrix[0][0])+cpoint[0])
    p1y=int((zAxis1[1]/zAxis1[2]*cameraMatrix[1][0])+cpoint[1])

    p2x=int((zAxis[0]/zAxis[2]*cameraMatrix[0][0])+cpoint[0])
    p2y=int((zAxis[1]/zAxis[2]*cameraMatrix[1][0])+cpoint[1])
 
    cv2.line(frame,(p1x,p1y),(p2x,p2y),(255,0,0),2)
    cv2.circle(frame,(p2x,p2y),3,(255,0,0))

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
    age_enabled = False
    headPose_enabled = False
    emotions_enabled = False
    landmarks_enabled = False  
  
    log.info("Reading IR...")
    # Face detection
    #log.info("Loading network files for Face Detection") 
    plugin,net=load_model("Face Detection",args.model,args.device.upper(),args.plugin_dir,1,1,args.cpu_extension)
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    exec_net = plugin.load(network=net, num_requests=2)
    n, c, h, w = net.inputs[input_blob].shape
    del net

    # age and gender   
    if args.model and args.ag_model:
       age_enabled =True
       #log.info("Loading network files for Age/Gender Recognition") 
       plugin,ag_net = load_model("Age/Gender Recognition",args.ag_model,args.device_ag.upper(),args.plugin_dir,1,2,args.cpu_extension)
       age_input_blob=next(iter(ag_net.inputs))
       age_out_blob=next(iter(ag_net.outputs))
       age_exec_net=plugin.load(network=ag_net, num_requests=2)
       ag_n, ag_c, ag_h, ag_w = ag_net.inputs[input_blob].shape
       del ag_net
       
    # Head Pose  
    if args.model and args.hp_model:
        headPose_enabled = True
        #log.info("Loading network files for Head Pose Estimation") 
        plugin,hp_net=load_model("Head Pose Estimation",args.hp_model,args.device_hp,args.plugin_dir,1,3,args.cpu_extension)
        hp_input_blob=next(iter(hp_net.inputs))
        hp_out_blob=next(iter(hp_net.outputs))
        hp_exec_net=plugin.load(network=hp_net, num_requests=2)
        hp_n, hp_c, hp_h, hp_w = hp_net.inputs[input_blob].shape
        del hp_net

    # Emotions  
    if args.model and args.em_model:
        emotions_enabled = True
        #log.info("Loading network files for Emotions Recognition")
        plugin,em_net=load_model("Emotions Recognition",args.em_model,args.device_em.upper(),args.plugin_dir,1,1,args.cpu_extension)
        em_input_blob=next(iter(em_net.inputs))
        em_out_blob=next(iter(em_net.outputs))
        em_exec_net=plugin.load(network=em_net, num_requests=2)
        em_n, em_c, em_h, em_w = em_net.inputs[input_blob].shape
        del em_net

    # Facial Landmarks
    if args.model and args.lm_model:
        landmarks_enabled = True
        #log.info("Loading network files for Facial Landmarks Estimation")
        plugin,lm_net=load_model("Facial Landmarks Estimation",args.lm_model,args.device_lm.upper(),args.plugin_dir,1,1,args.cpu_extension)
        lm_input_blob=next(iter(lm_net.inputs))
        lm_out_blob=next(iter(lm_net.outputs))
        lm_exec_net=plugin.load(network=lm_net, num_requests=2)
        lm_n, lm_c, lm_h, lm_w = lm_net.inputs[input_blob].shape
        del lm_net

    total_start = time.time()
 
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

    cap = cv2.VideoCapture(input_stream)
    if not cap.isOpened():
        sys.exit(1)
    cur_request_id = 0
    log.info("Starting inference ...")
    log.info("To stop the demo execution press Esc button")
    is_async_mode = True
    render_time = 0
    framesCounter = 0
    decode_time = 0
    visual_time = 0
    
    decode_prev_start = time.time()
    ret, frame = cap.read()
    decode_prev_finish = time.time()
    decode_prev_time = decode_prev_finish - decode_prev_start
    while cap.isOpened():
        analytics_time = 0
        decode_next_start = time.time()
        ret, frame = cap.read()
        decode_next_finish = time.time()
        decode_next_time = decode_next_finish - decode_next_start
        if not ret:
            break

        framesCounter+=1
        initial_w = cap.get(3)
        initial_h = cap.get(4)

        inf_start = time.time()
        in_frame = cv2.resize(frame, (w, h))
        in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        in_frame = in_frame.reshape((n, c, h, w))
        exec_net.start_async(request_id=cur_request_id, inputs={input_blob: in_frame})            
        if exec_net.requests[cur_request_id].wait(-1) == 0:
            inf_end = time.time()
            det_time = inf_end - inf_start

            #analytics_start_time =time.time()
            # Parse detection results of the current request
            res = exec_net.requests[cur_request_id].outputs[out_blob]
            for obj in res[0][0]:
                # Draw only objects when probability more than specified threshold
                if obj[2] > args.prob_threshold:
                    xmin = int(obj[3] * initial_w)
                    ymin = int(obj[4] * initial_h)
                    xmax = int(obj[5] * initial_w)
                    ymax = int(obj[6] * initial_h)

                    #Crop the face rectangle for further processing
                    clippedRect = frame[ymin:ymax, xmin:xmax]  
                    if (clippedRect.size)==0:
                       continue                     			
                  
                    height = ymax - ymin
                    width = xmax -xmin  

                    #Age and Gender
                    age_inf_time=0
                    if age_enabled:
                        age_inf_start = time.time()
                        clipped_face = cv2.resize(clippedRect, (ag_w, ag_h))
                        clipped_face = clipped_face.transpose((2, 0, 1))  # Change data layout from HWC to CHW
                        clipped_face = clipped_face.reshape((ag_n, ag_c, ag_h, ag_w))
                        ag_res = age_exec_net.start_async(request_id=0,inputs={'data': clipped_face})
                        if age_exec_net.requests[cur_request_id].wait(-1) == 0:
                            age_inf_end = time.time()
                            age_inf_time=age_inf_end - age_inf_start
                    #Heapose
                    hp_inf_time=0        
                    if headPose_enabled:
                        hp_inf_start = time.time()
                        clipped_face_hp = cv2.resize(clippedRect, (hp_w, hp_h))
                        clipped_face_hp = clipped_face_hp.transpose((2, 0, 1))  # Change data layout from HWC to CHW
                        clipped_face_hp = clipped_face_hp.reshape((hp_n, hp_c, hp_h, hp_w))
                        hp_res = hp_exec_net.start_async(request_id=0,inputs={'data': clipped_face_hp})
                        if hp_exec_net.requests[cur_request_id].wait(-1) == 0:
                            hp_inf_end = time.time()
                            hp_inf_time=hp_inf_end - hp_inf_start                       
                    #Emotion
                    em_inf_time=0      
                    if emotions_enabled:
                        em_inf_start = time.time()
                        clipped_face_em = cv2.resize(clippedRect, (em_w, em_h))
                        clipped_face_em = clipped_face_em.transpose((2, 0, 1))  # Change data layout from HWC to CHW
                        clipped_face_em = clipped_face_em.reshape((em_n, em_c, em_h, em_w))
                        em_res = em_exec_net.start_async(request_id=0,inputs={'data': clipped_face_em})
                        if em_exec_net.requests[cur_request_id].wait(-1) == 0:
                            em_inf_end = time.time()
                            em_inf_time=em_inf_end - em_inf_start                      

                    #Landmarks
                    lm_inf_time=0
                    if landmarks_enabled:
                        lm_inf_start = time.time()
                        clipped_face_lm = cv2.resize(clippedRect, (lm_w, lm_h))
                        clipped_face_lm = clipped_face_lm.transpose((2, 0, 1))  # Change data layout from HWC to CHW
                        clipped_face_lm = clipped_face_lm.reshape((lm_n, lm_c, lm_h, lm_w))
                        lm_exec_net.start_async(request_id=0,inputs={'data': clipped_face_lm})
                        if lm_exec_net.requests[cur_request_id].wait(-1) == 0:
                            lm_inf_end = time.time()
                            lm_inf_time=lm_inf_end - lm_inf_start
                            
                    analytics_time = age_inf_time + hp_inf_time + em_inf_time + lm_inf_time

                    visual_start = time.time()                                   
                    if args.no_show==False:    
                        if age_enabled:
                            age = int((age_exec_net.requests[cur_request_id].outputs['age_conv3'][0][0][0][0])*100)
                    
                            if(((age_exec_net.requests[cur_request_id].outputs['prob'][0][0][0][0])) > 0.5):
                                gender = 'F'
                                cv2.putText(frame, str(gender) + ','+str(age), (xmin, ymin - 7), cv2.FONT_HERSHEY_COMPLEX, 0.6, (10,10,200), 1)
                                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10,10,200), 2)
                            else:
                                gender = 'M'
                                cv2.putText(frame, str(gender) + ','+str(age), (xmin, ymin - 7), cv2.FONT_HERSHEY_COMPLEX, 0.6, (10,10,200), 1)
                                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 10, 10), 2)
                            if args.raw:
                                print("Predicted gender, age = {},{}".format(gender, age) )
                        else:
                            class_id = int(obj[1])                                     
                            # Draw box and label\class_id
                            color = (min(class_id * 12.5, 255), min(class_id * 7, 255), min(class_id * 5, 255))
                            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                            det_label = labels_map[class_id] if labels_map else str(class_id)
                            cv2.putText(frame, 'label' + ' ' + '#' + det_label + ': ' + str(obj[2]) ,(xmin, ymin - 7), \
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (10,10,200), 1)

                        if headPose_enabled:
                            pitch = ((hp_exec_net.requests[cur_request_id].outputs['angle_p_fc'][0][0]))
                            yaw   = ((hp_exec_net.requests[cur_request_id].outputs['angle_y_fc'][0][0]))
                            roll  = ((hp_exec_net.requests[cur_request_id].outputs['angle_r_fc'][0][0]))
                            cpoint=[int(xmin + (width/2)),int(ymin + (height/2))]
                            drawAxes(pitch,yaw,roll,cpoint,frame)
                            if args.raw:
                                print("Head pose results: yaw, pitch, roll = {}, {}, {}".format(yaw, pitch,roll))                                

                        if emotions_enabled:
                            emotion_values = em_exec_net.requests[cur_request_id].outputs['prob_emotion']                   
                            emotion_type = emotion_values.argmax()
                            result = emotions[emotion_type]
                            cv2.putText(frame, ',' + result,(xmin + 40, ymin - 7), cv2.FONT_HERSHEY_COMPLEX, 0.6, (10,10,200), 1)
                            if args.raw:
                                print("Predicted emotion = {}".format(result))
                        if landmarks_enabled:
                            if args.raw:
                                print("Normed Facial Landmarks coordinates (x, y):")
                            for i_lm in range(0,35):
                                normed_x= lm_exec_net.requests[0].outputs['align_fc3'][0][2*i_lm]
                                normed_y= lm_exec_net.requests[0].outputs['align_fc3'][0][(2*i_lm)+ 1]                                
                                x_lm = xmin + width * normed_x;
                                y_lm = ymin + height * normed_y;                            
                                cv2.circle(frame, (int(x_lm), int(y_lm)), 1+int(0.019 * width), (0,255,255), -1)
                                if args.raw:
                                    print(normed_x, normed_y)                                
                        
                        render_time_message = "OpenCV cap/rendering time: {:.2f} ms".format(render_time * 1000)
                        inf_time_message = "Face Detection time: {:.2f} ms ({:.2f} fps)".format((det_time * 1000),1/(det_time))           
                        if (clippedRect.size)!= 0 and analytics_time:
                            Face_analytics_time_message = "Face Analytics Networks time: {:.2f} ms ({:.2f} fps)".format((analytics_time * 1000),1/(analytics_time))
                        else:
                            Face_analytics_time_message = "Face Analytics Networks time: {:.2f} ms".format((analytics_time * 1000))

                        cv2.putText(frame, render_time_message, (15, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
                        cv2.putText(frame, inf_time_message, (15, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
                        if age_enabled or headPose_enabled or emotions_enabled or landmarks_enabled:
                            cv2.putText(frame, Face_analytics_time_message, (15,45), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
                        
                        # Rendering time
                        cv2.imshow("Detection Results", frame)
                        visual_end = time.time()
                        visual_time = visual_end - visual_start
        
                        render_end = time.time()
                        render_time = decode_prev_time + decode_next_time + visual_time
                    elif args.raw:
                        if age_enabled:
                            age = int((age_exec_net.requests[cur_request_id].outputs['age_conv3'][0][0][0][0])*100)                    
                            if(((age_exec_net.requests[cur_request_id].outputs['prob'][0][0][0][0])) > 0.5):
                                gender = 'F'
                            else:
                                gender = 'M'
                            print("Predicted gender, age = {},{}".format(gender, age) )
                        if emotions_enabled:
                            emotion_values = em_exec_net.requests[cur_request_id].outputs['prob_emotion']                   
                            emotion_type = emotion_values.argmax()
                            result = emotions[emotion_type]
                            print("Predicted emotion = {}".format(result))
                        if headPose_enabled:
                            pitch = ((hp_exec_net.requests[cur_request_id].outputs['angle_p_fc'][0][0]))
                            yaw   = ((hp_exec_net.requests[cur_request_id].outputs['angle_y_fc'][0][0]))
                            roll  = ((hp_exec_net.requests[cur_request_id].outputs['angle_r_fc'][0][0]))
                            print("Head pose results: yaw, pitch, roll = {}, {}, {}".format(yaw, pitch,roll))
                        if landmarks_enabled:
                            print("Normed Facial Landmarks coordinates (x, y):")
                            for i_lm in range(0,35):
                                normed_x= lm_exec_net.requests[0].outputs['align_fc3'][0][2*i_lm]
                                normed_y= lm_exec_net.requests[0].outputs['align_fc3'][0][(2*i_lm)+ 1]
                                x_lm = xmin + width * normed_x;
                                y_lm = ymin + height * normed_y;
                                print(normed_x, normed_y)
            
            key = cv2.waitKey(1)
            if key == 27:
                break
    total_finish = time.time()
    total= total_finish - total_start
    print("Total image throughput: ({:.2f} fps)".format(framesCounter*(1/total)))
    # Showing performance results
    if args.perf_counts:        
        perf_counts=exec_net.requests[0].get_perf_counts()
        print("performance counts:\n")
        total=0
        for layer, stats in perf_counts.items():
            total+=stats['real_time']
            print ("{:<40} {:<15} {:<10} {:<15} {:<8} {:<5} {:<5} {:<5} {:<10} {:<15}".format(layer, stats['status'], 'layerType:', stats['layer_type'], 'realTime:', stats['real_time'], 'cpu:', stats['cpu_time'],'execType:', stats['exec_type'] ))
        print ("{:<20} {:<7} {:<20}".format('TotalTime:',total ,'microseconds'))

    cv2.destroyAllWindows()
    log.info("Number of processed frames: {}".format(framesCounter))
    del exec_net
    del plugin
    log.info("Execution successful")

if __name__ == '__main__':
    sys.exit(main() or 0)
