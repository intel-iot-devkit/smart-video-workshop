
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
