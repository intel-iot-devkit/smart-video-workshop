all:
	g++ -fPIE -O3 -o tutorial1 --std=c++11 main.cpp -I. \
            -I/opt/intel/computer_vision_sdk/opencv/include/ \
            -I/opt/intel/computer_vision_sdk/deployment_tools/inference_engine/include/ \
            -I/opt/intel/computer_vision_sdk/deployment_tools/inference_engine/include/cpp \
            -L/opt/intel/computer_vision_sdk/deployment_tools/inference_engine/lib/ubuntu_16.04/intel64 -linference_engine -ldl -lpthread -lcpu_extension \
            -L/opt/intel/computer_vision_sdk/opencv/lib -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui -lopencv_videoio -lopencv_video -lgflags
