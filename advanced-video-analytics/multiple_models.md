# Advanced Video Analytics
The tutorial shows some techniques for developing advanced video analytics applications.

## Part 1. Chaining models: Use mutiple models in an application

The OpenVINO™ toolkit package includes security barrier sample which uses 3 models to detect cars, their number plates, color and number plate attributes from the input video or image of the cars. The sample demo script is provided in the OpenVINO™ toolkit package to run the sample. 

#### 1. Navigate to the security camera barrier sample build directory

	 cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release
  
#### 2. Run the executable for the security barrier sample with the mobilenet-ssd* model used in the first tutorial

	 ./security_barrier_camera_sample -i /opt/intel/computer_vision_sdk/deployment_tools/demo/car_1.bmp -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d CPU
 
#### 3. Run the security camera sample with Intel optimized pre-trained models 

    sudo ./demo_security_barrier_camera.sh

Above script will run the security barrier camera example with Intel pretrained models. Open the script to see the models used.

	gedit demo_security_barrier_camera.sh

At the bottom of the script, you can see that tt uses three pretrained models, vehicle-license-plate-detection-barrier, vehicle-attributes-recognition-barrier and license-plate-recognition-barrier to detect the car, it's make, color and license plate attributes. These pretrained models are optimized for particular tasks which yield better performance over generic object detection models. You can find more of such pretrained models under /opt/intel/computer_vision_sdk/deployment_tools/intel_models. 
 
Following car image will appear the at end of the above command execution. It shows the detection of the car, number plate, its attributes and color.  
<br>

![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/sampleop.png "car")

<br>


## Part 2. Use multiple models on different hardware

#### 0. Initialize the environmental variables

	source /opt/intel/computer_vision_sdk/bin/setupvars.sh

#### 1. Let's look at the face detection sample from the OpenVINO™ tookit package
	
	cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release
	 ./interactive_face_detection_sample -h
	 
#### 2. Check if a web cam is connected

	ls /dev/video*

#### 3. Set short path to access the pretrained models

	export models=/opt/intel/computer_vision_sdk/deployment_tools/intel_models/
	
#### 4. Run the face demo, face detection only, on the Movidius Compute stick

	./interactive_face_detection_sample -i /dev/video0 -m $models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -d MYRIAD

#### 5. Now we add (to the face detection) also an age and gender detection, running on the CPU

	./interactive_face_detection_sample -i /dev/video0 -m $models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -d MYRIAD -m_ag $models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -d_ag CPU 


#### 6. Now let’s add head position detection running on GPU.
 
 	./interactive_face_detection_sample -i /dev/video0 -m $models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -d MYRIAD -m_ag $models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -d_ag CPU -m_hp $models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d_hp GPU

#### 7. Now we’ll add an emotion detector, running on the GPU
	
	./interactive_face_detection_sample -i /dev/video0 -m $models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -d MYRIAD -m_ag $models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -d_ag CPU -m_hp $models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d_hp GPU -m_em $models/emotions-recognition-retail-0003/FP16/emotions-recognition-retail-0003.xml -d_em GPU
	

	

