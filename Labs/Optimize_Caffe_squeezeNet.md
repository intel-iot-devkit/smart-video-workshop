# Optimize a Caffe* Classification Model - SqueezeNet v1.1

In this lab, we are going to use the Model Downloader to download a Caffe* Classification model - SqueezeNet v1.1 from [Open Model Zoo](https://github.com/openvinotoolkit/open_model_zoo). Then use Model Optimizer to convert the model into Intermediate Representation format with both FP32 and FP16 data precision.   
## Part 1: Download a public pre-trained model with Model Downloader

In this section, you will use the Model Downloader to download a public pre-trained Caffe* classfication model.

#### 1. Navigate to the directory of Model Downloader and check the usage of Model Downloader
 	
	cd /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/
	python3 downloader.py -h

#### 2. Check all the available Intel or public pre-trained models on Open Model Zoo

	python3 downloader.py --print_all

#### 3. Download SqueezeNet v1.1 to the Workshop directory

	sudo python3 downloader.py --name squeezenet1.1 -o /opt/intel/workshop
	
#### 4. Check the downloaded model

	cd /opt/intel/workshop/public/squeezenet1.1
	ls

You will see the downloaded Caffe* model:

	squeezenet1.1.caffemodel  squeezenet1.1.prototxt  squeezenet1.1.prototxt.orig

To learn more about this model, you can either click [HERE](https://github.com/openvinotoolkit/open_model_zoo/blob/master/models/public/squeezenet1.1/squeezenet1.1.md), or:

	cd /opt/intel/openvino/deployment_tools/open_model_zoo/models/public/squeezenet1.1
	gedit squeezenet1.1.md  

> **Note**: From the model description file, you will need to understand the input and output **layer name**, **shape** of the input layer, **color order** and **mean value** or **scale value** if applicable for this mode

## Part 2: Convert the downloaded Caffe* model to IR format

In this session, you will use the Model Optimizer to convert the downloaded Caffe* classfication model to IR format with both FP32 and FP16 data precisions.

#### 1. Navigate to the Model Optimizer directory

	cd /opt/intel/openvino/deployment_tools/model_optimizer/

#### 2. Check the usage of Model Optimizer

	python3 mo.py -h

A list of general parameters for Model Optimizer will be printed out, to learn more about each parameter, you can refer to this [Document](https://docs.openvinotoolkit.org/latest/openvino_docs_MO_DG_prepare_model_convert_model_Converting_Model_General.html)

#### 3. Convert Squeezenet1.1 to IR with FP32 data precision

	sudo python3 mo.py \
	--input_shape=[1,3,227,227] \
	--input=data \
	--output=prob \
	--mean_values=data[104.0,117.0,123.0] \
	--input_model=/opt/intel/workshop/public/squeezenet1.1/squeezenet1.1.caffemodel \
	--input_proto=/opt/intel/workshop/public/squeezenet1.1/squeezenet1.1.prototxt \
	--data_type FP32 \
	-o /opt/intel/workshop/Squeezenet/FP32 \
	--model_name squeezenet1.1_fp32

#### 4. Check the converted model 
	
	cd /opt/intel/workshop/Squeezenet/FP32
	ls
	
You will see three fils were created under this folder, the .xml file is the topology file of the model, while the .bin file is the weight and bias.

	squeezenet1.1_fp32.bin  squeezenet1.1_fp32.mapping  squeezenet1.1_fp32.xml

#### 5. Convert Squeezenet1.1 to IR with FP16 data precision

	cd /opt/intel/openvino/deployment_tools/model_optimizer/
	
	sudo python3 mo.py \
	--input_shape=[1,3,227,227] \
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
