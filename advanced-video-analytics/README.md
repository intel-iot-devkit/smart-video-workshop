# Advanced Video Analytics
The tutorial shows some techniques for making advanced VA applications.

## Part 1. Chaining models: Use mutiple models in an application

The CV-SDK package includes security barrier sample which uses 3 models to detect cars, their number plates, color and number plate attributes from the input video or image of the cars. The sample demo script is provided in the CV-SDK package to run the sample. 

#### 1. Navigate to the demo directory

	cd /opt/intel/computer_vision_sdk/deployment_tools/demo
  
#### 2. Run the demo script for the security barrier sample

	sudo ./demo_squeezenet_download_convert_run.sh

Following car image will appear the at end of the script execution. It shows the dtections of cr, number plate, it's attributes and color.  
<br>

![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/sampleop.png "car")

<br>

#### 2. Open the demo script for the security barrier sample

    gedit demo_squeezenet_download_convert_run.sh

It runs the sample from /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/security_barrier_camera/ with following command.

    ./security_barrier_camera_sample -d CPU -i /opt/intel/computer_vision_sdk_2018.0.219/deployment_tools/demo/car_1.bmp -m /opt/intel/computer_vision_sdk_2018.0.234/deployment_tools/intel_models/vehicle-license-plate-detection-barrier-0007/FP32/vehicle-license-plate-detection-barrier-0007.xml -m_va /opt/intel/computer_vision_sdk_2018.0.234/deployment_tools/demo/../intel_models/vehicle-attributes-recognition-barrier-0010/FP32/vehicle-attributes-recognition-barrier-0010.xml -m_lpr /opt/intel/computer_vision_sdk_2018.0.234/deployment_tools/demo/../intel_models/license-plate-recognition-barrier-0001/FP32/license-plate-recognition-barrier-0001.xml

It uses three ICV models, vehicle-license-plate-detection-barrier-0007, vehicle-attributes-recognition-barrier-0010, license-plate-recognition-barrier-0001 to do different tasks in the application. These ICV models are optimized for doing particular tasks which leads to better performance as compared to generic object detection models. 
 
## Part 2. Use Media-SDK for encoding and decoding 
