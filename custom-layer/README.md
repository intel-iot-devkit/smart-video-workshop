# Intel® Distribution of OpenVINO™ Toolkit 2019 R1.0 Custom Layer Tutorial for Ubuntu* 16.04

### Custom Layers
Custom layers are NN (Neural Network) layers that are not explicitly supported by a given framework. This tutorial demonstrates how to run inference on topologies featuring custom layers allowing you to plug in your own implementation for existing or completely new layers.

The list of known layers is different for any particular framework. To see the layers supported by the Intel® Distribution of OpenVINO™ toolkit, refer to the Documentation: https://docs.openvinotoolkit.org/latest/_docs_MO_DG_Deep_Learning_Model_Optimizer_DevGuide.html#intermediate-representation-notation-catalog
<br><br>

*If your topology contains layers that are not in the list of known layers, the Model Optimizer considers them to be custom.*

The Model Optimizer searches for each layer of the input model in the list of known layers before building the model's internal representation, optimizing the model and producing the Intermediate Representation.

### Custom Layers implementation workflow in the Intel® Distribution of OpenVINO™ toolkit
When implementing the custom layer in the Intel® Distribution of OpenVINO™ toolkit for your pre-trained model, you will need to add extensions in both the Model Optimizer and the Inference Engine. The following figure shows the work flow for the custom layer implementation.
<br>

![image of CL workflow](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/custom-layer/workflow.png "CL Workflow")

<br>

### Example custom layer: Hyperbolic Cosine (cosh) function
We showcase custom layer implementation using a simple function; hyperbolic cosine (cosh). It's mathematically represented as:

![](https://latex.codecogs.com/gif.latex?cosh%28x%29%3D%5Cfrac%7Be%5E%7Bx%7D&plus;e%5E%7B-x%7D%7D%7B2%7D)

### Extension Generator
This tool generates extension source files with stubs for the core functions. To get the workable extension, you will add your implementation of these functions to the generated files.

### Steps to implement custom layers on Ubuntu* 16.04

1. Make sure you run through the [lab setup](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/Lab_setup.md).

2. Setup your environment for the Intel® Distribution of OpenVINO™ toolkit:<br>
    ```
    source /opt/intel/openvino/bin/setupvars.sh
    ```

3. Install prerequisites (code generator for running Python snippets):<br>
    ```
    sudo pip3 install cogapp
    ```
4. Create short path for the workshop folder

  ```
  export workshop_dir=/opt/intel/workshop/smart-video-workshop
  
  ```
5. Change ownership of the workshop directory to the current user
Note: replace the usernames below with your user account name

	sudo chown username.username -R /opt/intel/workshop/

### Create the TensorFlow* model (weights, graphs, checkpoints)
We create a simple model with a custom cosh layer. The weights are random and untrained, however sufficient for demonstrating Custom Layer conversion.

	 cd $workshop_dir/custom-layer/create_tf_model

	 mkdir -p tf_model
	 
	 chmod +x build_cosh_model.py

    ./build_cosh_model.py tf_model


### Generate template files using the Extension Generator:

   We're using `$workshop_dir/custom-layer/extgen_output/` as the target extension path:<br><br>
   This will create templates that will be partially replaced by Python* and C++ code for executing the layer.


	mkdir -p $workshop_dir/custom-layer/extgen_output/

    python3 /opt/intel/openvino/deployment_tools/tools/extension_generator/extgen.py new --mo-tf-ext --mo-op --ie-cpu-ext --ie-gpu-ext --output_dir=$workshop_dir/custom-layer/extgen_output/


   Answer the Model Optimizer extension generator questions as follows:
   
   
    Please enter layer name:
    [Cosh]

    Do you want to automatically parse all parameters from model file...
    [n]

    Please enter all parameters in format...
    When you finish please enter 'q'
    [q]

    Do you want to change any answer (y/n) ?
    [n]

    Please enter operation name:
    [Cosh]

    Please input all attributes that should be output in IR...
    ...
    When you finish enter 'q'
    [q]

    Please input all internal attributes for your operation...
    ...
    When you finish enter 'q'
    [q]

    Does your operation change shape? (y/n)
    [n]

    Do you want to change any answer (y/n) ?
    [n]

    Please enter operation name:
    [Cosh]

    Please enter all parameters in format...
    ...
    When you finish please enter 'q'
    [q]

    Do you want to change any answer (y/n) ?
    [n]
    ```

   The output will be similar to the following:

<br>

![image of extgen output](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/custom-layer/extgen_output.png "extgen output")

<br>


### Register custom layer for the Model Optimizer

 Add Custom (cosh) Python Layers:
   Copy to the Model Optimizer Ops Directory:<br>
   This allows the Model Optimizer to find the Python implementation of cosh.

    sudo cp $SW/custom-layer/cosh.py /opt/intel/openvino/deployment_tools/model_optimizer/mo/ops/


#### Generate IR with custom layer using Model Optimizer
  We run the Model Optimizer for TensorFlow to convert and optimize the new model for the Intel® Distribution of OpenVINO™ toolkit. We explicitly set the batch to 1 because the model has an input dim of "-1". TensorFlow allows "-1" as a variable indicating "to be filled in later", but the Model Optimizer requires explicit information for the optimization process. The output is the full name of the final output layer.<br><br>

	cd tf_model
	mkdir -p $workshop_dir/custom-layer/cl_ext_cosh

    mo_tf.py --input_meta_graph model.ckpt.meta --batch 1 --output "ModCosh/Activation_8/softmax_output" --extensions $workshop_dir/custom-layer/extgen_output/user_mo_extensions --output_dir $workshop_dir/custom-layer/create_tf_model/tf_model

### Inference Engine custom layer implementation for the Intel® CPU

1. Copy CPU and GPU source code to the Model Optimizer extensions directory:<br>
   This will be used for building a back-end library for applications that implement cosh.<br><br>
    ```
    cp $workshop_dir/custom-layer/ext_cosh.cpp $workshop_dir/custom-layer/extgen_output/user_ie_extensions/cpu/
    ```



10. Compile the C++ extension library:<br>
   Here we're building the back-end C++ library to be used by the Inference Engine for executing the cosh layer.<br><br>
    ```
	cd $workshop_dir/custom-layer/extgen_output/user_ie_extensions/cpu
    ```
    ```
	cp $workshop_dir/custom-layer/CMakeLists.txt .
    ```
    ```
	mkdir -p build && cd build
    ```
    ```
	cmake ..
    ```
    ```
	make -j$(nproc)
    ```
    <br>

    ```
	cp libcosh_cpu_extension.so $workshop_dir/custom-layer/cl_ext_cosh
    ```

11. Test your results:<br>

    <b>Using a C++ Sample:</b><br>
    ```
    ~/inference_engine_samples_build/intel64/Release/classification_sample -i /opt/intel/openvino/deployment_tools/demo/car.png -m $workshop_dir/custom-layer/create_tf_model/tf_model/model.ckpt.xml -d CPU -l $workshop_dir/custom-layer/cl_ext_cosh/libcosh_cpu_extension.so
    ```
    <br><b>Using a Python Sample:</b><br>

    Prep: Install the OpenCV library and copy an appropriate sample to your home directory for ease of use:<br>
    ```
    sudo pip3 install opencv-python
    ```

    <br>Try running the Python Sample without including the cosh extension library. You should see the error describing unsupported Cosh operation.
    ```
    python3 /opt/intel/openvino/deployment_tools/inference_engine/samples/python_samples/classification_sample/classification_sample.py -i /opt/intel/openvino/deployment_tools/demo/car.png  -m $workshop_dir/custom-layer/create_tf_model/tf_model/model.ckpt.xml -d CPU
    ```

    <br>Now run the command with the cosh extension library:<br>
    ```
    python3 /opt/intel/openvino/deployment_tools/inference_engine/samples/python_samples/classification_sample/classification_sample.py -i /opt/intel/openvino/deployment_tools/demo/car.png  -m $workshop_dir/custom-layer/create_tf_model/tf_model/model.ckpt.xml -l $workshop_dir/custom-layer/cl_ext_cosh/libcosh_cpu_extension.so -d CPU
    ```
### Inference Engine custom layer implementation for the Intel® integrated GPU

1. Copy GPU source code for cosh custom kernel .cl and .xml files to the cldnn library folder.<br>
    ```
    sudo cp $workshop_dir/custom-layer/cosh_kernel* /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/cldnn_global_custom_kernels/
    ```
2. Test your results

  <b>Using a C++ Sample:</b><br>
  ```
  ~/inference_engine_samples_build/intel64/Release/classification_sample -i /opt/intel/openvino/deployment_tools/demo/car.png -m $workshop_dir/custom-layer/create_tf_model/tf_model/model.ckpt.xml -d GPU -c /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/cldnn_global_custom_kernels/cosh_kernel.xml
  ```


Thank you for following this tutorial. Your feedback answering this brief survey will help us to improve it:
[Intel Custom Layer Survey](https://intelemployee.az1.qualtrics.com/jfe/form/SV_1ZjOKaEIQUM5FpX)
