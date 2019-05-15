/*
----
This file is part of SECONDO.

Copyright (C) 2015, University if Hagen, 
Faculty of Mathematics and  Computer Science,
Database Systems for New Applications.

SECONDO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

SECONDO is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SECONDO; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
----


1 Alternative implementation of r tree based optics algorithm

Todo:
   Removing requirement that the complete input relation has to fit
   to the main memory.

*/

#include "OrderSeeds.h"
#include "Algebras/Rectangle/RectangleAlgebra.h"
#include "Algebras/Relation-C++/RelationAlgebra.h"
#include "Algebras/Stream/Stream.h"
#include "DistFunction.h"


#include "SetOfObjectsR.h"

#include <iostream>     
#include <algorithm>    
#include <vector>       

namespace clusteropticsalg
{

  // attribute type for clustering
  // Set of Objects
  // OrderSeeds
  // Distance function 

template< class T, class SoO, class DistFun>
class OpticsGen{

public:

typedef OrderSeeds<SoO> ORDERSEEDS;

/*

1.1 Constructor

*/   
   OpticsGen(Word _instream, int attrPos, double _eps, int _minPts,  
            double _UNDEFINED, ListExpr _resultType, 
            size_t maxMem, DistFun _distfun):
    minPts(_minPts),  
    UNDEFINED(_UNDEFINED), distfun(_distfun){
      Stream<Tuple> stream(_instream);
      setOfObjects = new SoO(stream, attrPos, _distfun, _eps,
                              maxMem, _resultType);
      orderSeeds = new ORDERSEEDS(setOfObjects, UNDEFINED);
      optics();
      setOfObjects->finish();
   }

/*
1.2 Destructor

*/

   ~OpticsGen(){
      delete setOfObjects;
      delete orderSeeds;
   }

/*
1.3 ~next~ function

Returns the next output tuple.

*/
   Tuple* next(){
      return setOfObjects->next();
   }

private:
   int minPts;
   SoO* setOfObjects;
   ORDERSEEDS* orderSeeds;
   double UNDEFINED;
   DistFun distfun;
   std::set<TupleId> deferred;

/*
1.5 main algorithm

*/

   void optics(){ // optics main loop
      GenericRelationIterator* it = setOfObjects->MakeScan();
      Tuple* tuple;
      while( ( tuple = it->GetNextTuple() )){
          TupleId id = it->GetTupleId();
          bool processed = setOfObjects->getProcessed(id);
          tuple->DeleteIfAllowed();
          if(!processed){
             expandCluster(id);
          }
      }
      delete it; 

      std::set<TupleId>::iterator itd;
      for(itd=deferred.begin(); itd!=deferred.end();itd++){
         TupleId object = *itd;
         setOfObjects->updateProcessed(object,true);
         setOfObjects->append(object);
      }
   }

/*
1.6 expandCluster

Puts new elements to a cluster

*/
   void expandCluster(TupleId object){
      Tuple* tuple = setOfObjects->GetTuple(object);
      std::list<TupleId>* neighbors = setOfObjects->getNeighbors(object);
      double coreDist = setCoreDistance(tuple, object, neighbors);

      if(coreDist != UNDEFINED){
         setOfObjects->updateReachability(object, UNDEFINED);
         setOfObjects->updateProcessed(object,true);
         orderSeeds->update(*neighbors, object);
         delete neighbors;    
         setOfObjects->append(object);
         while(!orderSeeds->empty()){
           TupleId currentId = orderSeeds->next();
           Tuple* curTup = setOfObjects->GetTuple(currentId);
           neighbors = setOfObjects->getNeighbors(currentId);
           setOfObjects->updateProcessed(currentId, true);
           coreDist = setCoreDistance(curTup, currentId, neighbors);
           setOfObjects->append(currentId);
           deferred.erase(currentId);
           if(coreDist != UNDEFINED){
              orderSeeds->update(*neighbors, currentId);
           }
           delete neighbors;
           curTup->DeleteIfAllowed();
         }
      } else { // no core point, try to process later
         delete neighbors;
         deferred.insert(object);
      }
      tuple->DeleteIfAllowed();
   }



/*
1.8 setCoreDistance

Computes the core distance of an element. 
The core distance is undefined of less than minPTs neighbors 
available, the distance to the min-pts neighbor (ordered by distance)
otherwise.

*/
  double setCoreDistance(Tuple* tuple, TupleId id, 
                         std::list<TupleId>* neighbors){
      if(neighbors->size() <(size_t) minPts){
          setOfObjects->updateCoreDistance(id, UNDEFINED);
          return UNDEFINED;
      }
      // find out the distance to the minPts't neighbor

      // maximum heap having exactly minPts entries
      // if the heap is full an a new entry shoul be inserted:
      // if the new entry is bigger than the stored maximum, ignore
      // otherwise replace the maximum value with the new value 
      // and let sink in this value
      double heap[minPts]; 
      std::list<TupleId>::iterator it;
      int entries = 0; 
      for(it= neighbors->begin(); it!=neighbors->end();it++){
         double dist = setOfObjects->distance(tuple, *it);
         if(entries < minPts){ // heap has capacity
            heap[entries] = dist;
            int son = entries+1;
            // let go up the new dist
            while(son > 1){
              int father = (son)/2;
              if(heap[father-1] < dist){
                 heap[son-1] = heap[father-1];
                 heap[father-1] = dist;
                 son = father; 
              } else {
                 break;
              }
            } 
            entries++;
         } else {
            if(dist < heap[0]){
               heap[0] = dist; // replace old maximum by new value
               int pos = 1;
               int s1 = pos * 2;
               int s2 = pos * 2+1;
               while(s1 <= minPts){ // there is at least one son
                   int s;
                   if(s2 <= minPts){
                      // get son with maximum value
                      s = heap[s1-1] < heap[s2-1] ? s2 : s1;
                   } else {
                      // there is only one son
                      s = s1;
                   }
                   if(heap[pos-1] < heap[s-1]){ // new value smaller than son
                      heap[pos-1] = heap[s-1];
                      heap[s-1] = dist;
                   } else {
                      // stop sinking
                      break;
                   }
                   pos = s;
                   s1 = pos * 2;
                   s2 = s1 + 1;
               }
            }
         } 
      } 
      setOfObjects->updateCoreDistance(id, heap[0]); 
      return heap[0];     
   }

};

} // end of namespace



