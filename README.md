# Optimized Inference at the Edge with Intel® Tools and Technologies 
This workshop will walk you through a computer vision workflow using the latest Intel® technologies and comprehensive toolkits including support for deep learning algorithms that help accelerate smart video applications. You will learn how to optimize and improve performance with and without external accelerators and utilize tools to help you identify the best hardware configuration for your needs. This workshop will also outline the various frameworks and topologies supported by Intel® accelerator tools. 

## How to Get Started
   
> :warning: For the in-class training, the hardware and software setup part has already been done on the workshop hardware. In-class training participants should directly move to Workshop Agenda section. 

In order to use this workshop content, you will need to setup your hardware and install the Intel® Distribution of OpenVINO™ toolkit for infering your computer vision application.  
### 1. Hardware requirements
The hardware requirements are mentioned in the System Requirement section of the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)

### 2. Operating System
These labs have been validated on Ubuntu* 16.04 OS. 

### 3. Software installation steps
#### a). Install Intel® Distribution of OpenVINO™ toolkit 
Use steps described in the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)
to install the Intel® Distribution of OpenVINO™ toolkit, configure Model Optimizer, run the demos, additional steps to install Intel® Media SDK and OpenCL™ mentioned in the the guide. 

#### b). Install git, python libraries
	sudo apt install git
	sudo apt install python3-pip
	sudo apt install libgflags-dev
    
#### c). Run the demo scipts and compile samples
Delete $HOME/inference_engine_samples folder if it already exists. 

	rm -rf $HOME/inference_engine_samples
	
Run demo scripts (any one of them or both if you want to both the demos) which will generate the folder $HOME/inference_engine_samples with the current Intel® Distribution of OpenVINO™ toolkit built. 

	cd /opt/intel/openvino/deployment_tools/demo
	./demo_squeezenet_download_convert_run.sh
	./demo_security_barrier_camera.sh
	
	sudo chown -R username.username $HOME/inference_engine_samples_build
	cd $HOME/inference_engine_samples_build
	make
	
#### d). Download models using model downloader scripts in Intel® Distribution of OpenVINO™ toolkit installed folder
   - Install python3 (version 3.5.2 or newer) 
   - Install yaml and requests modules with command:

	sudo -E pip3 install pyyaml requests
   
   - Run model downloader script to download example deep learning models
  		
	cd /opt/intel/openvino/deployment_tools/tools/model_downloader
	sudo python3 downloader.py --name mobilenet-ssd,ssd300,ssd512,squeezenet1.1,face-detection-retail-0004,face-detection-retail-0004-fp16,age-gender-recognition-retail-0013,age-gender-recognition-retail-0013-fp16,head-pose-estimation-adas-0001,head-pose-estimation-adas-0001-fp16,emotions-recognition-retail-0003,emotions-recognition-retail-0003-fp16,facial-landmarks-35-adas-0002,facial-landmarks-35-adas-0002-fp16


#### e). Install Intel® System Studio, VNC viewer and Setup on development machine

Follow the [guide](./up2-vision-kit/setup_intel_system_studio_2019.md) to install Intel® System Studio and VNC viewer on your development machine.
	
> :warning: This workshop content has been validated with Intel® Distribution of OpenVINO™ toolkit version R1 (openvino_toolkit_2019.1.094). 

		
## Workshop Agenda
* **Smart Video/Computer Vision Tools Overview**
  - Slides - [Introduction to Smart Video Tools](./presentations/01-Introduction-to-Intel-Smart-Video-Tools.pdf)

* **Training a Deep Learning Model**
  - Slides - [Training a Deep Learning Model](./presentations/DL_training_model.pdf)
  - Lab - [Training a Deep Learning Model](./dl-model-training/README.md)
  
* **Basic End to End Object Detection Inference Example**
  - Slides - [Basic End to End Object Detection Example](./presentations/02-03_Basic-End-to-End-Object-Detection-Example.pdf)
  - Lab Setup - [Lab Setup Instructions](./Lab_setup.md)
  - Lab - [Object Detection with Caffe* model](./object-detection/README.md)
  - Lab - [Classification with TensorFlow* model](./advanced-video-analytics/tensor_flow.md)
  - Lab - [Object Detection with YOLOv3* model](./object-detection/README_yolov3.md)

* **Hardware Heterogeneity**
  - Lab - [Hardware Heterogeneity](./hardware-heterogeneity/README.md)

* **HW Acceleration with Intel® Movidius™ Neural Compute Stick**
  - Lab - [HW Acceleration with Intel® Movidius™ Neural Compute Stick](./HW-Acceleration-with-Movidious-NCS/README.md) 
  
* **FPGA Inference Accelerator**
  - Slides - [HW Acceleration with Intel® FPGA](./presentations/04-HW-Acceleration-with-FPGA.pdf)

* **Optimization Tools and Techniques** 
  - Slides - [Optimization Tools and Techniques](/presentations/04-05_Optimization_and_advanced_analytics.pdf)
  - Lab 1 - [Optimization Tools and Techniques](./optimization-tools-and-techniques/README.md)
  - Lab 2- [Intel® VTune™ Amplifier tutorial](./optimization-tools-and-techniques/README_VTune.md)
  
* **Advanced Video Analytics**
  - Lab - [Multiple models usage example](./advanced-video-analytics/multiple_models.md)
<!----  
* **UP²\* AI Vision Development kit as Edge**
  - Setup - [Development machine and Internet Connection Sharing](./up2-vision-kit/dev_machine_setup.md)
  - Lab - [Interact face detection on UP2 kit using Intel® System Studio](./up2-vision-kit/openvino-projects-using-iss2019.md) ---->

* **Implement Custom Layers for Inference on CPU and Integrated GPU**
  - Lab - [Custom Layer](./custom-layer/README.md)
  
* **Additional Examples - Reference Implementations**
  - Industrial 
  	- [Safety Gear Detection](./safety-gear-example/README.md)
	- [Restricted Zone Notifier](https://github.com/intel-iot-devkit/restricted-zone-notifier-cpp)
  	- [Object Size Detector](https://github.com/intel-iot-devkit/object-size-detector-cpp)
  - Retail 
  	- [Store Traffic Monitor](https://github.com/intel-iot-devkit/store-traffic-monitor)
	- [Shopper Gaze Monitor](https://github.com/intel-iot-devkit/shopper-gaze-monitor-cpp)
	
* **Workshop Survey**
  - [Workshop Survey](https://idz.qualtrics.com/jfe/form/SV_a9GvOxtOrOziykB)
  - [Custom Layer Tutorial Survey](https://intelemployee.az1.qualtrics.com/jfe/form/SV_1ZjOKaEIQUM5FpX)
  
> #### Disclaimer

> Intel and the Intel logo are trademarks of Intel Corporation or its subsidiaries in the U.S. and/or other countries. 
 
> *Other names and brands may be claimed as the property of others
