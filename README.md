# Optimized Inference at the Edge with Intel® Tools and Technologies 
This workshop will walk you through the workflow using Intel® Distribution of OpenVINO™ toolkit for inferencing deep learning algorithms that help accelerate vision, automatic speech recognition, natural language processing, recommendation systems and many other applications. You will learn how to optimize and improve performance with or without external accelerators and utilize tools to help you identify the best hardware configuration for your needs. This workshop will also outline the various frameworks and topologies supported by Intel® Distribution of OpenVINO™ toolkit. 


> :warning: Labs of this workshop have been validated with **Intel® Distribution of OpenVINO™ toolkit 2021.3 (openvino_toolkit_2021.3.394)**. Some of the videos shown below is based on OpenVINO 2021.2, might be slightly different from the slides, but the content is largely the same. **FPGA plugin will no longer be supported by the OpenVINO stardard release, you can find the FPGA content from earlier branches.**
	
## Workshop Agenda

* **Intel® Distribution of OpenVINO™ toolkit Overview** 
  - Training Slides - [Part1](./presentations/OpenVINO_Training_Part1_2021.3.pdf), [Part2](./presentations/OpenVINO_Training_Part2_2021.3.pdf)
  - Training Video Series - [Intel® Distribution of OpenVINO™ Toolkit Training](https://software.intel.com/content/www/us/en/develop/video-series/openvino-toolkit-on-demand-workshop.html)
  - Lab Setup - [Lab Setup Instructions](./Lab_setup.md)
  > :warning: Please make sure you have gone through all the steps in the **Lab Setup**, all the Labs below are based on the assumption that user has correctly installed OpenVINO toolkit on the local development system.
  
* **Model Optimizer** 
  - Lab1 - [Optimize a Caffe* Classification Model - SqueezeNet v1.1](./Labs/Optimize_Caffe_squeezeNet.md)
  - Lab2 - [Optimize a Tensorflow* Object Detection Model - SSD with MobileNet](./Labs/Optimize_Tensorflow_Mobilenet-SSD.md)

* **Inference Engine** 
  - Lab3 - [Run Classfication Sample application with the optimized SqueezeNet v1.1](./Labs/Run_Classification_Sample.md)
  - Lab4 - [Run Object Detection Sample application with the optimized SSD with MobileNet](./Labs/Run_Object_Detection_Sample.md)
  - Lab5 - [Run Benchmark App with Hetero plugin](./Labs/Run_Benchmark_Hetero.md)

* **Accelerators based on Intel® Movidius™ Vision Processing Unit** 
  - Lab6 - [HW Acceleration with Intel® Movidius™ Neural Compute Stick2](./Labs/Run_Samples_with_NCS2.md)
  - Lab7 - [Run Benchmark App with Multi plugin](./Labs/Run_Benchmark_Multi.md)
  
* **Multiple Models in One Application**  
  - Lab8 - [Run Security Barrier Demo Application](./Labs/Run_Security_Barrier_Demo.md) 
  
* **Deep Learning Workbench** 
  - [Short Video Tutorials on YouTube](https://www.youtube.com/playlist?list=PLTseHiQLIfGM6ltiaeh9fL8qfxiE-u4fw)
  
* **Deep Learning Streamer** 
  - Lab9 - [Build a Media Analytic Pipeline with DL Streamer](./Labs/Build_DL_Streamer_Pipeline.md)
  - Demo - [DL Streamer Pipeline](https://software.intel.com/content/www/us/en/develop/videos/part-14-demonstration-of-deep-learning-streamer.html)

* **Intel® DevCloud for the Edge** 
  - Demo - [Intel® DevCloud for the Edge Walkthrough](https://software.intel.com/content/www/us/en/develop/videos/part-16-demonstration-of-intel-devcloud-for-the-edge.html)


## Further Reading Materials
* **Support for Microsoft ONNX runtime in OpenVINO**
  - Slides - [ONNX runtime and OpenVINO](./presentations/ONNX_runtime_and_OpenVINO.pdf)


> #### Disclaimer

> Intel and the Intel logo are trademarks of Intel Corporation or its subsidiaries in the U.S. and/or other countries. 
 
> *Other names and brands may be claimed as the property of others
