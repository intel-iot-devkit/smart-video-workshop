# Part1: Up2 AI Vision Kit OOBE


# Part2: Using Intel System Studio to build your application on host laptop and run it on Up2
This tutorial will guide you through how to import existing Makefile project and CMake project into Intel System Studio, then run the applications both locally on the host laptop and remotely on the target Up2 board. All the results and outputs from both local and remote application will be shown on host laptop display.

### Import Makefile Project - Object-detection
#### 1. Pre-requisites
Please complete at least first three Labs in this workshop, make sure at least you have **.bin** and **.xml** files generated in the directory: **/opt/intel/workshop/smart-video-workshop/object-detection/mobilenet-ssd/FP32**

#### 2. Copy the object-detection folder to Intel System Studio workspace and to UP2 /home/upsquared/
> **Note:** *replace the IP_address below with your UP2 IP address*

	cp -r /opt/intel/workshop/smart-video-workshop/object-detection /home/intel/system_studio/workspace
	cd /home/intel/system_studio/workspace/object-detection
	rm -f tutorial1 ROIviewer Makefile_ROIviewer
	scp -r /home/intel/system_studio/workspace/object-detection upsquared@IP_address:/home/upsquared/

#### 3. Create a C++ project named object-detection in Intel System Studio
1. Open Intel System Studio pre-installed on your laptop by double-click the icon on Desktop
2. Choose **File -> New -> Project** to start the new project wizard.
3. Expand **C/C++** and select **C++ project**, Click Next.
4. Type the name **object-detection** for the project in the Name field.
5. In the Toolchains list, choose **Linux GCC**. Click Finish.
If you see an 'Old project will be overridden' message, click OK.
If you see an ‘Open Associated Perspective’ message, click Yes.
6. Expand project, double click **Makefile**, add below commands after existing commands, then save and close

        g++ -fPIE -O0 -g -o ROIviewer --std=c++11 ROIviewer.cpp -I. \
        -I/opt/intel/computer_vision_sdk/opencv/include/ \
        -L/opt/intel/computer_vision_sdk/opencv/lib -lopencv_core -lopencv_imgcodecs -lopencv_imgproc \
        -lopencv_highgui -lopencv_videoio -lopencv_video -lgflags
        
7. Right click the project name, at the bottom of the options, select **Properties -> C/C++ Build**
8. Uncheck **"Generate Makefiles automatically"**, then click **"workspace"** and select **object-detection**, click OK
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_C_C++_Build_Setup.png "C/C++ Build Setup")

	<br>

9. Click the little hammer icon to build the project, once complete, you will see two binaries files: **tutorial1** and **ROIviewer** generated

#### 4. Run tutorial1 and ROIviewer as local application on your laptop
##### tutorial1_local:
1. Right click **tutorial1**, select **Run As -> Run Configurations...**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration.png "Open Run Configuration")

	<br>

2. then doulbe click **C/C++ Application**, it will generate a configuration named tutorial1, rename it to **tutorial1_local**, click Apply
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_tutorial1_local.png "Setup Tutorial1_local Run Configuration")

	<br>

3. Click **Arguments** tag, add below arguments in **Program arguments:** then click **Apply** and **OK**

        ./tutorial1 -i /home/intel/system_studio/workspace/object-detection/Cars\ -\ 1900.mp4 -m /home/intel/system_studio/workspace/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_tutorial1_local_arguments.png "Setup Tutorial1_local Run Configuration")

	<br>

4. You will see the inference running locally on your laptop, and it will print out the results in the console windows

##### ROIviewer_local:
1. Right click **ROIviewer**, select **Run As -> Run Configurations...**, then doulbe click **C/C++ Application**, it will generate a configuration named tutorial1, rename it to **ROIviewer_local**, click Apply
2. Click **Arguments** tag, add below arguments in **Program arguments:** then click Apply and OK

        ./ROIviewer -i /home/intel/system_studio/workspace/object-detection/Cars\ -\ 1900.mp4 -l /home/intel/system_studio/workspace/object-detection/pascal_voc_classes.txt

3. You will see the ROIviewer running locally on your laptop, a video playing running cars with tags will be opened

#### 5. Run tutorial1 and ROIviewer as remote application on Up2 board
##### tutorial1_remote:
1. Right click **tutorial1**, select **Run As -> Run Configurations...**, then doulbe click **C/C++ Remote Application**, it will generate a configuration named tutorial1, rename it to **tutorial1_remote**, click Apply
2. Click **New** button after **Connection:**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_tutorial1_remote.png "Setup Tutorial1_remote Run Configuration")

	<br>
3. In the droplist, choose **SSH**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Create_a_New_Connection.png "Setup Tutorial1_remote Run Configuration")

	<br>
4. Then type **IP address** of your UP2 board, username: **upsquared**, choose **password based authentication**, then type **upsquared** as password, then click Finish
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Setup_New_Connection.png "Setup Tutorial1_remote Run Configuration")

	<br>

5. In **Remote Absolute File Path for C/C++ Application**, type:

		/home/upsquared/tutorial1
6. In **Commands to execute before application**

		source /opt/intel/computer_vision_sdk/bin/setupvars.sh
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_tutorial1_remote_commands_run_before_application.png "Setup Tutorial1_remote Run Configuration")

	<br>
7. Click **Arguments** tag, add below arguments in **Program arguments:** then click Apply and OK

        ./tutorial1 -i /home/upsquared/object-detection/Cars\ -\ 1900.mp4 -m /home/upsquared/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml

8. You will see the inference running remotely on UP2, and it will print out the results in the console windows on your host laptop

##### ROIviewer_remote:
1. Right click **ROIviewer**, select **Run As -> Run Configurations...**, then doulbe click **C/C++ Remote Application**, it will generate a configuration named tutorial1, rename it to **ROIviewer_remote**, click Apply
> **Note:** *If you have done creating a SSH connection for tutorial1_remote, skip step 2 here, just select **upsquared** from the droplist in Connection*
2. Click **New** button after **Connection:**, in the droplist, choose **SSH**, then type **IP address** of your UP2 board, username: **upsquared**, choose **password based authentication**, then type **upsquared** as password, then click Finish
3. In "Remote Absolute File Path for C/C++ Application", type:

		/home/upsquared/ROIviewer
4. In "Commands to execute before application"

		source /opt/intel/computer_vision_sdk/bin/setupvars.sh
5. Click **Arguments** tag, add below arguments in **Program arguments:** then click Apply and OK

        ./ROIviewer -i /home/upsquared/object-detection/Cars\ -\ 1900.mp4 -l /home/upsquared/object-detection/pascal_voc_classes.txt

6. You will see an **ERROR** message saying:

        (video:17654): Gtk-WARNING **: cannot open display: 
        logout

7. To solve this issue, open a Terminal on your laptop, type below commands and keep this terminal open

        ssh upsquared@IP_address -X
        echo %DISPLAY
        
   it will give you something like this
   
        localhost:10.0
        
8. Type below commands to "Commands to execute before application" in **ROIviewer_remote** Run Configuration, click Apply and Run, you will see the expected video displayed on your sceen

        export DISPLAY=localhost:10.0
        source /opt/intel/computer_vision_sdk/bin/setupvars.sh
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_Run_Configuration_ROIviewer_remote.png "Setup ROIviewer_remote Run Configuration")

	<br>

### Import CMake Project - Samples 
Only running interactive_face_detection sample in this workshop


#### 1. Copy the Samples folder to Intel System Studio workspace
	cp -r /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples /home/intel/system_studio/workspace
	
#### 2. Create a C++ project named samples in Intel System Studio
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

#### 3. Run interactive_face_detection_sample as local application on your laptop
1. Right click **interactive_face_detection_sample**, select **Run As -> Run Configurations...**
	<br>

	![image of Intel System Studio](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS_samples_Run_Configuration.png "Open Run Configuration")

	<br>

2. then doulbe click **C/C++ Application**, it will generate a configuration named tutorial1, rename it to **interactive_face_detection_sample_local**, click Apply
3. Click **Arguments** tag, add below arguments in **Program arguments:** then click **Apply** and **OK**

        ./interactive_face_detection_sample -m ${ROOT_DIR}/intel_models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -m_ag ${ROOT_DIR}/intel_models/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013.xml -m_hp ${ROOT_DIR}/intel_models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d GPU -d_ag GPU -d_hp GPU
4. Click **Variables… -> Edit Variables -> New…** and add a new variable named **ROOT_DIR** with the value **/opt/intel/computer_vision_sdk/deployment_tools**, click Apply
5. Click Run, you will see the realtime face detection with age, gender and head pose prediction on upper-left running locally on your laptop, and it will print out the results in the console windows

#### 4. Run interactive_face_detection_sample as remote application on UP2 then display the results on your laptop
1. Right click **interactive_face_detection_sample**, select **Run As -> Run Configurations...**, then doulbe click **C/C++ Remote Application**, it will generate a configuration named tutorial1, rename it to **interactive_face_detection_sample_remote**, click Apply
> **Note:** *If you have done creating a SSH connection for tutorial1_remote, skip step 2 here, just select **upsquared** from the droplist in Connection*
2. Click **New** button after **Connection:**, in the droplist, choose **SSH**, then type **IP address** of your UP2 board, username: **upsquared**, choose **password based authentication**, then type **upsquared** as password, then click Finish
3. In "Remote Absolute File Path for C/C++ Application", type:

		/home/upsquared/interactive_face_detection_sample
	
4. In "Commands to execute before application"

		export DISPLAY=localhost:10.0
		source /opt/intel/computer_vision_sdk/bin/setupvars.sh
5. Click **Arguments** tag, add below arguments in **Program arguments:** then click Apply and OK

		./interactive_face_detection_sample -m ${ROOT_DIR}/intel_models/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -m_ag ${ROOT_DIR}/intel_models/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013.xml -m_hp ${ROOT_DIR}/intel_models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -d GPU -d_ag GPU -d_hp GPU

6. You will see an **ERROR** message saying:

		/home/upsquared/interactive_face_detection_sample: error while loading shared libraries: libcpu_extension.so: cannot open shared object file: No such file or directory
		logout

7. To solve this issue, open a Terminal on your laptop, type below commands and keep this terminal open

		scp -r /home/intel/system_studio/workspace/samples/build/Debug/intel64/Debug/lib upsquared@<ip_address>:/home/upsquared/
		
8. Back to Run Configuration, in "Commands to execute before application"

		export DISPLAY=localhost:10.0
        
9. You will see an **ERROR** message saying:

		Illegal instruction (core dumped)
		logout
		
10. To solve this issue, expand cmake folder under project, open **OptimizationFlags.cmake** file, then comment out line 25-27, save and close, remove **Build** folder and rebuild the project

		#set(ENABLE_SSE42   ${HAVE_SSE42})
		#set(ENABLE_AVX2    ${HAVE_AVX2})
		#set(ENABLE_AVX512F ${HAVE_AVX512F})

10. Run Step 7 again, then you can run interactive_face_detection_sample_remote
