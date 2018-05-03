# Optimizing Intel® Computer Vision SDK Applications
This tutorial shows some techniques to get better performance from computer vision applications with model optimizer and inference engine.

### 1. Tuning parameters in Model Optimizer
The default batch size for model optimizer is 1. In this section we will see how chnage in batch size affect the performance, 
### 2. Pick the right model based on application and hardware
Use/train a model with the right performance/accuracy tradeoffs. Performance differences between models can be bigger than any optimization you can do at the inference app level.
Run various SSD models on the car detection example which we used in the initial tutorial and observe the performance. We will run these tests on different hardware accelerator to determine how application performance depends on models as well as hardware. 

#### Set environmental variables and navigate to object detection tutorial directory

	source /opt/intel/computer_vision_sdk/bin/setupvars.sh
	cd /object-detection

#### a) CPU
 
	./tutorial_1 -m /model/ssd/512/caffe/FP32/ssd512.xml
	./tutorial_1 -m /model/ssd/300/caffe/FP32/ssd300.xml
	./tutorial_1 -m /model/ssd/GoogleNet/SSD_GoogleNet_v2_fp32.xml
	./tutorial_1 -m /model/mobilenet-ssd/caffe/FP32/mobilenet-ssd.xml

#### b) GPU
 
	./tutorial_1 -m /model/ssd/512/caffe/FP32/ssd512.xml -d GPU
	./tutorial_1 -m /model/ssd/300/caffe/FP32/ssd300.xml -d GPU
	./tutorial_1 -m /model/ssd/GoogleNet/SSD_GoogleNet_v2_fp32.xml -d GPU
	./tutorial_1 -m /model/mobilenet-ssd/caffe/FP32/mobilenet-ssd.xml -d GPU

#### c) Movidius NCS

	./tutorial_1 -m /model/ssd/512/caffe/FP32/ssd512.xml -d GPU
	./tutorial_1 -m /model/ssd/300/caffe/FP32/ssd300.xml -d GPU
	./tutorial_1 -m /model/ssd/GoogleNet/SSD_GoogleNet_v2_fp32.xml -d GPU
	./tutorial_1 -m /model/mobilenet-ssd/caffe/FP32/mobilenet-ssd.xml -d GPU

### 3. Use the right data type for your target HW and accuracy needs
In this section, we will consider example of GPU for which FP16 operations are more optimized as compared to FP32 operations. We will run the object detection example with SSD models with data types FP16 and FP32 and observe the performance difference. 

	./tutorial_1 -m /model/ssd/GoogleNet/SSD_GoogleNet_v2_fp32.xml -d GPU
	./tutorial_1 -m /model/ssd/GoogleNet/SSD_GoogleNet_v2_fp16.xml -d GPU

From the performance numbers, it’s clear that we got much better performance for FP16 models. 


### 4. Use async
Async API can improve overall frame rate of the application. While accelerator is busy with the inference, the application can continue doing ecoding, decoding or post inferefernce data processing on the host. For this section we will use the object_detection_demo_ssd_async sample. This sample keeps two parallel infer requests and while the current is processed, the input frame for the next is being captured. This essentially hides the latency of capturing, so that the overall framerate is rather determined by the MAXIMUM(detection time, input capturing time) and not the SUM(detection time, input capturing time).
#### a) Navigate to the object_detection_demo_ssd_async sample build directory

    cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release
    
#### b) Run the async example

    ./object_detection_demo_ssd_async -i /home/intel/workshopApr25/workshop-tutorials/test_content/video/cars_1920x1080.h264 -m /home/intel/workshopApr25/workshop-tutorials/test_content/IR/SSD/SSD_GoogleNet_v2_fp32.xml 

There are important performance caveats though, for example the tasks that run in parallel should try to avoid oversubscribing the shared compute resources. e.g. if the inference is performed on the FPGA, and the CPU is essentially idle, than it makes sense to do things on the CPU in parallel. But if the inference is performed say on the GPU, than it can take little gain to do the (resulting video) encoding on the same GPU in parallel, because the device is already busy.





