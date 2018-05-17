This example shows how to use hetero plugin to define preferences to run different network layers on different hardware types. 

#### 1. Navigate to the tutorial sample directory

	cd $SV/object-detection/
  
#### 2. Run the security barrier object detection sample with hetero plugin 

##### a) Prioritizing running on GPU first.

	./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:GPU,CPU
    

##### a) Prioritizing running on CPU first.

     ./tutorial1 -i $SV/object-detection/Cars\ -\ 1900.mp4 -m $SV/object-detection/mobilenet-ssd/FP32/mobilenet-ssd.xml -d HETERO:CPU,GPU 
     
    

