
# Movidius Neural Compute Stick (NCS)

Let's see how Intel CV-SDK provides hardware abstraction to run the security barrier application which we built in previous modules on Movidius NCS. 

#### Connect Movidius NCS to your development laptop
<br>

![image of Movidius NCS to computer](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/Movidius.png "connected NCS")

<br>

#### Run the security barrier application on Movidius Neural Compute Stick (NCS)
Set target hardware as Movidius NCS with
```
-d MYRYAD
```
```
./security_barrier_camera_sample -d MYRYAD -i "/opt/intel/computer_vision_sdk_2018.0.211/deployment_tools/demo/cars-on-highway-1409.mp4" -m "/object-detection/squeezenet_SSD.xml -pc" 
```
You will get following error as Movidius NCS supports only FP16 format. 
<br>

![image of Movidius NCS error for FP32 model](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/NCSerror.png)

<br>

The Model optimizer by default generate FP32 IR files if the data type is not particularly specified.

Let's run the model optimizer to get IR files in FP16 format suitable for the Movidius NCS. 
  
    mkdir FP16
	  python3 mo_caffe.py --input_model /object-detection/model/squeezenet_SSD.caffemodel --data_type FP16 -o /object-detection/FP16

Check if the .xml and .bin files are created in folder FP16. 

Now run the security barrier application with these new IR files.

    ./security_barrier_camera_sample -d MYRYAD -i "/opt/intel/computer_vision_sdk_2018.0.211/deployment_tools/demo/cars-on-highway-1409.mp4" -m "/object-detection/FP16/squeezenet_SSD.xml -pc" 
