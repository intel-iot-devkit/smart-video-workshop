# Build your application on laptop and run it on Up2 with Intel System Studio - CMake Porject
This tutorial will guide you through how to import existing Makefile projects into Intel System Studio, then run the applications both locally on the host laptop and remotely on the target Up2 board. All the results and outputs from both local and remote application will be shown on host laptop display.

### Import existing CMake Project - Samples(interact-face-detection)
#### 1. Pre-requisites
> :warning: Please make sure you have setup the [Internet Connection Sharing](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/up2-vision-kit/dev_machine_setup.md) to get an IP address for your Up2 AI Vision Kit

Only running **interactive_face_detection** sample in this workshop, to save the build time, we remove unused projects from this sample folder.


#### 2. Copy the Samples folder to Intel System Studio workspace
	cp -r /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples /home/intel/system_studio/workspace
	
#### 3. Create a C++ project named samples in Intel System Studio
1. Open Intel System Studio pre-installed on your laptop by double-click the icon on Desktop
2. Choose **File -> New -> Project** to start the new project wizard.
3. Expand **C/C++** and select **C++ project**, Click Next.
4. Type the name **samples** for the project in the Name field.
5. In the Toolchains list, choose **Linux GCC**. Click Finish.
If you see an 'Old project will be overridden' message, click OK.
If you see an ‘Open Associated Perspective’ message, click Yes.
6. Right click the project name, at the bottom of the options, select **Properties -> C/C++ Build**
7. Expand **C/C++ Build** and select **Toolchain Editor**. The Tool Chain Editor options are displayed on the right, from the **Current Builder** droplist, choose **CMake Builder (portable)**. Click **OK**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_CMake_C_C++_Build_Setup.png "CMake C/C++ Build Setup")

	<br>
8. Expand project, delete below folders
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_CMake_sample_simplify.png "CMake C/C++ Build Setup")

	<br>
9. Update **CMakeLists.txt** by commenting out the deleted directories, only keeping the **interactive_face_detection_sample** uncommented, save and close CMakeLists.txt

		#add_subdirectory(object_detection_sample)
		add_subdirectory(interactive_face_detection_sample)
		#add_subdirectory(security_barrier_camera_sample)
		#add_subdirectory(object_detection_demo_ssd_async)
		#add_subdirectory(object_detection_sample_ssd)
		#add_subdirectory(classification_sample)
		#add_subdirectory(classification_sample_async)
		#add_subdirectory(hello_classification)
		#add_subdirectory(hello_request_classification)
		#add_subdirectory(segmentation_sample)
		#add_subdirectory(style_transfer_sample)

10. Click the little hammer icon to build the project, once complete, you will see **interactive_face_detection_sample** generated with some other testing purpose binaries

### Run interactive_face_detection_sample as local application on your laptop
1. Right click **interactive_face_detection_sample**, select **Run As -> Run Configurations...**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_samples_Run_Configuration.png "Open Run Configuration")

	<br>

2. then doulbe click **C/C++ Application**, it will generate a configuration named tutorial1, rename it to **interactive_face_detection_sample_local**, click Apply
3. Click **Arguments** tag, add below arguments in **Program arguments:** then click **Apply** and **OK**

        ./interactive_face_detection_sample -m ${ROOT_DIR}/intel_models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -m_ag ${ROOT_DIR}/intel_models/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013.xml -m_hp ${ROOT_DIR}/intel_models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d GPU -d_ag GPU -d_hp GPU
4. Click **Variables… -> Edit Variables -> New…** and add a new variable named **ROOT_DIR** with the value **/opt/intel/computer_vision_sdk/deployment_tools**, click Apply
5. Click Run, you will see the realtime face detection with age, gender and head pose prediction on upper-left running locally on your laptop, and it will print out the results in the console windows

### Run interactive_face_detection_sample as remote application on UP2 then display the results on your laptop
1. Right click **interactive_face_detection_sample**, select **Run As -> Run Configurations...**, then doulbe click **C/C++ Remote Application**, it will generate a configuration named tutorial1, rename it to **interactive_face_detection_sample_remote**, click Apply
> **Note:** *If you have done creating a SSH connection for tutorial1_remote, skip step 2 here, just select **upsquared** from the droplist in Connection*
2. Click **New** button after **Connection:**, in the droplist, choose **SSH**, then type **IP address** of your UP2 board, username: **upsquared**, choose **password based authentication**, then type **upsquared** as password, then click Finish
3. In **Remote Absolute File Path for C/C++ Application**, type:

		/home/upsquared/interactive_face_detection_sample
	
4. In **Commands to execute before application**, type:
> **Note:** *Remember to open a Terminal on your laptop, type **ssh upsquared@IP_address -X** and keep this terminal open, for running a GUI application remotely and display it locally*

		export DISPLAY=localhost:10.0
		source /opt/intel/computer_vision_sdk/bin/setupvars.sh
5. Click **Arguments** tag, add below arguments in **Program arguments:** then click Apply and OK

		./interactive_face_detection_sample -m ${ROOT_DIR}/intel_models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -m_ag ${ROOT_DIR}/intel_models/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013.xml -m_hp ${ROOT_DIR}/intel_models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d GPU -d_ag GPU -d_hp GPU

6. You will see an **ERROR** message saying:

		/home/upsquared/interactive_face_detection_sample: error while loading shared libraries: libcpu_extension.so: cannot open shared object file: No such file or directory
		logout
		
7. This is because of two **.so** library files were generated and needed to run this application correctly but running as Remote Application Intel System Studio only passes the binary to the target device. To solve this issue, open a Terminal on your laptop, type below commands, then back to Intel System Studio, run the application again

		scp -r /home/intel/system_studio/workspace/samples/build/Debug/intel64/Debug/lib upsquared@<ip_address>:/home/upsquared/
		        
8. In **Commands to execute before application**, type:

		export LD_LIBRARY_PATH=/home/upsquared/lib
		export DISPLAY=localhost:10.0
		source /opt/intel/computer_vision_sdk/bin/setupvars.sh
9. Now you will see an new **ERROR** message saying:

		Illegal instruction (core dumped)
		logout
		
10. This is because we compiled this application on a laptop which has advanced CPU extensions than the target system, then the generated binary will not able to run on the target device. To solve this issue, we need to tell the compiler not to use those advanced CPU extensions. Expand cmake folder under project, open **OptimizationFlags.cmake** file, then comment out line 25-27, save and close, remove **Build** folder and rebuild the project

		#set(ENABLE_SSE42   ${HAVE_SSE42})
		#set(ENABLE_AVX2    ${HAVE_AVX2})
		#set(ENABLE_AVX512F ${HAVE_AVX512F})

11. Run Step 7 again, since you have generated new **.so** files, then you can run interactive_face_detection_sample_remote
