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
import logging as log
from openvino.inference_engine import IENetwork, IEPlugin
from enum import Enum
import collections



class output_mode_type(Enum):
    CLASSIFICATION_MODE=1
    SSD_MODE=2


def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", help="Path to an .xml file with a trained model.", required=True, type=str)
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
    parser.add_argument("--labels", help="Labels mapping file", default=None, type=str)
    parser.add_argument("-pt", "--prob_threshold", help="Probability threshold for detections filtering",
                        default=0.5, type=float)
    parser.add_argument("-fr", help="maximum frames to process", default=256, type=int)
    parser.add_argument("-b", help="Batch size", default=1, type=int)
    
    return parser


def main():
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
    args = build_argparser().parse_args()
    model_xml = args.model
    model_bin = os.path.splitext(model_xml)[0] + ".bin"
    args.cpu_extension="/opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release/lib/libcpu_extension.so"

    preprocess_times = collections.deque()
    infer_times = collections.deque()
    postprocess_times = collections.deque()
    
    ROIfile=open("ROIs.txt","w"); # output stored here, view with ROIviewer
    
    # Plugin initialization for specified device and load extensions library if specified
    log.info("Initializing plugin for {} device...".format(args.device))
    plugin = IEPlugin(device=args.device, plugin_dirs=args.plugin_dir)
    if args.cpu_extension and 'CPU' in args.device:
        plugin.add_cpu_extension(args.cpu_extension)

        
    # Read IR
    log.info("Reading IR...")
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

    #Set Batch Size
    batchSize = args.b
    frameLimit = args.fr
    assert len(net.inputs.keys()) == 1, "Demo supports only single input topologies"
    assert len(net.outputs) == 1, "Demo supports only single output topologies"
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    log.info("Loading IR to the plugin...")
    exec_net = plugin.load(network=net, num_requests=2)
       
    # Read and pre-process input image
    n, c, h, w = net.inputs[input_blob].shape
    output_dims=net.outputs[out_blob].shape
    infer_width=w;
    infer_height=h;
    num_channels=c;
    channel_size=infer_width*infer_height
    full_image_size=channel_size*num_channels
    
    print("inputdims=",w,h,c,n)
    print("outputdims=",output_dims[3],output_dims[2],output_dims[1],output_dims[0])
    if int(output_dims[3])>1 :
        print("SSD Mode")
        output_mode=output_mode_type.SSD_MODE
    else:
        print("Single Classification Mode")
        output_mode=CLASSIFICATION_MODE
        output_data_size=int(output_dims[2])*int(output_dims[1])*int(output_dims[0])
    del net
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

    cur_request_id = 0
    next_request_id = 1

    log.info("Starting inference in async mode...")
    is_async_mode = True
    render_time = 0

    framenum = 0
    process_more_frames=True
    frames_in_output=batchSize
    
    while process_more_frames:
        time1 = time.time()
        for mb in range(0 , batchSize):
            ret, frame = cap.read()
            if not ret or (framenum >= frameLimit):
                process_more_frames=False
                frames_in_output=mb
                break

            # convert image to blob
            # Fill input tensor with planes. First b channel, then g and r channels
            in_frame = cv2.resize(frame, (w, h))
            in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
            in_frame = in_frame.reshape((n, c, h, w))
			
        time2 = time.time()
        diffPreProcess = time2 - time1
        if process_more_frames:
            preprocess_times.append(diffPreProcess*1000)
            
        # Main sync point:
        # in the truly Async mode we start the NEXT infer request, while waiting for the CURRENT to complete
        # in the regular mode we start the CURRENT request and immediately wait for it's completion
        inf_start = time.time()
        if is_async_mode:
            exec_net.start_async(request_id=next_request_id, inputs={input_blob: in_frame})
        else:
            exec_net.start_async(request_id=cur_request_id, inputs={input_blob: in_frame})
        if exec_net.requests[cur_request_id].wait(-1) == 0:
            inf_end = time.time()
            det_time = inf_end - inf_start
            infer_times.append(det_time*1000)
            time1 = time.time()

            # Parse detection results of the current request
            res = exec_net.requests[cur_request_id].outputs[out_blob]
            for obj in res[0][0]:
                # Write into ROIs.txt only objects when probability more than specified threshold
            	if obj[2] > args.prob_threshold:
                    confidence=obj[2]
                    locallabel = obj[1] - 1
                    print(str(0),str(framenum),str(locallabel),str(confidence),str(obj[3]),str(obj[4]),str(obj[5]),str(obj[6]), file=ROIfile)

        
        sys.stdout.write("\rframenum:"+str(framenum))
        sys.stdout.flush()
        render_start = time.time()
        framenum = framenum+1   
        time2 = time.time()
        diffPostProcess = time2 - time1
        postprocess_times.append(diffPostProcess*1000)

        if is_async_mode:
            cur_request_id, next_request_id = next_request_id, cur_request_id

            
    print("\n")
    preprocesstime=0
    inferencetime=0
    postprocesstime=0
    
    for obj in preprocess_times:
         preprocesstime+=obj
    for obj in infer_times:
        inferencetime+=obj
    for obj in postprocess_times:
        postprocesstime+=obj

        
    print("Preprocess: ",preprocesstime/(len(preprocess_times)*batchSize),"\tms/frame")
    print("Inference:  ",inferencetime/(len(infer_times)*batchSize),"\tms/frame")
    print("Postprocess:" ,postprocesstime/(len(postprocess_times)*batchSize),"\tms/frame")

    del exec_net
    del plugin


if __name__ == '__main__':
    sys.exit(main() or 0)
