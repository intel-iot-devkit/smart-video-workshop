
# Docker* based OpenVINO™ projects with Intel® System Studio 2019
In this lab, developers who are interested in using the Intel® System Studio Eclipse*-based Integrated Development Environment (IDE) with the OpenVINO™ toolkit to develop Computer Vision and Deep Learning optimized applications, will have a chance to experience how to create, build, and run the Docker* based OpenVINO™ projects on either the host laptop and target UP²* board.

## Create and Build a New Project in Intel® System Studio - Interactive Face Detection Demo

In this section, we step you through creating and building a new project based on the OpenVINO™ sample projects available in the Intel® System Studio Eclipse*-based IDE.

1. You need a custom Docker* image in order to use the OpenVINO samples. Make sure you have completed [Create a Custom Docker* image](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/up2-vision-kit/setup_intel_system_studio_2019.md#2--create-a-custom-docker-image) session. If you have already done this, skip this step. 
2. Choose **File > New > Project** from the menu to start the new project wizard.
3. Expand **Intel Application Development** and select **C++ Project**. Click **Next**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_New_project_wizard.png)  
  
    <br>
    
4. Click to open the **Tool Samples** tab.
5. Expand **OpenVINO™ Toolkit** and select **Face Detection**. The sample project name appears in the New Project Name field. If you wish to change it, type over the displayed name.
6. For Builder and Build Options, leave CMake and Docker selected.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/Builder_and_Build_Options.JPG)  
  
    <br>
    
7. Click **Next**.
8. Select the custom Docker image you created in the [Create a Custom Docker* image](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/up2-vision-kit/setup_intel_system_studio_2019.md#2--create-a-custom-docker-image) session.
9. Click **Finish** to start the build process.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/Select_a_docker_container.png)  
  
    <br>
    
CMake creates the necessary make files for the project, and then starts a build. View the build progress in the CMakeconsole and CDT buildconsole at the bottom of the workspace.

## Create a connection to the local system
1. Make sure your target device is functioning properly and can be reached on the network by your host system.
2. On the main toolbar, click the arrow next to the New Connection box, and then select New Connection.


3. Select Connection for container based C/C++ applications or Java* applications, and then click Next.


4. Type a name in the Connection Name field.
5. Enter **localhost** in the Address field, and then click Finish.
6. When prompted, provide the appropriate credentials to access your device, and then click OK.

## Run Interactive Face Detection Demo on your host laptop

- This demo showcases the Object Detection task applied to face recognition using a sequence of neural networks.
- Async API can improve the overall frame-rate of the application. Rather than waiting for inference to complete, the application can continue operating on the host while accelerator is busy.
- This demo maintains four parallel infer requests for the Age/Gender Recognition, Head Pose Estimation, Emotions Recognition, and Facial Landmarks Estimation that run simultaneously.

### Step 1. Update the launch configuration
1. On the main toolbar, click the down arrow next to the Run button, and then select Run Configurations.


2. Click to open C/C++ Application built in a container and running on Linux.
3. Select Security_Barrier_Camera.
4. On the Main tab, under C/C++ Application, click Search Project.


5. Select security_barrier_camera_demo.


### Step 2. [Optional] Verify that the ROOT_DIR variable is set
1. Still on the Main tab, click the Variables button.


2. Click Edit Variables.


3. Verify that ROOT_DIR is set to /opt/intel/computer_vision_sdk/deployment tools.


4. Click Cancel twice to close the dialogs.

### Step 3. [Optional] Verify that commands are set properly
1. Still on the Main tab, review the Commands to execute before application to make sure the paths are set properly for your target system, as follows.
> **Note:** The following assumes that OpenVINO is installed on the default location for a user with root privileges. If you’ve installed OpenVINO in a different folder, modify the first line below accordingly.

        export INTEL_CVSDK_DIR=/opt/intel/computer_vision_sdk_2018.4.420; 
        export INFENG=$INTEL_CVSDK_DIR/deployment_tools/inference_engine; 
        export IE_PLUGINS_PATH=$INFENG/lib/ubuntu_16.04/intel64; 
        [ ! -d /tmp/OpenVINO ] && mkdir /tmp/OpenVINO; 
        cp $INFENG/lib/ubuntu_16.04/intel64/libcpu_extension_sse4.so /tmp/OpenVINO/libcpu_extension.so; 
        export LD_LIBRARY_PATH=/tmp/OpenVINO:$INTEL_CVSDK_DIR/opencv/lib:/opt/intel/opencl:$INFENG/external/gna/lib:$INFENG/external/mkltiny_lnx/lib:$INFENG/external/omp/lib:$INFENG/lib/ubuntu_16.04/intel64:$LD_LIBRARY_PATH;
        export DISPLAY=:0;
        

> **Tip:** If your system has a processor that supports the AVX instructions, you can use a more optimized version of the libcpu_extension. To do this, change this part of the above command:

From this: 

    cp $INFENG/lib/ubuntu_16.04/intel64/libcpu_extension_sse4.so /tmp/OpenVINO/libcpu_extension.so;

To this:

    cp $INFENG/lib/ubuntu_16.04/intel64/libcpu_extension_avx2.so /tmp/OpenVINO/libcpu_extension.so;

### Step 4. Verify that arguments are set properly and Run
1. Select the Arguments tab.
2. Verify that the Program arguments are set properly. Change them as needed.


3. [Optional] Run with video instead of a single image. To use the car-detection.mp4 video:
    - Find the video in GitHub*. Click intel-iot-devkit/sample-videos.
    - Download the video to a folder on your target system.
    - Provide the path to the video file in the arguments in step 3 above.
4. Click Apply and Run. 
 
