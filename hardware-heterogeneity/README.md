This example shows to use hetero plugin to define preferences to run diffrerent network layers on different hardware types. 

#### 1. Navigate to the tutorial sample directory

	cd $SV/object-detection/
  
#### 2. Run the security barrier object detection sample with hetero plugin 

##### a) Prioritizing running on GPU first.

	./tutorial1 -i $SV/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/sqeeznet_ssd/squeezenet_ssd.xml -d HETERO:GPU,CPU
    

##### a) Prioritizing running on CPU first.

     ../tutorial1 -i $SV/object-detection/models/cars_1920x1080.h264 -m $SV/object-detection/models/sqeeznet_ssd/squeezenet_ssd.xml -d HETERO:CPU,GPU 
     
    

