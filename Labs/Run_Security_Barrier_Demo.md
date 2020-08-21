# Run Security Barrier Demo Application
In this lab, we will run a Security Barrier Demo Application to show multiple models used in one application.

## Part 1. Chaining models: Use mutiple models in an application

The Intel® Distribution of OpenVINO™ toolkit package includes security barrier sample which uses 3 models to detect cars, their number plates, color and number plate attributes from the input video or image of the cars. The sample demo script is provided in the Intel® Distribution of OpenVINO™ toolkit package to run the sample. 

#### 1. Navigate to the security camera barrier demo script directory

	cd /opt/intel/openvino/deployment_tools/demo/
 
#### 2. Run the security camera sample with Intel optimized pre-trained models 
    
	sudo ./demo_security_barrier_camera.sh

Above script will run the security barrier camera example with Intel® pretrained models. Open the script to see the models used.

	gedit demo_security_barrier_camera.sh

At the bottom of the script, you can see that tt uses three pretrained models, **vehicle-license-plate-detection-barrier**, **vehicle-attributes-recognition-barrier** and **license-plate-recognition-barrier** to detect the car, it's make, color and license plate attributes. These pretrained models are optimized for particular tasks which yield better performance over generic object detection models. You can find more of such pretrained models under /opt/intel/openvino/deployment_tools/intel_models. 
 
Following car image will appear the at end of the above command execution. It shows the detection of the car, number plate, its attributes and color.  
<br>

![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/sampleop.png "car")

<br>


## Part 2. Use multiple models on different hardware
When you run the demo script above, from the terminal prints, we will see the actual command for running this demo application is this:

	./security_barrier_camera_demo -d CPU -d_va CPU -d_lpr CPU \
	-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp \
	-m /home/intel/openvino_models/ir/intel/vehicle-license-plate-detection-barrier-0106/FP16/vehicle-license-plate-detection-barrier-0106.xml \
	-m_lpr /home/intel/openvino_models/ir/intel/license-plate-recognition-barrier-0001/FP16/license-plate-recognition-barrier-0001.xml \
	-m_va /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml

#### 1. Navigate to the demo application directory 

	cd $HOME/inference_engine_demos_build/intel64/Release

#### 2. Run demo with different hardware
Here we can change any of the "CPU" to GPU, MYRIAD, or HETERO, MULTI plugins:

	./security_barrier_camera_demo -d GPU -d_va MYRIAD -d_lpr MULTI:CPU,MYRIAD \
	-i /opt/intel/openvino/deployment_tools/demo/car_1.bmp \
	-m /home/intel/openvino_models/ir/intel/vehicle-license-plate-detection-barrier-0106/FP16/vehicle-license-plate-detection-barrier-0106.xml \
	-m_lpr /home/intel/openvino_models/ir/intel/license-plate-recognition-barrier-0001/FP16/license-plate-recognition-barrier-0001.xml \
	-m_va /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml

#### 3. Explore the source code to learn more about how to chain multiple models

	cd /opt/intel/openvino/deployment_tools/open_model_zoo/demos/security_barrier_camera_demo
	gedit main.cpp
	

