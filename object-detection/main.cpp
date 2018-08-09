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


#include <string>
#include <chrono>
#include <gflags/gflags.h>

#include <ie_device.hpp>
#include <ie_plugin_config.hpp>
#include <ie_plugin_dispatcher.hpp>
#include <ie_plugin_ptr.hpp>
#include <inference_engine.hpp>
#include <ie_plugin_cpp.hpp>
#include <ie_extension.h>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/video/video.hpp>

#include <opencv2/opencv.hpp>
#include <inference_engine.hpp>
#include <ie_plugin_config.hpp>



using namespace std;
using namespace cv;
using namespace InferenceEngine::details;
using namespace InferenceEngine;


typedef enum {
    CLASSIFICATION_MODE,
    SSD_MODE
} output_mode_type;



static const char help_message[]   = "Print a usage message";
static const char input_message[]  = "Required. Path to input video file";
static const char model_message[]  = "Required. Path to model file.";
static const char batch_message[]  = "Batch size.";
static const char thresh_message[] = "Threshold (0-1: .5=50%)";
static const char target_device_message[] = "Infer target device (CPU or GPU or MYRIAD)";
static const char maxframes_message[] = "maximum frames to process";


DEFINE_bool(h, false, help_message);
DEFINE_string(i, "", input_message);
DEFINE_string(m, "", model_message);
DEFINE_int32(b, 1, batch_message);
DEFINE_int32(fr,256, maxframes_message);
DEFINE_double(thresh, 0.4, thresh_message);
DEFINE_string(d, "CPU", target_device_message);

void showUsage()
{
    std::cout << std::endl;
    std::cout << "[usage]" << std::endl;
    std::cout << "\ttutorial1 [option]" << std::endl;
    std::cout << "\toptions:" << std::endl;
    std::cout << std::endl;
    std::cout << "\t\t-h              " << help_message << std::endl;
    std::cout << "\t\t-i <path>       " << input_message << std::endl;
    std::cout << "\t\t-model <path>   " << model_message << std::endl;
    std::cout << "\t\t-b #            " << batch_message << std::endl;
    std::cout << "\t\t-thresh #       " << thresh_message << std::endl;
    std::cout << "\t\t-d <device>     " << target_device_message << std::endl;
    std::cout << "\t\t-fr #           " << maxframes_message << std::endl;
}


int main(int argc, char *argv[]) {

    chrono::high_resolution_clock::time_point tmStart, tmEnd;
    chrono::high_resolution_clock::time_point time1,time2;
    chrono::duration<double> diff;

    deque<double> preprocess_times;
    deque<double> infer_times;
    deque<double> postprocess_times;

    try {
        gflags::ParseCommandLineNonHelpFlags(&argc, &argv, true);

        if (FLAGS_h) {
            showUsage();
            return 1;
        }

        if ((FLAGS_i.empty())||(FLAGS_m.empty())) {
            std::cout << "ERROR: input and model file required" << std::endl;
            showUsage();
            return 1;
        }

        bool badDevice = FLAGS_d.compare("CPU") && FLAGS_d.compare("FPGA") && FLAGS_d.compare("GPU") && FLAGS_d.compare("MYRIAD") && (FLAGS_d.find("HETERO")==string::npos);
        if (badDevice)
        {
            std::cout << "ERROR: bad device.  Must be CPU,GPU,MYRIAD,FPGA,or HETERO" << std::endl;
            showUsage();
            return 1;
        }


        FILE *ROIfile=fopen("ROIs.txt","w"); // output stored here, view with ROIviewer

        /** ---------------------1. Load Plugin ---------------------------------------------------------------------**/
        InferenceEngine::PluginDispatcher dispatcher({""});
        InferenceEngine::InferenceEnginePluginPtr _plugin(dispatcher.getPluginByDevice(FLAGS_d));
        InferencePlugin plugin(_plugin);


        //in some cases it might be possible to skip this step, but most models use these extensions to run on CPU
        if (FLAGS_d.find("CPU")!=string::npos)
        {
            string s_ext_plugin = "/opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release/lib/libcpu_extension.so";
            auto extension_ptr = make_so_pointer<InferenceEngine::IExtension>(s_ext_plugin);
            plugin.AddExtension(extension_ptr);
        }

        /** ---------------------2. Read IR Generated by ModelOptimizer (.xml and .bin files) -----------------------**/
        CNNNetReader network_reader;
        network_reader.ReadNetwork(FLAGS_m);
        network_reader.ReadWeights(FLAGS_m.substr(0, FLAGS_m.size() - 4) + ".bin");
        CNNNetwork network = network_reader.getNetwork();


        // --------------------
        // Set batch size
        // --------------------
        network.setBatchSize(FLAGS_b);
        size_t batchSize = network.getBatchSize();


        /** ---------------------3. Request/set IO ---------------------------------------------**/

        /** Get information about topology inputs **/
        InferenceEngine::InputsDataMap input_info(network.getInputsInfo());
        InferenceEngine::SizeVector inputDims;
        for (auto &item : input_info) {
            auto input_data = item.second;
            input_data->setPrecision(Precision::U8);
            input_data->setLayout(Layout::NCHW);
            inputDims=input_data->getDims();
        }
        cout << "inputDims=";
        for (int i=0; i<inputDims.size(); i++) {
            cout << (int)inputDims[i] << " ";
        }
        cout << endl;
        const int infer_width=inputDims[0];
        const int infer_height=inputDims[1];
        const int num_channels=inputDims[2];
        const int channel_size=infer_width*infer_height;
        const int full_image_size=channel_size*num_channels;


        /** Get information about topology outputs **/
        output_mode_type output_mode;
        InferenceEngine::OutputsDataMap output_info(network.getOutputsInfo());
        InferenceEngine::SizeVector outputDims;
        for (auto &item : output_info) {
            auto output_data = item.second;
            output_data->setPrecision(Precision::FP32);
            output_data->setLayout(Layout::NCHW);
            outputDims=output_data->getDims();
        }
        cout << "outputDims=";
        for (int i=0; i<outputDims.size(); i++) {
            cout << (int)outputDims[i] << " ";
        }
        cout << endl;
        if (outputDims[3]>1)
        {
            cout << "SSD Mode" << endl;
            output_mode=SSD_MODE;
        }
        else
        {
            cout << "Single Classification Mode" << endl;
            output_mode=CLASSIFICATION_MODE;
        }
        const int output_data_size=outputDims[1]*outputDims[2]*outputDims[3];
        //outputDims[0] is batchSize

        /** ---------------------4. Loading model to the plugin -----------------------------------------------------**/
        auto executable_network = plugin.LoadNetwork(network, {});

        /** ---------------------5. Create infer request ------------------------------------------------------------**/
        auto async_infer_request = executable_network.CreateInferRequest();


        /** ---------------------6. Other prep for main loop  ------------------------------------------------------------**/
        //open video capture
        VideoCapture cap(FLAGS_i);
        if (!cap.isOpened())   // check if VideoCapture init successful
        {
            cout << "Could not open input file" << endl;
            return 1;
        }

        Mat frame,frameInfer;

        // get the input blob buffer pointer location
        unsigned char *input_buffer;
        unsigned char *input_buffer_current_image;
        for (auto &item : input_info) {
            auto input_name = item.first;
            auto input_data = item.second;
            auto input = async_infer_request.GetBlob(input_name);
            input_buffer = input->buffer().as<PrecisionTrait<Precision::U8>::value_type *>();
        }

        // get the output blob pointer location
        float *output_buffer;
        float *output_buffer_current_image;
        for (auto &item : output_info) {
            auto output_name = item.first;
            auto output = async_infer_request.GetBlob(output_name);
            output_buffer = output->buffer().as<PrecisionTrait<Precision::FP32>::value_type *>();
        }

        int framenum=0;
        bool process_more_frames=true;
        int frames_in_output=batchSize;

        /** ------------------------------------------------------------------**/
        /** ---------           MAIN LOOP                        -------------**/
        /** ------------------------------------------------------------------**/
        do {

            /** ---------------------7. Prepare input -------------------------------------------------------------------**/

	    time1 = chrono::high_resolution_clock::now();
            for (int mb=0; mb < batchSize; mb++)
            {
                
                input_buffer_current_image=input_buffer+(full_image_size*mb);
                cap.read(frame);
                if ( (!frame.data) || (framenum>=FLAGS_fr) ) {
                    process_more_frames=false;
                    frames_in_output=mb;
                }
                if (!process_more_frames) break;

                //convert image to blob
                cv::resize(frame, frameInfer, cv::Size(infer_width, infer_height));

                /** Fill input tensor with planes. First b channel, then g and r channels **/
                for (size_t pixelnum = 0; pixelnum < channel_size; ++pixelnum) {
                    for (size_t ch = 0; ch < num_channels; ++ch) {
                        input_buffer_current_image[(ch * channel_size) + pixelnum] = frameInfer.at<cv::Vec3b>(pixelnum)[ch];
                    }
                }
            }
            time2 = chrono::high_resolution_clock::now();
            diff = time2-time1;
	    


            if (process_more_frames)
            {
		preprocess_times.push_back(diff.count()*1000.0);

                /** ---------------------7. Do inference --------------------------------------------------------------------**/
		time1 = chrono::high_resolution_clock::now();
                async_infer_request.StartAsync();
                async_infer_request.Wait(IInferRequest::WaitMode::RESULT_READY);
		time2 = chrono::high_resolution_clock::now();
                diff = time2-time1;
		infer_times.push_back(diff.count()*1000.0);

                /** ---------------------8. Process output ------------------------------------------------------------------**/

                time1 = chrono::high_resolution_clock::now();
                for (int mb=0; mb < frames_in_output; mb++)
                {

                    if (framenum>=FLAGS_fr) {
                        process_more_frames=false;
                        break;
                    }
                    output_buffer_current_image=output_buffer+(output_data_size*mb);

                    if (output_mode == CLASSIFICATION_MODE)
                    {
                        int max_label=0;
                        float max_confidence=0.0;
                        for (int l=0; l<outputDims[1]; l++)
                        {
                            if (output_buffer_current_image[l]>max_confidence) {
                                max_confidence=output_buffer_current_image[l];
                                max_label=(int)l;
                            }
                        }
                        if (max_confidence>FLAGS_thresh)
                        {
                            fprintf(ROIfile,"%d %d %d %f %d %d %d %d \n",0,framenum,max_label,max_confidence,0,0,1,1);
                        }
                    }
                    else
                    {
                        int maxProposalCount=outputDims[2];
                        for (int c = 0; c < maxProposalCount; c++)
                        {
                            float *localbox=&output_buffer_current_image[c * 7];
                            float image_id   = localbox[0];
                            float locallabel = localbox[1] - 1;
                            float confidence = localbox[2];

                            if (confidence>FLAGS_thresh)
                            {
                                fprintf(ROIfile,"%d %d %lf %lf %lf %lf %lf %lf \n",0,framenum,locallabel,confidence,localbox[3],localbox[4],localbox[5],localbox[6]);
                            }
                        }
                    }
                    cout << "frame: " << framenum+1 << "\r";
                    fflush(stdout);
                    framenum++;

                }
                time2 = chrono::high_resolution_clock::now();
                diff = time2-time1;
	        postprocess_times.push_back(diff.count()*1000.0);
            }
        } while (process_more_frames);

        fclose(ROIfile);

    } catch (const InferenceEngine::details::InferenceEngineException& ex) {
        std::cerr << ex.what() << std::endl;
        return EXIT_FAILURE;
    }



    
    if (preprocess_times.size()>1) // ignore first batch -- it is always slower
    {
    	preprocess_times.pop_front();
    }

    //uncomment here to print times for each batch
    //for (int i=0;i<preprocess_times.size();i++) {printf("%d %f %f %f\n",i,preprocess_times.at(i),infer_times.at(i),postprocess_times.at(i));}
  
    cout << "Preprocess: "  << (accumulate(preprocess_times.begin(), preprocess_times.end(), 0.0) / (preprocess_times.size()*FLAGS_b)) << " \tms/frame" << endl;
    cout << "Inference:  "  << (accumulate(infer_times.begin(), infer_times.end(), 0.0) / (infer_times.size()*FLAGS_b)) << " \tms/frame" << endl;
    cout << "Postprocess:"  << (accumulate(postprocess_times.begin(), postprocess_times.end(), 0.0) / (postprocess_times.size()*FLAGS_b)) << " \tms/frame" << endl;


    return EXIT_SUCCESS;
}
