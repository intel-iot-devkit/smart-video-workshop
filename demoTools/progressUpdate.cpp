#include <string>
#include <iostream>
#include <sstream>
#include <fstream>
#include <time.h>
#include <omp.h>
#include <stdlib.h>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc_c.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/video/video.hpp>
#include <vector>
#include <algorithm> 
#include <assert.h>

using namespace std;
using namespace cv;

void progressUpdate(string file_name, double time_diff, int frame_count, int video_len){

	ofstream progress;
	progress.open(file_name);
	double cur_progress = 100*frame_count/video_len;
	double remaining_time = (time_diff/frame_count)*(video_len-frame_count);
	double  estimated_time = (time_diff/frame_count)*video_len;
	progress<<setprecision(1)<<fixed<<cur_progress<<'\n';
	progress<<setprecision(1)<<fixed<<remaining_time<<'\n';
	progress<<setprecision(1)<<fixed<<estimated_time<<'\n';
	progress.close();
}
