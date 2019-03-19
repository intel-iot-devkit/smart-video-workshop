# Optimizing Computer Vision Applications
This tutorial shows some techniques to get better performance for computer vision applications with the Intel® Distribution of OpenVINO™ toolkit. 


## 1. Tune parameters - set batch size
In this section, we will see how changes in the batch size affect the performance. We will use the SSD300 model for the experiments.  

The default batch size for the Model Optimizer is 1. 

### Let us first look at the performance numbers for the batch size 1. 

	export SV=/opt/intel/workshop/smart-video-workshop/
	source /opt/intel/computer_vision_sdk/bin/setupvars.sh
	cd $SV/object-detection
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml


### Change the batch size to 2 and run the object-detection example for new batch size

	cd $SV/object-detection
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -b 2

### Run the example for different batch sizes 
Change the batch sizes to 8,16,32,64,128 and so on and see the performance diffrence in terms of the inference time.


### 2. Pick the right model based on application and hardware
Use/train a model with the right performance/accuracy tradeoffs. Performance differences between models can be bigger than any optimization you can do at the inference app level.
Run various SSD models from the model_downloader in the car detection example which we used in the initial tutorial and observe the performance. We will run these tests on different hardware accelerators to determine how application performance depends on models as well as hardware. 

### Run Model Optimizer on the models to get IR files
	cd $SV/object-detection
	mkdir -p SSD512/{FP16,FP32} 
	mkdir -p SSD300/{FP16,FP32} 
	
	cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/ssd/512/caffe/ssd512.caffemodel -o $SV/object-detection/SSD512/FP32
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/ssd/512/caffe/ssd512.caffemodel -o $SV/object-detection/SSD512/FP16 --data_type FP16
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/ssd/300/caffe/ssd300.caffemodel -o $SV/object-detection/SSD300/FP32
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/ssd/300/caffe/ssd300.caffemodel -o $SV/object-detection/SSD300/FP16 --data_type FP16
		
### Set environmental variables and navigate to object detection tutorial directory

	source /opt/intel/computer_vision_sdk/bin/setupvars.sh
	cd $SV/object-detection

#### a) CPU
 
 	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP32/ssd300.xml
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD512/FP32/ssd512.xml
	
	
#### b) GPU
 
 	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d GPU
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP32/ssd300.xml -d GPU
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD512/FP32/ssd512.xml -d GPU
	
	
#### c) Intel® Movidius™ Neural Compute Stick

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP16/mobilenet-ssd.xml -d MYRIAD
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP16/ssd300.xml -d MYRIAD
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD512/FP16/ssd512.xml -d MYRIAD
	
> **Note**: There is often USB write error for Intel® Movidius™ Neural Compute Stick, please try re-running the command. Sometimes it takes 3 trials. 

	
### 3. Use the right data type for your target harware and accuracy needs
In this section, we will consider an example running on a GPU. FP16 operations are better optimized than FP32 on GPUs. We will run the object detection example with SSD models with data types FP16 and FP32 and observe the performance difference. 

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP32/ssd300.xml -d GPU 
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP16/ssd300.xml -d GPU

It is clear that we got better performance with FP16 models. 


### 4. Use async
The async API can improve the overall frame rate of the application. While the accelerator is busy with running inference operations, the application can continue encoding, decoding or post inference data processing on the host. For this section, we will use the object_detection_demo_ssd_async sample. This sample makes asynchronous requests to the inference engine. This reduces the inference request latency, so that the overall framerate is determined by the MAXIMUM(detection time, input capturing time) and not the SUM(detection time, input capturing time).
#### a) Navigate to the object_detection_demo_ssd_async sample build directory

	cd $HOME/inference_engine_samples/intel64/Release
    
#### b) Run the async example

	./object_detection_demo_ssd_async -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml

> Press tab to switch to sync mode. Observe the number of fps (frames per second) for both sync and async mode. The number frames processed per second are more in async than the sync mode. 

There are important performance caveats though. Tasks that run in parallel should try to avoid oversubscribing to shared computing resources. For example, if the inference tasks are running on the FPGA and the CPU is essentially idle, then it makes sense to run tasks on the CPU in parallel. 
