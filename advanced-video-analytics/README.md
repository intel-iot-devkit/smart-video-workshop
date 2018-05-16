# Advanced Video Analytics
The tutorial shows some techniques for making advanced video analytics applications.

## Part 1. Chaining models: Use mutiple models in an application

The OpenVINO™ toolkit package includes security barrier sample which uses 3 models to detect cars, their number plates, color and number plate attributes from the input video or image of the cars. The sample demo script is provided in the OpenVINO™ toolkit package to run the sample. 

#### 1. Navigate to the security camera barrier sample build directory

	cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release
  
#### 2. Run the executable for the security barrier sample with the Squeezenet* model used in the first tutorial

	sudo ./security_barrier_camera_sample -i /opt/intel/computer_vision_sdk_2018.0.219/deployment_tools/demo/car_1.bmp -m $SV/object-detection/models/sqeeznet_ssd/squeezenet_ssd.xml -d CPU

#### 3. Run the security camera sample with ICV models 

    sudo ./security_barrier_camera_sample -d CPU -i /opt/intel/computer_vision_sdk_2018.0.219/deployment_tools/demo/car_1.bmp -m /opt/intel/computer_vision_sdk_2018.0.234/deployment_tools/intel_models/vehicle-license-plate-detection-barrier-0007/FP32/vehicle-license-plate-detection-barrier-0007.xml -m_va /opt/intel/computer_vision_sdk_2018.0.234/deployment_tools/demo/../intel_models/vehicle-attributes-recognition-barrier-0010/FP32/vehicle-attributes-recognition-barrier-0010.xml -m_lpr /opt/intel/computer_vision_sdk_2018.0.234/deployment_tools/demo/../intel_models/license-plate-recognition-barrier-0001/FP32/license-plate-recognition-barrier-0001.xml

It uses three ICV models, vehicle-license-plate-detection-barrier-0007, vehicle-attributes-recognition-barrier-0010, license-plate-recognition-barrier-0001 to perform different tasks in the application. These ICV models are optimized for particular tasks which yields better performance over generic object detection models. 
 
Following car image will appear the at end of the above command execution. It shows the detection of the car, number plate, its attributes and color.  
<br>

![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/sampleop.png "car")

<br>
