# Optimized Inference at the Edge with Intel® Tools and Technologies 
This workshop will walk you through a computer vision workflow using the latest Intel® technologies and comprehensive toolkits including support for deep learning algorithms that help accelerate smart video applications. You will learn how to optimize and improve performance with and without external accelerators and utilize tools to help you identify the best hardware configuration for your needs. This workshop will also outline the various frameworks and topologies supported by Intel® accelerator tools. 

> :warning: This workshop content has been validated with Intel® Distribution of OpenVINO™ toolkit version R4 2020 (openvino_toolkit_2020.4.287). 

## How to Get Started
   
In order to use this workshop content, you will need to setup your hardware and install the Intel® Distribution of OpenVINO™ toolkit for infering your computer vision application.  
### 1. System requirements
System Requirement can be found from [HERE](https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit/system-requirements.html)

### 2. Operating System
These labs have been validated on Ubuntu* 18.04 OS. 

### 3. Software installation steps
#### a). Install Intel® Distribution of OpenVINO™ toolkit 
[Download](https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit/choose-download/linux.html) Linux*-based Intel® Distribution of OpenVINO™ toolkit and use steps described in the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)
to install the Intel® Distribution of OpenVINO™ toolkit, set the Environment Variables, configure Model Optimizer, run the Verification Scripts to verify installation, and additional steps to enable the toolkit components to use GPU or VPU on your system.

#### b). Run the demo scipts and compile samples
Run demo scripts (any one of them or both if you want to both the demos) which will generate the folder $HOME/inference_engine_samples with the current Intel® Distribution of OpenVINO™ toolkit built. 

	cd /opt/intel/openvino/deployment_tools/demo
	./demo_squeezenet_download_convert_run.sh
	./demo_security_barrier_camera.sh
	
	cd $HOME/inference_engine_samples_build
	make

	cd $HOME/inference_engine_demos_build
	make
	
## Workshop Agenda
* **Intel® Distribution of OpenVINO™ toolkit Overview**
  - Slides - [Introduction to Smart Video Tools](./presentations/01.%20Intel%20Distribution%20of%20OpenVINO%20Toolkit%20Overview.pdf)
  - Lab Setup - [Lab Setup Instructions](./Lab_setup.md)
  
* **Model Optimizer**
  - Slides - [Model Optimizer](./presentations/02.%20Model%20Optimizer.pdf)
  - Lab1 - [Optimize a Caffe* Classification Model - SqueezeNet v1.1](./Labs/Optimize_Caffe_squeezeNet.md)
  - Lab2 - [Optimize a Tensorflow* Object Detection Model - SSD with MobileNet](./Labs/Optimize_Tensorflow_Mobilenet-SSD.md)

* **Inference Engine**
  - Slides - [Inference Engine](./presentations/03.%20Inference%20Engine.pdf)
  - Lab3 - [Run Classfication Sample application with the optimized SqueezeNet v1.1](./hREADME.md)
  - Lab4 - [Run Object Detection Sample application with the optimized SSD with MobileNet](./hREADME.md)
  - Lab5 - [Run Benchmark App with Hetero plugin](./README.md)

* **Accelerators based on Intel® Movidius™ Vision Processing Unit**
  - Slides - [Accelerators based on Intel® Movidius™ VPU](./presentations/04.%20Accelerators%20based%20on%20Intel®%20Movidius™%20Vision%20Processing%20Unit.pdf)
  - Lab6 - [HW Acceleration with Intel® Movidius™ Neural Compute Stick2](./HW-Acceleration-with-Movidious-NCS/README.md)
  - Lab7 - [Run Benchmark App with Multi plugin](./README.md)
  
* **Accelerators based on Intel® Arria® FPGA**
  - Slides - [Accelerators based on Intel® Arria® FPGA](./presentations/05.%20Accelerators%20based%20on%20Intel®%20Arria®%20FPGA.pdf)

* **Multiple Models in One Application** 
  - Slides - [Multiple Models in One Application](./presentations/08.%20Multiple%20Models%20in%20One%20Application.pdf) 
  - Lab8 - [Run Security Barrier Demo Application](./README.md) 
  
* **Deep Learning Workbench**
  - Slides - [Deep Learning Workbench](./presentations/06.%20Deep%20Learning%20Workbench.pdf) 
  - Demo Video - [DL Workbench Walkthrough](./README.md)
  
* **Deep Learning Streamer**
  - Slides - [Deep Learning Streamer](./presentations/07.%20Deep%20Learning%20streamer.pdf) 
  - Lab9 - [Build a Media Analytic Pipeline with DL Streamer](./README.md)

* **Intel® DevCloud for the Edge**
  - Slides - [Intel® DevCloud for the Edge](./presentations/09.%20Intel%20DevCloud%20for%20the%20Edge.pdf) 
  - Demo Video - [Intel® DevCloud for the Edge Walkthrough](./README.md)


## Further Reading Materials
* **Support for Microsoft ONNX runtime in OpenVINO**
  - Slides - [ONNX runtime and OpenVINO](./presentations/ONNX_runtime_and_OpenVINO.pdf)
  
* **Healthcare applications and Required Features**
  - Slides - [Healthcare Applications](./presentations/Healthcare_presentation.pdf)
  

> #### Disclaimer

> Intel and the Intel logo are trademarks of Intel Corporation or its subsidiaries in the U.S. and/or other countries. 
 
> *Other names and brands may be claimed as the property of others
