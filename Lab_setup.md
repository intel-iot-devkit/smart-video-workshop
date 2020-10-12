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

	cd /opt/intel/openvino_2021/deployment_tools/demo
	./demo_squeezenet_download_convert_run.sh
	./demo_security_barrier_camera.sh
	
	cd $HOME/inference_engine_samples_build
	make

	cd $HOME/inference_engine_demos_build
	make

## Lab setup
Set the folder to execute labs in the workshop github.

### Download workshop content and set directory path
#### 1. Create the workshop directory

	sudo mkdir -p /opt/intel/workshop/
	
#### 2. Change ownership of the workshop directory to the current user 

> **Note:** *replace the usernames below with your user account name*
		
	sudo chown username.username -R /opt/intel/workshop/

#### 3. Navigate to the new directory

	cd /opt/intel/workshop/

#### 4. Download and clone the workshop content to the current directory (/opt/intel/workshop/smart-video-workshop).

	git clone https://github.com/intel-iot-devkit/smart-video-workshop.git
	
