# Optimizing Computer Vision Applications
This tutorial shows some techniques to get better performance for computer vision applications with Model Optimizer and Inference Engine. 


## 1. Tune parameters in Model Optimizer
In this section, we will see how changes in the batch size affect the performance. We will use the SSD300 model for the experiments.  
For SSD models, the batch size is required to be set at Model Optimizer level. The default batch size for the Model Optimizer is 1. 

#### Let us first look at the performance numbers for the batch size 1. 

	cd $SV/object-detection
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml


#### Change the batch size to 2 using Model Optimizer
 Create batch_size/batch_2 folder to store the IR files. 
 
 	cd $SV/object-detection/mobilenet-ssd/
 	mkdir batch_size
	mkdir batch_2
	
Use -b flag to define the batch size.

	cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer$  
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/mobilenet-ssd/caffe/mobilenet-ssd.caffemodel -o $SV/object-detection/mobilenet-ssd/batch_size/batch_2 -b 2

#### Run the object-detection example for new batch size

	cd $SV/object-detection
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/batch_size/batch_2/mobilenet-ssd.xml

#### Run the example for batch size 8 and 16
The similer instructions can be used to change batch size to 8 and 16 using Model Optimizer. Once it is done, run the example again and observe the performace. 


### 2. Pick the right model based on application and hardware
Use/train a model with the right performance/accuracy tradeoffs. Performance differences between models can be bigger than any optimization you can do at the inference app level.
Run various SSD models from model_downloader on the car detection example which we used in the initial tutorial and observe the performance. We will run these tests on different hardware accelerator to determine how application performance depends on models as well as hardware. 

#### Run Model Optimizer on the models to get IR files
	cd $SV/object-detection
	mkdir SSD512 && cd SSD512 && mkdir FP32 && mkdir FP16 
	cd $SV/object-detection
	mkdir SSD300 && cd SSD300 && mkdir FP32 && mkdir FP16 
	
	cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/ssd/512/caffe/ssd512.caffemodel -o $SV/object-detection/SSD512/FP32
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/ssd/512/caffe/ssd512.caffemodel -o $SV/object-detection/SSD512/FP16 --data_type FP16
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/ssd/300/caffe/ssd300.caffemodel -o $SV/object-detection/SSD300/FP32
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/ssd/300/caffe/ssd300.caffemodel -o $SV/object-detection/SSD300/FP16 --data_type FP16
		
#### Set environmental variables and navigate to object detection tutorial directory

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
	
	
#### c) Movidius NCS

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d MYRIAD
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP32/ssd300.xml -d MYRIAD
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD512/FP32/ssd512.xml -d MYRIAD
			
	
### 3. Use the right data type for your target harware and accuracy needs
In this section, we will consider example of GPU for which FP16 operations are better optimized than FP32 operations. We will run the object detection example with SSD models with data types FP16 and FP32 and observe the performance difference. 

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP32/ssd300.xml -d GPU 
	
	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP16/ssd300.xml -d GPU

From the performance numbers, it is clear that we got better performance for FP16 models. 


### 4. Use async
Async API can improve overall frame rate of the application. While accelerator is busy with the inference, the application can continue performing ecoding, decoding or post inference data processing on the host. For this section we will use the object_detection_demo_ssd_async sample. This sample keeps two parallel inference requests and while the current is processed, the input frame for the next is being captured. This essentially hides the latency of capturing, so that the overall framerate is determined by the MAXIMUM(detection time, input capturing time) and not the SUM(detection time, input capturing time).
#### a) Navigate to the object_detection_demo_ssd_async sample build directory

	cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release
    
#### b) Run the async example

	./object_detection_demo_ssd_async -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml

There are important performance caveats though, for example the tasks that run in parallel should try to avoid oversubscribing the shared compute resources. e.g. if the inference is performed on the FPGA, and the CPU is essentially idle, then it makes sense to do things on the CPU in parallel. But if the inference is performed say on the GPU, than it can gain little to perform the (resulting video) encoding on the same GPU in parallel, because the device is already busy.
