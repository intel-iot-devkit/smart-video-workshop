This example shows to use hetero plugin to define preferences to run diffrerent network layers on different hardware types. 

#### 1. Navigate to the tutorial sample directory

	cd $SV/object-detection/
  
#### 2. Run the security barrier object detection sample with hetero plugin 

##### a) Prioritizing running on GPU first.

	./tutorial1 -i cars_1920x1080.h264 -m $SV/object-detection/models/sqeeznet_ssd/squeezenet_ssd.xml -d HETERO:GPU,CPU
    
Check where everything is running with –pc

	  ./tutorial1 -i cars_1920x1080.h264 -m $SV/object-detection/models/sqeeznet_ssd/squeezenet_ssd.xml -d HETERO:GPU,CPU -pc
    
    performance counts:

    subgraph1: conv1              EXECUTED       layerType: Convolution        realTime: 462        cpu: 86             execType: GPU
    subgraph1: conv10             EXECUTED       layerType: Convolution        realTime: 907        cpu: 71             execType: GPU
    subgraph1: data_cldnn_inpu... EXECUTED       layerType: Reorder            realTime: 504        cpu: 104            execType: GPU
    subgraph1: fire2/concat       EXECUTED       layerType: Concat             realTime: 35         cpu: 50             execType: GPU
    subgraph1: fire2/expand1x1    EXECUTED       layerType: Convolution        realTime: 131        cpu: 76             execType: GPU
    subgraph1: fire2/expand3x3    EXECUTED       layerType: Convolution        realTime: 227        cpu: 92             execType: GPU
    subgraph1: fire2/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0          cpu: 0              execType: None
    subgraph1: fire2/relu_expa... OPTIMIZED_OUT  layerType: ReLU               realTime: 0          cpu: 0              execType: None
    subgraph1: fire2/relu_sque... OPTIMIZED_OUT  layerType: ReLU               realTime: 0          cpu: 0              execType: None
    subgraph1: fire2/squeeze1x1   EXECUTED       layerType: Convolution        realTime: 69         cpu: 50             execType: GPU
    subgraph1: fire3/concat       EXECUTED       layerType: Concat             realTime: 28         cpu: 38             execType: GPU

Note: execType GPU for layers executed on GPU.  Also, skipped relu.

##### a) Prioritizing running on CPU first.

     ../tutorial1 -i cars_1920x1080.h264 -m $SV/object-detection/models/sqeeznet_ssd/squeezenet_ssd.xml -d HETERO:CPU,GPU -pc
     
     subgraph1: conv1              EXECUTED       layerType: Convolution        realTime: 257        cpu: 257            execType: jit_avx2
    subgraph1: conv10             EXECUTED       layerType: Convolution        realTime: 789        cpu: 789            execType: jit_avx2_1x1
    subgraph1: data_nchw_nchw     EXECUTED       layerType: Reorder            realTime: 52         cpu: 52             execType: reorder
    subgraph1: fire2/concat       NOT_RUN        layerType: Concat             realTime: 0          cpu: 0              execType: unknown
    subgraph1: fire2/expand1x1    EXECUTED       layerType: Convolution        realTime: 54         cpu: 54             execType: jit_avx2_1x1
    subgraph1: fire2/expand3x3    EXECUTED       layerType: Convolution        realTime: 213        cpu: 213            execType: jit_avx2
    subgraph1: fire2/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0          cpu: 0              execType: undef
    subgraph1: fire2/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0          cpu: 0              execType: undef
    subgraph1: fire2/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0          cpu: 0              execType: undef

Note: jit to CPU instruction set and ran with FP16 input!

