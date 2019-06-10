# Safety gear detection with Intel® Distribution of OpenVINO™ toolkit

The Safety Gear Detection Sample is another demonstration of the powerful capabilities of the Intel® Distribution of the OpenVINO™ toolkit to perform object detection. The sample presents a video frame-by-frame to the Inference Engine (IE) which subsequently uses an optimized trained neural network, mobilenet-ssd, to detect people and their safety gear. This public model is a mobilenet neural network (SSD – Single Shot MultiBox Detector framework) that has been pre-trained to detect objects in a video clip.

### Download workshop content and set directory path
#### 1. Create the workshop directory

	sudo mkdir -p /opt/intel/workshop/

#### 2. Change ownership of the workshop directory to the current user

> **Note:** *replace the usernames below with your user account name*

	sudo chown username.username -R /opt/intel/workshop/

#### 3. Navigate to the new directory

	cd /opt/intel/workshop/

#### 4. Download and clone the workshop content to the current directory (/opt/intel/workshop/smart-video-workshop).

	git clone https://github.com/intel-iot-devkit/smart-video-workshop.git

#### 5. Set short path for the workshop directory

	export SV=/opt/intel/workshop/smart-video-workshop/

## Part 1: Optimize a deep-learning model using the Model Optimizer (MO)

In this section, you will use the Model Optimizer to convert a trained model to two Intermediate Representation (IR) files (one .bin and one .xml). The Inference Engine requires this model conversion so that it can use the IR as input and achieve optimum performance on Intel hardware.

#### 1. Create a directory to store IR files

	cd $SV/safety-gear-example/
	mkdir -p mobilenet-ssd/FP32

#### 2. Navigate to the Intel® Distribution of OpenVINO™ toolkit install directory

	cd /opt/intel/openvino/deployment_tools/model_optimizer

#### 3. Run the Model Optimizer on the pretrained Caffe* model. This step generates one .xml file and one .bin file and place both files in the tutorial samples directory (located here: /safety-gear-example/)

	python3 mo_caffe.py --input_model $SV/safety-gear-example/worker_safety_mobilenet.caffemodel -o $SV/safety-gear-example/mobilenet-ssd/FP32

> **Note:** Although this tutorial uses Single Shot MultiBox Detector (SSD) on a trained mobilenet-ssd* model, the Inference Engine is compatible with other neural network architectures, such as AlexNet*, GoogleNet*, MxNet* etc.

<br>

The Model Optimizer converts a pretrained Caffe* model to make it compatible with the Intel Inference Engine and optimizes it for Intel® architecture. These are the files you would include with your C++ application to apply inference to visual data.

> **Note:** if you continue to train or make changes to the Caffe* model, you would then need to re-run the Model Optimizer on the updated model.

#### 4. Navigate to the tutorial sample model directory

	cd $SV/safety-gear-example/mobilenet-ssd/FP32

#### 5. Verify creation of the optimized model files (the IR files)

	ls

You should see the following two files listed in this directory: **worker_safety_mobilenet.xml** and **worker_safety_mobilenet.bin**


## Part 2: Use the worker_safety_mobilenet* model and Inference Engine in an object detection application


#### 1. Open the sample app (main.cpp) in the editor of your choice to view the lines that call the Inference Engine.

	cd $SV/object-detection/
	gedit main.cpp

* Line 130 &#8212; loads the Inference Engine plugin for use within the application
* Line 144 &#8212; initializes the network object
* Line 210 &#8212; loads model to the plugin
* Line 228 &#8212; allocate input blobs
* Line 238 &#8212; allocate output blobs
* Line 289 &#8212; runs inference using the optimized model


#### 2. Close the source file

#### 3. Source your environmental variables

	source /opt/intel/openvino/bin/setupvars.sh

#### 4. Build the sample application with make file

 	cd $SV/object-detection/
	make

#### 5. Check the test video file from the safety-gear-example folder.


Open the Safety_Full_Hat_and_Vest_2.mp4 file from the $SV/safety-gear-example folder.
We will use that as the test file.

#### 6. Run the sample application to use the Inference Engine on the test video
The below command runs the application

	./tutorial1 -i $SV/safety-gear-example/Safety_Full_Hat_and_Vest_2.mp4 -m $SV/safety-gear-example/mobilenet-ssd/FP32/worker_safety_mobilenet.xml

> **Note:** If you get an error related to "undefined reference to 'google::FlagRegisterer...", try uninstalling libgflags-dev: sudo apt-get remove libgflags-dev

#### 7. Display output
For simplicity of the code and in order to put more focus on the performance number, video rendering with rectangle boxes for detected objects has been separated from main.cpp.

	 make -f Makefile_ROIviewer
	./ROIviewer -i $SV/safety-gear-example/Safety_Full_Hat_and_Vest_2.mp4 -l $SV/safety-gear-example/pascal_voc_classes.txt

You should see a video play with people wearing safety gear and bounding boxes around them.

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

 Make sure that you have sourced the environmental variables for each newly opened terminal window.

	source /opt/intel/openvino/bin/setupvars.sh

	export SV=/opt/intel/workshop/smart-video-workshop/

	cd $SV/object-detection

#### 1. CPU
```
./tutorial1 -i $SV/safety-gear-example/Safety_Full_Hat_and_Vest_2.mp4 -m $SV/safety-gear-example/mobilenet-ssd/FP32/worker_safety_mobilenet.xml -d CPU
```
You will see the **total time** it took to run the inference.

#### 2. GPU
Since you installed the OpenCL™ drivers to use the GPU, you can run the inference on GPU and compare the difference.

Set target hardware as GPU with **-d GPU**
```
./tutorial1 -i $SV/safety-gear-example/Safety_Full_Hat_and_Vest_2.mp4 -m $SV/safety-gear-example/mobilenet-ssd/FP32/worker_safety_mobilenet.xml -d GPU
```

The **total time** between CPU and GPU will vary depending on your system.
