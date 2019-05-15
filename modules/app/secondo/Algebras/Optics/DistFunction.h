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
//characters   [1]  verbatim:  [$]  [$]
//characters   [2]  formula:  [$]  [$]
//characters   [3]  capital:  [\textsc{] [}]
//characters   [4]  teletype:  [\texttt{] [}]

1 Header file "DistFunction.h"[4]

March-October 2014, Marius Haug

1.1 Overview

This file contains the implementation of the distance function needed by the
MMMTree.
The classes ~DistCount~, ~IntDist~, ~PointDist~ and ~StringDist~ are orginally
from "MMRTreeAlgebra.cpp".

1.2 Includes

*/
#include <limits>
#include "Algebras/Spatial/Point.h"
#include "StandardTypes.h"
#include "StringUtils.h"
#include "Algebras/TupleIdentifier/TupleIdentifier.h"
#include "Algebras/GeneralTree/DistfunReg.h"
#include "Algebras/Picture/PictureAlgebra.h"

#ifndef OPTICS_DISTFUNCTION_H
#define OPTICS_DISTFUNCTION_H

namespace clusteropticsalg
{
/*
1.3 Declarations and definition of the class ~DistCount~

*/
 class DistCount
 {
  public: 
   DistCount() { cnt = 0; }
      
   void reset() { cnt =0; }

   size_t getCount() { return cnt; }

  protected:
   size_t cnt;
 };
/*
1.4 Declarations and definition of the class ~IntDist~

*/
 class IntDist: public DistCount
 {
  public:

   double operator()(const std::pair<CcInt*,TupleId>& p1
    ,const std::pair<CcInt*,TupleId>& p2)
   {
      return operator()(p1.first, p2.first);
   }

   double operator()(const CcInt* p1, const CcInt* p2){
    DistCount::cnt++;
    assert(p1);
    assert(p2);
  
    if(!p1->IsDefined() && !p2->IsDefined())
    {
     return 0;
    }
   
    if(!p1->IsDefined() || !p2->IsDefined())
    {
     return std::numeric_limits<double>::max();
    }
   
    int i1 = p1->GetValue();
    int i2 = p2->GetValue();
    int c = i1-i2;
   
    return c<0?-c:c;
   }

   std::ostream& print(const std::pair<CcInt*,TupleId>& p, std::ostream& o)
   {
    o << *(p.first);
    return o;
   }
 };
/*
1.5 Declarations and definition of the class ~RealDist~

*/
 class RealDist: public DistCount
 {
  public:

   double operator()(const std::pair<CcReal*,TupleId>& p1
    ,const std::pair<CcReal*,TupleId>& p2) {
     return operator()(p1.first, p2.first);
   }

   double operator()(const CcReal* p1, const CcReal* p2){
    DistCount::cnt++;
    assert(p1);
    assert(p2);
  
    if(!p1->IsDefined() && !p2->IsDefined())
    {
     return 0;
    }
   
    if(!p1->IsDefined() || !p2->IsDefined())
    {
     return std::numeric_limits<double>::max();
    }
   
    int i1 = p1->GetValue();
    int i2 = p2->GetValue();
    int c = i1-i2;
    return c<0?-c:c;
   }

   std::ostream& print(const std::pair<CcReal*,TupleId>& p, std::ostream& o)
   {
    o << *(p.first);
    return o;
   }
 };
/*
1.6 Declarations and definition of the class ~PointDist~

*/
 class PointDist: public DistCount
 {
  public:
  
   double operator()(const std::pair<Point*,TupleId>& p1
    ,const std::pair<Point*,TupleId>& p2) {
     return operator()(p1.first, p2.first);
   }

   double operator()(const Point* p1, const Point* p2){
    cnt++;
    assert(p1);
    assert(p2);
    
    if(!p1->IsDefined() && !p2->IsDefined())
    {
     return 0;
    }
    
    if(!p1->IsDefined() || !p2->IsDefined())
    {
     return std::numeric_limits<double>::max();
    }
    
    return p1->Distance(*(p2));
   }
     
   std::ostream& print(const std::pair<Point*,TupleId>& p, std::ostream& o)
   {
    o << *(p.first);
    return o;
   }
 };
/*
1.7 Declarations and definition of the class ~StringDist~

*/
 class StringDist: public DistCount
 {
  public:
  
   double operator()(const std::pair<CcString*,TupleId>& p1
    ,const std::pair<CcString*,TupleId>& p2) {
      return operator()(p1.first, p2.first);
   }

   double operator()(const CcString* p1, const CcString* p2){
    cnt++;
    assert(p1);
    assert(p2);
   
    if(!p1->IsDefined() && !p2->IsDefined())
    {
     return 0;
    }
    
    if(!p1->IsDefined() || !p2->IsDefined())
    {
     return std::numeric_limits<double>::max();
    }
    
    return stringutils::ld(p1->GetValue(), p2->GetValue());
   }
     
   std::ostream& print(const std::pair<CcString*,TupleId>& p, std::ostream& o)
   {
    o << *(p.first);
    return o;
   }
 };
/*
1.8 Declarations and definition of the class ~CustomDist~

*/ 
 template<class T, class R>
 class CustomDist: public DistCount
 { 
  private:
   QueryProcessor* qp;
   Supplier fun;
   ArgVectorPointer funargs;
 
  public:  
   void initialize(QueryProcessor* queryProcessor, Supplier function)
   {
    qp = queryProcessor;
    fun = function;
    funargs = qp->Argument(fun);
   }

   CustomDist(): qp(0), fun(0) { }

   CustomDist(QueryProcessor * _qp, Supplier _fun ): qp(_qp), fun(_fun){
      funargs = qp->Argument(fun);
   }

   CustomDist( const CustomDist& src): 
        qp(src.qp), fun(src.fun), funargs(src.funargs) {}

   CustomDist& operator=(const CustomDist& src){
      this->qp = src.qp;
      this->fun = src.fun;
      funargs = qp->Argument(fun);
      return *this; 
   }


   
   double operator()(const std::pair<T,TupleId>& p1 ,
                     const std::pair<T,TupleId>& p2) {
       return operator()(p1.first, p2.first);
    }
   
    double operator()(const T& p1, const T& p2){
    cnt++;
    assert(p1);
    assert(p2);

    

    if(!p1->IsDefined() && !p2->IsDefined())
    {
     return 0;
    }
    
    if(!p1->IsDefined() || !p2->IsDefined())
    {
     return std::numeric_limits<double>::max();
    }

    funargs = qp->Argument(fun);
    (*funargs)[0] = SetWord(p1);
    (*funargs)[1] = SetWord(p2); 
    
    Word funRes;
    qp->Request(fun, funRes);

    
    R* result;
    result = (R*) funRes.addr;

    if(!result->IsDefined()){
       return std::numeric_limits<double>::max();
    }

        
    double c = result->GetValue();

    return c < 0 ? -c : c;
   }
     
   std::ostream& print(const std::pair<T,TupleId>& p, std::ostream& o)
   {
    o << *(p.first);
    return o;
   }
 };

/*
1.8 Declarations and definition of the class ~TupleDist~

*/ 
template<class R>
class TupleDist: public DistCount {
  private:
  QueryProcessor* qp;
  Supplier fun;
  ArgVectorPointer funargs;
 
  public:
  TupleDist(): qp(0), fun(0) {}

  TupleDist(QueryProcessor * _qp, Supplier _fun) : qp(_qp), fun(_fun) {
    funargs = qp->Argument(fun);
  }

  void initialize(QueryProcessor* queryProcessor, Supplier function) {
    qp = queryProcessor;
    fun = function;
  }

  double operator() (const std::pair<Tuple*, TupleId>& p1,
                     const std::pair<Tuple*, TupleId>& p2) {
    return operator()(p1.first, p2.first);
  }

  double operator() (Tuple *t1, Tuple *t2) {
    cnt++;
    assert(t1);
    assert(t2);
    Word funRes;
    ArgVectorPointer vector;
    vector = qp->Argument(fun);
    ((*vector)[0]).setAddr(t1);
    ((*vector)[1]).setAddr(t2);
    qp->Request(fun, funRes);
    R* result;
    result = (R*)funRes.addr;
    return result->GetValue();
  }

  std::ostream& print(const std::pair<Tuple*, TupleId>& p, std::ostream& o) {
    o << *(p.first);
    return o;
  }
};

/*
1.9 Declarations and definition of the class ~PictureDist~

*/
 class PictureDist: public DistCount
 {
  private:
   bool init;
   gta::DistfunInfo df;
     
  public:
   
   PictureDist()
   {
    init = false;
   };
   
   double operator()(const std::pair<Picture*,TupleId>& p1
    ,const std::pair<Picture*,TupleId>& p2) {
     return operator()(p1.first, p2.first);
   }
   
   double operator()(const Picture* p1, const Picture* p2){
    cnt++;
    assert(p1);
    assert(p2);
   
    if(!p1->IsDefined() && !p2->IsDefined())
    {
     return 0;
    }
    
    if(!p1->IsDefined() || !p2->IsDefined())
    {
     return std::numeric_limits<double>::max();
    }
    
    if(!gta::DistfunReg::isInitialized())
    {
     gta::DistfunReg::initialize();
    }
    
    if(!init)
    {
     gta::DistDataId id = gta::DistDataReg::getId(Picture::BasicType()
      ,gta::DistDataReg::defaultName(Picture::BasicType()));
     
     df = gta::DistfunReg::getInfo(gta::DFUN_DEFAULT, id);
     
     init = true;
    }
    
    double distance;
    gta::DistData* d1 = df.getData(p1);
    gta::DistData* d2 = df.getData(p2);
    df.dist(d1,d2, distance);
    delete d1;
    delete d2; 
    return distance;
   }
     
   std::ostream& print(const std::pair<Picture*,TupleId>& p, std::ostream& o)
   {
    o << *(p.first);
    return o;
   }
 };

 template <unsigned int dim>
 class RectDist: public DistCount{
    public:
      double operator()(const Rectangle<dim>* r1, const Rectangle<dim>* r2){
         DistCount::cnt++;
         if(!r1->IsDefined() && !r2->IsDefined()){
           return 0;
         }
         if(!r1->IsDefined() || !r2->IsDefined()){
           return std::numeric_limits<double>::max();
         }
         return r1->Distance(*r2);
      } 
      double operator()(const std::pair<Rectangle<dim>*, TupleId>& p1,
                        const std::pair<Rectangle<dim>*, TupleId>& p2){
         return operator()(p1.first, p2.first);
      }
 };
 
 class MLabelDist: public DistCount {
  public:
   double operator()(const stj::MLabel* m1, const stj::MLabel* m2) {
     DistCount::cnt++;
     return m1->Distance(*m2);
   }
   
   double operator()(const std::pair<stj::MLabel*, TupleId>& p1,
                     const std::pair<stj::MLabel*, TupleId>& p2) {
     return operator()(p1.first, p2.first);
   }
   
   std::ostream& print(const std::pair<stj::MLabel*, TupleId>& p, 
                       std::ostream& o) {
     o << *(p.first);
     return o;
   }
 };
}

#endif


