# Object Detection with Intel® Computer Vision SDK 

This tutorial uses a Single Shot MultiBox Detector (SSD) on a trained SqeezeNet* model to walk you through the basic steps of using two key components of the Intel® CV SDK: the Model Optimizer and Inference Engine. 

Model optimizer takes pre-trained deep learning models and optimizes them for performance/space with conservative topology transformations. The biggest boost is from conversion to data types matching the hardware. 

Inference is the process of using a trained neural network to interpret meaning from data, such as images. The code sample in this tutorial feeds a short video of cars, frame-by-frame, to the Inference Engine which subsequently utilizes an optimized trained neural network. 

### Install the tutorial support files

#### Set PATH variables
The location that you downlaoded the SMart Video workshop content. For example, if you download the MSart Video workshop to *~/Desktop/smart-video-workshop-master

	export LAB_DIR=/home/intel/Desktop/smart-video-workshop-master
	export IE_SAMPLE_DIR=/opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/
	export MODEL_OPT_DIR=/opt/intel/computer_vision_sdk/deployment_tools/model_optimizer

#### Compile samples
	
	cd $IE_SAMPLE_DIR
	sudo mkdir -p build && cd build
	sudo cmake –DCMAKE_BUILD_TYPE=Debug  ..
	sudo make   

If this errors out, run the demo script

	source /opt/intel/computer_vision_sdk/bin/setupvars.sh
	cd /opt/intel/computer_vision_sdk/deployment_tools/demo
	sudo ./demo_security_barrier_camera.sh
	
## Part 1: Optimize a deep-learning model using the Model Optimizer (MO)

In this section, you will use the Model Optimizer to convert a trained model to two Intermediate Representation (IR) files (one .bin and one .xml). The Inference Engine requires this model conversion so it can use the IR as input and achieve optimum performance on Intel hardware.

#### 1. Navigate to the cv-sdk directory

	cd $MODEL_OPT_DIR

#### 2. Run the Model Optimizer on the pretrained Caffe* model. This step generates one .xml file and one .bin file and place both files in the tutorial samples directory (located here: /object-detection/)

	python3 mo_caffe.py --input_model $LAB_DIR/object-detection/models/sqeeznet_ssd/squeezenet_ssd.caffemodel -o $LAB_DIR/object-detection/models/sqeeznet_ssd/

> **Note:** Although this tutorial uses Single Shot MultiBox Detector (SSD) on a trained Sqeezenet* model, the inference engine is compatible with other neural network architectures, such as AlexNet*, GoogleNet*, MxNet* etc.


The Model Optimizer converts a pretrained Caffe model to be compatible with the Intel Inference Engine and optimizes it for Intel architecture. These are the files you would include with your C++ application to apply inference to visual data.
	
> **Note:** if you continue to train or make changes to the Caffe model, you would then need to re-run the Model Optimizer on the updated model.

#### 3. Navigate to the tutorial sample model directory

	cd $LAB_DIR/object-detection/models/sqeeznet_ssd/

#### 4. Verify creation of the optimized model files (the IR files)

	ls

You should see the following two files listed in this directory: **squeezenet_ssd.xml** and **squeezenet_ssd.bin**


## Part 2: Use the sqeezenet model and Inference Engine in an object detection application


#### 1. Open the sample app (main.cpp) in the editor of your choice to view the lines that call the Inference Engine.

* Line 123 - loads the Inference Engine plugin for use within the application
* Line 137 - initializes the network object
* Line 221 - allocate input blobs
* Line 231 - allocate output blobs
* Line 282 - runs inference using the optimized model

#### 2. Close the source file

#### 3. Source your environmental variables

	source /opt/intel/computer_vision_sdk/bin/setupvars.sh

#### 4. Build the sample application with cmake
Move up to the sample directory and build.
	
	cd ../..
 	make

#### 5. Before running, download the test video file to a new videos directory. 
Note: For dry-run on May 4th, the video is in the object-detectoin/models folder, cars_1920x1080.h264.

	wget https://pixabay.com/en/videos/download/video-1900_source.mp4?attachment  


#### 6. Run the security barrier sample application to use the Inference Engine on a video
The below command runs the application 
	 
	 cd ../..
	./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $LAB_DIR/object-detection/models/sqeeznet_ssd/squeezenet_ssd.xml 
 
> **Note:** If you get an error related to "undefined reference to 'google::FlagRegisterer...", try uninstalling libgflags-dev: sudo apt-get remove libgflags-dev

#### 7. Display output
For simplicity of the code and put more focus on the performance number, the rendering the video with rectangle baxes for object detection has been separated. 

	 make -f Makefile_ROIviewer 
	./ROIviewer -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -l $LAB_DIR/object-detection/pascal_voc_classes.txt 
	
You should see a video play with cars running on the highway and red bounding boxes around them. 

Here are the parameters used in the above coomand to run the application:

	./tutorial1 -h

		-h              Print a usage message
		-i <path>       Required. Path to input video file
		-model <path>   Required. Path to model file.
		-b #            Batch size.
		-thresh #       Threshold (0-1: .5=50%)
		-d <device>     Infer target device (CPU or GPU or MYRIAD)
		-fr #           maximum frames to process
	

## Part 3: Run the example on different hardware

**IT'S BEST TO OPEN A NEW TERMINAL WINDOW SO YOU CAN COMPARE THE RESULTS**

#### 1. CPU
```
./tutorial1 -i $SV/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/sqeeznet_ssd/squeezenet_ssd.xml -d CPU
```
You'll see the **Total time** it took to run.

#### 2. GPU
Since you installed the OpenCL™ drivers to use the GPU, you can try running inference on the GPU and compare the difference.

Set target hardware as GPU with
```
-d GPU
```
```
./tutorial1 -i $LAB_DIR/object-detection/models/cars_1920x1080.h264 -m $LAB_DIR/object-detection/models/sqeeznet_ssd/squeezenet_ssd.xml -d GPU
```

The **Total time** between CPU and GPU will vary depending on your system.
