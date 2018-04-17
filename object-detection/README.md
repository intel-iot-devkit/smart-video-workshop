# Object Detection with Intel® Computer Vision SDK 

This tutorial uses a Single Shot MultiBox Detector (SSD) on a trained SqeezeNet* model to walk you through the basic steps of using two key components of the Intel® CV SDK: the Model Optimizer and Inference Engine. 

Model optimizer takes pre-trained deep learning models and optimizes them for performance/space with conservative topology transformations. The biggest boost is from conversion to data types matching the hardware. 

Inference is the process of using a trained neural network to interpret meaning from data, such as images. The code sample in this tutorial feeds a short video of cars, frame-by-frame, to the Inference Engine which subsequently utilizes an optimized trained neural network. 

### Install the tutorial support files

#### 1. Install gflags and python libraries

	sudo apt install libgflags-dev
	
	sudo apt install python3-pip
    
    pip3 install -r /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/requirements_caffe.txt
    
## Part 1: Optimize a deep-learning model using the Model Optimizer (MO)

In this section, you will use the Model Optimizer to convert a trained model to two Intermediate Representation (IR) files (one .bin and one .xml). The Inference Engine requires this model conversion so it can use the IR as input and achieve optimum performance on Intel hardware.

#### 1. Navigate to the cv-sdk directory

	cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer

#### 2. Run the Model Optimizer on the pretrained Caffe* model. This step generates one .xml file and one .bin file and place both files in the tutorial samples directory (located here: /object-detection/)

	python3 mo_caffe.py --input_model /object-detection/model/squeezenet_SSD.caffemodel -o /object-detection/

> **Note:** Although this tutorial uses Single Shot MultiBox Detector (SSD) on a trained Sqeezenet* model, the inference engine is compatible with other neural network architectures, such as AlexNet*, GoogleNet*, MxNet* etc.

<br>

The Model Optimizer converts a pretrained Caffe model to be compatible with the Intel Inference Engine and optimizes it for Intel architecture. These are the files you would include with your C++ application to apply inference to visual data.
	
> **Note:** if you continue to train or make changes to the Caffe model, you would then need to re-run the Model Optimizer on the updated model.

#### 3. Navigate to the tutorial sample directory

	cd /object-detection/

#### 4. Verify creation of the optimized model files (the IR files)

	ls

You should see the following two files listed in this directory: **squeezenet_SSD.xml** and **squeezenet_SSD.bin**

<br>
<br>

## Part 2: Use the optimized models and Inference Engine in a pedestrian detection application


#### 1. Open the sample app (main.cpp) in the editor of your choice to view the lines that call the Inference Engine.
<ul><ul>
	<li> Line 39 &#8212; adds the Inference Engine plugin to your application</li>
	<li> Line 107 &#8212; sets the confidence threshold for object detection</li>
	<li> Line 391 &#8212; loads the Inference Engine plugin for use within the application</li>
	<li> Line 417 &#8212; initializes the network object</li>
	<li> Line 637 &#8212; runs inference using the optimized model
</ul></ul>

#### 2. Close the source file

#### 3. Set the path

	source /opt/intel/computer_vision_sdk/bin/setupvars.sh

#### 4. Build the sample application with cmake

 	mkdir -p build
	cd build
	cmake -DCMAKE_BUILD_TYPE=Release ..
	make -j8 security_barrier_camera_sample

#### 5. Before running, download the test video file to a new videos directory:

	wget https://videos.pexels.com/videos/cars-on-highway-1409 -P 


#### 6. Run the security barrier sample application to use the Inference Engine on a video
The below command runs the application 

 
> **Note:** If you get an error related to "undefined reference to 'google::FlagRegisterer...", try uninstalling libgflags-dev: sudo apt-get remove libgflags-dev

You should see a video play with cars running on the highway and red bounding boxes around them. 

<br>

### Explore using different parameters to see how they affect the results

#### 1. Adjust the number of video frames to run through the Inference Engine
The sample video file contains approximately 790 frames; however, in the previous example we opted to ran inference on a subset of those frames. Update the -fr parameter flag to adjust the amount of frames being processed through the Inference Engine.
	
	./IEobjectdetection -i /opt/intel/tutorials/cvsdk_hello_world/samples/hello_world_1.avi -fr 200 -m SSD_GoogleNetV2.xml -d CPU -f pascal_voc_classes.txt -t SSD

#### 2. Modify the object detection confidence level threshold
You can also try overriding the confidence level threshold. By setting the new threshold to 0.1, you will see a lot more bounding boxes around the people, but will have more instances of 'false' boxes appearing around non-pedestrian objects.
	
	./IEobjectdetection -i /opt/intel/tutorials/cvsdk_hello_world/samples/hello_world_1.avi -fr 200 -m SSD_GoogleNetV2.xml -d CPU -f pascal_voc_classes.txt -t SSD
	
<br>
<br>
