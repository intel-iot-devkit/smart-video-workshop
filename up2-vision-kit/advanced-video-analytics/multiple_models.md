# Advanced Video Analytics
The tutorial shows some techniques for developing advanced video analytics applications.

## Part 1. Chaining models: Use mutiple models in an application

The Intel® Distribution of OpenVINO™ toolkit package includes security barrier sample which uses 3 models to detect cars, their number plates, color and number plate attributes from the input video or image of the cars. The sample demo script is provided in the Intel® Distribution of OpenVINO™ toolkit package to run the sample. 

#### 1. Navigate to the security camera barrier sample build directory
	 export SV=/opt/intel/workshop/smart-video-workshop/
	 source /opt/intel/openvino/bin/setupvars.sh
	 cd $HOME/inference_engine_samples_build/intel64/Release
  
#### 2. Run the executable for the security barrier sample with the mobilenet-ssd* model used in the first tutorial

	 ./security_barrier_camera_demo -i /opt/intel/openvino/deployment_tools/demo/car_1.bmp -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d CPU
 
#### 3. Run the security camera sample with Intel optimized pre-trained models 

    cd /opt/intel/openvino/deployment_tools/demo/
    sudo ./demo_security_barrier_camera.sh

Above script will run the security barrier camera example with Intel® pretrained models. Open the script to see the models used.

	gedit demo_security_barrier_camera.sh

At the bottom of the script, you can see that tt uses three pretrained models, vehicle-license-plate-detection-barrier, vehicle-attributes-recognition-barrier and license-plate-recognition-barrier to detect the car, it's make, color and license plate attributes. These pretrained models are optimized for particular tasks which yield better performance over generic object detection models. You can find more of such pretrained models under /opt/intel/openvino/deployment_tools/intel_models. 
 
Following car image will appear the at end of the above command execution. It shows the detection of the car, number plate, its attributes and color.  
<br>

![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/sampleop.png "car")

<br>


## Part 2. Use multiple models on different hardware

#### 0. Initialize the environmental variables

	source /opt/intel/openvino/bin/setupvars.sh

#### 1. Let's look at the face detection sample from the Intel® Distribution of OpenVINO™ toolkit package
	
	cd $HOME/inference_engine_samples_build/intel64/Release
	 ./interactive_face_detection_demo -h
	 
#### 2. Check if a web cam is connected

	ls /dev/video*

#### 3. Set short path to access the pretrained models

	export models=/opt/intel/openvino/deployment_tools/tools/model_downloader
	
#### 4. Run the face demo, face detection only, on the Intel® Movidius™ Neural Compute stick

	./interactive_face_detection_demo -i cam -m $models/Retail/object_detection/face/sqnet1.0modif-ssd/0004/dldt/face-detection-retail-0004-fp16.xml -d MYRIAD


#### 5. Now we add (to the face detection) also an age and gender detection, running on the CPU

	./interactive_face_detection_demo -i cam -m $models/Retail/object_detection/face/sqnet1.0modif-ssd/0004/dldt/face-detection-retail-0004-fp16.xml -d MYRIAD -m_ag $models/Retail/object_attributes/age_gender/dldt/age-gender-recognition-retail-0013.xml -d_ag CPU 



#### 6. Now let’s add head position detection running on GPU.
 
 	./interactive_face_detection_demo -i cam -m $models/Retail/object_detection/face/sqnet1.0modif-ssd/0004/dldt/face-detection-retail-0004-fp16.xml -d MYRIAD -m_ag $models/Retail/object_attributes/age_gender/dldt/age-gender-recognition-retail-0013.xml -d_ag CPU -d_ag CPU -m_hp $models/Transportation/object_attributes/headpose/vanilla_cnn/dldt/head-pose-estimation-adas-0001-fp16.xml -d_hp GPU

#### 7. Now we’ll add an emotion detector, running on the GPU
	
	./interactive_face_detection_demo -i cam -m $models/Retail/object_detection/face/sqnet1.0modif-ssd/0004/dldt/face-detection-retail-0004-fp16.xml -d MYRIAD -m_ag $models/Retail/object_attributes/age_gender/dldt/age-gender-recognition-retail-0013.xml -d_ag CPU -d_ag CPU -m_hp $models/Transportation/object_attributes/headpose/vanilla_cnn/dldt/head-pose-estimation-adas-0001-fp16.xml -d_hp GPU -d_hp GPU -m_em $models/Retail/object_attributes/emotions_recognition/0003/dldt/emotions-recognition-retail-0003-fp16.xml -d_em GPU
	
#### 8. Now let's add facial landmarks detector, running on the GPU
	
	./interactive_face_detection_demo -i cam -m $models/Retail/object_detection/face/sqnet1.0modif-ssd/0004/dldt/face-detection-retail-0004-fp16.xml -d MYRIAD -m_ag $models/Retail/object_attributes/age_gender/dldt/age-gender-recognition-retail-0013.xml -d_ag CPU -d_ag CPU -m_hp $models/Transportation/object_attributes/headpose/vanilla_cnn/dldt/head-pose-estimation-adas-0001-fp16.xml -d_hp GPU -d_hp GPU -m_em $models/Retail/object_attributes/emotions_recognition/0003/dldt/emotions-recognition-retail-0003-fp16.xml -d_em GPU -m_lm  $models/Transportation/object_attributes/facial_landmarks/custom-35-facial-landmarks/dldt/facial-landmarks-35-adas-0002.xml -d_lm CPU
	

