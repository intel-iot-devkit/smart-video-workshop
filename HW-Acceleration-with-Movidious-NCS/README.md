
# Intel® Movidius™ Neural Compute Stick (NCS)

This lab shows how Intel OpenVINO™ toolkit provides hardware abstraction to run the sample object detection application which was built in previous modules on Movidius™ NCS. 

#### Connect Movidius™ NCS to your development laptop
<br>

![image of Movidius NCS to computer](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/Movidius.png "connected NCS")

<br>

#### System check
First make sure the USB rules are set up.

	cat <<EOF > 97-usbboot.rules
	SUBSYSTEM=="usb", ATTRS{idProduct}=="2150", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
	SUBSYSTEM=="usb", ATTRS{idProduct}=="f63b", ATTRS{idVendor}=="03e7", GROUP="users", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
	EOF
	
	sudo cp 97-usbboot.rules /etc/udev/rules.d/
	
	sudo udevadm control --reload-rules
	
	sudo udevadm trigger
	
	sudo ldconfig

Then check if the device is visible with lsusb.
	
	lsusb
	
The output will be

	Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
	Bus 001 Device 015: ID 03e7:2150  

Here ID 03e7:2150 without a description string is the Movidius device.

#### Setup a short path for the workshop directory

	export SV=/opt/intel/workshop/smart-video-workshop/

#### Run the sample application on Movidius™ Neural Compute Stick (NCS)
Set target hardware as Movidius™ NCS with **-d MYRIAD**
  
	cd $SV/object-detection/

```
 ./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d MYRIAD
```
You will get following error as Movidius™ NCS supports only FP16 format. 
<br>

![image of Movidius NCS error for FP32 model](https://github.com/intel-iot-devkit/smart-video-workshop/blob/master/images/NCSerror.png)

<br>

The Model Optimizer by default generate FP32 IR files if the data type is not particularly specified.

Let's run the Model Optimizer to get IR files in FP16 format suitable for the Movidius™ NCS. 
  
    cd $SV/object-detection/mobilenet-ssd
    mkdir FP16
    
    cd /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer
	
	python3 mo_caffe.py --input_model /opt/intel/computer_vision_sdk/deployment_tools/model_downloader/object_detection/common/mobilenet-ssd/caffe/mobilenet-ssd.caffemodel -o $SV/object-detection/mobilenet-ssd/FP16 --scale 256 --mean_values [127,127,127] --data_type FP16

Check if the .xml and .bin files are created in folder $SV/object-detection/SSD300/FP16. 
	 
	 cd $SV/object-detection/mobilenet-ssd/FP16
	 ls
	
Now run the example application with these new IR files.

     cd $SV/object-detection/
    ./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP16/mobilenet-ssd.xml -d MYRIAD
