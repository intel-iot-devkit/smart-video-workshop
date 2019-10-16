OPENVINO_FLAGS=-I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/include \
            -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/include/cpp/ \
	    -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/samples/common/ \
	    -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/src/extension/ \
	    -I$(INTEL_CVSDK_DIR)/opencv/include \
	    -L$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/lib/intel64 \
	    -L$(INTEL_CVSDK_DIR)/opencv/lib \
            -L/opt/intel/openvino/deployment_tools/inference_engine/samples/build/intel64/Release/lib/ \
	    -lgflags -linference_engine -ldl -lpthread -lcpu_extension_avx2 \
            -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui -lopencv_videoio -lopencv_video -lgflags 

all: tutorial1 ROI_writer


tutorial1: main.cpp
	g++ -fPIE -O3 -fopenmp -o tutorial1 --std=c++11 main.cpp $(OPENVINO_FLAGS) 


#	g++ -fPIE -O3 -fopenmp -o tutorial1 --std=c++11 main.cpp -I. \
#            -I$(INTEL_CVSDK_DIR)/opencv/include/ \
#            -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/include/ \
#            -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/include/cpp \
#            -L$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/lib/ubuntu_16.04/intel64 -linference_engine -ldl -lpthread -lcpu_extension \
#            -L/opt/intel/computer_vision_sdk/opencv/lib \
#            -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui -lopencv_videoio \
#            -lopencv_video -lgflags \
#            -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/samples/ \
#            -I./ \
#            -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/samples/common/format_reader/ \
#            -I$(INTEL_CVSDK_DIR)/opencv/include \
#            -I/usr/local/include \
#            -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/samples/thirdparty/gflags/include \
#            -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/include -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/include/cpp -I$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/samples/extension -L$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/bin/intel64/Release/lib -L$(INTEL_CVSDK_DIR)/deployment_tools/inference_engine/lib/ubuntu_16.04/intel64 -L/opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release/lib -L$(INTEL_CVSDK_DIR)/opencv/lib -ldl -linference_engine -lopencv_highgui -lopencv_core -lopencv_imgproc -lopencv_videoio -lgflags_nothreads -lopencv_imgcodecs -lopencv_imgcodecs -lcpu_extension

ROI_writer: ROI_writer.cpp 
	g++ -fPIE -O0 -fopenmp -g -o ROI_writer --std=c++11 ROI_writer.cpp -I. \
            -I/opt/intel/openvino/opencv/include/ \
            -L/opt/intel/openvino/opencv/lib -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui -lopencv_videoio -lopencv_video -lgflags

