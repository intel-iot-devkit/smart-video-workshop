# Build your application on laptop and run it on UP²* with Intel System Studio - CMake Project
This tutorial will guide you through how to import existing CMake projects into Intel® System Studio, then run the applications both locally on the host laptop and remotely on the target UP²* board. All the results and outputs from both local and remote application will be shown on host laptop display.

### Import existing CMake Project - Samples(interact-face-detection)
#### 1. Pre-requisites
> :warning: Please make sure you have setup the [Internet Connection Sharing](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/up2-vision-kit/dev_machine_setup.md) to get an **IP address** for your UP Squared* AI Vision Kit, it should be a 10.42.0.xxx

Clean up some settings during our preparation of the workshop on Intel® System Studio by running below commands:

	cd /home/<username>/system_studio/workspace/.metadata/.plugins/
	rm -rf org.eclipse.core.*
	rm -rf org.eclipse.debug.*
	cd

#### 2. Prepare the samples project folder to Intel® System Studio workspace
	cd /home/<username>/system_studio/workspace
	mkdir samples
	cp /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/CMakeLists.txt /home/<username>/system_studio/workspace/samples
	cp -r /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/common /home/<username>/system_studio/workspace/samples
	cp -r /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/thirdparty /home/<username>/system_studio/workspace/samples
	cp -r /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/interactive_face_detection_demo /home/<username>/system_studio/workspace/samples
	
#### 3. Create a C++ project named samples in Intel® System Studio
1. Open Intel® System Studio pre-installed on your laptop by double-click the icon on Desktop
2. Go to **Window** -> **Preferences** -> **Intel(R) System Studio** -> **Hide unsupported wizards**, **uncheck** the box, hit Apply then OK
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Uncheck_Hide_Unsupported_Wizards.png "Uncheck")

	<br>
3. Choose **File -> New -> Project** to start the new project wizard.
4. Expand **C/C++** and select **C++ project**, Click Next.
5. Type the name **samples** for the project in the Name field.
6. In the Toolchains list, choose **Linux GCC**. Click Finish.
If you see an 'Old project will be overridden' message, click OK.
If you see an ‘Open Associated Perspective’ message, click Yes.
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Create_C++_Project.png "Create C++ Project")

	<br>
7. Right click the project name, at the bottom of the options, select **Properties -> C/C++ Build**
8. Expand **C/C++ Build** and select **Toolchain Editor**. The Tool Chain Editor options are displayed on the right, from the **Current Builder** droplist, choose **CMake Builder (portable)**. Click **Apply**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_CMake_C_C++_Build_Setup.png "CMake C/C++ Build Setup")

	<br>
	
9. Double click **CMake**, then select **Host OS overrides**, on the right panel, click **Add...** of **CMake cache entries to define (-D)**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Host_OS_Overrides.png "CMake C/C++ Build Setup")

	<br>
	
10. In the **Add new CMake Define** window, put **CMAKE_BUILD_TYPE** into Variable name, select **STRING** as Type, and put **Release** into Value, click **Apply**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_CMAKE_BUILD_TYPE.png "CMake C/C++ Build Setup")

	<br>
	
11. Click **C/C++ Build**, on the right panel, choose **Behavior** tag, then enter **-j8 interactive_face_detection_demo** after **Build (Incremnetal build)**, click **Apply** and **OK**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Build_Command.png "CMake C/C++ Build Setup")

	<br>
	
12. Click the little hammer icon on top left to build the project
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Click_To_Build_Project.png "CMake C/C++ Build Setup")

	<br>

### Run interactive_face_detection_sample as local application on your laptop
1. Right click **interactive_face_detection_sample** from **Binaries**, select **Run As -> Run Configurations...**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_samples_Run_Configuration.png "Open Run Configuration")

	<br>

2. Then doulbe click **C/C++ Application**, it will generate a configuration named interactive_face_detection_sample, rename it to **interactive_face_detection_sample_local**, click Apply
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_face_detection_local.png "Open Run Configuration")

	<br>
3. Click **Arguments** tag, add below arguments in **Program arguments:** then click **Apply** and **OK**

        -m ${ROOT_DIR}/intel_models/face-detection-retail-0004/FP32/face-detection-retail-0004.xml -m_ag ${ROOT_DIR}/intel_models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -m_hp ${ROOT_DIR}/intel_models/head-pose-estimation-adas-0001/FP32/head-pose-estimation-adas-0001.xml -d CPU -d_ag CPU -d_hp CPU
	
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_face_detection_local_arguments.png "Open Run Configuration")

	<br>	
4. Click **Variables… -> Edit Variables -> New…** and add a new variable named **ROOT_DIR** with the value **/opt/intel/computer_vision_sdk/deployment_tools**, click Apply
5. Click Run, you will see the realtime face detection with age, gender and head pose prediction on upper-left running locally on your laptop, and it will print out the results in the console windows

### Run interactive_face_detection_sample as remote application on UP²* then display the results on your laptop
1. Preparation:

	a. Open a new Terminal, type command below, we are sending necessary dependencies to the remote device:

		scp -r /home/<username>/system_studio/workspace/samples/build/Debug/intel64/Debug/lib upsquared@10.42.0.xxx:/home/upsquared/
		
	b. To run a graphic application on remote device and display on your host, here we use X11 Forwarding with SSH, open another Terminal on your laptop, type below command and **keep this terminal open**

		ssh upsquared@10.42.0.xxx -X 
	
	c. To get the read and write authority of the camera on the remote device, we need to type: 
	
		sudo chmod 666 /dev/video0
		
	> **Note:** upsquared@upsquared-UP-APL01:~$ sudo chmod 666 /dev/video0


1. Right click **interactive_face_detection_sample** from **Binaries**, select **Run As -> Run Configurations...**, then doulbe click **C/C++ Remote Application**, it will generate a configuration named interactive_face_detection_sample, rename it to **interactive_face_detection_sample_remote**, click Apply

2. Click **New** button after **Connection:**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_New_Connection.png "Setup New Connection")

	<br>
3. In the droplist, choose **SSH**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Create_a_New_Connection.png "Setup Tutorial1_remote Run Configuration")

	<br>
4. Then type **IP address** of your UP² board(10.42.0.xxx), username: **upsquared**, choose **password based authentication**, then type **upsquared** as password, then click Finish
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Setup_New_Connection.png "Setup Tutorial1_remote Run Configuration")

	<br>	

5. In **Remote Absolute File Path for C/C++ Application**, type:

		/home/upsquared/interactive_face_detection_demo
	
6. In **Commands to execute before application**, type:
	> **Note:** *Remember to open a Terminal on your laptop, type **ssh upsquared@10.42.0.xxx -X** and keep this terminal open, for running a GUI application remotely and display it locally*
	
		export DISPLAY=localhost:10.0
		export LD_LIBRARY_PATH=/home/upsquared/lib
		source /opt/intel/computer_vision_sdk/bin/setupvars.sh

	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_face_detection_remote.png "Setup face_detection_remote Run Configuration")

	<br>	
	
6. Click **Arguments** tag, add below arguments in **Program arguments:** then click Apply and OK

		-m ${ROOT_DIR}/intel_models/face-detection-retail-0004/FP32/face-detection-retail-0004.xml -m_ag ${ROOT_DIR}/intel_models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -m_hp ${ROOT_DIR}/intel_models/head-pose-estimation-adas-0001/FP32/head-pose-estimation-adas-0001.xml -d CPU -d_ag CPU -d_hp CPU
		
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_face_detection_remote_arguments.png "Setup face_detection_remote Run Configuration")

	<br>		

Now we can make a comparison of the performance running the same application between on our host laptop and on the UP² AI Vision kit, and you can load different models used here to different hardware by changing the arguments and see what is the optimized configuration for this application. More details of this sample project can be found from here: /opt/intel/computer_vision_sdk_2018.3.343/deployment_tools/documentation/docs/InferenceEngineInteractiveFaceDetectionSampleApplication.html

> **Note:** The max resolution of the camera on UP² is 1920 X 1080, the time for render each frame is unacceptable, which giving people lagging feeling. To solve this issue, we can set the camera resolution to 1280 X 720 by adding some codes in **main.c** under interact_face_detection_sample folder:

Line 858 above **const size_t width = (size_t) cap.get(CV_CAP_PROP_FRAM_WIDTH)**:

	cap.set(CV_CAP_PROP_FRAM_WIDTH,1280);
	cap.set(CV_CAP_PROP_FRAM_HEITHG,720);
	
After this, click save all and build all, then run your application again, it will give you better performance. 
