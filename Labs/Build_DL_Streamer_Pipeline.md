# Build a Media Analytic Pipeline with DL Streamer
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

	cd /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader/
	python3 downloader.py --name person-vehicle-bike-detection-crossroad-0078,person-attributes-recognition-crossroad-0230,vehicle-attributes-recognition-barrier-0039

#### 4. Add the DL Streamer element "gvadetect" to the pipeline

	gst-launch-1.0 \
	filesrc location=/opt/intel/workshop/person-bicycle-car-detection.mp4 ! \
	decodebin ! \
	videoconvert ! \
	video/x-raw,format=BGRx ! \
	gvadetect model=person-vehicle-bike-detection-crossroad-0078.xml \
	model-proc=person-vehicle-bike-detection-crossroad-0078.json \
	inference-interval=10 threshold=0.6 device=CPU ! queue ! \
	videoconvert ! fpsdisplaysink video-sink=xvimagesink sync=true
