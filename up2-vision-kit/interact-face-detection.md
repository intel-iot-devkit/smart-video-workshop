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
1. Right click **interactive_face_detection_demo** from **Binaries**, select **Run As -> Run Configurations...**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_samples_Run_Configuration.png "Open Run Configuration")

	<br>

2. Then doulbe click **C/C++ Application**, it will generate a configuration named **interactive_face_detection_demo**, you can rename it to **interactive_face_detection_demo_local**, click **Apply**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_face_detection_local.png "Open Run Configuration")

	<br>
3. Click **Arguments** tag, add below arguments in **Program arguments:** then click **Apply** and **OK**

        -i cam -m ${ROOT_DIR}/intel_models/face-detection-retail-0004/FP32/face-detection-retail-0004.xml -d CPU -m_ag ${ROOT_DIR}/intel_models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -d_ag CPU -m_hp ${ROOT_DIR}/intel_models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d_hp GPU -m_em ${ROOT_DIR}/intel_models/emotions-recognition-retail-0003/FP16/emotions-recognition-retail-0003.xml -d_em GPU
	
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_face_detection_local_arguments.png "Open Run Configuration")

	<br>	
4. Click **Variables… -> Edit Variables -> New…** and add a new variable named **ROOT_DIR** with the value **/opt/intel/computer_vision_sdk/deployment_tools**, click **OK**

5. Click **Apply** and **Run**, you will see the realtime face detection with age, gender, head pose prediction and mood analysis on the display

### Run interactive_face_detection_sample as remote application on target UP²* but display the processed video on host laptop

Cross compiling may cause issues while host and target system has different type of CPU. In this case, our host laptop has the Intel Core CPU while on the UP²*, it was using Intel Atom CPU. So, we need to set the flags for compiler running on the host, to disable the unsuppoted CPU extensions for the target system. In addition, since we don't connect monitors for UP²* but are going to run a graphic application on it, we will use X forwarding to send back the graphics to show on our host system. 

1. Right click **Build** under the **samples**, click **delete**:
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Delete_Build.png "Delete Build")

	<br>
	
2. Right click the project name, at the bottom of the options, select **Properties -> C/C++ Build**, double click **CMake**, then select **Host OS overrides**, on the right panel, click **Add...** of **CMake cache entries to define (-D)**. In the **Add new CMake Define** window, put **ENABLE_AVX2** into Variable name, select **BOOL** as Type, and put **OFF** into Value:
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_ENABLE_AVX2.png "Add Cmake Option")

	<br>
	
3. click **Add...** of **CMake cache entries to define (-D)**. In the **Add new CMake Define** window, put **ENABLE_AVX512F** into Variable name, select **BOOL** as Type, and put **OFF** into Value, then click **Apply**:
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_ENABLE_AVX512F.png "Add Cmake Option")

	<br>
	
4. Click the little hammer icon on top left to rebuild the project
5. Open a terminal, copy the generated CPU extension library to the target system by typing:

		cd /home/<username>/system_studio/workspace/samples/build/Debug/intel64/Release/
		scp -r lib upsquared@10.42.0.xxx:/home/upsquared/
		
6. To run a graphic application on remote device and display on your host, here we use X11 Forwarding with SSH, open another Terminal on your laptop, type below command and **keep this terminal open**

		ssh upsquared@10.42.0.xxx -X 
	
7. To get the read and write authority of the camera on the remote device, we need to type: 
	
		sudo chmod 666 /dev/video0
		
	> **Note:** upsquared@upsquared-UP-APL01:~$ sudo chmod 666 /dev/video0


8. Back to Intel System Studio interface, right click **interactive_face_detection_sample_demo** from **Binaries**, select **Run As -> Run Configurations...**, then doulbe click **C/C++ Remote Application**, it will generate a configuration named **interactive_face_detection_demo**, rename it to **interactive_face_detection_demo_remote**, click Apply

9. Click **New** button after **Connection:**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_New_Connection.png "Setup New Connection")

	<br>
10. In the droplist, choose **SSH**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Create_a_New_Connection.png "Setup Tutorial1_remote Run Configuration")

	<br>
11. Then type **IP address** of your UP² board(10.42.0.xxx), username: **upsquared**, choose **password based authentication**, then type **upsquared** as password, then click Finish
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Setup_New_Connection.png "Setup Tutorial1_remote Run Configuration")

	<br>	

12. In **Remote Absolute File Path for C/C++ Application**, type:

		/home/upsquared/interactive_face_detection_demo
		
13. In **Commands to execute before application**, type:
	> **Note:** *Remember to open a Terminal on your laptop, type **ssh upsquared@10.42.0.xxx -X** and keep this terminal open, for running a GUI application remotely and display it locally*
	
		export DISPLAY=localhost:10.0
		export LD_LIBRARY_PATH=/home/upsquared/lib
		source /opt/intel/computer_vision_sdk/bin/setupvars.sh

	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_face_detection_remote.png "Setup face_detection_remote Run Configuration")

	<br>	
	
6. Click **Arguments** tag, add below arguments in **Program arguments:** then click Apply and OK

		-i cam -m ${ROOT_DIR}/intel_models/face-detection-retail-0004/FP32/face-detection-retail-0004.xml -d CPU -m_ag ${ROOT_DIR}/intel_models/age-gender-recognition-retail-0013/FP32/age-gender-recognition-retail-0013.xml -d_ag CPU -m_hp ${ROOT_DIR}/intel_models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d_hp GPU -m_em ${ROOT_DIR}/intel_models/emotions-recognition-retail-0003/FP16/emotions-recognition-retail-0003.xml -d_em GPU
		
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_face_detection_remote_arguments.png "Setup face_detection_remote Run Configuration")

	<br>		

Now we can make a comparison of the performance running the same application between on our host laptop and on the UP² AI Vision kit, and you can load different models used here to different hardware by changing the arguments and see what is the optimized configuration for this application. More details of this sample project can be found from here: /opt/intel/computer_vision_sdk_2018.3.343/deployment_tools/documentation/docs/InferenceEngineInteractiveFaceDetectionSampleApplication.html

> **Note:** The max resolution of the camera on UP² is 1920 X 1080, the time for render each frame is unacceptable, which giving people lagging feeling. To solve this issue, we can set the camera resolution to 1280 X 720 by adding some codes in **main.c** under interact_face_detection_sample folder:

Line 85 above **const size_t width = (size_t) cap.get(CV_CAP_PROP_FRAM_WIDTH)**:

        cap.set(cv::CAP_PROP_FRAME_WIDTH,1280);
        cap.set(cv::CAP_PROP_FRAME_HEIGHT,720);
	
After this, click save all and build all, then run your application again, it will give you better performance. 
