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

import sys
import os
from argparse import ArgumentParser
import cv2
import logging as log
import struct
import collections



def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="Path to video file or image. 'cam' for capturing video stream from camera", required=True,
                        type=str)    
    parser.add_argument("-l", "--labels", help="Labels mapping file", required=True, type=str)
    parser.add_argument("--ROIfile",help="Path to ROI file.",default="ROIs.txt",type=str)
    parser.add_argument("-b", help="Batch size", default=0, type=int)
    parser.add_argument('-o', '--output_dir',
                        help='Location to store the results of the processing',
                        default=None,
                        required=True,
                        type=str)
    return parser

class ROI_data_type:
    framenum=""
    labelnum=""
    confidence=""
    xmin=""
    ymin=""
    xmax=""
    ymax=""
    
def main():
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
    args = build_argparser().parse_args()
    batch=args.b
    ROIs = collections.deque()
    assert os.path.isfile(args.ROIfile), "Specified ROIs.txt file doesn't exist"
    
    fin=open("ROIs.txt",'r')
    for l in fin:
        R=ROI_data_type()
        batchnum,R.framenum,R.labelnum,R.confidence,R.xmin,R.ymin,R.xmax,R.ymax=l.split()
        if int(batchnum)==batch:
            ROIs.append(R)

    if args.input == 'cam':
        input_stream = 0
    else:
        input_stream = args.input
        assert os.path.isfile(args.input), "Specified input file doesn't exist"
        
  #  print("opening", args.input," batchnum ",args.b,"\n")
    
    cap = cv2.VideoCapture(input_stream)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(os.path.join(args.output_dir, "cars_output.mp4"),0x00000021,fps,(width,height))

    if not cap.isOpened():
        print("could not open input video file")
    framenum=0
    if len(ROIs)>1:
        R=ROIs[0]
    else:
        print("empty ROI file");
    if args.labels:
        with open(args.labels, 'r') as f:
            labels_map = [x.strip() for x in f]
    else:
        labels_map = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ncols=cap.get(3)
        nrows=cap.get(4)
        while int(R.framenum)<framenum:
            if len(ROIs)>1:
                ROIs.popleft()
                R=ROIs[0];
            else:
                break
        while int(R.framenum)==framenum:
            xmin = int(float(R.xmin) * float(ncols))
            ymin = int(float(R.ymin) * float(nrows))
            xmax = int(float(R.xmax) * float(ncols))
            ymax = int(float(R.ymax) * float(nrows))
            
            class_id=int(float(R.labelnum)+1)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0),4,16,0)

            if len(labels_map)==0:
                templabel=int(float(R.labelnum))+":"+int(R.confidence*100.0)
                print(templabel)
            else:
                templabel=str(labels_map[int(float(R.labelnum))])+":"+str(int(float(R.confidence)*100.0))
                
            cv2.rectangle(frame, (xmin, ymin+32), (xmax, ymin), (155, 155, 155),-1,0)
            cv2.putText(frame, templabel, (xmin, ymin+24), cv2.FONT_HERSHEY_COMPLEX, 1.1, (0, 0, 0),3)
            
            if len(ROIs)>1:
                ROIs.popleft()
                R=ROIs[0]
            else:
                break
        time = (1/20)
        out.write(frame)   
        #cv2.imshow("Detection Results", frame)
        if cv2.waitKey(30)>=0:
            break
        if len(ROIs)<=1:
            break
        framenum+=1   
    cap.release()
        
main()

