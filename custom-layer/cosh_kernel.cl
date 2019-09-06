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

/* ===============================================================================
 * Generated file for Inference Engine extension for GPU plugin
 *
 * IMPLEMENT YOUR KERNEL HERE.
 *
 * Refer to the section "Adding Your Own Kernels to the Inference Engine" in 
 * OpenVINO documentation 
 * ===============================================================================*/

#pragma OPENCL EXTENSION cl_khr_fp16 : enable

__kernel void Cosh(const __global INPUT0_TYPE* input,
			__global OUTPUT0_TYPE* output)
{
	// global index definition set in the XML configuration file
	const uint idx = get_global_id(0);
	const uint idy = get_global_id(1);
	const uint idbf = get_global_id(2);
	const uint feature = idbf%OUTPUT0_DIMS[1];
	const uint batch = idbf/OUTPUT0_DIMS[1];

	const uint in_id = batch*INPUT0_PITCHES[0] + feature*INPUT0_PITCHES[1] +
			   idy*INPUT0_PITCHES[2] + idx*INPUT0_PITCHES[3] + INPUT0_OFFSET;
	const uint out_id = batch*OUTPUT0_PITCHES[0] + feature*OUTPUT0_PITCHES[1] +
			   idy*OUTPUT0_PITCHES[2] + idx*OUTPUT0_PITCHES[3] + OUTPUT0_OFFSET;

	INPUT0_TYPE value = input[in_id];
        output[out_id] = (exp(value) + exp(-value))/2;
}
