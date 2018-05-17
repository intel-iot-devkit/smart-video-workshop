# Object detection with OpenVINO™ toolkit

This tutorial uses a Single Shot MultiBox Detector (SSD) on a trained SSD300* model to walk you through the basic steps of using two key components of the OpenVINO™ toolkit: Model Optimizer and Inference Engine.

Model Optimizer takes pre-trained deep learning models and optimizes them for performance/space using conservative topology transformations. The biggest performance boost for a computer vision application can be achieved by converting data types to match the hardware.

Inference is the process of using a trained neural network to interpret data, such as images. This lab feeds a short video of cars, frame-by-frame, to the Inference Engine which subsequently utilizes an optimized trained neural network to detect cars.

## Set PATH variables
The location that you downlaoded the smart video workshop content to, for example, if you download the smart video workshop to *~/smart-video-workshop-master

> :warning: Be sure that you use the correct path to your smart video workshop labs directory.

	export SV=~/smart-video-workshop-master
	export MODEL_OPTIMIZER_DIR=/opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/

## Part 1: Optimize a deep-learning model using the Model Optimizer (MO)

In this section, you will use the Model Optimizer to convert a trained model to two Intermediate Representation (IR) files (one .bin and one .xml). The Inference Engine requires this model conversion so that it can use the IR as input and achieve optimum performance on Intel hardware.

### 1. Create a directory to store IR files

	cd $SV/object-detection/
	mkdir -p SSD300 && cd SSD300
	mkdir -p FP32

### 2. Navigate to the OpenVINO™ toolkit install directory

	cd $MODEL_OPTIMIZER_DIR

### 3. Run the Model Optimizer

Run the Model Optimizer on the pretrained Caffe* model. This step generates one .xml file and one .bin file and place both files in the tutorial samples directory (located here: /object-detection/)

	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/ssd/300/caffe/ssd300.caffemodel -o $SV/object-detection/SSD300/FP32

> :warning: Although this tutorial uses Single Shot MultiBox Detector (SSD) on a trained SSD300* model, the Inference Engine is compatible with other neural network architectures, such as AlexNet*, GoogleNet*, MxNet* etc.


The Model Optimizer converts a pretrained Caffe* model to make it compatible with the Intel Inference Engine and optimizes it for Intel architecture. These are the files you would include with your C++ application to apply inference to visual data.

> **Note:** if you continue to train or make changes to the Caffe* model, you would then need to re-run the Model Optimizer on the updated model.

#### 4. Navigate to the tutorial sample model directory

	cd $SV/object-detection/SSD300/FP32

#### 5. Verify creation of the optimized model files (the IR files)

	ls

You should see the following two files listed in this directory: **ssd300.xml** and **ssd300.bin**


## Part 2: Use the SSD300* model and Inference Engine in an object detection application


#### 1. Open the sample app (main.cpp) in the editor of your choice to view the lines that call the Inference Engine.

* Line 123 - loads the Inference Engine plugin for use within the application
* Line 137 - initializes the network object
* Line 221 - allocate input blobs
* Line 231 - allocate output blobs
* Line 282 - runs inference using the optimized model

#### 2. Close the source file

#### 3. Source your environmental variables

	source /opt/intel/computer_vision_sdk/bin/setupvars.sh

#### 4. Build the sample application with make file

 	cd $SV/object-detection/
	make

#### 5. Download the test video file to the object-detection folder.

	https://pixabay.com/en/videos/download/video-1900_source.mp4?attachment  
Cars - 1900.mp4 file will get downloaded. Put that file in the $SV/object-detection folder.

#### 6. Run the sample application to use the Inference Engine on the test video
The below command runs the application

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP32/ssd300.xml

> **Note:** If you get an error related to "undefined reference to 'google::FlagRegisterer...", try uninstalling libgflags-dev: sudo apt-get remove libgflags-dev

#### 7. Display output
For simplicity of the code and in order to put more focus on the performance number, video rendering with rectangle boxes for detected objects has been separated from main.cpp.

	 make -f Makefile_ROIviewer
	./ROIviewer -i $SV/object-detection/Cars\ -\ 1900.mp4 -l $SV/object-detection/pascal_voc_classes.txt

You should see a video play with cars running on the highway and red bounding boxes around them.

Here are the parameters used in the above command to run the application:

	./tutorial1 -h

		-h              Print a usage message
		-i <path>       Required. Path to input video file
		-model <path>   Required. Path to model file.
		-b #            Batch size.
		-thresh #       Threshold (0-1: .5=50%)
		-d <device>     Infer target device (CPU or GPU or MYRIAD)
		-fr #           Maximum frames to process


## Part 3: Run the example on different hardware

**IT'S BEST TO OPEN A NEW TERMINAL WINDOW SO THAT YOU CAN COMPARE THE RESULTS**

#### 1. CPU
```
./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP32/ssd300.xml -d CPU
```
You will see the **Total time** it took to run the inference.

#### 2. GPU
Since you installed the OpenCL™ drivers to use the GPU, you can run the inference on GPU and compare the difference.

Set target hardware as GPU with
```
-d GPU
```
```
./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/SSD300/FP32/ssd300.xml -d GPU
```

The **Total time** between CPU and GPU will vary depending on your system.
