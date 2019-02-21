
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
