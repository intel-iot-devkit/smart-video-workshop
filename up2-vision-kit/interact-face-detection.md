# Build your application on laptop and run it on Up2 with Intel System Studio - CMake Porject
This tutorial will guide you through how to import existing CMake projects into Intel System Studio, then run the applications both locally on the host laptop and remotely on the target Up2 board. All the results and outputs from both local and remote application will be shown on host laptop display.

### Import existing CMake Project - Samples(interact-face-detection)
#### 1. Pre-requisites
> :warning: Please make sure you have setup the [Internet Connection Sharing](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/up2-vision-kit/dev_machine_setup.md) to get an IP address for your Up2 AI Vision Kit

Clean up some settings during our preparation of the workshop on Intel System Studio by running below commands:

	rm -rf ~/system_stdio/workspace/.metadata/.plugins/org.eclipse.core.*
	rm -rf ~/system_stdio/workspace/.metadata/.plugins/org.eclipse.debug.*

#### 2. Copy the Samples folder to Intel System Studio workspace
	cp -r /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples /home/intel/system_studio/workspace
	
#### 3. Create a C++ project named samples in Intel System Studio
1. Open Intel System Studio pre-installed on your laptop by double-click the icon on Desktop
2. Choose **File -> New -> Project** to start the new project wizard.
3. Expand **C/C++** and select **C++ project**, Click Next.

> :warning: If you don't see **C++ project** under **C/C++** in **File -> New -> Project...**, go to Window -> Preferences -> Intel(R) System Studio -> **Hide unsupported wizards**, **uncheck** the box, hit Apply then OK, then try again

4. Type the name **samples** for the project in the Name field.
5. In the Toolchains list, choose **Linux GCC**. Click Finish.
If you see an 'Old project will be overridden' message, click OK.
If you see an ‘Open Associated Perspective’ message, click Yes.
6. Right click the project name, at the bottom of the options, select **Properties -> C/C++ Build**
7. Expand **C/C++ Build** and select **Toolchain Editor**. The Tool Chain Editor options are displayed on the right, from the **Current Builder** droplist, choose **CMake Builder (portable)**. Click **OK**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_CMake_C_C++_Build_Setup.png "CMake C/C++ Build Setup")

	<br>

8. Expand project, delete below folders. In this lab, we will only run **interactive_face_detection** sample, in order to save the build time, we will remove unused projects from this sample folder. You can check all the other samples from **SamplesOverview** document located in: **/opt/intel/computer_vision_sdk_2018.3.343/deployment_tools/documentation/docs/SamplesOverview.html**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_CMake_sample_simplify.png "CMake C/C++ Build Setup")

	<br>
9. Update **CMakeLists.txt** by commenting out the deleted directories, only keeping the **interactive_face_detection_sample** uncommented, save and close CMakeLists.txt

	line 128:

		#add_subdirectory(speech_sample)
		
	line 142-158:

		#add_subdirectory(object_detection_sample)
		add_subdirectory(interactive_face_detection_sample)
		#add_subdirectory(security_barrier_camera_sample)
		#add_subdirectory(object_detection_demo_ssd_async)
		#add_subdirectory(object_detection_sample_ssd)
		#add_subdirectory(classification_sample)
		#add_subdirectory(classification_sample_async)
		#add_subdirectory(hello_autoresize_classification)
		#add_subdirectory(hello_classification)
		#add_subdirectory(hello_request_classification)
		#add_subdirectory(segmentation_sample)
		#add_subdirectory(mask_rcnn_sample)
		#add_subdirectory(style_transfer_sample)
		#add_subdirectory(end2end_video_analytics)
		#add_subdirectory(crossroad_camera_sample)
		#add_subdirectory(smart_classroom_sample)
		#add_subdirectory(multichannel_face_detection)
		
	line 166:

		#add_subdirectory(validation_app)

10. Since we are going to run the application on both laptop with an Intel Core CPU and on Up2 with an Intel Atom CPU, some of the CPU extensions are not supported for Atom, we want to make sure we disable it for compiler. Expand **cmake** folder under project samples, double click **OptimizationFlags.cmake**, then comment out line 26 and 27, save and close the file. Learn more about the Supported Devices from here: /opt/intel/computer_vision_sdk_2018.3.343/deployment_tools/documentation/docs/SupportedPlugins.html

		#            set(ENABLE_AVX2    ${HAVE_AVX2})
		#            set(ENABLE_AVX512F ${HAVE_AVX512F})

11. Click the little hammer icon to build the project, once complete, you will see **interactive_face_detection_sample** generated in **Binaries**

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

### Run interactive_face_detection_sample as remote application on UP2 then display the results on your laptop
1. Preparation:

	a. Open a new Terminal, type command below, we are sending necessary dependencies to the remote device:

		scp -r /home/intel/system_studio/workspace/samples/build/Debug/intel64/Debug/lib upsquared@10.42.0.xxx:/home/upsquared/
		
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
4. Then type **IP address** of your UP2 board(10.42.0.xxx), username: **upsquared**, choose **password based authentication**, then type **upsquared** as password, then click Finish
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Setup_New_Connection.png "Setup Tutorial1_remote Run Configuration")

	<br>	

5. In **Remote Absolute File Path for C/C++ Application**, type:

		/home/upsquared/interactive_face_detection_sample
	
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

Now we can make a comparison of the performance running the same application between on our host laptop and on the Up2 AI Vision kit, and you can load different models used here to different hardware by changing the arguments and see what is the optimized configuration for this application. More details of this sample project can be found from here: /opt/intel/computer_vision_sdk_2018.3.343/deployment_tools/documentation/docs/InferenceEngineInteractiveFaceDetectionSampleApplication.html

> **Note:** The output of the Up2 AI Kit is too big for the display, we can resize the windows by adding some codes in **main.c** under interact_face_detection_sample folder:

Line 48 below: using namespace InferenceEngine;

	using namespace cv;
	
Line 1105 above: cv::imshow("Detection results", prev_frame);

	cv::namedWindow( "Detection results", WINDOW_NORMAL);
	cv::resizeWindow("Detection results", 1280, 720);
