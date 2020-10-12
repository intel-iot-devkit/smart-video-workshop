# Optimized Inference at the Edge with Intel® Tools and Technologies 
This workshop will walk you through a computer vision workflow using the latest Intel® technologies and comprehensive toolkits including support for deep learning algorithms that help accelerate smart video applications. You will learn how to optimize and improve performance with and without external accelerators and utilize tools to help you identify the best hardware configuration for your needs. This workshop will also outline the various frameworks and topologies supported by Intel® accelerator tools. 

> :warning: Labs of this workshop have been validated with **Intel® Distribution of OpenVINO™ toolkit 2021.1 (openvino_toolkit_2021.1.110)**. Videos shown below is based on OpenVINO 2020R2, might be slightly different from the slides, but the content is largely the same. **FPGA plugin will no longer be supported by the OpenVINO stardard release, you can find the FPGA content from ealier branches.**
	
## Workshop Agenda
* **Intel® Distribution of OpenVINO™ toolkit Overview** - [[Slides]](./presentations/01.%20Intel%20Distribution%20of%20OpenVINO%20Toolkit%20Overview.pdf) [[Video]](https://software.intel.com/content/www/us/en/develop/videos/part-1-intel-distribution-of-openvino-toolkit-overview.html)
  - Lab Setup - [Lab Setup Instructions](./Lab_setup.md)
  > :warning: Please make sure you have gone through all the steps in the **Lab Setup**, all the Labs below are based on the assumption that user has correctly installed OpenVINO toolkit on the local development system.
  
* **Model Optimizer** - [[Slides]](./presentations/02.%20Model%20Optimizer.pdf) [[Video]](https://software.intel.com/content/www/us/en/develop/videos/part-2-model-optimizer.html)
  - Lab1 - [Optimize a Caffe* Classification Model - SqueezeNet v1.1](./Labs/Optimize_Caffe_squeezeNet.md)
  - Lab2 - [Optimize a Tensorflow* Object Detection Model - SSD with MobileNet](./Labs/Optimize_Tensorflow_Mobilenet-SSD.md)

* **Inference Engine** - [[Slides]](./presentations/03.%20Inference%20Engine.pdf) [[Video]](https://software.intel.com/content/www/us/en/develop/videos/part-4-inference-engine.html)
  - Lab3 - [Run Classfication Sample application with the optimized SqueezeNet v1.1](./Labs/Run_Classification_Sample.md)
  - Lab4 - [Run Object Detection Sample application with the optimized SSD with MobileNet](./Labs/Run_Object_Detection_Sample.md)
  - Lab5 - [Run Benchmark App with Hetero plugin](./Labs/Run_Benchmark_Hetero.md)

* **Accelerators based on Intel® Movidius™ Vision Processing Unit** - [[Slides]](./presentations/04.%20Accelerators%20based%20on%20Intel®%20Movidius™%20Vision%20Processing%20Unit.pdf) [[Video]](https://software.intel.com/content/www/us/en/develop/videos/part-8-accelerators-based-on-intel-movidius-vision-processing-unit.html)
  - Lab6 - [HW Acceleration with Intel® Movidius™ Neural Compute Stick2](./Labs/Run_Samples_with_NCS2.md)
  - Lab7 - [Run Benchmark App with Multi plugin](./Labs/Run_Benchmark_Multi.md)
  
* **Multiple Models in One Application**  - [[Slides]](./presentations/08.%20Multiple%20Models%20in%20One%20Application.pdf) [[Video]](https://software.intel.com/content/www/us/en/develop/videos/part-6-multiple-models-in-one-application.html)
  - Lab8 - [Run Security Barrier Demo Application](./Labs/Run_Security_Barrier_Demo.md) 
  
* **Deep Learning Workbench** - [[Slides]](./presentations/06.%20Deep%20Learning%20Workbench.pdf) [[Video]](https://software.intel.com/content/www/us/en/develop/videos/part-11-deep-learning-workbench.html)
  - Demo - [DL Workbench Walkthrough](https://software.intel.com/content/www/us/en/develop/videos/part-12-demonstration-of-deep-learning-workbench.html)
  
* **Deep Learning Streamer** - [[Slides]](./presentations/07.%20Deep%20Learning%20streamer.pdf) [[Video]](https://software.intel.com/content/www/us/en/develop/videos/part-13-deep-learning-streamer.html)
  - Lab9 - [Build a Media Analytic Pipeline with DL Streamer](./Labs/Build_DL_Streamer_Pipeline.md)
  - Demo - [DL Streamer Pipeline](https://software.intel.com/content/www/us/en/develop/videos/part-14-demonstration-of-deep-learning-streamer.html)

* **Intel® DevCloud for the Edge** - [[Slides]](./presentations/09.%20Intel%20DevCloud%20for%20the%20Edge.pdf) [[Video]](https://software.intel.com/content/www/us/en/develop/videos/part-15-introduction-to-intel-devcloud-for-the-edge.html)
  - Demo - [Intel® DevCloud for the Edge Walkthrough](https://software.intel.com/content/www/us/en/develop/videos/part-16-demonstration-of-intel-devcloud-for-the-edge.html)


## Further Reading Materials
* **Support for Microsoft ONNX runtime in OpenVINO**
  - Slides - [ONNX runtime and OpenVINO](./presentations/ONNX_runtime_and_OpenVINO.pdf)
  
* **Healthcare applications and Required Features**
  - Slides - [Healthcare Applications](./presentations/Healthcare_presentation.pdf)
  
* [**Install Intel® Distribution of OpenVINO™ toolkit for** **Linux*** **from a Docker*** **Image**](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_docker_linux.html)


> #### Disclaimer

> Intel and the Intel logo are trademarks of Intel Corporation or its subsidiaries in the U.S. and/or other countries. 
 
> *Other names and brands may be claimed as the property of others
