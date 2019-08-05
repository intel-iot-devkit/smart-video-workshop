# Converting a TensorFlow* Model in Linux*
  
### Pre-Requisites: 
#### Change ownership of the directory to the current user 

> **Note:** *replace the usernames below with your user account name*
		
	sudo chown username.username -R /opt/intel
     
#### Download Model(s) from TensorFlow* -slim library 
There are a number of pre-trained public models in the TensorFlow*-slim repository. The models are distributed as Python scripts and checkpoint files.
First of all download repository with models.
Note: This is done in home directory(~)

    cd
    git clone https://github.com/tensorflow/models/
    cd models/research/slim

#### Export Inference Graph and download checkpoint file 
Export inference graph for one of the available models using the following command (Inception V1 in this example): 

    python3 export_inference_graph.py --alsologtostderr --model_name=inception_v1 --output_file=/tmp/inception_v1_inf_graph.pb
    
The script creates inference graph file with name “inception_v1_inf_graph.pb” in the /tmp direcory.

#### Download archive with checkpoint file (Inception V1 in this example): 

    export CHECKPOINT_DIR=/tmp/checkpoints
    
    mkdir $CHECKPOINT_DIR
    
    wget http://download.tensorflow.org/models/inception_v1_2016_08_28.tar.gz
    
    tar -xvf inception_v1_2016_08_28.tar.gz
    
    mv inception_v1.ckpt $CHECKPOINT_DIR
    
    rm inception_v1_2016_08_28.tar.gz

#### Freeze the model
The last step is to freeze the graph. To do this you need to know the output node of the model you are planning to freeze. This information is found by running the summarize_graph.

##### Summarize Graph 
Go to ~/models/research/slim/ directory and run summarize_graph.py script.

    cd ~/models/research/slim/
    
    python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo/utils/summarize_graph.py --input_model=/tmp/inception_v1_inf_graph.pb

The output layer/node name should be in the last line of text on the console and should look like:

1 input(s) detected:
Name: input, type: float32, shape: (-1,224,224,3)
1 output(s) detected:
InceptionV1/Logits/Predictions/Reshape_1Freeze Graph

 
##### Freeze the graph for Intel® Distribution of OpenVINO™ toolkit 
The script generates inception_v1_frozen.pb file with the frozen model in the directory you are currently in.
 
 	python3 $HOME/.local/lib/python3.5/site-packages/tensorflow/python/tools/freeze_graph.py --input_graph /tmp/inception_v1_inf_graph.pb --input_binary --input_checkpoint /tmp/checkpoints/inception_v1.ckpt --output_node_names InceptionV1/Logits/Predictions/Reshape_1 --output_graph inception_v1_frozen.pb

    
You might get warning message "Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA" while executing above command, ignore that. 

### Convert Frozen Tensorflow* model to IR using Model Optimizer 
Assuming you are in the ~/models/research/slim/ directory 

    python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo_tf.py --input_model inception_v1_frozen.pb --input_shape [1,224,224,3] --mean_values [1024,1024,1024] --scale_values [128,128,128]

This should produce “inception_v1_frozen.xml” and “inception_v1_frozen.bin” file. The xml file contains the topology information of the model and the bin file contains the model’s weights and biases. These two files are expected when using the inference engine so make note of the path.


### Run Classification Sample

The classification sample will showcase the Intel® Distribution of OpenVINO™ toolkit inference engine using TensorFlow model Inception_v1_frozen IR files (.xml & .bin) and an input image of a car to classify.
The classification collateral is defined as the input image car_1.bmp, the Inception_v1_frozen IR files (.xml & .bin), and the labels file inception_v1_frozen.labels.
Create a new directory that will hold the classification sample app and all needed components to run the classification sample
Note: The following steps should be followed and are assuming you are following the preceding steps. You should be in the home directory.

    source /opt/intel/openvino/bin/setupvars.sh
 
Navigate to the classification_sample executable file:

    cd $HOME/inference_engine_samples_build/intel64/Release

Place Classification App collateral in current local directory:

    sudo cp ~/models/research/slim/inception_v1_frozen.* .
    
    sudo cp /opt/intel/openvino/deployment_tools/demo/car_1.bmp  .
    
    sudo cp /opt/intel/openvino/deployment_tools/demo/squeezenet1.1.labels ./inception_v1_frozen.labels

#### Run Application
Note: To see all the flags that the sample takes as input run  ./classification_sample -h

    ./classification_sample -i car_1.bmp -m inception_v1_frozen.xml

Expected Output:


    [ INFO ] InferenceEngine: 
	API version ............ 2.0
	Build .................. custom_releases/2019/R2_f5827d4773ebbe727c9acac5f007f7d94dd4be4e
	Description ....... API
    [ INFO ] Parsing input parameters
    [ INFO ] Files were added: 1
    [ INFO ]     car_1.bmp
    [ INFO ] Creating Inference Engine
	CPU
	MKLDNNPlugin version ......... 2.0
	Build ........... 27579

    [ INFO ] Loading network files:
	inception_v1_frozen.xml
	inception_v1_frozen.bin
    [ INFO ] Preparing input blobs
    [ WARNING ] Image is resized from (749, 637) to (224, 224)
    [ INFO ] Batch size is 1
    [ INFO ] Preparing output blobs
    [ INFO ] Loading model to the device
    [ INFO ] Starting inference (1 iterations)
    [ INFO ] Processing output blobs

    Top 10 results:

    Image car_1.bmp

	classid probability label
	------- ----------- -----
	829     0.6013383   streetcar, tram, tramcar, trolley, trolley car
	905     0.1193138   window shade
	557     0.0587131   flagpole, flagstaff
	600     0.0273736   hook, claw
	812     0.0096623   space shuttle
	633     0.0080025   loupe, jeweler's loupe
	795     0.0052693   ski
	791     0.0045856   shopping cart
	652     0.0042737   military uniform
	689     0.0042265   overskirt


	total inference time: 10.1313218
	Average running time of one iteration: 10.1313218 ms

	Throughput: 98.7038034 FPS

    [ INFO ] Execution successful





