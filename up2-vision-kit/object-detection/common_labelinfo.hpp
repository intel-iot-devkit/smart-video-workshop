/*
// Copyright (c) 2018 Intel Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
*/


#include <vector>
#include <stdio.h>
#include <string>
#include <fstream>
#include <iostream>
#include <string.h>


typedef struct {
    std::string label;
    bool useclass;
} labelinfo;


//read labels from file, combine with useclass flags to return a vector
//with label name and whether it is used
std::vector <labelinfo> readlabels(std::string labelfile,std::string useclassflags)
{
    std::vector<labelinfo> labels= {};

    if (labelfile.length() == 0) 
    {
	std::cout << "No labels file" << std::endl;
        return labels;
    }
    unsigned int nuseclasses=useclassflags.length();

    // -----------------
    // if no useclassflags, use all of them
    // count # of lines in the file, create classflags of all 1s
    // -----------------
    if (nuseclasses==0)
    {
        unsigned int numlabels=0;
        std::ifstream infile(labelfile,std::ifstream::in);

        if (!infile.is_open()) {
            std::cout << "Could not open labels file" << std::endl;
            return labels;
        } else {

            std::string tmpstr;
            while (infile.good()) {
                getline(infile, tmpstr);
                if (infile.good()) {
                    numlabels++;
                }
            }
            infile.close();
        }
        nuseclasses=numlabels;
    }
    printf("nuseclasses=%d\n",nuseclasses);


    // ----------------
    // Read class names
    // ----------------
    char *classflags = NULL;

    classflags = (char *)malloc(nuseclasses);

    if(classflags != NULL)
    {
        memcpy(classflags, useclassflags.c_str(), nuseclasses);

        std::ifstream infile(labelfile,std::ifstream::in);

        std::string tmpstr;
        while (infile.good()) {
            getline(infile, tmpstr);
            if (infile.good()) {
                labelinfo tmplabel;
                tmplabel.label=tmpstr;
                int pos=labels.size();
                if (pos<nuseclasses)
                {
                    tmplabel.useclass=(classflags[pos]=='1')?true:false;
                }
                else
                {
                    tmplabel.useclass=false;
                }
                labels.push_back(tmplabel);
            }
        }

        infile.close();


        free(classflags);
    }
    else
        std::cout << "Failed to allocate memory !" << std::endl;

    return labels;
}



