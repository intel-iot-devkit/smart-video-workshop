
# Introducing Multi-Device Execution 

Multi-Device plugin automatically assigns inference requests to available computational devices to execute the requests in parallel. 

This example shows how to use **MULTI** plugin to share the inference burden onto different hardware types. Here, we will use the command line option to define MULTI plugin usage.  

### Car detection tutorial example 
#### 1. Navigate to the tutorial directory
	export SV=/opt/intel/workshop/smart-video-workshop
	source /opt/intel/openvino/bin/setupvars.sh
	cd $SV/object-detection/
  
#### 2. Run the car detection tutorial with hetero plugin 

##### a) Prioritizing running on GPU first.

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:GPU,CPU
    

##### a) Prioritizing running on CPU first.

     ./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:CPU,GPU 

Observe the performance time required to process each frame by Inference Engine. For this particular example, inferance ran faster when prioritized for CPU as oppose to when GPU was the first priority.  

### Inference Engine classification sample     
Intel® Distribution of OpenVINO™ toolkit install folder (/opt/intel/openvino/) includes various samples for developers to understand how Inference Engine APIs can be used. These samples have -pc flag implmented which shows per topology layer performance report. This will allow to see which layers are running on which hardware. We will run a very basic classification sample as an example in this section. We will provide car image as input to the classification sample. The output will be object labels with confidence numbers.  

#### Go to samples build directory
Make sure you have build the samples as per the instructions given in the [How to Get Started](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/README.md) section. 
> **Note** For the in-class workshop sessions, the samples are already built in the OS image. 

	 cd $HOME/inference_engine_demos_build/intel64/Release


#### Run classification sample with hetero plugin, prioritizing running on CPU first.

	 ./object_detection_demo_ssd_async -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:CPU,GPU -pc
	
performance counts:


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/cpu.png)

 > Note: jit to CPU instruction set


#### Now, run with GPU first

	  ./object_detection_demo_ssd_async -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:GPU,CPU -pc

performance counts:

![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/gpu.png)



> Note: execType GPU for layers executed on GPU.  Also, skipped relu.



