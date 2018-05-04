# Optimizing Intel® Computer Vision SDK Applications
This tutorial shows some techniques to get better performance from computer vision applications with model optimizer and inference engine. 


### 1. Tuning parameters in Model Optimizer
In this section we will see how change in batch size affect the performance. We will use the sqeezenet SSD model for the experiments in this session.  
For SSD models, the batch size is required to be set at model optimizer level. The default batch size for model optimizer is 1. 

#### Let's first look at the performance numbers for the batch size 1. 

	 cd $LAB_DIR/object-detection
	./tutorial1 -i cars_1920x1080.h264 -m /models/sqeeznet_ssd/squeezenet_ssd.xml


#### Change the batch size to 2 using model optimizer
 Create batch_size/batch_2 folder to store the IR files. 
 
 	cd /models/sqeeznet_ssd/
 	mkdir /batch_size/batch_2
	
Use -b flag to define the batch size.

	cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer$  
	python3 mo_caffe.py --input_model $LAB_DIR/object-detection/models/sqeeznet_ssd/squeezenet_ssd.caffemodel -o $LAB_DIR/object-detection/models/sqeeznet_ssd/batch_size/batch_2 -b 2

#### Run the object-detection example for with new batch size

	cd $LAB_DIR/object-detection
	./tutorial1 -i cars_1920x1080.h264 -m /models/sqeeznet_ssd/batch_size/batch_2/squeezenet_ssd.xml

#### Run the example for batch size 8 and 16
The similer instructions can be used to change batch size to 8 and 16 using model optimizer. Once it is done, run the example again and observe the performace. 


### 2. Pick the right model based on application and hardware
Use/train a model with the right performance/accuracy tradeoffs. Performance differences between models can be bigger than any optimization you can do at the inference app level.
Run various SSD models on the car detection example which we used in the initial tutorial and observe the performance. We will run these tests on different hardware accelerator to determine how application performance depends on models as well as hardware. 

#### Set environmental variables and navigate to object detection tutorial directory

	source /opt/intel/computer_vision_sdk/bin/setupvars.sh
	cd $LAB_DIR/object-detection

#### a) CPU
 
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m /models/model_downloader/object_detection/common/ssd/512/caffe/FP32/ssd512.xml
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/ssd/300/caffe/FP32/ssd300.xml
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/ssd/GoogleNet/SSD_GoogleNet_v2_fp32.xml
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/mobilenet-ssd/caffe/FP32/mobilenet-ssd.xml

#### b) GPU
 
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m /models/model_downloader/object_detection/common/ssd/512/caffe/FP32/ssd512.xml -d GPU
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/ssd/300/caffe/FP32/ssd300.xml -d GPU
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/ssd/GoogleNet/SSD_GoogleNet_v2_fp32.xml -d GPU
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/mobilenet-ssd/caffe/FP32/mobilenet-ssd.xml -d GPU


#### c) Movidius NCS

	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m /models/model_downloader/object_detection/common/ssd/512/caffe/FP32/ssd512.xml -d MYRIAD
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/ssd/300/caffe/FP32/ssd300.xml -d MYRIAD
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/ssd/GoogleNet/SSD_GoogleNet_v2_fp32.xml -d MYRIAD
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/mobilenet-ssd/caffe/FP32/mobilenet-ssd.xml -d MYRIAD

### 3. Use the right data type for your target HW and accuracy needs
In this section, we will consider example of GPU for which FP16 operations are more optimized as compared to FP32 operations. We will run the object detection example with SSD models with data types FP16 and FP32 and observe the performance difference. 

	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/ssd/GoogleNet/SSD_GoogleNet_v2_fp32.xml -d GPU 
	
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/model_downloader/object_detection/common/ssd/GoogleNet/SSD_GoogleNet_v2_fp16.xml -d GPU

From the performance numbers, it’s clear that we got much better performance for FP16 models. 


### 4. Use async
Async API can improve overall frame rate of the application. While accelerator is busy with the inference, the application can continue doing ecoding, decoding or post inferefernce data processing on the host. For this section we will use the object_detection_demo_ssd_async sample. This sample keeps two parallel infer requests and while the current is processed, the input frame for the next is being captured. This essentially hides the latency of capturing, so that the overall framerate is rather determined by the MAXIMUM(detection time, input capturing time) and not the SUM(detection time, input capturing time).
#### a) Navigate to the object_detection_demo_ssd_async sample build directory

    cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release
    
#### b) Run the async example

    ./object_detection_demo_ssd_async -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $LAB_DIR/object-detection/models/model_downloader/object_detection/common/ssd/GoogleNet/SSD_GoogleNet_v2_fp32.xml 

There are important performance caveats though, for example the tasks that run in parallel should try to avoid oversubscribing the shared compute resources. e.g. if the inference is performed on the FPGA, and the CPU is essentially idle, than it makes sense to do things on the CPU in parallel. But if the inference is performed say on the GPU, than it can take little gain to do the (resulting video) encoding on the same GPU in parallel, because the device is already busy.





