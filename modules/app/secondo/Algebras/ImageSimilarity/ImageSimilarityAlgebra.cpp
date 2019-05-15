/*
----
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
Foundation, Inc., 59 Temple Place, Suite 330, Boston, 
MA  02111-1307  USA
----

//paragraph [1] Title: [{\Large \bf \begin{center}] [\end{center}}]
//paragraph [10] Footnote: [{\footnote{] [}}]
//[TOC] [\tableofcontents]

[1] Image Similarity Algebra

March 2017 Michael Loris

The Image Similarity Algebra for SECONDO provides operations to store 
pictures in JPEG format into m-trees. It consists a ~Signature~ object 
representing a the signature of a single JPEG image. The object is a 
subtype of the Attribute class. The Image Similarity Algebra consists of 
multiple files, including external files for k-means clustering.


[TOC]

1.2 Defines and includes

*/

#include <iostream>

#include "Algebra.h"
#include "NestedList.h"
#include "QueryProcessor.h"
#include "SecondoSystem.h"
#include "../../Tools/Flob/DbArray.h"
#include "Attribute.h"
#include "Symbols.h"
#include "ListUtils.h"
#include "AlgebraManager.h"
#include "Operator.h"
#include "LogMsg.h"
#include "StandardTypes.h"
#include "../FText/FTextAlgebra.h"

#include <sys/stat.h>
#include <unistd.h>
#include <string>
#include "JPEGImage.h"
#include "SQFDCalculator.h" // this is not pretty, it duplicates code 
#include "EMDCalculator.h"  
#include "ImageSimilarityAlgebra.h"



extern NestedList* nl;
extern QueryProcessor* qp;
extern AlgebraManager* am;


namespace FeatureSignaturealg{


/*
1.5 Operator ~calcSQFD~

*/


ListExpr calcSQFDTM(ListExpr args) 
{
    if ( nl->ListLength(args) == 2) 
    {
        ListExpr arg1 = nl->First(args);
        ListExpr arg2 = nl->Second(args);
        
        if (
            nl->IsEqual(arg1, FeatureSignature::BasicType()) &&
            nl->IsEqual(arg2, FeatureSignature::BasicType()))
            {
            return nl->SymbolAtom(CcReal::BasicType());
        }
    }
    return nl->SymbolAtom(Symbol::TYPEERROR());
}


int calcSQFDVM(Word* args, Word& result,
                   int message, Word& local, Supplier s)
{
    //res->ClearDBArray();
    FeatureSignature* fs1 = static_cast<FeatureSignature*>(args[0].addr);
    FeatureSignature* fs2 = static_cast<FeatureSignature*>(args[1].addr);
    
    result = qp->ResultStorage(s);
    
    CcReal* res = (CcReal*) result.addr;
    SQFDCalculator sqfd;
    
    std::vector<FeatureSignatureTuple> fst1;
    for (int i = 0; i < fs1->GetNoFeatureSignatureTuples(); i++)
    {
		fst1.push_back(fs1->GetFeatureSignatureTuple(i));
	}
	
	std::vector<FeatureSignatureTuple> fst2;
    for (int i = 0; i < fs2->GetNoFeatureSignatureTuples(); i++)
    {
		fst2.push_back(fs2->GetFeatureSignatureTuple(i));
	}
    
    res->Set(true, sqfd.calcSQFD(fst1, fst2));
        
    return 0;
}

OperatorSpec calcSQFDSpec(
	"featuresignature x featuresignature -> real",
	"sqfd(_,_)",
	"Computes the SQFD between two signatures",
	"query sqfd (sig1, sig2)"
);

Operator calcSQFDOp(
	"sqfd",
	calcSQFDSpec.getStr(),
	calcSQFDVM,
	Operator::SimpleSelect,
	calcSQFDTM
);

/*
1.6 Operator ~calcEMD~

*/

ListExpr calcEMDTM(ListExpr args) 
{
    if ( nl->ListLength(args) == 2) 
    {
        ListExpr arg1 = nl->First(args);
        ListExpr arg2 = nl->Second(args);
        
        if (
            nl->IsEqual(arg1, FeatureSignature::BasicType()) &&
            nl->IsEqual(arg2, FeatureSignature::BasicType()))
            {
            return nl->SymbolAtom(CcReal::BasicType());
        }
    }
    return nl->SymbolAtom(Symbol::TYPEERROR());
}


int calcEMDVM(Word* args, Word& result,
                   int message, Word& local, Supplier s)
{
    //res = static_cast<double*>(result.addr);
    //res->ClearDBArray();
    FeatureSignature* fs1 = static_cast<FeatureSignature*>(args[0].addr);
    FeatureSignature* fs2 = static_cast<FeatureSignature*>(args[1].addr);
    
    result = qp->ResultStorage(s);
    
    CcReal* res = (CcReal*) result.addr;
    
    EMDCalculator emdCalc;
    
    std::vector<FeatureSignatureTuple> fst1;
    for (int i = 0; i < fs1->GetNoFeatureSignatureTuples(); i++)
    {
		fst1.push_back(fs1->GetFeatureSignatureTuple(i));
	}
	
	std::vector<FeatureSignatureTuple> fst2;
    for (int i = 0; i < fs2->GetNoFeatureSignatureTuples(); i++)
    {
		fst2.push_back(fs2->GetFeatureSignatureTuple(i));
	}
    
    double dist = emdCalc.calcEMD(fst1, fst2);
    //std::cout << "dist:" << dist << std::endl;
    res->Set(true, dist);
        
    return 0;
}

OperatorSpec calcEMDSpec(
	"featuresignature x featuresignature -> real",
	"emd(_,_)",
	"Computes the EMD between two signatures",
	"query emd (sig1, sig2)"
);

Operator calcEMDOp(
	"emd",
	calcEMDSpec.getStr(),
	calcEMDVM,
	Operator::SimpleSelect,
	calcEMDTM
);



/*
2 Operator ~readSignatureFromFile~

*/

bool 
FeatureSignature::readSignatureFromFile(
	const std::string _fileName, 
    const int colorSpace, 
    const int coaRange, 
    const int conRange, 
    const int patchSize,
    const int percentSamples, 
    const int noClusters)
{
    
    this->fileName = _fileName;
    
    if(this->fileName == ""
        || !(access (this->fileName.c_str(), F_OK) != -1))
        //|| S_ISDIR(fileName.st_mode)
    {
        std::cerr << "readSignatureFromFile: Cannot open file '" 
        << this->fileName << "'!" << endl;
        SetDefined(false);
        return false;
    }
    
    JPEGImage ji;
    
    ji.importJPEGFile(this->fileName, 
                        colorSpace, 
                        coaRange,
                        conRange,
                        patchSize, 
                        percentSamples, 
                        noClusters);
    
    ji.computeCoarsenessValues(coaRange);

    ji.computeContrastValues(conRange);

    //unsigned int noDataPoints = ji.height * ji.width;
    
    unsigned int noDataPoints 
		= (unsigned int) static_cast<double>(ji.width * ji.height) 
		/ static_cast<double>(percentSamples);

    ji.clusterFeatures(noClusters, DIMENSIONS, noDataPoints);

    for (auto tupl : ji.signature)
    {
        this->Append(tupl);
    }

    SetDefined(true);
    return true;
}


/*
2.1 Type mapper for operator ~readSignatureFromFile~

*/
ListExpr readSignatureFromFileTM(ListExpr args) 
{
    if ( nl->ListLength(args) == 7) 
    {
        ListExpr arg1 = nl->First(args);
        ListExpr arg2 = nl->Second(args);
        ListExpr arg3 = nl->Third(args);
        ListExpr arg4 = nl->Fourth(args);
        ListExpr arg5 = nl->Fifth(args);
        ListExpr arg6 = nl->Sixth(args);
        ListExpr arg7 = nl->Seventh(args);
        
        if (
            (nl->IsEqual(arg1, FText::BasicType()) ||
            nl->IsEqual(arg1, CcString::BasicType())
            ) &&
            nl->IsEqual(arg2, CcInt::BasicType()) &&
            nl->IsEqual(arg3, CcInt::BasicType()) &&
            nl->IsEqual(arg4, CcInt::BasicType()) &&
            nl->IsEqual(arg5, CcInt::BasicType()) &&
            nl->IsEqual(arg6, CcInt::BasicType()) &&
            nl->IsEqual(arg7, CcInt::BasicType()))
            {
            return nl->SymbolAtom(FeatureSignature::BasicType());
        }
    }
    return nl->SymbolAtom(Symbol::TYPEERROR());
}


int readSignatureFromFileSelect(ListExpr args) 
{
    ListExpr arg1 = nl->First(args);
    if (nl->IsEqual(arg1, FText::BasicType())) 
        return 0;
    if (nl->IsEqual(arg1, CcString::BasicType()))
        return 1;
            
    return -1;
}


/*
2.2 Value mapper for operator ~readSignatureFromFile~

*/
template<class StringType>
int readSignatureFromFileFun(Word* args, Word& result,
                   int message, Word& local, Supplier s)
{
    result = qp->ResultStorage(s);
    FeatureSignature* res = static_cast<FeatureSignature*>(result.addr);
    res->ClearDBArray();
    
    StringType* fileName = static_cast<StringType*>(args[0].addr);
    
    CcInt* colorSpace = static_cast<CcInt*>(args[1].addr);
    CcInt* coaRange = static_cast<CcInt*>(args[2].addr);
    CcInt* conRange = static_cast<CcInt*>(args[3].addr);
    CcInt* patchSize = static_cast<CcInt*>(args[4].addr);
    CcInt* percentSamples = static_cast<CcInt*>(args[5].addr);
    CcInt* noClusters = static_cast<CcInt*>(args[6].addr);

    if(fileName->IsDefined())
    {
        res->readSignatureFromFile(
				fileName->GetValue(),
				colorSpace->GetIntval(), 
				coaRange->GetIntval(), 
				conRange->GetIntval(), 
				patchSize->GetIntval(),
				percentSamples->GetIntval(), 
				noClusters->GetIntval());
    } 
    else 
    {
        res->SetDefined(false);
    }
    
    return 0;
}


/*
2.3 Selection of value mapper for operator ~readSignatureFromFile~

*/

ValueMapping readSignatureFromFileVM[] = 
{
    readSignatureFromFileFun<FText>,
    readSignatureFromFileFun<CcString>
};


/*
2.4 Specificaton for operator ~readSignatureFromFile~

*/
    
static const std::string readSignatureFromFileSpec  =
    "( ( \"Signature\" \"Syntax\" \"Meaning\" "
    "\"Example\" ) "
    "( <text> {text|string} -> featuresignature"
    "</text--->"
    "<text>readSignatureFromFile(fileName, colorSpace, coarseness, "
    "contrast, patch, percent, cluster) </text--->"
     "<text>Creates a feature signature from a jpeg file. The "
     "colorSpace parameter allows the following settings: 1 for RGB, 2 "
     "for HSV, 3 for CIELAB. "
     "The coarseness parameter defines the edge length of a square of "
     "neighbor pixels which should be analyzed. This parameter strongly "
     "affects performance. Good values are between 1 and 7. "
     "The contrast parameter defines the edge length of a square of "
     "neighbor pixels which should be analyzed. Good values are between"
     " 1 and 7. "
     "The patch parameter defines the edge length of a square of pixels"
     " to be extracted from an image. A good value is 1, which "
     "corresponds to a single pixel. "
     "The percent parameter denotes how many pixels should be extracted"
     " from an image. "
     "The cluster parameter defines how many clusters the k-means "
     "algorithm should create. Good values are between 10 and 100. "
     " </text--->"
"<text>query readSignatureFromFile('test.jpg', 3, 3, 7, 1, 10, 100)</text--->"
    "</text--->"
"<text>query readSignatureFromFile('test.jpg', 3, 3, 7, 1, 10, 100)</text--->"
    ") )";

/*
2.5 Creation of an Operator instance for operator ~readSignatureFromFile~

*/
static Operator readSignatureFromFileOp(
                        "readSignatureFromFile",
                        readSignatureFromFileSpec,
                        2,
                        readSignatureFromFileVM,
                        readSignatureFromFileSelect,
                        readSignatureFromFileTM);
                        
                        
/*
3 Print functions for tuples

*/

std::ostream& operator<<(std::ostream& os, const FeatureSignatureTuple& ist)
{
  os << "(" 
  << ist.weight << "," 
  << ist.centroid.x << "," 
  << ist.centroid.y << ","
  << ist.centroid.colorValue1 << "," 
  << ist.centroid.colorValue2 << ","
  << ist.centroid.colorValue3 << ","
  << ist.centroid.coarseness << ","
  << ist.centroid.contrast << ","
  << ")";
  return os;
}


std::ostream& operator<<(std::ostream& os, const FeatureSignature& p)
{
  //os << " State: " << p.GetState()
  //<< "<" << p.GetFileName() << ">"
  //<< "<";

  for(int i = 0; i < p.GetNoFeatureSignatureTuples(); i++)
    os << p.GetFeatureSignatureTuple(i) << " ";

  os << ">";

  return os;
}


/*
4 Constructors for FeatureSignature class

This first constructor creates a new FeatureSignature.

*/
FeatureSignature::FeatureSignature(const int n) :
  Attribute(true),
  FeatureSignatureTuples(n)
{
  SetDefined(true);
}


FeatureSignature::FeatureSignature(const int n, 
    const double *W, 
    const int *X, 
    const int *Y,
    const double *R,
    const double *G,
    const double *B,
    const double *COA,
    const double *CON) :
  Attribute(true),
  FeatureSignatureTuples(n) 
{
  SetDefined(true);
  
  if( n > 0 )
  {
    for( int i = 0; i < n; i++ )
    {	  
      FeatureSignatureTuple fst(
      W[i], X[i], Y[i], R[i], G[i], B[i], COA[i], CON[i]);
      Append(fst);
    }  
  }
}


/*
4.1 Copy Constructor

*/
FeatureSignature::FeatureSignature(const FeatureSignature& src):
  Attribute(src.IsDefined()),
  FeatureSignatureTuples(src.FeatureSignatureTuples.Size()),
  fileName(src.fileName)
{
  FeatureSignatureTuples.copyFrom(src.FeatureSignatureTuples);
}


/*

4.2 Destructor

*/
FeatureSignature::~FeatureSignature()
{
}


FeatureSignature& FeatureSignature::operator=(
    const FeatureSignature& src){
  FeatureSignatureTuples.copyFrom(src.FeatureSignatureTuples);
  return *this;
}


/*
4.3 NumOfFLOBs method

*/
int FeatureSignature::NumOfFLOBs() const
{
  return 1;
}


/*
4.4 GetFLOB method

*/
Flob *FeatureSignature::GetFLOB(const int i)
{
  assert(i >= 0 && i < NumOfFLOBs());
  return &FeatureSignatureTuples;
}


/*
4.5 Compare method
todo: Not yet implemented. Needed to be a tuple attribute.

*/
int FeatureSignature::Compare(const Attribute*) const
{
  return 0;
}


/*
 * 
4.6 HashValue method
Only the weights are taken, converted to string, concantenated and then
a hash value is calculated and returned.

*/
size_t FeatureSignature::HashValue() const 
{   
    std::string hashString;
    for (int i = 0; this->GetNoFeatureSignatureTuples(); i++)
    {
        FeatureSignatureTuple fst = GetFeatureSignatureTuple(i);
        hashString += std::to_string(fst.weight);
    }
    std::hash<std::string> hashFunction;
    size_t hashValue = hashFunction(hashString);    
    return  hashValue;
}


/*
4.6 Adjacent method

Not required.

*/
bool FeatureSignature::Adjacent(const Attribute*) const
{
  return 0;
}


/*
4.7 Clone method

Returns a new created FeatureSignature (clone) which is a
copy of ~this~.

*/
FeatureSignature *FeatureSignature::Clone() const
{ 
  FeatureSignature *is = new FeatureSignature(*this);
  return is;
}


/*
4.8 Copy method


*/
void FeatureSignature::CopyFrom(const Attribute* right){
  *this = *((FeatureSignature*)right);
}


/*
4.9 Sizeof method

*/
size_t FeatureSignature::Sizeof() const
{
  return sizeof(*this);
}


/*
5 Print method

*/
std::ostream& FeatureSignature::Print(std::ostream& os) const
{
  return (os << *this);
}


/*
5.1 Append method

Appends an FeatureSignatureTple ~ist~ at the end of the FeatureSignature.

*/
void FeatureSignature::Append(const FeatureSignatureTuple& fst)
{
  FeatureSignatureTuples.Append(fst);
}


/*
2.3.10 Complete

Turns the FeatureSignature into the ~complete~ state.

*Precondition* ~state == partial~. // todo: remove states

*/


/*
5.2 Correct method

Not yet implemented.

*/
bool FeatureSignature::Correct()
{
  return true;
}


/*
5.3 Destroy method

Turns the FeatureSignature into the ~closed~ state destroying the
FeatureSignatureTuple array.

*/
void FeatureSignature::Destroy()
{
  FeatureSignatureTuples.destroy();
}


/*
5.4 NoFeatureSignatureTuples

Returns the number of tuples of the FeatureSignature.

*/
int FeatureSignature::GetNoFeatureSignatureTuples() const
{
  return FeatureSignatureTuples.Size();
}


/*
5.5 GetFeatureSignatureTuple

Returns a signature tuple indexed by ~i~.

*/
FeatureSignatureTuple FeatureSignature::GetFeatureSignatureTuple(int i) 
const
{
    assert(0 <= i && i < GetNoFeatureSignatureTuples());

    FeatureSignatureTuple fst;
    FeatureSignatureTuples.Get(i, &fst);
    return fst;
}


/*
5.6 IsEmpty method

Returns if the FeatureSignature is empty or not.

*/
const bool FeatureSignature::IsEmpty() const
{
    // todo: report correct number
    return GetNoFeatureSignatureTuples() == 0;
}


/*
6 FeatureSignature Algebra.

*/

/*

6.2 In method, gets information of the object from an nl

*/  
ListExpr FeatureSignature::Out(ListExpr typeInfo, Word value)
{    
    FeatureSignature* imgsig 
        = static_cast<FeatureSignature*>(value.addr);
  
    if(!imgsig->IsDefined())
    {
        return nl->SymbolAtom(Symbol::UNDEFINED());
    }
  
    if( imgsig->IsEmpty() )
    {
        return (nl->TheEmptyList());
    }
    else
    {
        
        
    // SECONDO will sometimes give weird numbers for the first
    // coarseness value of a signature
    double tmpHotFix = 
    imgsig->GetFeatureSignatureTuple(0).centroid.coarseness;
    
    if (tmpHotFix < 1.0)
    {
        tmpHotFix = 1.0;
      //  std::cout << "cout, < 0.0:" << tmpHotFix << std::endl;
    } else if (tmpHotFix > 5.0)
    { 
     //   std::cout << "cout, > 5.0:" << tmpHotFix << std::endl;
        tmpHotFix = 5.0;
    }
        
    //ListExpr tmpRes = nl->OneElemList(
    //    nl->RealAtom(imgsig->GetFeatureSignatureTuple(0).weight));
    ListExpr tmpRes = nl->OneElemList(
        nl->RealAtom(imgsig->GetFeatureSignatureTuple(0).weight));
            
    ListExpr lst = tmpRes;
    
    lst = nl->Append(lst, nl->IntAtom(
        imgsig->GetFeatureSignatureTuple(0).centroid.x));
    lst = nl->Append(lst, nl->IntAtom(
        imgsig->GetFeatureSignatureTuple(0).centroid.y));
    lst = nl->Append(lst, nl->RealAtom(
        imgsig->GetFeatureSignatureTuple(0).centroid.colorValue1));
    lst = nl->Append(lst, nl->RealAtom(
        imgsig->GetFeatureSignatureTuple(0).centroid.colorValue2));
    lst = nl->Append(lst, nl->RealAtom(
        imgsig->GetFeatureSignatureTuple(0).centroid.colorValue3));
    lst = nl->Append(lst, nl->RealAtom(
        tmpHotFix));
    lst = nl->Append(lst, nl->RealAtom(
        imgsig->GetFeatureSignatureTuple(0).centroid.contrast));
        
        
    //std::cout << "out:" << std::endl
    //<< " " << imgsig->GetFeatureSignatureTuple(0).weight
    //<< " " << imgsig->GetFeatureSignatureTuple(0).centroid.x
    //<< " " << imgsig->GetFeatureSignatureTuple(0).centroid.colorValue1
    //<< " " << imgsig->GetFeatureSignatureTuple(0).centroid.colorValue2
    //<< " " << imgsig->GetFeatureSignatureTuple(0).centroid.colorValue3
    //<< " " << tmpHotFix
    //<< " " << imgsig->GetFeatureSignatureTuple(0).centroid.contrast 
    //<< std::endl;
    
    ListExpr result = nl->OneElemList(tmpRes);
            
    ListExpr last = result;
    
    for(int i = 1; i < imgsig->GetNoFeatureSignatureTuples(); i++)
    {
        ListExpr tmpRes = nl->OneElemList(
            nl->RealAtom(imgsig->GetFeatureSignatureTuple(i).weight));
                
        ListExpr lst = tmpRes;

        lst = nl->Append(lst, nl->IntAtom(
            imgsig->GetFeatureSignatureTuple(i).centroid.x));
        lst = nl->Append(lst, nl->IntAtom(
            imgsig->GetFeatureSignatureTuple(i).centroid.y));
        lst = nl->Append(lst, nl->RealAtom(
            imgsig->GetFeatureSignatureTuple(i).centroid.colorValue1));
        lst = nl->Append(lst, nl->RealAtom(
            imgsig->GetFeatureSignatureTuple(i).centroid.colorValue2));
        lst = nl->Append(lst, nl->RealAtom(
            imgsig->GetFeatureSignatureTuple(i).centroid.colorValue3));
        lst = nl->Append(lst, nl->RealAtom(
            imgsig->GetFeatureSignatureTuple(i).centroid.coarseness));
        lst = nl->Append(lst, nl->RealAtom(
            imgsig->GetFeatureSignatureTuple(i).centroid.contrast));    
        last = nl->Append(last, tmpRes);
        
    //std::cout 
    //<< imgsig->GetFeatureSignatureTuple(i).weight
    //<< " " << imgsig->GetFeatureSignatureTuple(i).centroid.x
    //<< " " << imgsig->GetFeatureSignatureTuple(i).centroid.colorValue1
    //<< " " << imgsig->GetFeatureSignatureTuple(i).centroid.colorValue2
    //<< " " << imgsig->GetFeatureSignatureTuple(i).centroid.colorValue3
    //<< " " << imgsig->GetFeatureSignatureTuple(i).centroid.coarseness
    //<< " " << imgsig->GetFeatureSignatureTuple(i).centroid.contrast 
    //<< std::endl;
    }

    return result;
  }
}


/*

6.2 In function, gets object's info from a nested list

*/  
Word
FeatureSignature::In(const ListExpr typeInfo, const ListExpr instance,
           const int errorPos, ListExpr& errorInfo, bool& correct)
{
    FeatureSignature* imgsig = new FeatureSignature(0);
    
    if(listutils::isSymbolUndefined(instance)){
        imgsig->SetDefined(false);
        correct = true;
        return SetWord(imgsig);
    }
    
    imgsig->SetDefined(true);
    
    
    ListExpr first = nl->Empty();
    ListExpr rest = instance;
      
    while(!nl->IsEmpty(rest))
    {
        first = nl->First(rest);
        rest = nl->Rest(rest);
        
        if( nl->ListLength(first) == 8 &&
            nl->IsAtom(nl->First(first )) &&
            nl->AtomType(nl->First(first)) == RealType &&
            nl->IsAtom(nl->Second(first)) &&
            nl->AtomType(nl->Second(first)) == IntType && 
            nl->IsAtom(nl->Third(first)) &&
            nl->AtomType(nl->Third(first)) == IntType &&
            nl->IsAtom(nl->Fourth(first)) &&
            nl->AtomType(nl->Fourth(first)) == RealType &&
            nl->IsAtom(nl->Fifth(first )) &&
            nl->AtomType(nl->Fifth(first)) == RealType &&
            nl->IsAtom(nl->Sixth(first )) &&
            nl->AtomType(nl->Sixth(first)) == RealType &&
            nl->IsAtom(nl->Seventh(first )) &&
            nl->AtomType(nl->Seventh(first)) == RealType &&
            nl->IsAtom(nl->Eigth(first)) &&            
            nl->AtomType(nl->Eigth(first)) == RealType 
         )
        {
            FeatureSignatureTuple fst( 
                nl->RealValue(nl->First(first)),
                nl->IntValue(nl->Second(first)),
                nl->IntValue(nl->Third(first)),
                nl->RealValue(nl->Fourth(first)),
                nl->RealValue(nl->Fifth(first)),
                nl->RealValue(nl->Sixth(first)),
                nl->RealValue(nl->Seventh(first)),
                nl->RealValue(nl->Eigth(first))                                
            );
            imgsig->Append(fst);
            
            //std::cout 
            //<< " " << nl->RealValue(nl->First(first))
            //<< " " << nl->IntValue(nl->Second(first)) 
            //<< " " << nl->IntValue(nl->Third(first))
            //<< " " << nl->RealValue(nl->Fourth(first))
            //<< " " << nl->RealValue(nl->Fifth(first))
            //<< " " << nl->RealValue(nl->Sixth(first))
            //<< " " << nl->RealValue(nl->Seventh(first))
            //<< " " << nl->RealValue(nl->Eigth(first)) 
            //<< " " << std::endl;
            
        }
        else
        {
            correct = false;
            delete imgsig;
            return SetWord(Address(0));
        }
    }
    
  //imgsig->Complete();
  correct = true;
  return SetWord(imgsig);
}


/*
6.3 Property method, describing the signature of the type constructor

*/
ListExpr FeatureSignature::Property()
{
  return (nl->TwoElemList(
         nl->FiveElemList(
            nl->StringAtom("Signature"),
            nl->StringAtom("Example Type List"),
            nl->StringAtom("List Rep"),
            nl->StringAtom("Example List"),
            nl->StringAtom("Remarks")),
         nl->FiveElemList(
            nl->StringAtom("->" + Kind::DATA() ),
            nl->StringAtom(FeatureSignature::BasicType()),
            nl->StringAtom("(<tuple>*) where <tuple> is "
            "(r i i r r r r r)"),
            nl->StringAtom("((1.2 3 4 1.0 2.3 3.1 2.1 2.3))"),
            nl->StringAtom("weight(double), position (int), texture (double)"
                          ))));
}


/*
6.4 Kind method

This method checks whether the type constructor is applied correctly.

*/
bool
FeatureSignature::KindCheck( ListExpr type, ListExpr& errorInfo )
{
  return (nl->IsEqual( type, FeatureSignature::BasicType() ));
}


/*

6.5 ~Create~-function

*/
Word FeatureSignature::Create(const ListExpr typeInfo)
{    
    FeatureSignature* imgsig = new FeatureSignature(0);
    return (SetWord(imgsig));
}


/*
6.6 ~Delete~-function

*/
void FeatureSignature::Delete(const ListExpr typeInfo, Word& w)
{
  FeatureSignature* imgsig = (FeatureSignature*)w.addr;

  imgsig->Destroy();
  delete imgsig;
}


/*
6.7 ~Open~-function

*/
bool
FeatureSignature::Open( SmiRecord& valueRecord,
             size_t& offset,
             const ListExpr typeInfo,
             Word& value )
{
  FeatureSignature *p = 
  (FeatureSignature*)Attribute::Open(valueRecord, offset, typeInfo);
  value.setAddr( p );
  return true;
}


/*
6.7 ~Save~-function

*/
bool
FeatureSignature::Save( SmiRecord& valueRecord,
             size_t& offset,
             const ListExpr typeInfo,
             Word& value )
{
  FeatureSignature *p = (FeatureSignature *)value.addr;
  Attribute::Save( valueRecord, offset, typeInfo, p );
  return true;
}


/*
6.8 ~Close~-function

*/
void FeatureSignature::Close(const ListExpr typeInfo, Word& w)
{
  FeatureSignature* imgsig = (FeatureSignature*)w.addr;
  delete imgsig;
}


/*
6.9 ~Clone~-method

*/
Word FeatureSignature::Clone(const ListExpr typeInfo, const Word& w)
{
  return SetWord( ((FeatureSignature*)w.addr)->Clone() );
}

/*
7 ~SizeOf~-method

*/
int FeatureSignature::SizeOfObj()
{
  return sizeof(FeatureSignature);
}


/*
7.1 ~Cast~-method

*/
void* FeatureSignature::Cast(void* addr)
{
  return (new (addr) FeatureSignature);
}


/*
7.2 Creation of the type constructor instance

*/
TypeConstructor imgsig(
        FeatureSignature::BasicType(),               
        FeatureSignature::Property,
        FeatureSignature::Out,   FeatureSignature::In,
        0,              0,                  
        FeatureSignature::Create,  FeatureSignature::Delete,
        FeatureSignature::Open,    FeatureSignature::Save,
        FeatureSignature::Close,   FeatureSignature::Clone,
        FeatureSignature::Cast,
        FeatureSignature::SizeOfObj,
        FeatureSignature::KindCheck);


/*
4 FeatureSignatureAlgebra

*/


class ImageSimilarityAlgebra : public Algebra
{
  public:
    ImageSimilarityAlgebra() : Algebra()
    {
      AddTypeConstructor(&imgsig);
      AddOperator(&readSignatureFromFileOp);
      AddOperator(&calcSQFDOp);
      AddOperator(&calcEMDOp);

      imgsig.AssociateKind(Kind::DATA());
    }
    ~ImageSimilarityAlgebra() {};
};


/*

5 Initialization of Algebra

*/


extern "C"
Algebra*
InitializeImageSimilarityAlgebra(NestedList *nlRef, QueryProcessor *qpRef)
{
  nl = nlRef;
  qp = qpRef;
  return (new ImageSimilarityAlgebra());
}

} // end of namespace
