/*
This file is part of SECONDO.

Copyright (C) 2004, University in Hagen, Department of Computer Science,
Database Systems for New Applications.

SECONDO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

SECONDO is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SECONDO; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

*/

#include "Algebra.h"
#include "NestedList.h"
#include "NList.h"
#include "QueryProcessor.h"
#include "AlgebraManager.h"
#include "StandardTypes.h"
#include "Symbols.h"
#include "ListUtils.h"
#include "Algebras/Relation-C++/RelationAlgebra.h"
#include "STR.h"

#include <string>
#include <iostream>
#include <vector>
#include "RTreeTouch.h"
#include "NodeT.h"


using namespace std;
using namespace mmrtreetouch;

namespace STR {

    vector<vector <Tuple *> > splitInSlices(
            Tuple * arr[],
            int numOfPartitions,
            int array_size)
    {
        int numOfObjsInSlices = ceil((float)array_size/numOfPartitions)*2;

        int counter = 0;

        vector<Tuple *> temp;
        vector<vector <Tuple *> > container;


        for( int i = 0; i < array_size; i++ ) {
            counter++;

            temp.push_back(arr[i]);

            if (counter % numOfObjsInSlices == 0) {
                container.push_back(temp);
                temp.clear();
            }
        }

        if (!temp.empty()) {
            container.push_back(temp);
        }

        return container;
    }

    vector<vector <Tuple *> > sortSecondDimension(
            vector<vector <Tuple *> > container,
            int leftAttrIndex)
    {
        vector<vector <Tuple *> > sortedSlicedList;

        for (vector<Tuple *> currentSlice: container) {
            Tuple * arr[currentSlice.size()];
            copy(currentSlice.begin(), currentSlice.end(), arr);
            // it copies the content of currentSlice vector to arr (array)

            mergeSort(arr, 0, (int)(currentSlice.size()-1), 'y', leftAttrIndex);

            int arraySize = sizeof(arr)/ sizeof(arr[0]);

            vector<Tuple *> v(arr, arr + arraySize);

            sortedSlicedList.push_back(v);
        }

        return sortedSlicedList;
    }

    string bucketInfo(vector<NodeT*> bucketVector)
    {
        stringstream info;
        info << (int)bucketVector.size() << "(";

        //for(CRelAlgebra::TBlock* tb : fTBlockVector) {


        for (int i=0; i < (int)bucketVector.size(); i++) {
        //for (NodeT* bucket: bucketVector) {
            NodeT* bucket = bucketVector.at(i);

            //info << (i+1) << "[";
            info << (i+1) << "[" << (int)bucket->objects.size();

            /*
            for (int j=0; j < (int) bucket->objects.size(); j++) {
                Tuple* object = bucket->objects.at(j);
                Attribute * attr =object->GetAttribute(0);

                info << (j+1) <<"(Tuple title: " << attr->toText()  << ")";

            }
             */

            info << "]";
        }

        info << ")";

        cout << info.str() << endl;

        return info.str();
    }

    vector<NodeT*> packInBuckets(
            vector<vector <Tuple *> > sortedSlicedList,
            int sizeOfSortedList,
            int initialListSize,
            int numOfPartitions,
            int leftStreamWordIndex)
    {
        int numOfItemsInBucket = ceil((float)initialListSize/numOfPartitions);
        vector<NodeT*> containerOfBuckets;
        NodeT* bucketNode = NULL;
        int counter = 0;

        for (vector<Tuple *> innerList : sortedSlicedList) {

            while((int)innerList.size() > 0){
                counter++;

                if (bucketNode == NULL) {
                    bucketNode = new NodeT(99999, true);
                }

                bucketNode->level = 0;
                bucketNode->addObject(innerList.front(), leftStreamWordIndex);
                innerList.erase(innerList.begin());

                if(counter % numOfItemsInBucket == 0){

                    containerOfBuckets.push_back(bucketNode);

                    bucketNode = NULL;
                }
            }
            innerList.clear();

            if (bucketNode != NULL) {
                containerOfBuckets.push_back(bucketNode);
            }

        }

        return containerOfBuckets;
    }

    void mergeSort(
            Tuple * arr[],
            int l,
            int r,
            char direction,
            int leftAttrIndex)
    {
        if (l < r)
        {
            int m = l+(r-l)/2;

            mergeSort(arr, l, m, direction, leftAttrIndex);
            mergeSort(arr, m+1, r, direction, leftAttrIndex);

            merge(arr, l, m, r, direction, leftAttrIndex);
        }
    }

    void merge(
            Tuple * arr[],
            int l,
            int m,
            int r,
            char direction,
            int leftAttrIndex)
    {
        Attribute * attr1, * attr2;
        float valueL, valueR;
        int i, j, k;
        int n1 = m - l + 1;
        int n2 =  r - m;

        Tuple * L[n1], * R[n2];

        for (i = 0; i < n1; i++)
            L[i] = arr[l + i];
        for (j = 0; j < n2; j++)
            R[j] = arr[m + 1+ j];

        i = 0;
        j = 0;
        k = l;
        while (i < n1 && j < n2)
        {
            if (direction == 'x') {

                attr1 = L[i]->GetAttribute(leftAttrIndex);
                attr2 = R[j]->GetAttribute(leftAttrIndex);

                valueL = (attr1->getMinX() + attr1->getMaxX()) / 2;
                valueR = (attr2->getMinX() + attr2->getMaxX()) / 2;

            } else if (direction == 'y') {

                attr1 = L[i]->GetAttribute(leftAttrIndex);
                attr2 = R[j]->GetAttribute(leftAttrIndex);

                valueL = (attr1->getMinY() + attr1->getMaxY()) / 2;
                valueR = (attr2->getMinY() + attr2->getMaxY()) / 2;
            }


            if (valueL <= valueR)
            {
                arr[k] = L[i];
                i++;
            }
            else
            {
                arr[k] = R[j];
                j++;
            }
            k++;
        }

        while (i < n1)
        {
            arr[k] = L[i];
            i++;
            k++;
        }

        while (j < n2)
        {
            arr[k] = R[j];
            j++;
            k++;
        }
    }

    void createArrayFromTupleVector(Tuple * arr[], vector<Tuple*> tuples) {

        // # 1. creating array
        for (int i = 0; i< (int) tuples.size(); i++) {
            arr[i] = tuples.at(i);
        }
        tuples.clear();
    }

    /*
     * 1. create Array
     * 2. run mergeSort - sort by first dimension - x
     * 3. split in slices
     * 4. run mergeSort - sort by second dimension - y
     * 5. pack in buckets
     */
    vector<NodeT*> createBuckets(
            vector<Tuple*> tuples,
            int _firstStreamWordIndex) {
        int size = (int) tuples.size();

        // # 1 create Array
        Tuple * arr[size] = {};
        STR::createArrayFromTupleVector(arr, tuples);

        // # 2 run mergeSort - sort by first dimension - x
        STR::mergeSort(arr, 0, size - 1, 'x', _firstStreamWordIndex);

        // # 3
        int numOfPartitions = 10;
        vector<vector <Tuple *> > container = STR::splitInSlices(
                arr,
                numOfPartitions,
                size);

        // # 4
        vector<vector <Tuple *> > sortedSlicedList = STR::sortSecondDimension(
                container,
                _firstStreamWordIndex);

        // # 5
        return STR::packInBuckets(
                sortedSlicedList,
                (int)sortedSlicedList.size(),
                size,
                numOfPartitions,
                _firstStreamWordIndex);
    }

}