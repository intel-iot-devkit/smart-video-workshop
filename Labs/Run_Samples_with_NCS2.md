
# Run Samples with Intel® Movidius™ Neural Compute Stick 2

In this lab, we will run the Classfication and Object Detection sample applications with NCS2. 

#### 1. Connect Intel® Movidius™ Neural Compute Stick to your development laptop
<br>

![image of Movidius NCS to computer](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/Movidius.png "connected NCS")

<br>

#### 2. System check
Follow the instruction of [Steps for Intel® Neural Compute Stick 2](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_linux.html#additional-NCS-steps) from the [Install Intel® Distribution of OpenVINO™ toolkit for Linux*](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_linux.html) to setup the USB rules for NCS2.

	
Then check if the device is visible with lsusb:
	
	lsusb
	
You will see message like below:

	Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
	Bus 001 Device 015: ID 03e7:2485 

Here ID 03e7:2150 without a description string is the Movidius device.

#### 3. Run the sample application on Intel® Movidius™ Neural Compute Stick (NCS)
Set target hardware as Intel® Movidius™ NCS with **-d MYRIAD**, remember to use **FP16** datatype for MYRIAD plugin.

Run Classification Sample Application with NCS2:

	cd /opt/intel/openvino/deployment_tools/inference_engine/samples/python/classification_sample_async
	
	python3 classification_sample_async.py \
	-m /opt/intel/workshop/Squeezenet/FP16/squeezenet1.1_fp16.xml \
	-i /opt/intel/workshop/smart-video-workshop/Labs/daisy.jpg \
	-d MYRIAD \
	--labels /opt/intel/workshop/smart-video-workshop/Labs/squeezetnet_label.txt 

Run Object Detection Sample Application with NCS2:

	cd /opt/intel/openvino/deployment_tools/inference_engine/samples/python/object_detection_sample_ssd/
	
	python3 object_detection_sample_ssd.py \
	-m /opt/intel/workshop/Mobilenet-SSD-v1/FP16/mobilenet-ssd-v1-fp16.xml \
	-i /opt/intel/workshop/smart-video-workshop/Labs/birds.jpg \
	-d MYRIAD  
	
	eog out.bmp

## Further Reading
To learn more about MYRIAD plugin, pleae refer to [MYRIAD Plugin](https://docs.openvinotoolkit.org/latest/openvino_docs_IE_DG_supported_plugins_MYRIAD.html) session on OpenVINO documentation.
