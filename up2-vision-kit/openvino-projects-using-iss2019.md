
# Docker* based OpenVINO™ projects with Intel® System Studio 2019
In this lab, developers who are interested in using the Intel® System Studio Eclipse*-based Integrated Development Environment (IDE) with the OpenVINO™ toolkit to develop Computer Vision and Deep Learning optimized applications, will have a chance to experience how to create, build, and run the Docker* based OpenVINO™ projects on either the host laptop and target UP²* board.

## Create and Build a New Project in Intel® System Studio - Interactive Face Detection Demo

In this section, we step you through creating and building a new project based on the OpenVINO™ sample projects available in the Intel® System Studio Eclipse*-based IDE.

0. Open Intel System Studio by seraching in the Ubuntu serach bar or from the shortcut created on the Desktop on the laptop. 

> :warning: For the in-class training, the **custom Docker* image** has already been created on the workshop laptop. In-class training participants should directly move to **Step 2**. 

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
8. Select the custom Docker image, the name should be something like "Ubuntu OpenVINO R5".
9. Click **Finish** to start the build process.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/Select_a_docker_container.png)  
  
    <br>
    
CMake creates the necessary make files for the project, and then starts a build. View the build progress in the CMakeconsole and CDT buildconsole at the bottom of the workspace.

## Run Interactive Face Detection Demo on your host laptop

- Now let's run the face recognition demo application using a sequence of neural networks.
- From the source code, you can see Async API can improve the overall frame-rate of the application. Rather than waiting for inference to complete, the application can continue operating on the host while accelerator is busy.
- You can also find four parallel infer requests for the Age/Gender Recognition, Head Pose Estimation, Emotions Recognition, and Facial Landmarks Estimation that run simultaneously.

### Step1. Create a connection to the local system
1. On the main toolbar, click the **arrow** next to the **New Connection** box, and then select **New Connection**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_NEW_CONNECTION.png)  
  
    <br>

2. Select **Connection for container based C/C++ applications or Java applications**, and then click **Next**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_Connection_for_container.png)  
  
    <br>

3. Type a name in the **Connection Name** field, here we used **Local**.
4. Enter **localhost** in the **Address** field, and then click **Finish**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_Local_connection.png)  
  
    <br>

5. When prompted, provide the appropriate credentials to access your device, and then click **OK**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_connection_login_password.png)  
  
    <br>

### Step 2. Update the launch configuration
1. On the main toolbar, click the down arrow next to the Run button, and then select **Run Configurations**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_Run_Configuration.png)  
  
    <br>

2. Click to open **C/C++ Application built in a container and running on Linux**.
3. Select **Face_Detection**.
4. On the **Main** tab, click **Search Project**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_Search_Project.png)  
  
    <br>

5. Select **interactive_face_detection_demo**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_Program_Selection.png)  
  
    <br>

### Step 3. [Optional] Verify that the ROOT_DIR variable is set
1. Still on the **Mai**n tab, click the **Variables** button.
2. Click **Edit Variables**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_variables_button_0.png)  
  
    <br>

3. Verify that **ROOT_DIR** is set to **/opt/intel/computer_vision_sdk/deployment tools**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_verify_root_dir.png)  
  
    <br>

4. Click **Cancel** twice to close the dialogs.

### Step 4. Verify that commands are set properly
1. Still on the **Main** tab, review the **Commands to execute before application** to make sure the paths are set properly for your system, as follows.
> **Note:** The following assumes that OpenVINO is installed on the default location for a user with root privileges. If you’ve installed OpenVINO in a different folder, modify the first line below accordingly.

    export INTEL_CVSDK_DIR=/opt/intel/openvino; 
    export INFENG=$INTEL_CVSDK_DIR/deployment_tools/inference_engine; 
    export IE_PLUGINS_PATH=$INFENG/lib/ubuntu_16.04/intel64; 
    [ ! -d /tmp/OpenVINO ] && mkdir /tmp/OpenVINO; 
    cp $INFENG/lib/ubuntu_16.04/intel64/libcpu_extension_avx2.so /tmp/OpenVINO/libcpu_extension.so; 
    export LD_LIBRARY_PATH=/tmp/OpenVINO:$INTEL_CVSDK_DIR/opencv/lib:/opt/intel/opencl:$INFENG/external/gna/lib:$INFENG/external/mkltiny_lnx/lib:$INFENG/external/omp/lib:$INFENG/lib/ubuntu_16.04/intel64:$LD_LIBRARY_PATH;
    export DISPLAY=:0;
        
### Step 5. Verify that arguments are set properly and Run
1. Select the **Arguments** tab.
2. Verify that the **Program arguments** are set as follows.

        ./interactive_face_detection_demo -i cam -m /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_detection/face/sqnet1.0modif-ssd/0004/dldt/face-detection-retail-0004-fp16.xml -d MYRIAD -m_ag /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_attributes/age_gender/dldt/age-gender-recognition-retail-0013.xml -d_ag CPU -d_ag CPU -m_hp /opt/intel/openvino/deployment_tools/tools/model_downloader/Transportation/object_attributes/headpose/vanilla_cnn/dldt/head-pose-estimation-adas-0001-fp16.xml -d_hp GPU -d_hp GPU -m_em /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_attributes/emotions_recognition/0003/dldt/emotions-recognition-retail-0003-fp16.xml -d_em GPU -m_lm  /opt/intel/openvino/deployment_tools/tools/model_downloader/Transportation/object_attributes/facial_landmarks/custom-35-facial-landmarks/dldt/facial-landmarks-35-adas-0002.xml -d_lm CPU


3. Click **Apply** and **Run**. 
 
## Run Interactive Face Detection Demo on target Up2* AI Vision Board
Now, let's push the application to run on our remote system - Up2* AI Vision Board

### Step1. Create a connection to the local system
1. On the main toolbar, click the **arrow** next to the **New Connection** box, and then select **New Connection**.
2. Select **Connection for container based C/C++ applications or Java applications**, and then click **Next**.
3. Type a name in the **Connection Name** field, here we used **Remote**.
4. Enter **10.42.0.xxx** which you obtained from [Development machine and Internet Connection Sharing](./up2-vision-kit/dev_machine_setup.md) session, in the **Address** field, and then click **Finish**.
    <br>
  
    ![](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_remote_connection.png)  
  
    <br>

5. When prompted, provide the appropriate credentials to access your device, here both username and password are **upsquared** and then click **OK**.
6. Open a terminal, type commands below and **KEEP THIS TERMINAL OPEN**.

        ssh upsquared@10.42.0.xxx -X

### Step 2. Verify that commands are set properly
1. Still on the **Main** tab, review the **Commands to execute before application** to make sure the paths are set properly for your system, as follows.
> **Note:** The following assumes that OpenVINO is installed on the default location for a user with root privileges. If you’ve installed OpenVINO in a different folder, modify the first line below accordingly.

    export INTEL_CVSDK_DIR=/opt/intel/openvino; 
    export INFENG=$INTEL_CVSDK_DIR/deployment_tools/inference_engine; 
    export IE_PLUGINS_PATH=$INFENG/lib/ubuntu_16.04/intel64; 
    [ ! -d /tmp/OpenVINO ] && mkdir /tmp/OpenVINO; 
    cp $INFENG/lib/ubuntu_16.04/intel64/libcpu_extension_sse4.so /tmp/OpenVINO/libcpu_extension.so; 
    export LD_LIBRARY_PATH=/tmp/OpenVINO:$INTEL_CVSDK_DIR/opencv/lib:/opt/intel/opencl:$INFENG/external/gna/lib:$INFENG/external/mkltiny_lnx/lib:$INFENG/external/omp/lib:$INFENG/lib/ubuntu_16.04/intel64:$LD_LIBRARY_PATH;
    export XAUTHORITY=/home/upsquared/.Xauthority;
    export DISPLAY=localhost:10.0;
        
### Step 3. Verify that arguments are set properly and Run
1. Select the **Arguments** tab.
2. Verify that the **Program arguments** are set as follows.

        -i cam -m /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_detection/face/sqnet1.0modif-ssd/0004/dldt/face-detection-retail-0004-fp16.xml -d MYRIAD -m_ag /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_attributes/age_gender/dldt/age-gender-recognition-retail-0013.xml -d_ag CPU -d_ag CPU -m_hp /opt/intel/openvino/deployment_tools/tools/model_downloader/Transportation/object_attributes/headpose/vanilla_cnn/dldt/head-pose-estimation-adas-0001-fp16.xml -d_hp GPU -d_hp GPU -m_em /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_attributes/emotions_recognition/0003/dldt/emotions-recognition-retail-0003-fp16.xml -d_em GPU -m_lm  /opt/intel/openvino/deployment_tools/tools/model_downloader/Transportation/object_attributes/facial_landmarks/custom-35-facial-landmarks/dldt/facial-landmarks-35-adas-0002.xml -d_lm CPU


3. Click **Apply** and **Run**. 
