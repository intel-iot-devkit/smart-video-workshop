/*
 Copyright (c) 2018 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/

// ===============================================================================
// Generated file for Inference Engine extension for CPU plugin
//
// IMPLEMENT YOUR KERNEL HERE.
//
// You need to edit this file in order to:
//  1. initialize parameters (in constructor)
//  2. implement inference logic (in execute() method)
//
// Refer to the section "Adding Your Own Kernels to the Inference Engine" in
// OpenVINO* documentation (either online or offline in
// <INSTALL_DIR>/deployment_tools/documentation/docs/index.html an then navigate
// to the corresponding section).
// ===============================================================================

//#define IE_THREAD 1

#include "ext_list.hpp"
#include "ext_base.hpp"
#include "ie_parallel.hpp"
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>

namespace InferenceEngine {
namespace Extensions {
namespace Cpu {

class CoshImpl: public ExtLayerBase {
public:
    explicit CoshImpl(const CNNLayer* layer) {
        try {
            /* Layer SetUp
            *  Read parameters from IR and/or initialise them here.
            *
            *  Implemented functions for reading parameters are:
            *  for single value:
            *     getParamAsFloat, getParamAsInt, getParamsAsBool, getParamAsString
            *  for array
            *     getParamAsFloats, getParamAsInts
            *
            * Functions are declared in Inference Engine folder include/ie_layers.h
            *--------------------------------------------------------------------------------
            * Example of parameters reading is:
            *   scale_=layer->GetParamAsFloat("scale")
            *-------------------------------------------------------------------------------*/
            
            /* Set configuration: specify data format for layer
             *   For more information about data formats see: 
             *   "Inference Engine Memory primitives" in OpenVINO documentation
             *------------------------------------------------------------------------------*/

			addConfig(layer, { DataConfigurator(ConfLayout::PLN) }, { DataConfigurator(ConfLayout::PLN) });
        } catch (InferenceEngine::details::InferenceEngineException &ex) {
            errorMsg = ex.what();
        }
    }

    StatusCode execute(std::vector<Blob::Ptr>& inputs, std::vector<Blob::Ptr>& outputs,
                       ResponseDesc *resp) noexcept override {
        // Add implementation for layer inference here
        // Examples of implementations are in OpenVINO samples/extensions folder
	float* src_data = inputs[0]->buffer();
        float* dst_data = outputs[0]->buffer();

        SizeVector dims = inputs[0]->getTensorDesc().getDims();

        int N = static_cast<int>((dims.size() > 0) ? dims[0] : 1);
        int C = static_cast<int>((dims.size() > 1) ? dims[1] : 1);
        int H = static_cast<int>((dims.size() > 2) ? dims[2] : 1);
        int W = static_cast<int>((dims.size() > 3) ? dims[3] : 1);

	//hyperbolic cosine is given by : (e^x + e^-x)/2
	parallel_for(N*C*H*W, [&](int ii) {
		dst_data[ii] = (exp(src_data[ii]) + exp(-src_data[ii]))/2;
        });
        return OK;
    }

private:
};

REG_FACTORY_FOR(ImplFactory<CoshImpl>, Cosh);

}  // namespace Cpu
}  // namespace Extensions
}  // namespace InferenceEngine
