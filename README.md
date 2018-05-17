# Optimized Inference at the Edge with Intel® Tools and Technologies 
This workshop will walk you through a computer vision workflow using the latest Intel® technologies and comprehensive toolkits including support for deep learning algorithms that help accelerate smart video applications. You will learn how to optimize and improve performance with and without external accelerators and utilize tools to help you identify the best hardware configuration for your needs. This workshop will also outline the various frameworks and topologies supported by Intel® accelerator tools. 

## How to Get Started
   
## Note: For the in-class training, the hardware and software setup part has already been done on the workshop hardware. In-class training participants should directly move to Workshop Agenda section. 

In order to use this workshop content, you will need to setup your hardware and install OpenVINO™ toolkit for infering your computer vision application.  
### 1. Hardware requirements
The hardware requirements are mentioned in the System Requirement section of the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)

### 2. Operating System
These labs have been validated on Ubuntu 16.04 OS. 

### 3. Software installation steps
#### a). Install OpenVINO™ toolkit 
Use steps described in the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)
to install OpenVINO™ toolkit as well as MediaSDK and OpenCL* mentioned in the Post-Installation section of the guide. 

#### b). Install gflags and python libraries

	  $sudo apt install libgflags-dev
	  $sudo apt install python3-pip
    $pip3 install -r /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/requirements_caffe.txt

#### c). Compile samples
Compile in-built samples in OpenVINO™ toolkit 

	$cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/
	$sudo mkdir build && cd build
	$sudo cmake –DCMAKE_BUILD_TYPE=Debug ..
	$sudo make  

#### d). Download models using model downloader scripts in OpenVINO™ toolkit installed folder
   - Install python3 (version 3.5.2 or newer) 
   - Install yaml and requests modules with command:

   		$sudo -E pip3 install pyyaml requests
   
   - Run model downloader script with -h key to show help message:
  		
	$cd /opt/intel/computer_vision_sdk/deployment_tools/model_downloader
	$sudo ./downloader.py
		
		
## Workshop Agenda
* **Intel Smart Video/Computer Vision Tools Overview** - Priyanka
  - Slides - [Introduction to Intel Smart Video Tools](./presentations/01-Introduction-to-Intel-Smart-Video-Tools.pptx)

* **Basic End to End Object Detection Example** - Priyanka
  - Slides - [Basic End to End Object Detection Example](./presentations/02-Basic-End-to-End-Object-Detection-Example.pptx)
  - Lab - [Basic End to End Object Detection Example](./object-detection/README.md)

* **Hardware Heterogeneity** - Priyanka
  - Slides - [Hardware Heterogeneity](./presentations/03-Hardware-Heterogeneity.pptx) - Link is broken.
  - Lab - [Hardware Heterogeneity](./hardware-heterogeneity/README.md)

* **HW Acceleration with Intel® Movidius™ Neural Compute Stick** - Priyanka
  - Lab - [HW Acceleration with Intel® Movidius™ Neural Compute Stick](./HW-Acceleration-with-Movidious-NCS/README.md) 
  
* **FPGA Inference Accelerator** - Richard C
  - Slides - [HW Acceleration with Intel® Movidius™ Neural Compute Stick](./presentations/04-HW-Acceleration-with-FPGA.pptx)

* **Optimization Tools and Techniques** - Priyanka
  - Slides - [Optimization Tools and Techniques](./presentations/04_05_Optimization_and_advanced_analytics.pptx) - Link is broken.
  - Lab - [Optimization Tools and Techniques](./optimization-tools-and-techniques/README.md)
  
* **Advanced Video Analytics** - Priyanka
  - Slides - [Advanced Video Analytics](./presentations/04_05_Optimization_and_advanced_analytics.pptx)
  - Lab - [Advanced Video Analytics](./advanced-video-analytics/README.md)
