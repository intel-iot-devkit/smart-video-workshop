
# Intel® Distribution of OpenVINO™ toolkit hetero plugin 

This example shows how to use hetero plugin to define preferences to run different network layers on different hardware types. Here, we will use the command line option to define hetero plugin usage where the layer distribution is already defined. However, hetero plugin also allows developers to customize distribution of layers execution on different hardware by specifying it in the application code.  

### Car detection tutorial example 
#### 1. Navigate to the tutorial directory
	export SV=/opt/intel/workshop/smart-video-workshop
	source /opt/intel/computer_vision_sdk/bin/setupvars.sh
	cd $SV/object-detection/
  
#### 2. Run the car detection tutorial with hetero plugin 

##### a) Prioritizing running on GPU first.

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:GPU,CPU
    

##### a) Prioritizing running on CPU first.

     ./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:CPU,GPU 

Observe the performance time required to process each frame by Inference Engine. For this particular example, inferance ran faster when prioritized for CPU as oppose to when GPU was the first priority.  

### Inference Engine classification sample     
Intel® Distribution of OpenVINO™ toolkit install folder (/opt/intel/computer_vision_sdk/) includes various samples for developers to understand how Inference Engine APIs can be used. These samples have -pc flag implmented which shows per topology layer performance report. This will allow to see which layers are running on which hardware. We will run a very basic classification sample as an example in this section. We will provide car image as input to the classification sample. The output will be object labels with confidence numbers.  

#### 1. First, get the classification model and convert that to IR using Model Optimizer
For this example, we will use squeezenet model downloaded with the model downlaoder script while setting up the OS for the workshop. 

	cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/classification/squeezenet/1.1/caffe/squeezenet1.1.caffemodel -o $SV/object-detection/ 
	
To display labels after classifictaion, you will need a labels file for the SqueezeNet* model. Get the available labels file from demo directory to your working directory.  

	cp /opt/intel/computer_vision_sdk/deployment_tools/demo/squeezenet1.1.labels $SV/object-detection/


#### 2. Go to samples build directory
Make sure you have build the samples as per the instructions given in the [How to Get Started](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/README.md) section. 
> **Note** For the in-class workshop sessions, the samples are already built in the OS image. 

	 cd $HOME/inference_engine_samples/intel64/Release


#### 3. Run classification sample with hetero plugin, prioritizing running on GPU first.

	 ./classification_sample -i /opt/intel/computer_vision_sdk/deployment_tools/demo/car.png -m $SV/object-detection/squeezenet1.1.xml -d HETERO:GPU,CPU -pc
	
performance counts:


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/hetero_GPU_CPU.png)


> Note: execType GPU for layers executed on GPU.  Also, skipped relu.

#### 4. Now, run with CPU first

	 ./classification_sample -i /opt/intel/computer_vision_sdk/deployment_tools/demo/car.png -m $SV/object-detection/squeezenet1.1.xml -d HETERO:CPU,GPU -pc

performance counts:
<br>
![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/hetero_CPU_GPU.png "CPU")
<br>

 > Note: jit to CPU instruction set


