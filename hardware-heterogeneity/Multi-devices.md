
# Introducing Multi-Device Execution 

Multi-Device plugin automatically assigns inference requests to available computational devices to execute the requests in parallel. 

This example shows how to use **MULTI** plugin to share the inference burden onto different hardware types. Here, we will use the command line option to demonstrate MULTI plugin usage.  

## Hello Query Device
First, let's run the Hello Query Device sample application, which queries available Inference Engine devices on your platform and prints out their metrics and default configuration values.

#### 1. Navigate to sample application directory
	cd inference_engine_samples_build/intel64/Release/
  
#### 2. Run the Hello Query Device application 
	./hello_query_device
    
With the NCS2 plugged in, you will see three different Inference Engine devices available: CPU, GPU, MYRIAD on the workshop laptop

	Available devices: 
	Device: CPU
	Metrics: 
		AVAILABLE_DEVICES : [  ]
		SUPPORTED_METRICS : [ AVAILABLE_DEVICES SUPPORTED_METRICS FULL_DEVICE_NAME OPTIMIZATION_CAPABILITIES SUPPORTED_CONFIG_KEYS RANGE_FOR_ASYNC_INFER_REQUESTS RANGE_FOR_STREAMS ]
		FULL_DEVICE_NAME : Intel(R) Xeon(R) CPU E3-1268L v5 @ 2.40GHz
		OPTIMIZATION_CAPABILITIES : [ FP32 INT8 BIN ]
		SUPPORTED_CONFIG_KEYS : [ CPU_BIND_THREAD CPU_THREADS_NUM CPU_THROUGHPUT_STREAMS DUMP_EXEC_GRAPH_AS_DOT DYN_BATCH_ENABLED DYN_BATCH_LIMIT EXCLUSIVE_ASYNC_REQUESTS PERF_COUNT ]
		RANGE_FOR_ASYNC_INFER_REQUESTS : { 1, 1, 1 }
		RANGE_FOR_STREAMS : { 1, 8 }
	Default values for device configuration keys: 
		CPU_BIND_THREAD : YES
		CPU_THREADS_NUM : 0
		CPU_THROUGHPUT_STREAMS : 1
		DUMP_EXEC_GRAPH_AS_DOT : ""
		DYN_BATCH_ENABLED : NO
		DYN_BATCH_LIMIT : 0
		EXCLUSIVE_ASYNC_REQUESTS : NO
		PERF_COUNT : NO

	Device: GPU
	Metrics: 
		AVAILABLE_DEVICES : [  ]
		SUPPORTED_METRICS : [ AVAILABLE_DEVICES SUPPORTED_METRICS FULL_DEVICE_NAME OPTIMIZATION_CAPABILITIES SUPPORTED_CONFIG_KEYS NUMBER_OF_WAITING_INFER_REQUESTS NUMBER_OF_EXEC_INFER_REQUESTS RANGE_FOR_ASYNC_INFER_REQUESTS RANGE_FOR_STREAMS ]
		FULL_DEVICE_NAME : Intel(R) Gen9 HD Graphics
		OPTIMIZATION_CAPABILITIES : [ FP32 BIN FP16 ]
		SUPPORTED_CONFIG_KEYS : [ CLDNN_INT8_ENABLED CLDNN_MEM_POOL CLDNN_PLUGIN_PRIORITY CLDNN_PLUGIN_THROTTLE DUMP_KERNELS DYN_BATCH_ENABLED EXCLUSIVE_ASYNC_REQUESTS GPU_THROUGHPUT_STREAMS PERF_COUNT TUNING_MODE ]
		NUMBER_OF_WAITING_INFER_REQUESTS : 0
		NUMBER_OF_EXEC_INFER_REQUESTS : 0
		RANGE_FOR_ASYNC_INFER_REQUESTS : { 1, 2, 1 }
		RANGE_FOR_STREAMS : { 1, 2 }
	Default values for device configuration keys: 
		CLDNN_INT8_ENABLED : NO
		CLDNN_MEM_POOL : YES
		CLDNN_PLUGIN_PRIORITY : 0
		CLDNN_PLUGIN_THROTTLE : 0
		DUMP_KERNELS : NO
		DYN_BATCH_ENABLED : NO
		EXCLUSIVE_ASYNC_REQUESTS : NO
		GPU_THROUGHPUT_STREAMS : 1
		PERF_COUNT : NO
		TUNING_MODE : TUNING_DISABLED

	Device: MYRIAD.4.1-ma2480
	Metrics: 
		AVAILABLE_DEVICES : [ 4.1-ma2480 4.2-ma2480 4.4-ma2480 ]
		FULL_DEVICE_NAME : Intel Movidius Myriad X VPU
		SUPPORTED_METRICS : [ AVAILABLE_DEVICES FULL_DEVICE_NAME SUPPORTED_METRICS SUPPORTED_CONFIG_KEYS OPTIMIZATION_CAPABILITIES RANGE_FOR_ASYNC_INFER_REQUESTS ]
		SUPPORTED_CONFIG_KEYS : [ VPU_HW_STAGES_OPTIMIZATION VPU_LOG_LEVEL VPU_PRINT_RECEIVE_TENSOR_TIME VPU_NETWORK_CONFIG VPU_COMPUTE_LAYOUT VPU_CUSTOM_LAYERS VPU_IGNORE_IR_STATISTIC VPU_MYRIAD_FORCE_RESET VPU_MYRIAD_PLATFORM EXCLUSIVE_ASYNC_REQUESTS LOG_LEVEL PERF_COUNT CONFIG_FILE DEVICE_ID ]
		OPTIMIZATION_CAPABILITIES : [ FP16 ]
		RANGE_FOR_ASYNC_INFER_REQUESTS : { 3, 6, 1 }
	Default values for device configuration keys: 
		VPU_HW_STAGES_OPTIMIZATION : UNSUPPORTED TYPE
		VPU_LOG_LEVEL : UNSUPPORTED TYPE
		VPU_PRINT_RECEIVE_TENSOR_TIME : UNSUPPORTED TYPE
		VPU_NETWORK_CONFIG : UNSUPPORTED TYPE
		VPU_COMPUTE_LAYOUT : UNSUPPORTED TYPE
		VPU_CUSTOM_LAYERS : UNSUPPORTED TYPE
		VPU_IGNORE_IR_STATISTIC : UNSUPPORTED TYPE
		VPU_MYRIAD_FORCE_RESET : UNSUPPORTED TYPE
		VPU_MYRIAD_PLATFORM : UNSUPPORTED TYPE
		EXCLUSIVE_ASYNC_REQUESTS : UNSUPPORTED TYPE
		LOG_LEVEL : UNSUPPORTED TYPE
		PERF_COUNT : UNSUPPORTED TYPE
		CONFIG_FILE : UNSUPPORTED TYPE
		DEVICE_ID : UNSUPPORTED TYPE  

## Benchmark C++ Tool     
Benchmark C++ Tool provide estimation of deep learning inference performance on supported devices. Performance can be measured for two inference modes: synchronous (latency-oriented) and asynchronous (throughput-oriented).  
> **Note** The performance number mentioned below in this tutorial are obtained on a particular machine (Intel® Xeon® CPU E3-1268L v5 @ 2.4GHz x 8 + Intel® HD Graphics P530 (Skylake GT2) + 32 GB Memory).     

### First, let's take a look at the performance of each single Inference Engine device
#### 1. Navigate to sample application directory
	cd inference_engine_samples_build/intel64/Release/

#### 2. Run Benchmark tool application with CPU
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /opt/intel/openvino/deployment_tools/tools/model_downloader/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d CPU \
	-niter 1000

At the end of the output you will see the performance of CPU:

	Duration:   362.653 ms
	Latency:    1.43271 ms
	Throughput: 2757.46 FPS

#### 3. Run Benchmark tool application with GPU
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /opt/intel/openvino/deployment_tools/tools/model_downloader/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d GPU \
	-niter 1000

At the end of the output you will see the performance of GPU:

	Duration:   929.449 ms
	Latency:    3.69362 ms
	Throughput: 1075.91 FPS

#### 4. Run Benchmark tool application with MYRIAD
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /opt/intel/openvino/deployment_tools/tools/model_downloader/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MYRIAD.4.1-ma2480 \
	-niter 1000

At the end of the output you will see the performance of VPU:

	Duration:   2358.81 ms
	Latency:    9.31586 ms
	Throughput: 423.943 FPS

### Now let's try MULTI plugin with different combination of available Inference Engine devices
#### 1. Run Benchmark tool application with MULTI:CPU,GPU
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /opt/intel/openvino/deployment_tools/tools/model_downloader/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:CPU,GPU \
	-niter 1000

At the end of the output you will see the performance using both CPU and GPU, and it is better than using signle CPU or GPU:

	Duration:   323.819 ms
	Throughput: 3088.14 FPS
	
#### 2. Run Benchmark tool application with MULTI:CPU,MYRIAD
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /opt/intel/openvino/deployment_tools/tools/model_downloader/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:CPU,MYRIAD.4.1-ma2480 \
	-niter 1000

At the end of the output you will see the performance using both CPU and VPU, and it is better than using signle CPU or VPU:

	Duration:   340.964 ms
	Throughput: 2932.86 FPS

	
#### 3. Run Benchmark tool application with MULTI:GPU,MYRIAD
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /opt/intel/openvino/deployment_tools/tools/model_downloader/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:GPU,MYRIAD.4.1-ma2480 \
	-niter 1000

At the end of the output you will see the performance using both GPU and VPU, and it is better than using signle GPU or VPU:

	Duration:   695.06 ms
	Throughput: 1438.72 FPS

	
#### 4. Run Benchmark tool application with MULTI:CPU,GPU,MYRIAD
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /opt/intel/openvino/deployment_tools/tools/model_downloader/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:CPU,GPU,MYRIAD.4.1-ma2480 \
	-niter 1000

At the end of the output you will see the performance using CPU, GPU and VPU, and it is better than using signle CPU, GPU or VPU:

	Duration:   300.508 ms
	Throughput: 3354.32 FPS
	
### What if I have multiple NCS2?
In this example, we plugged three NCS2 to the laptop

#### 1. Run the Hello Query Device application 
	./hello_query_device

Then you will see multiple NCS2 from the prints:

	Available devices: 
	Device: CPU
	.
	.
	
	Device: GPU
	.
	.
	
	Device: MYRIAD.4.1-ma2480
	.
	.
	
	Device: MYRIAD.4.2-ma2480
	.
	.
		
	Device: MYRIAD.4.4-ma2480
	.
	.
		
		
#### 2. Run Benchmark tool application with multiple NCS2s
	./benchmark_app \
	-i /opt/intel/openvino/deployment_tools/demo/car.png \
	-m /opt/intel/openvino/deployment_tools/tools/model_downloader/intel/vehicle-attributes-recognition-barrier-0039/FP16/vehicle-attributes-recognition-barrier-0039.xml \
	-d MULTI:MYRIAD.4.1-ma2480,MYRIAD.4.2-ma2480,MYRIAD.4.4-ma2480 \
	-niter 1000

At the end of the output you will see the performance triples compare to single NCS2:

	Duration:   705.39 ms
	Throughput: 1429.00 FPS

