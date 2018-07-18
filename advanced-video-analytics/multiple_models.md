# Advanced Video Analytics
The tutorial shows some techniques for developing advanced video analytics applications.

## Part 1. Chaining models: Use mutiple models in an application

The OpenVINO™ toolkit package includes security barrier sample which uses 3 models to detect cars, their number plates, color and number plate attributes from the input video or image of the cars. The sample demo script is provided in the OpenVINO™ toolkit package to run the sample. 

#### 1. Navigate to the security camera barrier sample build directory

	 cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release
  
#### 2. Run the executable for the security barrier sample with the mobilenet-ssd* model used in the first tutorial

	 ./security_barrier_camera_sample -i /opt/intel/computer_vision_sdk/deployment_tools/demo/car_1.bmp -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d CPU
 
#### 3. Run the security camera sample with ICV models 

     ./security_barrier_camera_sample -d CPU -i /opt/intel/computer_vision_sdk/deployment_tools/demo/car_1.bmp -m /opt/intel/computer_vision_sdk/deployment_tools/intel_models/vehicle-license-plate-detection-barrier-0007/FP32/vehicle-license-plate-detection-barrier-0007.xml -m_va /opt/intel/computer_vision_sdk/deployment_tools/demo/../intel_models/vehicle-attributes-recognition-barrier-0010/FP32/vehicle-attributes-recognition-barrier-0010.xml -m_lpr /opt/intel/computer_vision_sdk/deployment_tools/demo/../intel_models/license-plate-recognition-barrier-0001/FP32/license-plate-recognition-barrier-0001.xml

It uses three ICV models, vehicle-license-plate-detection-barrier-0007, vehicle-attributes-recognition-barrier-0010, license-plate-recognition-barrier-0001 to perform different tasks in the application. These ICV models are optimized for particular tasks which yield better performance over generic object detection models. 
 
Following car image will appear the at end of the above command execution. It shows the detection of the car, number plate, its attributes and color.  
<br>

![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/sampleop.png "car")

<br>


## Part 2. Use multiple models on different hardware

#### 1. Let's look at the face detection sample from the OpenVINO tookit package
	
	cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release
	 ./interactive_face_detection_sample -h
	 
#### 2. Check if a web cam is connected

	ls /dev/video*

#### 3. set short path to access the ICV models

	export models=/opt/intel/computer_vision_sdk/deployment_tools/intel_models/
	
#### 4. Run the face demo, face detection only, on the Movidius Compute stick

	./interactive_face_detection_sample -i /dev/video0 -m $models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -d MYRIAD

#### 5. Now we add (to the face detection) also an age and gender detection, running on the CPU

	./interactive_face_detection_sample -i /dev/video0 -m $models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -d MYRIAD -m_ag $models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -d_ag CPU 


#### 6. Now let’s add head position detection running on GPU.
 
 	./interactive_face_detection_sample -i /dev/video0 -m $models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -d MYRIAD -m_ag $models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -d_ag CPU -m_hp $models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d_hp GPU

#### 7. Now we’ll add an emotion detector, running on the GPU
	
	./interactive_face_detection_sample -i /dev/video0 -m $models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -d MYRIAD -m_ag $models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -d_ag CPU -m_hp $models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d_hp GPU -m_em $models/emotions-recognition-retail-0003/FP16/emotions-recognition-retail-0003.xml -d_em GPU
	

	

