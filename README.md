# Optimized Inference at the Edge with Intel® Tools and Technologies 
This workshop will walk you through a computer vision workflow using the latest Intel® technologies and comprehensive toolkits including support for deep learning algorithms that help accelerate smart video applications. You will learn how to optimize and improve performance with and without external accelerators and utilize tools to help you identify the best hardware configuration for your needs. This workshop will also outline the various frameworks and topologies supported by Intel® accelerator tools. 

> :warning: This workshop content has been validated with Intel® Distribution of OpenVINO™ toolkit version R4 2020 (openvino_toolkit_2020.4.287). 

## How to Get Started
   
In order to use this workshop content, you will need to setup your hardware and install the Intel® Distribution of OpenVINO™ toolkit for infering your computer vision application.  
### 1. Hardware requirements
The hardware requirements are mentioned in the System Requirement section of the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)

### 2. Operating System
These labs have been validated on Ubuntu* 18.04 OS. 

### 3. Software installation steps
#### a). Install Intel® Distribution of OpenVINO™ toolkit 
Use steps described in the [install guide](https://software.intel.com/en-us/articles/OpenVINO-Install-Linux)
to install the Intel® Distribution of OpenVINO™ toolkit, set the Environment Variables, configure Model Optimizer, run the Verification Scripts to Verify Installation, and additional steps to enable the toolkit components to use GPU or VPU on your system.

#### b). Run the demo scipts and compile samples
Run demo scripts (any one of them or both if you want to both the demos) which will generate the folder $HOME/inference_engine_samples with the current Intel® Distribution of OpenVINO™ toolkit built. 

	cd /opt/intel/openvino/deployment_tools/demo
	./demo_squeezenet_download_convert_run.sh
	./demo_security_barrier_camera.sh
	
	sudo chown -R username.username $HOME/inference_engine_samples_build
	cd $HOME/inference_engine_samples_build
	make

	sudo chown -R username.username $HOME/inference_engine_demos_build
	cd $HOME/inference_engine_demos_build
	make
	
## Workshop Agenda
* **Smart Video/Computer Vision Tools Presentation**
  - Slides - [Introduction to Smart Video Tools](./presentations/OpenVINO%20in%203%20hours%202020-r4-v2.pdf)
 
 <!---
* **Training a Deep Learning Model**
  - Slides - [Training a Deep Learning Model](./presentations/DL_training_model.pdf)
  - Lab - Training a Deep Learning Model  [[Default](./dl-model-training/README.md)] [[Python](./dl-model-training/Python/Deep_Learning_Tutorial.ipynb)]
 --->
 
* **Basic End to End Object Detection Inference Example**
  <!---- Slides - [Basic End to End Object Detection Example](./presentations/02-03_Basic-End-to-End-Object-Detection-Example_R1_2020.pdf)--->
  - Lab Setup - [Lab Setup Instructions](./Lab_setup.md)
  - Lab - [Basic End to End Object Detection Example](./object-detection/README.md) <!--  [[Python](./object-detection/Python/basic_end_to_end_object_detection.ipynb)] -->

* **Hardware Heterogeneity**
  - Lab - [Hardware Heterogeneity](./hardware-heterogeneity/README.md) <!-- [[Python](./hardware-heterogeneity/Python/hardware-heterogeneity.ipynb)] -->

* **HW Acceleration with Intel® Movidius™ Neural Compute Stick**
  - Lab - [HW Acceleration with Intel® Movidius™ Neural Compute Stick](./HW-Acceleration-with-Movidious-NCS/README.md) <!--[[Python](./HW-Acceleration-with-Movidious-NCS/Python/HW_Acceleration_with_Movidius_NCS.ipynb)] -->
  
* **FPGA Inference Accelerator**
  - Slides - [HW Acceleration with Intel® FPGA](./presentations/FPGA.pdf)

* **Optimization Tools and Techniques** 
  <!---- - Slides - [Optimization Tools and Techniques](./presentations/04-05_Optimization_and_advanced_analytics_R2_2020.pdf) --->
  - Lab 1 - [Optimization Tools and Techniques](./optimization-tools-and-techniques/README.md) <!-- [[Python](./optimization-tools-and-techniques/Python/optimization_tools_and_techniques.ipynb)] -->
  <!---- - Lab 2- [Intel® VTune™ Amplifier tutorial](./optimization-tools-and-techniques/README_VTune.md) --->
  
* **Advanced Video Analytics**
  - Lab - [Multiple models usage example](./advanced-video-analytics/multiple_models.md) <!-- [[Python](./advanced-video-analytics/Python/advanced_video_analytics.ipynb)] -->
<!----  
* **UP²\* AI Vision Development kit as Edge**
  - Setup - [Development machine and Internet Connection Sharing](./up2-vision-kit/dev_machine_setup.md)
  - Lab - [Interact face detection on UP2 kit using Intel® System Studio](./up2-vision-kit/openvino-projects-using-iss2019.md) ---->

<!----
* **Implement Custom Layers for Inference on CPU and Integrated GPU**
  - Slides - [Custom Layer](./presentations/custom_layer.pdf)
  - Lab - [Custom Layer](./custom-layer/README.md)
---->

* **Support for Microsoft ONNX runtime in OpenVINO**
  - Slides - [ONNX runtime and OpenVINO](./presentations/ONNX_runtime_and_OpenVINO.pdf)
  
* **Healthcare applications and Required Features**
  - Slides - [Healthcare Applications](./presentations/Healthcare_presentation.pdf)
  
<!--	
* **Workshop Survey**
  - [Workshop Survey](https://idz.qualtrics.com/jfe/form/SV_a9GvOxtOrOziykB)
  - [Custom Layer Tutorial Survey](https://intelemployee.az1.qualtrics.com/jfe/form/SV_1ZjOKaEIQUM5FpX)
  - [Embedded Vision Summit Workshop Survey](https://intel.az1.qualtrics.com/jfe/form/SV_6RsCwmj6QGD3PAF)
  -->
> #### Disclaimer

> Intel and the Intel logo are trademarks of Intel Corporation or its subsidiaries in the U.S. and/or other countries. 
 
> *Other names and brands may be claimed as the property of others
