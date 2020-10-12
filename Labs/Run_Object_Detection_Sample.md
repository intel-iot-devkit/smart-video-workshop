# Run Object Detection Sample Application with the Optimized MobileNet SSD Model 

In this lab, we are going to run a classification Python sample application with the optimized SqueezeNet v1.1 Model we converted in [Lab2 - Optimize a Tensorflow* Object Detection Model - SSD with MobileNet](./Optimize_Tensorflow_Mobilenet-SSD.md).
 
#### 1. Navigate to the directory of the Python Sample Application 
 	
	cd /opt/intel/openvino_2021/deployment_tools/inference_engine/samples/python

#### 2. Navigate to the directory of object_detection_sample_ssd and check the usage of this sample application

	cd object_detection_sample_ssd/
	python3 object_detection_sample_ssd.py -h

#### 3. Run object_detection_sample_ssd Sample Application with MobileNet-SSD model on CPU

	python3 object_detection_sample_ssd.py \
	-m /opt/intel/workshop/Mobilenet-SSD-v1/FP32/mobilenet-ssd-v1-fp32.xml \
	-i /opt/intel/workshop/smart-video-workshop/Labs/birds.jpg \
	-d CPU  

The output would be something like this, we can see two objects with classid 16 have been detected:

	[0,16] element, prob = 0.992423    (130,336)-(881,895) batch id : 0 WILL BE PRINTED!
	[1,16] element, prob = 0.990345    (1158,475)-(1638,1022) batch id : 0 WILL BE PRINTED!
	[ INFO ] Image out.bmp created!

Now we can check an out.bmp has been generated, open it we will see the bounding box surround the detected objects:

	ls
	eog out.bmp
	

#### 4. Switch to another picture and run the same application on GPU with FP16 data precision model

	rm -f out.bmp
	python3 object_detection_sample_ssd.py \
	-m /opt/intel/workshop/Mobilenet-SSD-v1/FP16/mobilenet-ssd-v1-fp16.xml \
	-i /opt/intel/workshop/smart-video-workshop/Labs/dog_cat.jpg \
	-d GPU  

This time, two objects with different classid have been deteced:

	[0,17] element, prob = 0.98719    (222,483)-(1007,1072) batch id : 0 WILL BE PRINTED!
	[1,18] element, prob = 0.970389    (913,62)-(1669,1126) batch id : 0 WILL BE PRINTED!
	[ INFO ] Image out.bmp created!

You can download different pictures from the internet, and try the same application with the optimized MobileNet-SSD model.

#### 5. Explore the sourcecode
Now let's take a look at the sourcecode, and learn more about the Inference Engine API

	cd /opt/intel/openvino_2021/deployment_tools/inference_engine/samples/python/object_detection_sample_ssd
	gedit object_detection_sample_ssd.py


## Further Reading
To learn more about Object Detection Python* Sample SSD, please refer to this OpenVINO documentation [Object Detection Python* Sample SSD](https://docs.openvinotoolkit.org/latest/openvino_inference_engine_ie_bridges_python_sample_object_detection_sample_ssd_README.html)
