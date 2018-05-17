
# OpenVINO™ toolkit hetero plugin 

This example shows how to use hetero plugin to define preferences to run different network layers on different hardware types. 

### Car detection tutorial example 
#### 1. Navigate to the tutorial directory

	cd $SV/object-detection/
  
#### 2. Run the car detection tutorial with hetero plugin 

##### a) Prioritizing running on GPU first.

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:GPU,CPU
    

##### a) Prioritizing running on CPU first.

     ./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:CPU,GPU 

Observe the performance time required to process each frame by Inference Engine. For this particular example, inferance ran faster when prioritized for CPU as oppose to when GPU was the first priority.  

### Inference Engine classification sample     
OpenVINO install folder (/opt/intel/computer_vision_sdk/) includes various samples for developers to understand how Inference Engine APIs can be used. These samples have -pc flag implmented which shows per topology layer performance report. This will allow to see which layers are running on which hardware. We will run a very basic classification sample as an example in this section. We will provide car image as input to the classification sample. The output will be object labels with confidence numbers.  

#### 1. First, get the classification model and convert that to IR using Model Optimizer
For this example, we will use squeezenet model downloaded with the model downlaoder script while setting up the OS for the workshop. 

	cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/classification/squeezenet/1.1/caffe/squeezenet1.1.caffemodel -o $SV/object-detection/ 
	

#### 1. Go to samples build directory:

	 cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release


#### 2. Run classification sample with hetero plugin, prioritizing running on GPU first.

	 ./classification_sample -i /opt/intel/computer_vision_sdk/deployment_tools/demo/car.png -m $SV/object-detection/squeezenet1.1.xml -d HETERO:GPU,CPU -pc
	
performance counts:


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/hetero_GPU_CPU.png)


> Note: execType GPU for layers executed on GPU.  Also, skipped relu.

#### 4. Now, run with CPU first

	 ./classification_sample -i car.png -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:CPU,GPU -pc

performance counts:
<br>
![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/hetero_CPU_GPU.png "CPU")
<br>

 > Note: jit to CPU instruction set


