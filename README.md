# Optimized Inference at the Edge with Intel® Tools and Technologies 
This workshop will walk you through a computer vision workflow using the latest Intel® technologies and comprehensive toolkits including support for deep learning algorithms that help accelerate smart video applications. You will learn how to optimize and improve performance with and without external accelerators and utilize tools to help you identify the best hardware configuration for your needs. This workshop will also outline the various frameworks and topologies supported by Intel® accelerator tools. 

## How to Get Started
   
> :warning: For the in-class training, the hardware and software setup part has already been done on the workshop hardware. In-class training participants should directly move to Workshop Agenda section. 

In order to use this workshop content, you will need to setup your hardware and install OpenVINO™ toolkit for infering your computer vision application.  
### 1. Hardware requirements
The hardware requirements are mentioned in the System Requirement section of the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)

### 2. Operating System
These labs have been validated on Ubuntu 16.04 OS. 

### 3. Software installation steps
#### a). Install OpenVINO™ toolkit 
Use steps described in the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)
to install OpenVINO™ toolkit, build sample demos, build inference engine samples, install MediaSDK and OpenCL* mentioned in the the guide. 

#### b). Install git, gflags and python libraries
	sudo apt install git
	sudo apt install libgflags-dev
	sudo apt install python3-pip
    pip3 install -r /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/requirements_caffe.txt

#### c). Compile samples
Compile in-built samples in OpenVINO™ toolkit 

	source /opt/intel/computer_vision_sdk/bin/setupvars.sh
	cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/
	sudo mkdir build && cd build
	sudo cmake –DCMAKE_BUILD_TYPE=Release ..
	sudo make  

#### d). Download models using model downloader scripts in OpenVINO™ toolkit installed folder
   - Install python3 (version 3.5.2 or newer) 
   - Install yaml and requests modules with command:

	sudo -E pip3 install pyyaml requests
   
   - Run model downloader script to download example deep learning models
  		
	cd /opt/intel/computer_vision_sdk/deployment_tools/model_downloader
	sudo python3 downloader.py
		
		
## Workshop Agenda
* **Intel Smart Video/Computer Vision Tools Overview**
  - Slides - [Introduction to Intel Smart Video Tools](./presentations/01-Introduction-to-Intel-Smart-Video-Tools.pdf)

* **Basic End to End Object Detection Example**
  - Slides - [Basic End to End Object Detection Example](./presentations/02-Basic-End-to-End-Object-Detection-Example.pdf)
  - Lab - [Basic End to End Object Detection Example](./object-detection/README.md)

* **Hardware Heterogeneity**
  - Lab - [Hardware Heterogeneity](./hardware-heterogeneity/README.md)

* **HW Acceleration with Intel® Movidius™ Neural Compute Stick**
  - Lab - [HW Acceleration with Intel® Movidius™ Neural Compute Stick](./HW-Acceleration-with-Movidious-NCS/README.md) 
  
* **FPGA Inference Accelerator**
  - Slides - [HW Acceleration with Intel® Movidius™ Neural Compute Stick](./presentations/04-HW-Acceleration-with-FPGA.pdf)

* **Optimization Tools and Techniques** 
  - Slides - [Optimization Tools and Techniques](/presentations/04_05_Optimization_and_advanced_analytics.pdf)
  - Lab 1 - [Optimization Tools and Techniques](./optimization-tools-and-techniques/README.md)
  - Lab 2- [Intel® VTune™ Amplifier tutorial](./optimization-tools-and-techniques/README_VTune.md)
  
* **Advanced Video Analytics**
  - Lab - [Multiple models usage example](./advanced-video-analytics/multiple_models.md)
  - Lab - [Tensor Flow example](./advanced-video-analytics/tensor_flow.md)
