/*
 * Copyright (c) 2018 Intel Corporation.
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include <deque>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/video/video.hpp>
#include <omp.h>
#include <gflags/gflags.h>
#include <common_labelinfo.hpp>

using namespace std;
using namespace cv;

static const char help_message[] = "Print a usage message";
static const char input_message[] = "Required. Path to input video file";
static const char ROIfile_message[] = "Path to ROI file.";
static const char batchnum_message[] = "Batch # to display.";
static const char labels_message[] = "class labels file.";
static const char output_message[] = "Output file path.";
static const char resolution_message[] = "(double) factor to cut reolution by; 2. will cut the resolution by half.";
static const char keepframe_message[] = "Writer will keep every <skipframe> frames.";

DEFINE_bool(h, false, help_message);
DEFINE_string(i, "", input_message);
DEFINE_string(ROIfile, "ROIs.txt", ROIfile_message);
DEFINE_string(l, "", labels_message);
DEFINE_int32(b, 0, batchnum_message);
DEFINE_string(o, "output.mp4", output_message);
DEFINE_double(r, 1.0, resolution_message);
DEFINE_int32(k, 1, keepframe_message);

void showUsage()
{
    std::cout << std::endl;
    std::cout << "[usage]" << std::endl;
    std::cout << "\tROIviewer [option]" << std::endl;
    std::cout << "\toptions:" << std::endl;
    std::cout << std::endl;
    std::cout << "\t\t-h              " << help_message << std::endl;
    std::cout << "\t\t-i <path>       " << input_message << std::endl;
    std::cout << "\t\t-ROIfile <path> " << ROIfile_message << std::endl;
    std::cout << "\t\t-b #            " << batchnum_message << std::endl;
    std::cout << "\t\t-l <path>       " << labels_message << std::endl;
    std::cout << "\t\t-o <filename>       " << output_message << std::endl;
    std::cout << "\t\t-r <res>       " << resolution_message << std::endl;
    std::cout << "\t\t-k <keepframe>       " << keepframe_message << std::endl;
}

typedef struct {
    int framenum;
    double labelnum;
    double confidence;
    double xmin;
    double ymin;
    double xmax;
    double ymax;
}  ROI_data_type;


int main(int argc,char **argv)
{
    gflags::ParseCommandLineNonHelpFlags(&argc, &argv, true);

    if (FLAGS_h) {
        showUsage();
        return 1;
    }

    if ((FLAGS_i.empty())||(FLAGS_ROIfile.empty())) {
        std::cout << "ERROR: input and ROI file required" << std::endl;
        showUsage();
        return 1;
    }

    int batch=FLAGS_b;
    deque<ROI_data_type> ROIs;
    FILE *fin=fopen(FLAGS_ROIfile.c_str(),"r");
    if(!fin)  // check if we succeeded
    {
        cout << "could not open ROI file" << std::endl;
        return -1;
    }
    ROI_data_type R;
    int batchnum;
    while (!feof(fin))
    {
        fscanf(fin,"%d %d %lf %lf %lf %lf %lf %lf\n",
               &batchnum,
               &R.framenum,&R.labelnum,&R.confidence,&R.xmin,&R.ymin,&R.xmax,&R.ymax);
        if (batchnum==batch) ROIs.push_back(R);
    };

    printf("opening %s batchnum %d\n",FLAGS_i.c_str(),FLAGS_b);

    VideoCapture cap(FLAGS_i.c_str()); // open the input file
    if(!cap.isOpened())  // check if we succeeded
    {
        cout << "could not open input video file" << std::endl;
        return -1;
    }

    Mat frame;
    int framenum=0;


    if (ROIs.size()>0)  R=ROIs.at(0);
    else {
        cout << "empty ROI file" << endl;
        exit(1);
    }



    if (FLAGS_k < 1) {
        cout << "-k must be 1 or greter" << endl;
        exit(1);
    }

    std::vector<labelinfo> labeldata = readlabels(FLAGS_l,"");

    Size S = Size((int) cap.get(CAP_PROP_FRAME_WIDTH)/FLAGS_r,    // Acquire input size
                  (int) cap.get(CAP_PROP_FRAME_HEIGHT)/FLAGS_r);
    float o_fps = cap.get(CAP_PROP_FPS)/FLAGS_k;
    VideoWriter outputVideo(FLAGS_o+"/output.mp4", 0x00000021, o_fps, S, true);
    if (!outputVideo.isOpened())
    {
        cout  << "Could not open the output video for write: " << FLAGS_o+"/output.mp4" << endl;
        return -1;
    }

    std::string job_id = getenv("PBS_JOBID");
    std::string progress_data = FLAGS_o+"/v_progress_"+job_id+".txt";
    std::ofstream progress;
    size_t length = (size_t) cap.get(cv::CAP_PROP_FRAME_COUNT);
    double t1 = omp_get_wtime();

    for(;;)
    {
        cap >> frame; // get a new frame
        if (frame.empty()) break;
        int ncols=frame.cols;
        int nrows=frame.rows;

	//Progress Indicator
	if (framenum%10 == 0  || framenum%length == 0){
        	double t2 = omp_get_wtime()-t1;
    		progress.open(progress_data);
        	std::string cur_progress = std::to_string(int(100*framenum/length))+'\n';
        	std::string remaining_time = std::to_string(int((t2/framenum)*(length-framenum)))+'\n';
        	std::string estimated_time = std::to_string(int((t2/framenum)*length))+'\n';
        	progress<<cur_progress;
        	progress<<remaining_time;
        	progress<<estimated_time;

                progress.flush();
	        progress.close();
        }


        //catch up with current frame
        while (R.framenum<framenum) {
            if (ROIs.size()>1)
            {
                ROIs.pop_front();
                R=ROIs.at(0);
            }
            else break;
        }

        while (R.framenum==framenum)
        {

            float xmin       = R.xmin * (float)ncols;
            float ymin       = R.ymin * (float)nrows;
            float xmax       = R.xmax * (float)ncols;
            float ymax       = R.ymax * (float)nrows;

            rectangle(frame,
                      Point((int)xmin, (int)ymin),
                      Point((int)xmax, (int)ymax), Scalar(0, 255, 0),
                      4, LINE_AA,0);


            char tmplabel[32];
	    memset(tmplabel,0,32);
            if (labeldata.size()==0) 
            {
            	sprintf(tmplabel,"label %d: %d%%",(int)R.labelnum,(int)(R.confidence*100.0));
            } 
            else
            {
		sprintf(tmplabel,"%s: %d%%",labeldata.at(((int)R.labelnum)).label.c_str(),(int)(R.confidence*100.0));
            }

            rectangle(frame,
                      Point((int)xmin, (int)ymin+32),
                      Point((int)xmax, (int)ymin), Scalar(155, 155, 155),
                      FILLED, LINE_8,0);
            putText(frame,tmplabel,
                    Point((int)xmin, (int)ymin+24), FONT_HERSHEY_COMPLEX, 1.1,
                    Scalar(0, 0, 0),3);


            if (ROIs.size()>1)
            {
                ROIs.pop_front();
                R=ROIs.at(0);
            }
            else break;
        }
        //imshow("video", frame);
        if(framenum % FLAGS_k == 0) {
          resize(frame, frame, S);
          outputVideo << frame;
        }
        cout << "frame: " << framenum+1 << "\r";
        fflush(stdout);
        framenum++;
        if (ROIs.size()<=1) break;
    }


    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}
