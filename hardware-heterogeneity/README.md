
# OpenVINO™ toolkit hetero plugin 

This example shows how to use hetero plugin to define preferences to run different network layers on different hardware types. 

### Car detection tutorial example 
#### 1. Navigate to the tutorial directory

	cd $SV/object-detection/
  
#### 2. Run the car detection tutorial with hetero plugin 

##### a) Prioritizing running on GPU first.

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:GPU,CPU
    

##### a) Prioritizing running on CPU first.

     ./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:CPU,GPU 
     
### Inference Engine classification sample     
OpenVINO install folder (/opt/intel/computer_vision_sdk/) includes various samples for developers to understand how Inference Engine APIs can be used. These samples have One of the basic sample is a classificatoin sample. 

#### 1. First, go to samples build directory:
	
	$ cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release


#### 2. Run classification sample with hetero plugin, prioritizing running on GPU first.

$ ./classification_sample -i car.png -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:GPU,CPU
[ INFO ] InferenceEngine:
        API version ............ 1.0
        Build .................. 9911
[ INFO ] Parsing input parameters
[ INFO ] No extensions provided
[ INFO ] Loading plugin
[ INFO ] Plugin:
        API version ............ 1.0
        Build .................. heteroPlugin
        Description ....... heteroPlugin
[ INFO ] Loading network files:
        squeezenet1.1.xml
        squeezenet1.1.bin
[ INFO ] Preparing input blobs
[ WARNING ] Image is resized from (787, 259) to (227, 227)
[ INFO ] Batch size is 1
[ INFO ] Preparing output blobs
[ INFO ] Loading model to the plugin
[ INFO ] Starting inference (1 iterations)
[ INFO ] Average running time of one iteration: 6.28381 ms
[ INFO ] Processing output blobs

Top 10 results:

Image car.png

817 0.8457031 label sports car, sport car
511 0.0891113 label convertible
479 0.0395508 label car wheel
751 0.0085678 label racer, race car, racing car
436 0.0064659 label beach wagon, station wagon, wagon, estate car, beach waggon, station waggon, waggon
656 0.0034027 label minivan
586 0.0024509 label half track
717 0.0016336 label pickup, pickup truck
864 0.0010891 label tow truck, tow car, wrecker
581 0.0005560 label grille, radiator grille

[ INFO ] Execution successful

#### 3. Check where everything is running with –pc
$ ./classification_sample -i car.png -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:GPU,CPU -pc

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

#### 4. Now, run with CPU first
$ ./classification_sample -i car.png -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:CPU,GPU -pc

subgraph1: conv1              EXECUTED       layerType: Convolution        realTime: 257        cpu: 257            execType: jit_avx2
subgraph1: conv10             EXECUTED       layerType: Convolution        realTime: 789        cpu: 789            execType: jit_avx2_1x1
subgraph1: data_nchw_nchw     EXECUTED       layerType: Reorder            realTime: 52         cpu: 52             execType: reorder
subgraph1: fire2/concat       NOT_RUN        layerType: Concat             realTime: 0          cpu: 0              execType: unknown
subgraph1: fire2/expand1x1    EXECUTED       layerType: Convolution        realTime: 54         cpu: 54             execType: jit_avx2_1x1
subgraph1: fire2/expand3x3    EXECUTED       layerType: Convolution        realTime: 213        cpu: 213            execType: jit_avx2
subgraph1: fire2/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0          cpu: 0              execType: undef
subgraph1: fire2/relu_expa... NOT_RUN        layerType: ReLU               realTime: 0          cpu: 0              execType: undef
subgraph1: fire2/relu_sque... NOT_RUN        layerType: ReLU               realTime: 0          cpu: 0              execType: undef

 Note: jit to CPU instruction set


