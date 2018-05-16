# Optimized Inference at the Edge with Intel® Tools and Technologies 
This workshop will walk you through a computer vision workflow using the latest Intel® technologies and comprehensive toolkits including support for deep learning algorithms that help accelerate smart video applications. You will learn how to optimize and improve performance with and without external accelerators and utilize tools to help you identify the best hardware configuration for your needs. This workshop will also outline the various frameworks and topologies supported by Intel® accelerator tools. 

## How to Get Started
   
## Note: For the in-class training, the hardware and software setup part has already been done on the workshop hardware. In-class training participants should directly move to Workshop Agenda section. 

In order to use this workshop content, you will need to setup your hardware and install OpenVINO™ toolkit for infering your computer vision application.  
### Hardware requirements
The hardware requirements are mentioned in the System Requirement section of the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)

### Operating System
These labs have been validated on Ubuntu 16.04 OS. 

### Software installation steps
#### 1. Install OpenVINO™ toolkit 
Use steps described in the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)
to install OpenVINO™ toolkit as well as MediaSDK and OpenCL* mentioned in the Post-Installation section of the guide. 

#### 2. Install gflags and python libraries

	  $sudo apt install libgflags-dev
	  $sudo apt install python3-pip
    $pip3 install -r /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/requirements_caffe.txt

#### 3. Compile samples
Compile in-built samples in OpenVINO™ toolkit 

	$cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/
	$sudo mkdir build && cd build
	$sudo cmake –DCMAKE_BUILD_TYPE=Debug ..
	$sudo make  

## Workshop Agenda
* **Intel Smart Video/Computer Vision Tools Overview** - Priyanka
  - Slides - [Introduction to Intel Smart Video Tools](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/presentations/01-Introduction-to-Intel-Smart-Video-Tools.pptx)

* **Basic End to End Object Detection Example** - Priyanka
  - Slides - [Basic End to End Object Detection Example](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/presentations/02-Basic-End-to-End-Object-Detection-Example.pptx)
  - Lab - [Basic End to End Object Detection Example](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/object-detection/README.md)

* **Hardware Heterogeneity** - Priyanka
  - Slides - [Hardware Heterogeneity](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/presentations/03-Hardware-Heterogeneity.pptx)
  - Lab - [Hardware Heterogeneity](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/hardware-heterogeneity/README.md)

* **HW Acceleration with Intel® Movidius™ Neural Compute Stick** - Priyanka
  - Lab - [HW Acceleration with Intel® Movidius™ Neural Compute Stick](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/HW-Acceleration-with-Movidious-NCS/README.md) 
  
* **FPGA Inference Accelerator** - Richard C
  - Slides - [HW Acceleration with Intel® Movidius™ Neural Compute Stick](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/presentations/04-HW-Acceleration-with-FPGA.pptx)

* **Optimization Tools and Techniques** - Priyanka
  - Slides - [Optimization Tools and Techniques](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/presentations/04_05_Optimization_and_advanced_analytics.pptx)
  - Lab - [Optimization Tools and Techniques](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/optimization-tools-and-techniques/README.md)
  
* **Advanced Video Analytics** - Priyanka
  - Slides - [Advanced Video Analytics](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/presentations/04_05_Optimization_and_advanced_analytics.pptx)
  - Lab - [Advanced Video Analytics](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/advanced-video-analytics/README.md)
