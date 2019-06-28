# Intel® VTune™ Amplifier Tutorial

## Introduction
Intel® VTune™ Amplifier is a powerful performance analyzer that can help developers to better understand the factors impacting application performance. Using the analysis data provided, developers can optimize the application.

This tutorial will show how to run Intel® VTune™ Amplifier on an Intel® Distribution of OpenVINO™ toolkit Inference Engine application.

## Build and Load Intel® VTune™ Amplifier Sampling Driver
The Intel® VTune™ Amplifier sampling driver provides access to Performance Monitoring Unit (PMU) in your Intel® processor. This allows running Advanced Hotspots and General Exploration analysis types.

Open a terminal and run the following commands to build and load the Intel® VTune™ Amplifier Sampling Driver, replace &lt;group&gt; with your user’s group name (e.g. intel):
              
      cd /opt/intel/system_studio_2019/vtune_amplifier_2019/sepdk/src
      sudo ./build-driver -ni
      sudo ./insmod-sep -r -g <group>
      ./insmod-sep -q

> **Note**: The Build and Load Intel® VTune™ Amplifier Sampling Driver might fail due to missing libraries libelf-dev, libelf-devel or elfutils-libelf-devel. You may need to install them on your system.

      sudo apt-get install <Name of the missing library>

## Setup Environment Variables for Intel® VTune™ Amplifier
In a terminal run source setupvars.sh and amplxe-vars.sh scripts, and run amplxe-gui:

      source /opt/intel/openvino/bin/setupvars.sh
      source /opt/intel/system_studio_2019/vtune_amplifier_2019/amplxe-vars.sh

## Build the sample application
In a terminal, type following commands:

      cd /opt/intel/openvino/deployment_tools/inference_engine/samples/object_detection_demo_ssd_async
      sudo gedit main.cpp

Then leave the Text Editor open, click this link: [[main.cpp](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/optimization-tools-and-techniques/main.cpp)], copy all the source code into your opened **main.cpp** file, click save and close the text editor.

Next, type this command:

      sudo gedit object_detection_demo_ssd_async.hpp

Keep the Text Editor open, click this link: [[object_detection_demo_ssd_async.hpp](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/optimization-tools-and-techniques/object_detection_demo_ssd_async.hpp)], copy all the source code into your opened **object_detection_demo_ssd_async.hpp** file, click save and close the text editor.

Now, in the same terminal:

      cd /opt/intel/openvino/deployment_tools/inference_engine/samples
      ./build_samples.sh

Wait until you see "**Build completed, you can find binaries for all samples in the /home/intel/inference_engine_samples_build/intel64/Release subfolder.**", then type below command to start Intel® VTune™ Amplifier

      amplxe-gui

The Intel® VTune™ Amplifier GUI will open.

## Create New Project, Configure and Run Analysis
In the Intel® VTune™ Amplifier GUI click **New Project** toolbar icon to create a new project.


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/01-VTune-NewProject-2019u3.png)


When prompted, enter a project name, e.g. **_openvino-lab_**


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/02-VTune-Create_Project-OpenVINO_2019u3.png)

Press **Create Project** button.

Intel® VTune™ Amplifier will show **Configure Analysis** tab. Configure the analysis target under **WHERE** tab. In this case we’ll be using the local host as the target system and we’ll launch an application to profile.

In the **Application** path field type:

**_/home/intel/inference_engine_samples_build/intel64/Release/object_detection_demo_ssd_async_**

And in the **Application parameters** field type:

**_-i /home/shane/Downloads/facedetection.mp4 -m /opt/intel/openvino_2019.1.094/deployment_tools/tools/model_downloader/Retail/object_detection/face/sqnet1.0modif-ssd/0004/dldt/face-detection-retail-0004.xml_**


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/VTune2019_Create_Project.png)


Right side of GUI will show the section with the **Analysis Type**. Select **Hotspots** analysis here, and in the Hotspots configuration , select **Hardware Event-Based Sampling with CPU sampling interval, ms set to 1**, and check the **Collect stacks** checkbox.

> **Note**: If you get an error message about kernel-mode monitoring, check that you’ve loaded the Sampling Driver with the right group (see Build and Load Intel® VTune™ Amplifier Sampling Driver above). If you get an error message about analysis type requires either an acess to kernel-mode monitoring in the Linux* perf subsystem. Please set the perf_event_paranoid value to 1 or set the ptrace_scope value to 0 depending on the error message.

      sudo sh -c 'echo 1 > /proc/sys/kernel/perf_event_paranoid'
      sudo sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'

![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/04-VTune-OpenVINO-Analysis_Type-Crop_2019u3.png)


Click on the **Start** button to run and analyze the application.

## Review Analysis Summary

Once the application terminates (or the **Stop** button is clicked) Intel® VTune™ Amplifier will collect and analyze the profiling data. The overview of the analysis will be shown in the **Summary** tab. This summary will help you to identify potential high level issues, and provide you with clues on further performance investigation.

In the beginning of the summary, you’ll see the time, CPI (cycles per instruction), CPU frequency, thread count, and some other statistics. Hover with the mouse pointer over (?) signs to see the detailed description of the counter. Some of the counters here might be marked by red flags. Hover over the red flag to see more information on the flagged issue, and in some cases, suggestions for potential performance improvements.


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/VTune2019_Summary.png)


Next, there is the list of Top Hotspots and the list of Top Tasks. The Top Hotspots list shows 5 functions that took the most CPU time, and the Top Tasks, shows 5 tasks that took the most CPU time. Intel® Distribution of OpenVINO™ toolkit uses Intel® VTune™ Amplifier Instrumentation and Tracing Technology (ITT) to define these tasks.


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/VTune2019_Summary2.png)


The Effective CPU Utilization Histogram shows the percentage of the time the specific number of logical CPUs (cores or threads) were running simultaneously. If your application does not utilize all the available cores, it might be possible to improve the performance by parallelizing it.

Information about the platform, the application, and the profiling data collection are presented at the bottom on the **Summary** tab.

## Check Bottom-up and Platform Tabs for Detailed Information
Click on the **Bottom-up** tab. It will show the list of functions, by default sorted by execution time. In case of the Intel® Distribution of OpenVINO™ toolkit profiling it is useful to change the **Grouping** to **Task Domain / Task Type Function / Call Stack**. Click on a domain name to expand the tasks list in that domain. Note that the tasks correspond to the Inference Engine layers.

The execution timeline is displayed on the bottom part of the window. Note the threads of the application, and their behavior. This raises questions such as "Why does each thread have multiple (about 100) peaks?" and "Could this indicate excessive task switching?"


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/VTune2019_Bottom-up.png)


Try to zoom in on the timeline by clicking the mouse, dragging the mouse pointer over it, and then selecting **Zoom In on Selection** pop-up menu entry. In zoomed in view, the bottom-up view only shows hotspots (functions or tasks) observed during the selected time period. Also, note the task names on the OMP Master Thread and OpenCV thread. Use right click and Reset Zoom or Undo Previous Zoom pop-up menu entries to zoom out. 

The Platform tab shows both the application threads timeline, and the CPU metrics, such as CPU utilization and CPU Frequency. Just as in the Bottom-up tab, it is possible to zoom in to see more details for a given time period.

## Tune Intel® Distribution of OpenVINO™ Toolkit Parameters and Rerun Analysis
In the Intel® VTune™ Amplifier GUI click **Configure Analysis** toolbar icon to start a new analysis.


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/08-VTune-OpenVINO-New_Analysis-Icon_Crop_2019u3.png)


The previously configured **Analysis Type** settings will be shown. Click on the **WHAT** tab to change the application parameters. Add "-async" option to the **Application parameters**:

**_-i /home/shane/Downloads/facedetection.mp4 -m /opt/intel/openvino_2019.1.094/deployment_tools/tools/model_downloader/Retail/object_detection/face/sqnet1.0modif-ssd/0004/dldt/face-detection-retail-0004.xml -async_**

Keep the previously configured settings. Click on the **Start** button to run and analyze the application.

Once the application profiling is done, review the **Summary** tab. Note the changes from the previous analysis.

Switch to the **Bottom-up** tab and then to the **Platform** tab. Note how the thread behavior had changed. What in Intel® Distribution of OpenVINO™ toolkit caused this change in the behavior?


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/VTune2019_Platform.png)


## Compare Two Profiling Results
While developing and optimizing an application, it is useful to compare the profiling results of several runs. For example, this can be used to quantify the performance improvements due to an optimization, or to validate that the application performance has not been impacted by an application change (e.g. a bug fix).

> **Note**: Prior to running the comparison, make sure to close the analysis tabs for the profiling results that will be used in the comparison. Otherwise Intel® VTune™ Amplifier will produce database locked errors.

In the Intel® VTune™ Amplifier GUI click **Compare Results…** toolbar icon.


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/10-VTune-OpenVINO-Compare_Results-Icon-Crop_2019u3.png)


Select the two results you would like to compare, and click on the **Compare** button.

Intel® VTune™ Amplifier will compare the profiling data for two runs. In the displayed results, note that now the difference between two runs is shown. Particularly in this case we can see improvement in CPU time.


![image of the output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/VTune2019_Comparison.png)


Switch to the **Bottom-up** tab, make sure that the **Grouping** is set to **Task Domain / Task Type Function / Call Stack**, and click on the **InferenceEngine** domain to see the tasks in that domain.

Note that Intel® VTune™ Amplifier now also shows the difference in the metrics: instructions retired, CPI rate, time, and so on. This can be used to understand the impact on an optimization or an application change on the particular tasks or functions the application runs. Note how both "Wait Rate" and "Context Switch Time" improved in the second configuration.

## Disclaimer

Intel and the Intel logo are trademarks of Intel Corporation or its subsidiaries in the U.S. and/or other countries. 

*Other names and brands may be claimed as the property of others
