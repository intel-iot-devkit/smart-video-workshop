
# Run Benchmark App with Multi-Device Execution 

Multi-Device plugin automatically assigns inference requests to available computational devices to execute the requests in parallel. 

In this lab, we are going to run the [Benchmark App](https://docs.openvinotoolkit.org/latest/openvino_docs_IE_DG_Samples_Overview.html) using the **MULTI** plugin to share the inference burden onto different hardware types.  

## Hello Query Device
First, let's run the Hello Query Device sample application, which queries available Inference Engine devices on your platform and prints out their metrics and default configuration values.

#### 1. Navigate to sample application directory
	cd $HOME/inference_engine_samples_build/intel64/Release
  
#### 2. Run the Hello Query Device application 
	./hello_query_device
    
With the NCS2 plugged on the development system used to create this tutorial, we see three different Inference Engine devices available: CPU, GPU, MYRIAD on the workshop laptop

	Available devices: 
	Device: CPU
	...

	Device: GPU
	...

	Device: MYRIAD
	...

## Benchmark C++ Tool     
Benchmark C++ Tool provides estimation of deep learning inference performance on the supported devices. Performance can be measured for two inference modes: synchronous (latency-oriented) and asynchronous (throughput-oriented).  
> **Note** The performance number mentioned below in this tutorial are obtained on a particular machine (Intel® Xeon® CPU E3-1268L v5 @ 2.4GHz x 8 + Intel® HD Graphics P530 (Skylake GT2) + 32 GB Memory).     

### First, let's take a look at the performance of each single Inference Engine device
#### 1. Navigate to sample application directory
	cd inference_engine_samples_build/intel64/Release/

#### 2. Run Benchmark tool application with CPU
> **Note**: Make sure you have gone through the [Run the Verification Scripts to Verify Installation](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_linux.html#run-the-demos) during your installation of OpenVINO Toolkit. 

	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d CPU \
	-niter 1000

Performance of CPU on the development system:

	Duration:   362.653 ms
	Latency:    1.43271 ms
	Throughput: 2757.46 FPS

#### 3. Run Benchmark tool application with GPU
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d GPU \
	-niter 1000

Performance of GPU on the development system:

	Duration:   666.11 ms
	Latency:    2.60 ms
	Throughput: 1501.24 FPS


#### 4. Run Benchmark tool application with MYRIAD
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MYRIAD.4.1-ma2480 \
	-niter 1000

Performance of single NCS2 on the development system:

	Duration:   1830.12 ms
	Latency:    7.23 ms
	Throughput: 546.41 FPS

### Now let's try MULTI plugin with different combination of available Inference Engine devices
#### 1. Run Benchmark tool application with MULTI:CPU,GPU
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:CPU,GPU \
	-niter 1000

Performance of using both CPU and GPU on the development system, and it is better than using signle CPU or GPU:

	Duration:   285.83 ms
	Throughput: 3498.62 FPS

#### 2. Run Benchmark tool application with MULTI:CPU,MYRIAD
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:CPU,MYRIAD \
	-niter 1000

Performance of using both CPU and VPU on the development system, and it is better than using signle CPU or VPU:

	Duration:   340.964 ms
	Throughput: 2932.86 FPS

	
#### 3. Run Benchmark tool application with MULTI:GPU,MYRIAD
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:GPU,MYRIAD \
	-niter 1000

Performance of using both GPU and VPU on the development system,, and it is better than using signle GPU or VPU:
	
	Duration:   377.77 ms
	Throughput: 2647.13 FPS
	
#### 4. Run Benchmark tool application with MULTI:CPU,GPU,MYRIAD
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:CPU,GPU,MYRIAD \
	-niter 1000

Performance of using CPU, GPU and VPU on the development system, and it is better than using signle CPU, GPU or VPU:

	Duration:   283.01 ms
	Throughput: 3561.71 FPS
	
### What if I have multiple NCS2?
In this example, we plugged three NCS2 to the laptop

#### 1. Run the Hello Query Device application 
	./hello_query_device

Then you will see multiple NCS2 from the prints:

	Available devices: 
	Device: CPU
	...
	
	Device: GPU
	...
		
	Device: MYRIAD.1.4.1-ma2480
	...
	
	Device: MYRIAD.1.4.2-ma2480
	...

	Device: MYRIAD.1.4.4-ma2480
	...
	
#### 2. Run Benchmark tool application with multiple NCS2s
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /home/intel/openvino_models/ir/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:MYRIAD.1.4.1-ma2480,MYRIAD.1.4.2-ma2480,MYRIAD.1.4.4-ma2480 \
	-niter 1000

Performance of using three NCS2 on the development system triples performance of using single NCS2:

	Duration:   605.12 ms
	Throughput: 1665.80 FPS

## Further Reading
To learn more about Multi plugin, plase refer to [Multi-Device Plugin](https://docs.openvinotoolkit.org/latest/openvino_docs_IE_DG_supported_plugins_MULTI.html) session on OpenVINO documentation.

