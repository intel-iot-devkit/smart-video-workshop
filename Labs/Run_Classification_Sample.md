# Run Classification Sample Application with the Optimized SqueezeNet v1.1 Model 

In this lab, we are going to run a classification Python sample application with the optimized SqueezeNet v1.1 Model we converted in [Lab1 - Optimize a Caffe* Classification Model - SqueezeNet v1.1](./Optimize_Caffe_squeezeNet.md).
 
#### 1. Navigate to the directory of the Python Sample Application 
 	
	cd /opt/intel/openvino_2021/deployment_tools/inference_engine/samples/python

#### 2. Navigate to the directory of classification_sample_async and check the usage of this sample application

	cd classification_sample_async
	python3 classification_sample_async.py -h

#### 3. Run classification_sample_async Sample Application with SqueezeNet v1.1 model on CPU

	python3 classification_sample_async.py \
	-m /opt/intel/workshop/Squeezenet/FP32/squeezenet1.1_fp32.xml \
	-i /opt/intel/workshop/smart-video-workshop/Labs/daisy.jpg \
	-d CPU \
	--labels /opt/intel/workshop/smart-video-workshop/Labs/squeezetnet_label.txt 

The output would be something like this:

	classid probability
	------- -----------
	985: 'daisy',0.9918603
	309: 'bee',0.0062189
	108: 'sea anemone, anemone',0.0002938
	973: 'coral reef',0.0001974
	308: 'fly',0.0001486
	301: 'ladybug, ladybeetle, lady beetle, ladybird, ladybird beetle',0.0001268
	324: 'cabbage butterfly',0.0001079
	947: 'mushroom',0.0001005
	995: 'earthstar',0.0000976
	506: 'coil, spiral, volute, whorl, helix',0.0000964

#### 4. Switch to another picture and run the same application on GPU with FP16 data precision model

	python3 classification_sample_async.py \
	-m /opt/intel/workshop/Squeezenet/FP16/squeezenet1.1_fp16.xml \
	-i /opt/intel/workshop/smart-video-workshop/Labs/puppy.jpg \
	-d GPU \
	--labels /opt/intel/workshop/smart-video-workshop/Labs/squeezetnet_label.txt 

You will see the output like this:

	classid probability
	------- -----------
	208: 'Labrador retriever',0.5244141
	852: 'tennis ball',0.4282227
	805: 'soccer ball',0.0158691
	207: 'golden retriever',0.0066185
	222: 'kuvasz',0.0064087
	178: 'Weimaraner',0.0055656
	180: 'American Staffordshire terrier, Staffordshire terrier, American pit bull terrier, pit bull terrier',0.0020828
	190: 'Sealyham terrier, Sealyham',0.0020485
	251: 'dalmatian, coach dog, carriage dog',0.0012798
	176: 'Saluki, gazelle hound',0.0012589

You can download different pictures from the internet, and try the same application with the optimized SqueezeNet v1.1 model.

#### 5. Explore the sourcecode
Now let's take a look at the sourcecode, and learn more about the Inference Engine API

	cd /opt/intel/openvino_2021/deployment_tools/inference_engine/samples/python/classification_sample_async
	gedit classification_sample_async.py


## Further Reading
To learn more about Image Classification Python* Sample Async, please refer to this OpenVINO documentation [Image Classification Python* Sample Async](https://docs.openvinotoolkit.org/latest/openvino_inference_engine_ie_bridges_python_sample_classification_sample_async_README.html)
