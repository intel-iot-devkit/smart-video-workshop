import sys
import os
import cv2
import time
import numpy as np
import io


def placeBoxes(res, labels_map, prob_threshold, frame, initial_w, initial_h, is_async_mode, cur_request_id, det_time):
    for obj in res[0][0]:
        # Draw only objects when probability more than specified threshold
        if obj[2] > prob_threshold:
            xmin = int(obj[3] * initial_w)
            ymin = int(obj[4] * initial_h)
            xmax = int(obj[5] * initial_w)
            ymax = int(obj[6] * initial_h)
            class_id = int(obj[1])
            # Draw box and label\class_id
            inf_time_message = "Inference time: N\A for async mode" if is_async_mode else \
                    "Inference time: {:.3f} ms".format(det_time * 1000)
            async_mode_message = "Async mode is on. Processing request {}".format(cur_request_id) if is_async_mode else \
                    "Async mode is off. Processing request {}".format(cur_request_id)
            color = (min(class_id * 12.5, 255), min(class_id * 7, 255), min(class_id * 5, 255))
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
            det_label = labels_map[class_id] if labels_map else str(class_id)
            cv2.putText(frame, det_label + ' ' + str(round(obj[2] * 100, 1)) + ' %', (xmin, ymin - 7), cv2.FONT_HERSHEY_COMPLEX, 0.6, color, 1)
            cv2.putText(frame, inf_time_message, (15, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
            cv2.putText(frame, async_mode_message, (10, int(initial_h - 20)), cv2.FONT_HERSHEY_COMPLEX, 0.5,(10, 10, 200), 1)

    return frame

def post_process(input_stream, res_arr, labels_map, prob_threshold, out_path, det_time, is_async_mode):
    post_process = time.time()
    cap = cv2.VideoCapture(input_stream)
    if cap.isOpened():   
        width  = int(cap.get(3))
        height = int(cap.get(4))
        vw = cv2.VideoWriter(out_path, 0x00000021, 50.0, (width, height), True)
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        initial_w = cap.get(3)
        initial_h = cap.get(4)
        if i < res_arr.shape[0]:
            res = res_arr[i]
            if len(det_time): det_time_val = det_time.pop(0)
            if i%2 == 0: frame = placeBoxes(res, labels_map, prob_threshold, frame, initial_w, initial_h, is_async_mode, i, det_time_val)
        vw.write(frame)
        i+=1
        key = cv2.waitKey(1)
        if key == 27:
            break
    print("Post processing time: {0} sec" .format(time.time()-post_process))
    cap.release()
    vw.release()


