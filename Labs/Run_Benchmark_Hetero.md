
# Run Benchmark App with Hetero plugin

In this lab, we are going to run the [Benchmark App](https://docs.openvinotoolkit.org/latest/openvino_docs_IE_DG_Samples_Overview.html) using Hetero plugin with CPU and GPU. We will switch the sequence of the devices put after HETERO, and show the performance counters, which will help us to understand Hetero plugin better. 

#### 1. Navigate to the directory of samples build directory
Make sure you have build the samples as per the instructions given in the [How to Get Started](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/README.md#how-to-get-started) section. 

	 cd $HOME/inference_engine_samples_build/intel64/Release

We can check the usage of Benchmark App:

	./benchmark_app -h

#### 2. Run Benchmark App sample with hetero plugin, prioritizing running on CPU first.
We will the converted SqueezeNet v1.1 and run the inference 500 times.

	./benchmark_app \
	-i /opt/intel/workshop/smart-video-workshop/Labs/daisy.jpg \
	-m /opt/intel/workshop/Squeezenet/FP32/squeezenet1.1_fp32.xml \
	-d HETERO:CPU,GPU \
	-niter 500 \
	-pc
	
From the performance counts, we can see all the layers were executed by CPU, the inference realTime equeals to the CPU time, and the execType jit means it is CPU instruction set.

	subgraph0: data_U8_FP32_Add_  EXECUTED       layerType: Reorder            realTime: 21        cpu: 21              execType: jit_uni_I8
	subgraph0: Add_               EXECUTED       layerType: ScaleShift         realTime: 12        cpu: 12              execType: jit_avx2_FP32
	subgraph0: conv1              EXECUTED       layerType: Convolution        realTime: 134       cpu: 134             execType: jit_avx2_FP32
	subgraph0: relu_conv1         NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: pool1              EXECUTED       layerType: Pooling            realTime: 53        cpu: 53              execType: jit_avx_FP32
	subgraph0: fire2/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 23        cpu: 23              execType: jit_avx2_1x1_FP32
	subgraph0: fire2/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire2/expand1x1    EXECUTED       layerType: Convolution        realTime: 24        cpu: 24              execType: jit_avx2_1x1_FP32
	subgraph0: fire2/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire2/expand3x3    EXECUTED       layerType: Convolution        realTime: 158       cpu: 158             execType: jit_avx2_FP32
	subgraph0: fire2/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire2/concat       EXECUTED       layerType: Concat             realTime: 1         cpu: 1               execType: unknown_FP32
	subgraph0: fire3/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 40        cpu: 40              execType: jit_avx2_1x1_FP32
	subgraph0: fire3/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire3/expand1x1    EXECUTED       layerType: Convolution        realTime: 25        cpu: 25              execType: jit_avx2_1x1_FP32
	subgraph0: fire3/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire3/expand3x3    EXECUTED       layerType: Convolution        realTime: 159       cpu: 159             execType: jit_avx2_FP32
	subgraph0: fire3/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire3/concat       EXECUTED       layerType: Concat             realTime: 1         cpu: 1               execType: unknown_FP32
	subgraph0: pool3              EXECUTED       layerType: Pooling            realTime: 22        cpu: 22              execType: jit_avx_FP32
	subgraph0: fire4/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 21        cpu: 21              execType: jit_avx2_1x1_FP32
	subgraph0: fire4/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire4/expand1x1    EXECUTED       layerType: Convolution        realTime: 21        cpu: 21              execType: jit_avx2_1x1_FP32
	subgraph0: fire4/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire4/expand3x3    EXECUTED       layerType: Convolution        realTime: 160       cpu: 160             execType: jit_avx2_FP32
	subgraph0: fire4/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire4/concat       EXECUTED       layerType: Concat             realTime: 1         cpu: 1               execType: unknown_FP32
	subgraph0: fire5/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 39        cpu: 39              execType: jit_avx2_1x1_FP32
	subgraph0: fire5/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire5/expand1x1    EXECUTED       layerType: Convolution        realTime: 21        cpu: 21              execType: jit_avx2_1x1_FP32
	subgraph0: fire5/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire5/expand3x3    EXECUTED       layerType: Convolution        realTime: 161       cpu: 161             execType: jit_avx2_FP32
	subgraph0: fire5/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire5/concat       EXECUTED       layerType: Concat             realTime: 1         cpu: 1               execType: unknown_FP32
	subgraph0: pool5              EXECUTED       layerType: Pooling            realTime: 14        cpu: 14              execType: jit_avx_FP32
	subgraph0: fire6/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 18        cpu: 18              execType: jit_avx2_1x1_FP32
	subgraph0: fire6/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire6/expand1x1    EXECUTED       layerType: Convolution        realTime: 13        cpu: 13              execType: jit_avx2_1x1_FP32
	subgraph0: fire6/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire6/expand3x3    EXECUTED       layerType: Convolution        realTime: 97        cpu: 97              execType: jit_avx2_FP32
	subgraph0: fire6/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire6/concat       EXECUTED       layerType: Concat             realTime: 1         cpu: 1               execType: unknown_FP32
	subgraph0: fire7/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 25        cpu: 25              execType: jit_avx2_1x1_FP32
	subgraph0: fire7/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire7/expand1x1    EXECUTED       layerType: Convolution        realTime: 13        cpu: 13              execType: jit_avx2_1x1_FP32
	subgraph0: fire7/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire7/expand3x3    EXECUTED       layerType: Convolution        realTime: 99        cpu: 99              execType: jit_avx2_FP32
	subgraph0: fire7/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire7/concat       EXECUTED       layerType: Concat             realTime: 1         cpu: 1               execType: unknown_FP32
	subgraph0: fire8/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 31        cpu: 31              execType: jit_avx2_1x1_FP32
	subgraph0: fire8/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire8/expand1x1    EXECUTED       layerType: Convolution        realTime: 21        cpu: 21              execType: jit_avx2_1x1_FP32
	subgraph0: fire8/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire8/expand3x3    EXECUTED       layerType: Convolution        realTime: 170       cpu: 170             execType: jit_avx2_FP32
	subgraph0: fire8/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire8/concat       EXECUTED       layerType: Concat             realTime: 1         cpu: 1               execType: unknown_FP32
	subgraph0: fire9/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 42        cpu: 42              execType: jit_avx2_1x1_FP32
	subgraph0: fire9/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire9/expand1x1    EXECUTED       layerType: Convolution        realTime: 21        cpu: 21              execType: jit_avx2_1x1_FP32
	subgraph0: fire9/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire9/expand3x3    EXECUTED       layerType: Convolution        realTime: 170       cpu: 170             execType: jit_avx2_FP32
	subgraph0: fire9/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire9/concat       EXECUTED       layerType: Concat             realTime: 1         cpu: 1               execType: unknown_FP32
	subgraph0: conv10             EXECUTED       layerType: Convolution        realTime: 601       cpu: 601             execType: jit_avx2_1x1_FP32
	subgraph0: relu_conv10        NOT_RUN        layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: pool10/reduce      EXECUTED       layerType: Pooling            realTime: 11        cpu: 11              execType: jit_avx_FP32
	subgraph0: prob               EXECUTED       layerType: SoftMax            realTime: 2         cpu: 2               execType: jit_avx2_FP32
	subgraph0: prob_nChw8c_nch... EXECUTED       layerType: Reorder            realTime: 2         cpu: 2               execType: jit_uni_FP32
	subgraph0: out_prob           NOT_RUN        layerType: Output             realTime: 0         cpu: 0               execType: unknown_FP32
	
#### 3. Now, run with GPU first

	./benchmark_app \
	-i /opt/intel/workshop/smart-video-workshop/Labs/daisy.jpg \
	-m /opt/intel/workshop/Squeezenet/FP32/squeezenet1.1_fp32.xml \
	-d HETERO:GPU,CPU \
	-niter 500 \
	-pc

From the performance counts, we can see CPU time only a small portion of the total inference realTime, the execType indicates layers are executed on GPU.

	subgraph0: input:data_cldn... EXECUTED       layerType: Reorder            realTime: 73        cpu: 17              execType: reorder_data
	subgraph0: Add_               EXECUTED       layerType: ScaleShift         realTime: 62        cpu: 6               execType: generic_eltwise_ref
	subgraph0: conv1              EXECUTED       layerType: Convolution        realTime: 269       cpu: 6               execType: convolution_gpu_bfyx_to_bfyx_f16
	subgraph0: pool1              EXECUTED       layerType: Pooling            realTime: 105       cpu: 5               execType: pooling_gpu_blocked
	subgraph0: fire2/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 44        cpu: 5               execType: convolution_gpu_bfyx_f16_1x1
	subgraph0: fire2/expand1x1    EXECUTED       layerType: Convolution        realTime: 35        cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire2/expand3x3    EXECUTED       layerType: Convolution        realTime: 194       cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire2/concat       OPTIMIZED_OUT  layerType: Concat             realTime: 0         cpu: 0               execType: undef
	subgraph0: fire3/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 74        cpu: 5               execType: convolution_gpu_bfyx_f16_1x1
	subgraph0: fire3/expand1x1    EXECUTED       layerType: Convolution        realTime: 35        cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire3/expand3x3    EXECUTED       layerType: Convolution        realTime: 194       cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire3/concat       OPTIMIZED_OUT  layerType: Concat             realTime: 0         cpu: 0               execType: undef
	subgraph0: pool3              EXECUTED       layerType: Pooling            realTime: 51        cpu: 6               execType: pooling_gpu_blocked
	subgraph0: fire4/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 42        cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire4/expand1x1    EXECUTED       layerType: Convolution        realTime: 35        cpu: 6               execType: convolution_gpu_bfyx_f16
	subgraph0: fire4/expand3x3    EXECUTED       layerType: Convolution        realTime: 233       cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire4/concat       OPTIMIZED_OUT  layerType: Concat             realTime: 0         cpu: 0               execType: undef
	subgraph0: fire5/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 74        cpu: 5               execType: convolution_gpu_bfyx_f16_1x1
	subgraph0: fire5/expand1x1    EXECUTED       layerType: Convolution        realTime: 36        cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire5/expand3x3    EXECUTED       layerType: Convolution        realTime: 221       cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire5/concat       OPTIMIZED_OUT  layerType: Concat             realTime: 0         cpu: 0               execType: undef
	subgraph0: pool5              EXECUTED       layerType: Pooling            realTime: 37        cpu: 5               execType: pooling_gpu_blocked
	subgraph0: fire6/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 33        cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire6/expand1x1    EXECUTED       layerType: Convolution        realTime: 22        cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire6/expand3x3    EXECUTED       layerType: Convolution        realTime: 130       cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire6/concat       OPTIMIZED_OUT  layerType: Concat             realTime: 0         cpu: 0               execType: undef
	subgraph0: fire7/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 44        cpu: 5               execType: convolution_gpu_bfyx_f16_1x1
	subgraph0: fire7/expand1x1    EXECUTED       layerType: Convolution        realTime: 22        cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire7/expand3x3    EXECUTED       layerType: Convolution        realTime: 130       cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire7/concat       OPTIMIZED_OUT  layerType: Concat             realTime: 0         cpu: 0               execType: undef
	subgraph0: fire8/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 64        cpu: 5               execType: convolution_gpu_bfyx_f16_1x1
	subgraph0: fire8/expand1x1    EXECUTED       layerType: Convolution        realTime: 36        cpu: 6               execType: convolution_gpu_bfyx_f16
	subgraph0: fire8/expand3x3    EXECUTED       layerType: Convolution        realTime: 223       cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire8/concat       OPTIMIZED_OUT  layerType: Concat             realTime: 0         cpu: 0               execType: undef
	subgraph0: fire9/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 79        cpu: 5               execType: convolution_gpu_bfyx_f16_1x1
	subgraph0: fire9/expand1x1    EXECUTED       layerType: Convolution        realTime: 36        cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire9/expand3x3    EXECUTED       layerType: Convolution        realTime: 222       cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: fire9/concat       OPTIMIZED_OUT  layerType: Concat             realTime: 0         cpu: 0               execType: undef
	subgraph0: conv10             EXECUTED       layerType: Convolution        realTime: 771       cpu: 5               execType: convolution_gpu_bfyx_f16
	subgraph0: pool10/reduce      EXECUTED       layerType: Pooling            realTime: 23        cpu: 5               execType: pooling_gpu_blocked
	subgraph0: prob               OPTIMIZED_OUT  layerType: SoftMax            realTime: 0         cpu: 0               execType: undef
	subgraph0: data               EXECUTED       layerType: Input_layout       realTime: 0         cpu: 1               execType: undef
	subgraph0: relu_conv1         OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire2/relu_sque... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire2/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire2/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire3/relu_sque... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire3/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire3/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire4/relu_sque... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire4/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire4/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire5/relu_sque... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire5/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire5/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire6/relu_sque... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire6/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire6/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire7/relu_sque... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire7/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire7/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire8/relu_sque... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire8/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire8/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire9/relu_sque... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire9/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: fire9/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: relu_conv10        OPTIMIZED_OUT  layerType: ReLU               realTime: 0         cpu: 0               execType: undef
	subgraph0: prob_cldnn_outp... EXECUTED       layerType: Reorder            realTime: 39        cpu: 5               execType: softmax_gpu_items_class_optimized

> **Note**: The performance counts shown above is based on the development system used to create this tutorial.

## Further Reading
To learn more about HETEO plugin, please refere to [Heterogeneous Plugin](https://docs.openvinotoolkit.org/latest/openvino_docs_IE_DG_supported_plugins_HETERO.html) from OpenVINO documentation.


