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
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
----

//[_] [\_]
//characters      [1]   verbatim:   [$]   [$]
//characters      [2]   formula:    [$]   [$]
//characters      [3]   capital:    [\textsc{]  [}]
//characters      [4]   teletype:   [\texttt{]  [}]

1 Implementation file "DistDataReg.cpp"[4]

January-May 2008, Mirko Dibbert

*/
#include <sstream>
#include "DistDataReg.h"

#include "Algebras/Spatial/Point.h"
#include "Algebras/Spatial/SpatialAlgebra.h"
#include "Algebras/SymbolicTrajectory/Algorithms.h"
#include "PictureFuns.h"

#ifndef NO_MP3
//---------cru--------
#include "FVector.h"
//--------------------
#endif

#ifndef NO_IMAGESIMILARITY
#include "Algebras/ImageSimilarity/JPEGImage.h"
#include "Algebras/ImageSimilarity/ImageSimilarityAlgebra.h"
#include "Tools/Flob/DbArray.h"
#endif

using namespace gta;
using namespace std;

/*
Initialize static members:

*/
bool DistDataReg::initialized = false;
map<string, string> DistDataReg::defaultNames;
DistDataInfo DistDataReg::defaultInfo;
map<string, int> DistDataReg::distdataIds;
map<string, DistDataInfo> DistDataReg::distdataInfos;

/*
Default constructor for the ~DistDataInfo~ class:

*/
DistDataInfo::DistDataInfo()
: m_name("undef"), m_descr("undef"),
  m_getDataFun(0), m_id(false), m_flags(0)
{}

/*
Constructor for the ~DistDataInfo~ class:

*/
DistDataInfo::DistDataInfo(
        const string& name, const string& descr,
        int distdataId, const string& typeName,
        const GetDataFun getDataFun, char flags)
: m_name(name), m_descr(descr), m_getDataFun(getDataFun),
  m_flags(DDATA_IS_DEFINED | flags)
{
    int algebraId, typeId;
    SecondoSystem::GetCatalog()->GetTypeId(typeName, algebraId, typeId);
    m_id = DistDataId(algebraId, typeId, distdataId);
}

/*
Method ~DistDataAttribute::set~ (using "char"[4] arrays):

*/
void DistDataAttribute::set(
        bool defined, const char* data, size_t size,
        DistDataId distdataId)
{
    SetDefined(defined);
    if(defined)
    {
        m_data.resize(size);
        m_data.write(data,size,0);
        m_distdataId = distdataId;
    }
}

/*
Method ~DistDataAttribute::set~ (using "DistData"[4] objects):

*/
void DistDataAttribute::set(
        bool defined, DistData* data, DistDataId distdataId)
{
    SetDefined(defined);
    if(defined)
    {
        m_data.resize(data->size());
        m_data.write((const char*)data->value(), data->size(),0);
        m_distdataId = distdataId;
    }
}

/*
Method ~DistDataAttribute::CopyFrom~:

*/
void DistDataAttribute::CopyFrom(const Attribute* rhs)
{
    const DistDataAttribute* ddAttr =
            static_cast<const DistDataAttribute*>(rhs);

    SetDefined(ddAttr->IsDefined());
    if(ddAttr->IsDefined())
    {
        m_data.copyFrom(ddAttr->m_data);
        m_distdataId = ddAttr->distdataId();
    }
}

/*
Method ~DistDataReg::addInfo~:

*/
void DistDataReg::addInfo(DistDataInfo info)
{
    ostringstream osId;
    osId << info.algebraId() << "#"
         << info.typeId() << "#"
         << info.distdataId();
    distdataInfos [osId.str()] = info;

    distdataIds[info.name()] = info.distdataId();
}

/*
Method ~DistDataReg::defaultDataName~:

*/
string DistDataReg::defaultName(const string& typeName)
{
    if(!initialized)
        initialize();

    map<string, string>::iterator iter =
            defaultNames.find(typeName);
    if (iter == defaultNames.end())
        return DDATA_UNDEFINED;
    else
        return iter->second;
}

/*
Method ~DistDataReg::getDataId~:

*/
DistDataId DistDataReg::getId(
        const string& typeName, const string& distdataName)
{
    if(!initialized)
        initialize();

    int algebraId, typeId;
    SecondoSystem::GetCatalog()->GetTypeId(typeName, algebraId, typeId);

    map<string, int>::iterator iter;

    if (distdataName == DDATA_DEFAULT)
        iter = distdataIds.find(defaultName(typeName));
    else
        iter = distdataIds.find(distdataName);

    if (iter != distdataIds.end())
        return DistDataId(algebraId, typeId, iter->second);
    else
        return DistDataId(false);
}

/*
Method ~DistDataReg::getInfo~:

*/
DistDataInfo& DistDataReg::getInfo(DistDataId id)
{
    if(!initialized)
        initialize();

    if (!id.isDefined())
        return defaultInfo;

    ostringstream osId;
    osId << id.algebraId() << "#"
         << id.typeId() << "#"
         << id.distdataId();

    distdataIter iter = distdataInfos.find(osId.str());
    if (iter != distdataInfos.end())
        return iter->second;
    else
        return defaultInfo;
}

/*
Method ~DistDataReg::definedNames~:

*/
string DistDataReg::definedNames(const string& typeName)
{
    if(!initialized)
        initialize();

    // search first info object for typeName
    distdataIter iter = distdataInfos.begin();
    while ((iter != distdataInfos.end()) &&
            (iter->second.typeName() != typeName))
    {
        ++iter;
    }

    // process all info objects for typeName
    ostringstream result;
    while ((iter != distdataInfos.end()) &&
            (iter->second.typeName() == typeName))
    {
        result << "\"" << iter->second.name() << "\" ";
        ++iter;
    }

    return result.str();
}


#ifndef NO_IMAGESIMILARITY
/*
Method ~DistDataReg::getFeatureSignature~:
Dbarray<FeatureSignatureTuple> will be used 

*/

DistData* DistDataReg::getFeatureSignature(const void* attr)
{
	const FeatureSignaturealg::FeatureSignature* sig 
    = static_cast<const FeatureSignaturealg::FeatureSignature*>(attr);
    
	if (!sig->IsDefined())
	{
		char def = 0;
		return new DistData(1, &def);
	}
    
	if (sig->GetNoFeatureSignatureTuples() == 0)
		return new DistData(0, 0);
	
	
    size_t siz = sig->GetNoFeatureSignatureTuples() 
                    * sizeof(FeatureSignatureTuple);
                    
	char* buffer = new char[siz];   
	size_t offset = 0;
	
	for (int i = 0; i < sig->GetNoFeatureSignatureTuples(); i++)
	{
        FeatureSignatureTuple fst;
		fst = sig->GetFeatureSignatureTuple(i);
		
        memcpy(buffer + offset, &fst, sizeof(FeatureSignatureTuple));
        offset += sizeof(FeatureSignatureTuple);
	}
	
    DistData* res = new DistData(siz, buffer);
	delete[] buffer;
	return res;
}
#endif


/********************************************************************
Implementation of getdata functions:

********************************************************************/
/*
Method ~DistDataReg::getDataInt~:

*/

DistData* DistDataReg::getDataInt(const void* attr)
{
    int value = static_cast<const CcInt*>(attr)->GetValue();
    char buffer[sizeof(int)];
    memcpy(buffer, &value, sizeof(int));
    return new DistData(sizeof(int), buffer);
}

/*
Method ~DistDataReg::getDataReal~:

*/
DistData* DistDataReg::getDataReal(const void* attr)
{
    SEC_STD_REAL value = static_cast<const CcReal*>(attr)->GetValue();
    char buffer[sizeof(SEC_STD_REAL)];
    memcpy(buffer, &value, sizeof(SEC_STD_REAL));
    return new DistData(sizeof(SEC_STD_REAL), buffer);
}


/*
Method ~DistDataReg::getDataPoints~:

*/
DistData* DistDataReg::getDataPoints(const void* attr)
{
  const Points* points = static_cast<const Points*>(attr);
  if(!points->IsDefined()){ // undefined points value
     char def = 0;
     return new DistData(1,&def);
  }
  if(points->Size()==0){ // empty points value
     return new DistData(0,0);
  }
  size_t s = 2 * points->Size() * sizeof(Coord);
  char* buffer = new char[s];
  size_t offset=0;
  Point p;
  for(int i=0;i<points->Size();i++){
     points->Get(i,p);
     Coord x = p.GetX();
     Coord y = p.GetY();
     memcpy(buffer + offset, &x, sizeof(Coord));
     offset += sizeof(Coord);
     memcpy(buffer + offset, &y, sizeof(Coord));
     offset += sizeof(Coord);
  }
  DistData* res = new DistData(s,buffer);
  delete[] buffer;
  return res;

}

/*
Version for a usual point

*/
DistData* DistDataReg::getDataPoint(const void* attr) {
   // cast to the correct type
   const Point* point = static_cast<const Point*>(attr);
   // special treatment for undefined values
   if(!point->IsDefined()){ // undefined points value
      return new DistData(0,0);
   }
   // serialize the point
   Coord x = point->GetX();
   Coord y = point->GetY();

   char buffer[2*sizeof(Coord)];
   memcpy(buffer, &x, sizeof(Coord));
   memcpy(buffer + sizeof(Coord), &y, sizeof(Coord));
   return new DistData(2*sizeof(Coord) , buffer);
}



/*
Method ~DistDataReg::getDataHPoint~:

*/
DistData* DistDataReg::getDataHPoint(const void* attr)
{
    const HPointAttr *pAttr = static_cast<const HPointAttr*>(attr);
    HPoint *p = pAttr->hpoint();
    unsigned dim = p->dim();
    GTA_SPATIAL_DOM *coords = p->coords();
    char buffer[p->size()];
    memcpy(buffer, &dim, sizeof(unsigned));
    memcpy(buffer+sizeof(unsigned), coords, p->vectorlen());
    delete p;
    return new DistData(p->size(), buffer);
}

/*
Method ~DistDataReg::getDataString~:

*/
DistData* DistDataReg::getDataString(const void* attr)
{
    string value = static_cast<const CcString*>(attr)-> GetValue();
    return new DistData(value);
}

/*
Template Function ~DistDataReg::getDataSymTraj~:

*/
template<class M>
DistData* DistDataReg::getDataSymTraj(const void *attr) {
  char *bytes = 0;
  const M* traj = static_cast<const M*>(attr);
  size_t size;
  traj->serialize(size, bytes);
  DistData *result = new DistData(size, bytes);
  delete[] bytes;
  return result;
}



#ifndef NO_MP3
//----------------cru----------------
/*
Method ~DistDataReg::getDataFvector~:

*/
DistData* DistDataReg::getDataFVector(const void* attr){
  //cast to the correct type
  const FVector* fv = static_cast<const FVector*>(attr);

  //special treatment for undefined values
  if(!fv->IsDefined()){
    return new DistData(0,0);
  }

  //serialize the vector

  int dim = fv->getDim();

  char buffer[dim*sizeof(double)];

  for(int i=0; i<dim; i++){
    double elem = fv->getElem(i);
    memcpy(buffer+(i*sizeof(double)), &elem, sizeof(double));
  }
  return new DistData(dim*sizeof(double), buffer);
}

//-----------------------------------

#endif

/********************************************************************
Method ~DistDataReg::initialize~:

All avaliable distdata types must be registered in this method by calling the "addInfo"[4] method whith the respective "DistDataInfo" object. The parameter of the "DistDataInfo"[4] constructor have the following meaning:

  1 name of the distdata-type (unique for each type constructor)

  2 description of the distdata type

  3 id of the distdata type (unique for each defined distdata-type name)

  4 name of the assigned type constructor

  5 pointer to the respective getdata function

  6 flags (optional - currently no individual flags defined)

Constants for the name, description and type id's of the distdata-types are defined in "DistDataReg.h"[4].

*/
void DistDataReg::initialize()
{
    if (initialized)
        return;

    // the default DistDataInfo objects are automatically assigned,
    // depending on the default distance functions in the
    // DistfunReg class
#ifndef NO_MP3
//--------------------cru-------------------
    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
                         FVector::BasicType(), getDataFVector));
//------------------------------------------
#endif

#ifndef NO_IMAGESIMILARITY
    addInfo(DistDataInfo(
       DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
		FeatureSignaturealg::FeatureSignature::BasicType(), 
       getFeatureSignature));
#endif

    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
                         CcInt::BasicType(), getDataInt));

    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
                         CcReal::BasicType(), getDataReal));

    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
                         Points::BasicType(), getDataPoints));
    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
                         CcString::BasicType(), getDataString));

    addInfo(DistDataInfo(
       DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
       Point::BasicType(), getDataPoint));

    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
        "hpoint", getDataHPoint));

    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
        stj::MLabel::BasicType(), getDataSymTraj<stj::MLabel>));

    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
        stj::MLabels::BasicType(), getDataSymTraj<stj::MLabels>));

    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
        stj::MPlace::BasicType(), getDataSymTraj<stj::MPlace>));

    addInfo(DistDataInfo(
        DDATA_NATIVE, DDATA_NATIVE_DESCR, DDATA_NATIVE_ID,
        stj::MPlaces::BasicType(), getDataSymTraj<stj::MPlaces>));
        
 

    PictureFuns::initDistData();

    initialized = true;
}
