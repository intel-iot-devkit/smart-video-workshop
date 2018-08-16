
# Install Intel® System Studio 2018
(Assuming using Ubuntu Desktop 16.04 and OpenVINO Toolkit already properly installed)
1.	Go to https://software.intel.com/en-us/system-studio
2.	Select **Choose & Download**
3.	Click **Register & Download**
4.	Fill out the form then submit, an Email from **Intel Registration Center** will be sent to your registered Email address with **Serial Number** of Intel System Studio, you will enter into below page, select **Linux** as Development operating system and **Linux and Android** as Target operating system, then click **Continue**
  <br>  
  
  ![image of Intel_System_Studio_Choose_Host_and_Target_OS](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/Intel_System_Studio_Choose_Host_and_Target_OS.png "Figure 1")  
  
  <br>
  
5.	Download, by default **system_studio_2018_version_ultimate_edition.tar.gz**  will be downloaded to your **/home/username/Downloads** on your Ubuntu
6.	Abstract **system_studio_2018_version_ultimate_edition.tar.gz**
7.	Open a terminal, go to the abstracted installation directory and run **./install.sh**  
8.	Install as root user, type your password, enter the Serial Number Emailed to you, you can click **Customize** then **Next** to choose which components you’d like to install, here we only selected the **minimal requirements** for our workshop:
    1. Eclipse IDE
    2. Intel C++ Compiler 18.0
    3. Intel Threading Building Blocks 2018
    4. Intel VTune Amplifier 2018
 
<br>
  
![image of Intel_System_Studio_Components_List](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/Intel_System_Studio_Components_List.png "Figure 2")  
  
<br>  
<br>
  
![image of Intel_System_Studio_Customize_Components](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/Intel_System_Studio_Customize_Components.png "Figure 3")  
  
<br>  

9.	Click Next, **don’t** check **“Integrate to Wind River Linux and Wind River Workbench”** and **“Integrate into Android NDK”**, click Install
10.	Once installation complete, **uncheck** Launch Intel System Studio, Click Finish

# Prepare for running OpenVINO projects using Intel® System Studio
1.	Open a terminal, type **sudo gedit /opt/intel/system_studio_2018/iss_ide_eclipse-launcher.sh**
2.	Add **source /opt/intel/computer_vision_sdk/bin/setupvars.sh** after line 26, click save and close
3.	Go to desktop, double click Intel System Studio icon, go to **Window ->Preferences ->Intel(R) System Studio ->Hide unsupported wizards**, uncheck then hit Apply then OK
4.	Go to **Help -> Install new software… -> Add…**
Enter: **http://download.eclipse.org/releases/neon**, name it **“Neon”**
(Make sure you’re connected to the internet when you do this)
Once it loads, search for the **Marketplace Client** and install it.
(It’s going to ask you to restart ISS)
5.	Go to **Help -> Eclipse Marketplace -> cmake4eclipse**
(If you see cmake4eclipse listed, but cannot install it, close Intel System Studio, open a terminal, run sudo apt-get update && sudo apt-get upgrade, once done, come back and try again)
(It’s going to ask you to restart ISS again)
