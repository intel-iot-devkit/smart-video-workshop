# Object detection with YOLOv3 model and Intel® Distribution of OpenVINO™ toolkit

This tutorial uses a TensorFlow* implementation of YOLOv3 model for object detection using the Intel® Distribution of OpenVINO™ toolkit with two key components: Model Optimizer and Inference Engine.

Model Optimizer is a cross-platform command-line tool that takes pre-trained deep learning models and optimizes them for performance/space using conservative topology transformations. Inference engine provides a common API to deploy the deep learning model on hardware of choice.

### Install TensorFlow*

Check the TensorFlow* version
	
	pip3 list | grep tensorflow

If the Tensorflow* version is NOT 1.12, then

	pip3 install tensorflow==1.12

### Download the YOLOv3 TensorFlow* model
All YOLO* models are originally implemented in the DarkNet* framework and consist of two files:
.cfg file with model configurations and
.weights file with model weights
#### 1. Clone the repository

	export SV=/opt/intel/workshop/smart-video-workshop/
	cd $SV/object-detection/
	git clone https://github.com/mystic123/tensorflow-yolo-v3.git
	cd tensorflow-yolo-v3

#### 2. Checkout the commit that the conversion was tested on

	git checkout ed60b90

#### 3. Download coco.names file from the DarkNet website OR use labels that fit your task.

	wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names

#### 4. Download the yolov3.weights

	wget https://pjreddie.com/media/files/yolov3.weights

#### 5. Run a converter to freeze the graph

	python3 convert_weights_pb.py --class_names coco.names --data_format NHWC --weights_file yolov3.weights

## Part 1: Optimize a deep-learning model using the Model Optimizer (MO)

In this section, you will use the Model Optimizer to convert a trained model to two Intermediate Representation (IR) files (one .bin and one .xml). The Inference Engine requires this model conversion so that it can use the IR as input and achieve optimum performance on Intel hardware.

#### 1. Create a directory to store IR files

	cd $SV/object-detection/tensorflow-yolo-v3
	mkdir -p FP32


#### 2. Run the Model Optimizer on the frozen  YOLOv3 TensorFlow* model. This step generates one .xml file and one .bin file and place both files in the tutorial samples directory (located here: /object-detection/tensorflow-yolo-v3/FP32/)

	python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo_tf.py --input_model frozen_darknet_yolov3_model.pb --batch 1 --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/yolo_v3.json -o $SV/object-detection/tensorflow-yolo-v3/FP32

> **Note:** if you continue to train or make changes to the model, you would then need to re-run the Model Optimizer on the updated model.

#### 3. Navigate to the tutorial sample model directory

	cd $SV/object-detection/tensorflow-yolo-v3/FP32

#### 4. Verify creation of the optimized model files (the IR files)

	ls

You should see the following two files listed in this directory: **frozen_darknet_yolov3_model.xml** and **frozen_darknet_yolov3_model.bin**


## Part 2: Use the YOLOv3* model and Inference Engine in an object detection application


#### 1. Use the sample app (object_detection_demo_yolov3_async.py) from the Intel® Distribution of OpenVINO™ toolkit.

	cd /opt/intel/openvino/deployment_tools/inference_engine/samples/python_samples/object_detection_demo_yolov3_async

	python3 object_detection_demo_yolov3_async.py -h

#### 2. Source your environmental variables

	source /opt/intel/openvino/bin/setupvars.sh


#### 3. Run the sample application to use the Inference Engine on the test video
The below command runs the application with YOLOv3 IR model and the test video which you downloaded in previous step.


	python3 /opt/intel/openvino/deployment_tools/inference_engine/samples/python_samples/object_detection_demo_yolov3_async/object_detection_demo_yolov3_async.py -i /dev/video0 -m ./FP32/frozen_darknet_yolov3_model.xml -l /home/intel/inference_engine_samples_build/intel64/Release/lib/libcpu_extension.so


#### 1. Inference on CPU
```
python3 /opt/intel/openvino/deployment_tools/inference_engine/samples/python_samples/object_detection_demo_yolov3_async/object_detection_demo_yolov3_async.py -i /dev/video0 -m ./FP32/frozen_darknet_yolov3_model.xml -l /home/intel/inference_engine_samples_build/intel64/Release/lib/libcpu_extension.so -d CPU
```
You will see the **total time** it took to run the inference and see the detected objects captured by the camera video. 

#### 2. Inference on GPU
Since you installed the OpenCL™ drivers to use the GPU, you can run the inference on GPU and compare the difference.

Set target hardware as GPU with **-d GPU**
```
python3 /opt/intel/openvino/deployment_tools/inference_engine/samples/python_samples/object_detection_demo_yolov3_async/object_detection_demo_yolov3_async.py -i /dev/video0 -m ./FP32/frozen_darknet_yolov3_model.xml -d GPU
```

#### 3. Inference on Movidius NCS2
Connect the Movidius NCS2 to your dev machine via USB port. 

##### System check
First make sure the USB rules are set up.

	cat <<EOF > 97-myriad-usbboot.rules
	SUBSYSTEM=="usb", ATTRS{idProduct}=="2150", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
	SUBSYSTEM=="usb", ATTRS{idProduct}=="2485", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
	SUBSYSTEM=="usb", ATTRS{idProduct}=="f63b", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
	EOF


	sudo cp 97-myriad-usbboot.rules /etc/udev/rules.d/

	sudo udevadm control --reload-rules

	sudo udevadm trigger

Then check if the device is visible with lsusb.

	lsusb

The output for NCS2 will be

	Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
	Bus 001 Device 015: ID 03e7:2485

Here ID 03e7:2485 without a description string is the Movidius device.

##### Setup a short path for the workshop directory

	export SV=/opt/intel/workshop/smart-video-workshop/

	source /opt/intel/openvino/bin/setupvars.sh

##### Run the sample application on Intel® Movidius™ Neural Compute Stick2 (NCS2)
Set target hardware as Intel® Movidius™ NCS with **-d MYRIAD**

The Model Optimizer by default generate FP32 IR files if the data type is not particularly specified.

Let's run the Model Optimizer to get IR files in FP16 format suitable for the Intel® Movidius™ NCS2 by setting the data_type flag to FP16.

    cd $SV/object-detection/tensorflow-yolo-v3/

    mkdir -p FP16

	python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo_tf.py --input_model frozen_darknet_yolov3_model.pb --batch 1 --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/yolo_v3.json -o $SV/object-detection/tensorflow-yolo-v3/FP16 --data_type FP16

Now run the example application with these new IR files.

	python3 /opt/intel/openvino/deployment_tools/inference_engine/samples/python_samples/object_detection_demo_yolov3_async/object_detection_demo_yolov3_async.py -i /dev/video0 -m ./FP16/frozen_darknet_yolov3_model.xml -d MYRIAD
