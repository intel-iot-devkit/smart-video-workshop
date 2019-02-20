
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

6.  Then click **Download**, by default **intel-sw-tools-installation-bundle.zip**  will be downloaded to your **/home/username/Downloads** on your Ubuntu
  <br>  
  
  ![image of Intel_System_Studio_Choose_Host_and_Target_OS](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/ISS2019_Download_Full_Package.png "Figure 1")  
  
  <br>

7.  Unzip the zip file, then you will see three files:
    1. intel-sw-tools-config-custom.json
    2. intel-sw-tools-license.lic
    3. system_studio_2019_update_2.tar.gz
    
8.  Extract **system_studio_2019_update_2.tar.gz**

        tar -xvf system_studio_2019_update_2.tar.gz

9.  Open a terminal, go to the extracted installation directory and run **sudo ./install.sh**  
10.  Install as root user, type your password, enter the Serial Number Emailed to you, you can click **Customize** then **Next** to choose which components you’d like to install, here we only selected the **minimal requirements** for our workshop:

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
1.  Go to [Get Docker CE for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/), install the latest Docker* CE edition
2.  Go to [Create a Custom Docker* Image](https://software.intel.com/en-us/articles/get-started-with-openvino-and-intel-system-studio-2019#inpage-nav-4-3)

You are all set for creating a Docker* based Intel® Distribution of OpenVINO™ project with Intel® System Studio 2019 now.
