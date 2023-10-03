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
import numpy as np
import logging as log
from time import time
from openvino.inference_engine import IENetwork, IEPlugin


def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", help="Path to an .xml file with a trained model.", required=True, type=str)
    parser.add_argument("-i", "--input", help="Path to a folder with images or path to an image files", required=True,
                        type=str, nargs="+")
    parser.add_argument("-l", "--cpu_extension",
                        help="MKLDNN (CPU)-targeted custom layers.Absolute path to a shared library with the kernels "
                             "impl.", type=str, default=None)
    parser.add_argument("-pp", "--plugin_dir", help="Path to a plugin folder", type=str, default=None)
    parser.add_argument("-d", "--device",
                        help="Specify the target device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device specified (CPU by default)", default="CPU",
                        type=str)
    parser.add_argument("--labels", help="Labels mapping file", default=None, type=str)
    parser.add_argument("-nt", "--number_top", help="Number of top results", default=10, type=int)
    parser.add_argument("-ni", "--number_iter", help="Number of inference iterations", default=1, type=int)
    parser.add_argument("-pc", "--perf_counts", help="Report performance counters", default=False, action="store_true")

    return parser


def main():
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
    args = build_argparser().parse_args()
    model_xml = args.model
    model_bin = os.path.splitext(model_xml)[0] + ".bin"
    

    # Plugin initialization for specified device and load extensions library if specified
    plugin = IEPlugin(device=args.device, plugin_dirs=args.plugin_dir)
    if args.cpu_extension and 'CPU' in args.device:
        plugin.add_cpu_extension(args.cpu_extension)
    else:
        plugin.set_config({"PERF_COUNT":"YES"})
    # Read IR
    log.info("Loading network files:\n\t{}\n\t{}".format(model_xml, model_bin))
    net = IENetwork(model=model_xml, weights=model_bin)

    if plugin.device == "CPU":
        supported_layers = plugin.get_supported_layers(net)
        not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        if len(not_supported_layers) != 0:
            log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      format(plugin.device, ', '.join(not_supported_layers)))
            log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                      "or --cpu_extension command line argument")
            sys.exit(1)

    assert len(net.inputs.keys()) == 1, "Sample supports only single input topologies"
    assert len(net.outputs) == 1, "Sample supports only single output topologies"

    log.info("Preparing input blobs")
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    net.batch_size = len(args.input)

    # Read and pre-process input images
    n, c, h, w = net.inputs[input_blob].shape
    images = np.ndarray(shape=(n, c, h, w))
    for i in range(n):
        image = cv2.imread(args.input[i])
        if image.shape[:-1] != (h, w):
            log.warning("Image {} is resized from {} to {}".format(args.input[i], image.shape[:-1], (h, w)))
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        images[i] = image
    log.info("Batch size is {}".format(n))

    # Loading model to the plugin
    log.info("Loading model to the plugin")
    exec_net = plugin.load(network=net,num_requests=2)
    
    del net
    # Start sync inference
    log.info("Starting inference ({} iterations)".format(args.number_iter))
    infer_time = []
    for i in range(args.number_iter):
        t0 = time()
        res = exec_net.infer(inputs={input_blob: images})
        infer_time.append((time()-t0)*1000)
    # Processing output blob
    log.info("Processing output blob")
    res = res[out_blob]
    log.info("Top {} results: ".format(args.number_top))
    if args.labels:
        with open(args.labels, 'r') as f:
            labels_map = [x.split(sep=' ', maxsplit=0)[-1].strip() for x in f]
    else:
        labels_map = None
    for i, probs in enumerate(res):                                            
        probs = np.squeeze(probs)
        top_ind = np.argsort(probs)[-args.number_top:][::-1]
        for id in top_ind:
            det_label = labels_map[id] if labels_map else "#{}".format(id)
            
            print("{:<5}{:.7f} label {}".format(id,probs[id], det_label))
        print("\n")
    total_inference=np.sum(np.asarray(infer_time))
    log.info("Average running time of one iteration: {:.2f} ms".format(np.average(np.asarray(infer_time))))
    log.info("total running time of inference: {:.2f} ms" .format(total_inference))
    log.info("Throughput: {:.2f} FPS".format((1000*args.number_iter*n)/total_inference))
    print("\n")

    #printing performance counts

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
    

if __name__ == '__main__':
    sys.exit(main() or 0)
