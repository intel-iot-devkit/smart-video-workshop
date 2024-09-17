
# Install Intel® System Studio 2019
(Assuming using Ubuntu* Desktop 16.04 and Intel® Distribution of OpenVINO™ toolkit already properly installed)
1.  Go to https://software.intel.com/en-us/system-studio
2.  Select **Choose & Download**
3.  Click **Register & Download**
4.  Fill out the form then submit, an Email from **Intel Registration Center** will be sent to your registered Email address with **Serial Number** of Intel® System Studio, you will enter into below page, select **Linux** as Development operating system and **Linux and Android** as Target operating system, then click **Continue**
5.  Click **Get the Full Package**
    <br>
  
    ![image of Intel_System_Studio_Choose_Host_and_Target_OS](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_Choose_OS.png "Figure 1")  
  
    <br>
  
6.  Then click **Download**, by default **intel-sw-tools-installation-bundle.zip**  will be downloaded to your **/home/username/Downloads** on your Ubuntu, if you are downloading it from Windows, after download, copy the whole **intel-sw-tools-installation-bundle.zip file** to your Ubuntu OS
    <br>  
  
    ![image of Intel_System_Studio_Choose_Host_and_Target_OS](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_Download_Full_Package.png "Figure 1")  
  
    <br>

7.  Unzip the zip file, then you will see three files:
    1. intel-sw-tools-config-custom.json
    2. intel-sw-tools-license.lic
    3. system_studio_2019_update_2.tar.gz
    
8.  Extract **system_studio_2019_update_2.tar.gz**

        tar -xvf system_studio_2019_update_2.tar.gz

9.  Open a terminal, go to the extracted directory and run as root user

        sudo ./install.sh
    
10.  Installation GUI will pop up, enter the Serial Number Emailed to you, you can click **Customize** then **Next** to choose which components you’d like to install, here we only selected the necessary components for our workshop:

        1. Docker* based build system
        2. Eclipse IDE
        3. GUN* GDB 8.0
        4. Intel® C++ Compiler 19.0
        5. Intel Threading Building Blocks 2019
        6. Intel® VTune™ Amplifier 2019
        7. Yocto Project Compatible Application Development Plugins

      <br>

      ![image of Intel_System_Studio_Components_List](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_Installation_Select_Components.png "Figure 2")  

      <br>  

11.  Click Next, **don’t** check **“Integrate to Wind River Linux and Wind River Workbench”** and **“Integrate into Android NDK”**, click Install
12.  Once installation complete, **uncheck** Launch Intel® System Studio, Click Finish

# Prepare Docker* based OpenVINO projects using Intel® System Studio 2019
### 1.  Install the latest Docker* CE edition

Follow the instructions on [Get Docker CE for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### 2.  Create a Custom Docker* Image

Before you can run or debug OpenVINO sample applications in the Intel System Studio Eclipse*-based IDE, you need to create a custom Docker* image (also referred to as a “platform”). 

**Step 1. Download the customized Docker file**

We’ve provided a Docker file that you can use to create the custom Docker image.

1. Download the Docker file from: https://software.intel.com/en-us/download/intel-system-studio-and-openvino-docker-file-for-r5.
2. Extract the Docker file from the archive to a location on your host system. 

**Step 2. Add a custom Docker image**

Use the **Platform Support Manager** to add a new custom Docker image to Intel System Studio.

1. From the IDE toolbar, choose **Project > Manage installed development platforms** to open the **Platform Support Manager**.
    <br>
  
    ![](../images/Platform%20Support%20Manager.png)  
  
    <br>

2. Click the **New** button, which is located below the list of platforms, to open the Add Custom Docker Image dialog.
    <br>
  
    ![](../images/Add%20Custom%20Docker%20Image.png)  
  
    <br>

3. Enter information, as follows:

    1. **Custom Image Name**: Type a name for the custom image. For example, Ubuntu OpenVINO R5.
    2. **Select Base Image**: Select Ubuntu Linux 16.04 64 bit (GCC) v14 or a later version, if available.
    3. **Docker ID**: Type an identifier. It **must be all **lowercase and cannot contain spaces**. For example, iss-ubuntu-16.04-openvino-r5. Make sure the ID does not end with a dash. This will cause an error.
    4. **Description**: Type a description. This field cannot be left empty.
    5. **Dockerfile**: Click Browse and select the custom Docker file you downloaded in Step 1 above.
    
4. Click **Finish**, The new custom Docker image is now listed under Custom Linux Platform. The Status column shows Not Installed.
    <br>
  
    ![](../images/Custom%20Linux%20Platform.png)
    
    <br>

**Step 3. Build the new custom Docker image**

1. Still on the Platform Support Manager dialog, under **Custom Linux Platform**, select the checkbox next to the custom Docker image you just added.
2. Click **Start**.
3. When a message saying that the installation may take more than 15 minutes appears, click **Yes** to continue.
The time to complete the process varies and there will be periods where the progress bar and status messages in the console remain static.
4. Wait until the following messages appear in the console to indicate that the process is complete:

        Successfully built 123xyz
        Successfully tagged iss-ubuntu-16.04-some-id:latest

5. Click **Close**.

You are all set for creating a Docker* based Intel® Distribution of OpenVINO™ project with Intel® System Studio 2019 now.
Reference Document: [Create a Custom Docker* Image](https://software.intel.com/en-us/articles/get-started-with-openvino-and-intel-system-studio-2019#inpage-nav-4-3)
