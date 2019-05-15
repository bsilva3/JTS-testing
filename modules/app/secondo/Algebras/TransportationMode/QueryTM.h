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

//paragraph [1] Title: [{\Large \bf \begin {center}] [\end {center}}]
//[TOC] [\tableofcontents]

[1] Header File of the Transportation Mode Algebra

March, 2011 Jianqiu xu

[TOC]

1 Overview

2 Defines and includes

*/
#ifndef __QUERYTM_H__
#define __QUERYTM_H__

#include <fstream>
#include <stack>
#include <vector>
#include <queue>
#include "Attribute.h"
#include "Tools/Flob/DbArray.h"
#include "Algebras/Rectangle/RectangleAlgebra.h"
#include "WinUnix.h"
#include "AvlTree.h"
#include "Symbols.h"
#include "AlmostEqual.h"
#include "Algebras/Spatial/SpatialAlgebra.h"
#include "Algebras/Temporal/TemporalAlgebra.h"


#include "NestedList.h"

#include "QueryProcessor.h"
#include "Algebras/RTree/RTreeAlgebra.h"
#include "Algebras/BTree/BTreeAlgebra.h"
#include "Algebras/Temporal/TemporalAlgebra.h"
#include "StandardTypes.h"
#include "LogMsg.h"
#include "NList.h"
#include "Algebras/Relation-C++/RelationAlgebra.h"
#include "ListUtils.h"
#include "Algebras/Network/NetworkAlgebra.h"
#include "Algebras/Spatial/SpatialAlgebra.h"
#include "Partition.h"
#include "PaveGraph.h"
#include "Indoor.h"
#include "GeneralType.h"

/*
query processing on generic moving objects and data types 

*/
struct QueryTM{
  unsigned int count;
  TupleType* resulttype; 
  std::vector<Line> line_list1;
  std::vector<Line3D> line3d_list; 

  QueryTM(){ count = 0; resulttype = NULL;} 
  ~QueryTM(){if(resulttype != NULL) resulttype->DeleteIfAllowed();}
 
 
  ////////////////////////////////////////////////////////////////////////////
  //////////get 2D line in space or 3D line in a building///////////////////
  ////////////////////////////////////////////////////////////////////////////
  void GetLineOrLine3D(GenRange* gr, Space* sp);
  
  void GetLineInRoad(int , Line* l, Space* sp);
  void GetLineInRegion(int , Line* l, Space* sp);
  void GetLineInFreeSpace(Line* l);
  void GetLineInBusNetwork(int, Line* l, BusNetwork* bn);
  void GetLineInGRoom(int, Line* l, Space* sp);
};


#endif
