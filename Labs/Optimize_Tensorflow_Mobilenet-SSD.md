# Optimize a Tensorflow* Object Detection Model - ssd_mobilenet_v1_coco

In this lab, we are going to use the Model Downloader to download a Tensorflow* Object Detection model - ssd_mobilenet_v1_coco from [Open Model Zoo](https://github.com/openvinotoolkit/open_model_zoo). Then use Model Optimizer to convert the model into Intermediate Representation format with both FP32 and FP16 data precision.  

#### Set short path for the workshop directory

	export SV=/opt/intel/workshop/smart-video-workshop/
    
## Part 1: Download a public pre-trained model with Model Downloader

In this section, you will use the Model Downloader to download a public pre-trained Tensorflow* Object Detection model.

#### 1. Navigate to the directory of Model Downloader and check the usage of Model Downloader
 	
	cd /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/
	python3 downloader.py -h

#### 2. Check all the available Intel or public pre-trained models on Open Model Zoo

	python3 downloader.py --print_all

#### 3. Download SqueezeNet v1.1 to the Workshop directory

	sudo python3 downloader.py --name ssd_mobilenet_v1_coco -o /opt/intel/workshop
	
#### 4. Check the downloaded model

	cd /opt/intel/workshop/public/ssd_mobilenet_v1_coco/ssd_mobilenet_v1_coco_2018_01_28
	ls

You will see the downloaded Tensorflow* model:

	checkpoint                 model.ckpt.data-00000-of-00001  model.ckpt.meta  saved_model
	frozen_inference_graph.pb  model.ckpt.index                pipeline.config

To learn more about this model, you can either click [HERE](https://github.com/openvinotoolkit/open_model_zoo/blob/master/models/public/ssd_mobilenet_v1_coco/ssd_mobilenet_v1_coco.md), or:

	cd /opt/intel/openvino/deployment_tools/open_model_zoo/models/public/ssd_mobilenet_v1_coco
	gedit ssd_mobilenet_v1_coco.md  

> **Note**: From the model description file, you will need to understand the input and output **layer name**, **shape** of the input layer, **color order** and **mean value** or **scale value** if applicable for this model.

## Part 2: Convert the downloaded Tensorflow* model to IR format

In this session, you will use the Model Optimizer to convert the downloaded Tensorflow* Object Detection model to IR format with both FP32 and FP16 data precisions.

#### 1. Navigate to the Model Optimizer directory

	cd /opt/intel/openvino/deployment_tools/model_optimizer/

#### 2. Check the usage of Model Optimizer

	python3 mo.py -h

A list of general parameters for Model Optimizer will be printed out, to learn more about each parameter, you can refer to this [Document](https://docs.openvinotoolkit.org/latest/openvino_docs_MO_DG_prepare_model_convert_model_Converting_Model_General.html)

#### 3. Convert ssd_mobilenet_v1_coco to IR with FP32 data precision
There are also Model Optimizer parameters

	sudo python3 mo.py \
	--reverse_input_channels \
	--input_shape=[1,300,300,3] \
	--input=image_tensor \
	--output=detection_scores,detection_boxes,num_detections \
	--transformations_config=/opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json \
	--tensorflow_object_detection_api_pipeline_config=/opt/intel/workshop/public/ssd_mobilenet_v1_coco/ssd_mobilenet_v1_coco_2018_01_28/pipeline.config \
	--input_model=/opt/intel/workshop/public/ssd_mobilenet_v1_coco/ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb \
	-o /opt/intel/workshop/Mobilenet-SSD-v1/FP32 \
	--model_name mobilenet-ssd-v1-fp32

#### 4. Check the converted model 
	
	cd /opt/intel/workshop/Mobilenet-SSD-v1/FP32
	ls
	
You will see three fils were created under this folder, the .xml file is the topology file of the model, while the .bin file is the weight and bias.

	mobilenet-ssd-v1-fp32.bin  mobilenet-ssd-v1-fp32.mapping  mobilenet-ssd-v1-fp32.xml

#### 5. Convert Squeezenet1.1 to IR with FP16 data precision

	sudo python3 mo.py --input_shape=[1,3,227,227] \
	--input=data \
	--output=prob \
	--mean_values=data[104.0,117.0,123.0] \
	--input_model=/opt/intel/workshop/public/squeezenet1.1/squeezenet1.1.caffemodel \
	--input_proto=/opt/intel/workshop/public/squeezenet1.1/squeezenet1.1.prototxt \
	--data_type FP16 \
	-o /opt/intel/workshop/Squeezenet/FP16 \
	--model_name squeezenet1.1_fp16

#### 4. Check the converted model 
	
	cd /opt/intel/workshop/Squeezenet/FP16
	ls
	
You will see three fils were created under this folder, the .xml file is the topology file of the model, while the .bin file is the weight and bias.

	squeezenet1.1_fp16.bin  squeezenet1.1_fp16.mapping  squeezenet1.1_fp16.xml

## Further Reading
To learn more about converting a Caffe* model using Model Optimizer, please refer to this OpenVINO documentation [Converting a Caffe* Model](https://docs.openvinotoolkit.org/latest/openvino_docs_MO_DG_prepare_model_convert_model_Convert_Model_From_Caffe.html)
