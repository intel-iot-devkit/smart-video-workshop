# Build a Vehicle & Pedestrian Tracking Media Analytic Pipeline with DL Streamer
In this lab, we will build a Media Analyuse step by step using gst-launch-1.0 in the command line environment.

#### 1. Download the video we are going to run the inference on

	cd /opt/intel/workshop
	wget https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4
	
#### 2. Build a Media Processing Pipeline
After running below command, you will see the downloaded video displayed on the screen.

	gst-launch-1.0 \
	filesrc location=/opt/intel/workshop/person-bicycle-car-detection.mp4 ! \
	decodebin ! \
	videoconvert ! \
	video/x-raw,format=BGRx ! \
	videoconvert ! fpsdisplaysink video-sink=xvimagesink sync=true

#### 3. Download the pre-trained models we are going use to build the Media Analytic Pipeline

	cd /opt/intel/openvino_2021/deployment_tools/open_model_zoo/tools/downloader/
	python3 downloader.py --name person-vehicle-bike-detection-crossroad-0078,person-attributes-recognition-crossroad-0230,vehicle-attributes-recognition-barrier-0039

#### 4. Add the DL Streamer element "gvadetect" to the pipeline to detect vehicle and pedestrian and element "gvawatermark" to show the bounding box
In addition to provide the path to the model, a path to JSON file with description of input/output layers pre-processing/post-processing flags is also necessary for **gvadetect** element. In this lab, we can find the JSON file in the DL Stremer sample directory. Also, we can setup the inference interval, threshold for the model, and which device we'd like this model to run on.

	gst-launch-1.0 \
	filesrc location=/opt/intel/workshop/person-bicycle-car-detection.mp4 ! \
	decodebin ! \
	videoconvert ! \
	video/x-raw,format=BGRx ! \
	gvadetect model=/opt/intel/openvino_2021/deployment_tools/open_model_zoo/tools/downloader/intel/person-vehicle-bike-detection-crossroad-0078/FP32/person-vehicle-bike-detection-crossroad-0078.xml \
	model-proc=/opt/intel/openvino_2021/data_processing/dl_streamer/samples/gst_launch/vehicle_pedestrian_tracking/model_proc/person-vehicle-bike-detection-crossroad-0078.json \
	inference-interval=5 threshold=0.6 device=CPU ! queue ! \
	gvawatermark ! \
	videoconvert ! fpsdisplaysink video-sink=xvimagesink sync=true

#### 5. Add the DL Streamer element "gvatrack" to the pipeline, so that even we don't inference every frame, we still can see the continous bounding boxes around the detected objects

	gst-launch-1.0 \
	filesrc location=/opt/intel/workshop/person-bicycle-car-detection.mp4 ! \
	decodebin ! \
	videoconvert ! \
	video/x-raw,format=BGRx ! \
	gvadetect model=/opt/intel/openvino_2021/deployment_tools/open_model_zoo/tools/downloader/intel/person-vehicle-bike-detection-crossroad-0078/FP32/person-vehicle-bike-detection-crossroad-0078.xml \
	model-proc=/opt/intel/openvino_2021/data_processing/dl_streamer/samples/gst_launch/vehicle_pedestrian_tracking/model_proc/person-vehicle-bike-detection-crossroad-0078.json \
	inference-interval=5 threshold=0.6 device=CPU ! queue ! \
	gvatrack tracking-type="short-term" ! queue ! \
	gvawatermark ! \
	videoconvert ! fpsdisplaysink video-sink=xvimagesink sync=true

#### 6. Add two DL Streamer elements "gvaclasify" to the pipelie, to recongnize the attributes of detected vehciles and pedestrians
Same as the "gvadetect", we will need to provide path to model and json file, setup the interval frames, threshould and choose device to run the inference.

	gst-launch-1.0 \
	filesrc location=/opt/intel/workshop/person-bicycle-car-detection.mp4 ! \
	decodebin ! \
	videoconvert ! \
	video/x-raw,format=BGRx ! \
	gvadetect model=/opt/intel/openvino_2021/deployment_tools/open_model_zoo/tools/downloader/intel/person-vehicle-bike-detection-crossroad-0078/FP32/person-vehicle-bike-detection-crossroad-0078.xml \
	model-proc=/opt/intel/openvino_2021/data_processing/dl_streamer/samples/gst_launch/vehicle_pedestrian_tracking/model_proc/person-vehicle-bike-detection-crossroad-0078.json \
	inference-interval=5 threshold=0.6 device=CPU ! queue ! \
	gvatrack tracking-type="short-term" ! queue ! \
	gvaclassify model= /opt/intel/openvino_2021/deployment_tools/open_model_zoo/tools/downloader/intel/person-attributes-recognition-crossroad-0230/FP32/person-attributes-recognition-crossroad-0230.xml \
	model-proc= /opt/intel/openvino_2021/data_processing/dl_streamer/samples/gst_launch/vehicle_pedestrian_tracking/model_proc/person-attributes-recognition-crossroad-0230.json \
	reclassify-interval=10 device=CPU object-class=person ! queue ! \
 	gvaclassify model= /opt/intel/openvino_2021/deployment_tools/open_model_zoo/tools/downloader/intel/vehicle-attributes-recognition-barrier-0039/FP32/vehicle-attributes-recognition-barrier-0039.xml \
	model-proc= /opt/intel/openvino_2021/data_processing/dl_streamer/samples/gst_launch/vehicle_pedestrian_tracking/model_proc/vehicle-attributes-recognition-barrier-0039.json \
	reclassify-interval=10 device=CPU object-class=vehicle ! queue ! \
	gvawatermark ! \
	videoconvert ! fpsdisplaysink video-sink=xvimagesink sync=true

## Further Reading
To learn more about Deep Learning Streamer, please refer to this GitHub repo - [DL Streamer repository](https://github.com/opencv/gst-video-analytics), or [DL Streamer Wiki](https://github.com/opencv/gst-video-analytics/wiki), to explore more DL Streamer examples, check the [DL Streamer Samples](https://docs.openvinotoolkit.org/latest/gst_samples_README.html) session from OpenVINO documentation.
