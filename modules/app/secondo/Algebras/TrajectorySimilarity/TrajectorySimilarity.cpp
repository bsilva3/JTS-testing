/*
----
This file is part of SECONDO.

Copyright (C) 2015, University in Hagen, Department of Computer Science,
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
//paragraph [1] Title: [{\Large \bf \begin{center}] [\end{center}}]
//paragraph [2] Filename: [{\tt \begin{center}] [\end{center}}]

[1] Trajectory Similarity Algebra

[2] TrajectorySimilarity.cpp

\tableofcontents

\noindent

1 Introduction

The Trajectory Similarity Algebra provides operators to measure the distance
or similarity of trajectories.

These similarity measures work on sequences of points or on sequences of tuples
of instants and points. Therefore this algebra provides the type constructors
~pointseq~ and ~tpointseq~. See the file {\tt PointSeq.cpp} for more
information.

The distance and similarity operators are implemented and described in detail in
the following files:

  * {\tt EndPointDistance.cpp}

    * ~dist\_origin~

    * ~dist\_destination~

    * ~dist\_origin\_and\_destination~

  * {\tt EuclideanDistance.cpp}

    * ~dist\_euclidean~

  * {\tt LCSS.cpp}

    * ~lcss~

    * ~rel\_lcss~

    * ~dist\_lcss~

  * {\tt LIPDistance.cpp}

    * ~dist\_lip~

    * ~dist\_stlip~

    * ~dist\_spstlip2~

    * ~genlip~

    * ~genlip2~

The classes, structs, and functions of this algebra reside in the C++ namespace
{\tt tsa} (short for Trajectory Similarity Algebra).

This file implements the class ~TrajectorySimilarityAlgebra~ that registers the
algebra's type constructors and operators with SECONDO. The type constructors
and operators themselves are implemented in separate files of this algebra.


2 Includes

*/

#include "TrajectorySimilarity.h"


namespace tsa {

/*
3 Implementation of Class ~TrajectorySimilarityAlgebra~

3.1 Constructor

*/

TrajectorySimilarityAlgebra::TrajectorySimilarityAlgebra()
  : Algebra()
{
/*
Register type constructors.

*/
  addPointSeqTC();
  addTPointSeqTC();

/*
Register operators.

*/
  addIsEmptyOp();
  addNoComponentsOp();
  addToDLineOp();
  addToPointSeqOp();
  addToTPointSeqOp();
  addSampleToPointSeqOp();
  addSampleToTPointSeqOp();

  addEndPointDistOp();
  addEuclideanDistOp();
  addLCSSOp();
  addLIPDistOp();
}

} //-- namespace tsa


/*
4 Initialize Algebra

*/

extern "C"
Algebra* InitializeTrajectorySimilarityAlgebra(
    NestedList* nlRef, QueryProcessor* qpRef)
{
  return new tsa::TrajectorySimilarityAlgebra;
}
