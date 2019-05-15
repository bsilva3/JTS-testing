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

[1] Implementation of the End-Point Distance Operators

[2] EndPointDistance.cpp

\tableofcontents

\noindent

1 Introduction

This file implements and registers end-point distance operators that have been
described as ~common origin~, ~common destination~, and ~common origin and
destination~ in \cite[section 3.3]{GNP+11}. These operators measure the distance
between the origin and destination points of two point sequences.


1.1 Operators

The operators

        $dist\_origin : SEQ \times SEQ\ [\times geoid] \rightarrow real$,
        \newline
        $dist\_destination : SEQ \times SEQ\ [\times geoid] \rightarrow real$,
        and\newline
        $dist\_origin\_and\_destination : SEQ \times SEQ\ [\times geoid]
        \rightarrow real$

with $SEQ \in \{pointseq,\ tpointseq\}$ measure the Euclidean distance between
specific 2-dimensional end-points of two point sequences of type ~SEQ~.

The temporal components of ~tpointseq~ objects are ignored. The computation
takes the ~geoid~ into account, if specified. If any of the two sequences is
~undefined~ or empty (i.e. it contains no point), the result is ~undefined~.

1.1.1 ~dist\_origin~

The operator ~dist\_origin~ measures the distance between the ~first~ points of
two point sequences.

1.1.2 ~dist\_destination~

The operator ~dist\_destination~ measures the distance between the ~last~ points
of two point sequences.

1.1.2 ~dist\_origin\_and\_destination~

The operator ~dist\_origin\_and\_destination~ measures the ~sum~ of the
distances between the first points and the last points of two point sequences.


2 Includes

*/

#include "PointSeq.h"
#include "TrajectorySimilarity.h"
#include "VectorTypeMapUtils.h"

#include "Algebras/Spatial/Geoid.h"
#include "QueryProcessor.h"


namespace tsa {

/*
3 Registration of Operators

3.1 Common Declarations

*/
template<class SEQ>
using end_point_op_type = double (*)(const SEQ&, const SEQ&, const Geoid*);

template<class SEQ, bool HAS_GEOID, end_point_op_type<SEQ> FUNC>
int EndPointDistValueMap(
    Word* args, Word& result, int /*message*/, Word& /*local*/, Supplier s);


/*
3.2 ~dist\_origin~

*/
template<class SEQ>
double dist_origin(const SEQ& seq1, const SEQ& seq2, const Geoid* geoid)
{
  const Point p1 = seq1.get(0);
  const Point p2 = seq2.get(0);
  return euclideanDistance(p1, p2, geoid);
}

ValueMapping dist_origin_functions[] = {
  EndPointDistValueMap<PointSeq,  /*HAS_GEOID*/ false, dist_origin>,
  EndPointDistValueMap<PointSeq,  /*HAS_GEOID*/ true,  dist_origin>,
  EndPointDistValueMap<TPointSeq, /*HAS_GEOID*/ false, dist_origin>,
  EndPointDistValueMap<TPointSeq, /*HAS_GEOID*/ true,  dist_origin>,
  nullptr
};

struct DistOriginInfo : OperatorInfo
{
  DistOriginInfo() : OperatorInfo()
  {
    name      = "dist_origin";
    signature = PointSeq::BasicType() + " x " + PointSeq::BasicType()
                + " -> " + CcReal::BasicType();
    appendSignature(
                PointSeq::BasicType() + " x " + PointSeq::BasicType() + " x "
                + Geoid::BasicType() + " -> " + CcReal::BasicType());
    appendSignature(
                TPointSeq::BasicType() + " x " + TPointSeq::BasicType()
                + " -> " + CcReal::BasicType());
    appendSignature(
                TPointSeq::BasicType() + " x " + TPointSeq::BasicType() + " x "
                + Geoid::BasicType() + " -> " + CcReal::BasicType());
    syntax    = "dist_origin(_, _[, _])";
    meaning   = "Euclidean distance between the two first points of the "
                "sequences. The geoid is taken into account, if specified. "
                "If any of the sequences is not defined or empty, the result "
                "is undefined.\n"
                "The time complexity is O(1).";
  }
};


/*
3.3 ~dist\_destination~

*/
template<class SEQ>
double dist_destination(const SEQ& seq1, const SEQ& seq2, const Geoid* geoid)
{
  const Point p1 = seq1.get(seq1.GetNoComponents() - 1);
  const Point p2 = seq2.get(seq2.GetNoComponents() - 1);
  return euclideanDistance(p1, p2, geoid);
}

ValueMapping dist_destination_functions[] = {
  EndPointDistValueMap<PointSeq,  /*HAS_GEOID*/ false, dist_destination>,
  EndPointDistValueMap<PointSeq,  /*HAS_GEOID*/ true,  dist_destination>,
  EndPointDistValueMap<TPointSeq, /*HAS_GEOID*/ false, dist_destination>,
  EndPointDistValueMap<TPointSeq, /*HAS_GEOID*/ true,  dist_destination>,
  nullptr
};

struct DistDestinationInfo : OperatorInfo
{
  DistDestinationInfo() : OperatorInfo()
  {
    name      = "dist_destination";
    signature = PointSeq::BasicType() + " x " + PointSeq::BasicType()
                + " -> " + CcReal::BasicType();
    appendSignature(
                PointSeq::BasicType() + " x " + PointSeq::BasicType() + " x "
                + Geoid::BasicType() + " -> " + CcReal::BasicType());
    appendSignature(
                TPointSeq::BasicType() + " x " + TPointSeq::BasicType()
                + " -> " + CcReal::BasicType());
    appendSignature(
                TPointSeq::BasicType() + " x " + TPointSeq::BasicType() + " x "
                + Geoid::BasicType() + " -> " + CcReal::BasicType());
    syntax    = "dist_destination(_, _[, _])";
    meaning   = "Euclidean distance between the two last points of the "
                "sequences. The geoid is taken into account, if specified. "
                "If any of the sequences is not defined or empty, the result "
                "is undefined.\n"
                "The time complexity is O(1).";
  }
};


/*
3.4 ~dist\_origin\_and\_destination~

*/
template<class SEQ>
double dist_origin_and_destination(
    const SEQ& seq1, const SEQ& seq2, const Geoid* geoid)
{
  const Point po1 = seq1.get(0);
  const Point po2 = seq2.get(0);
  const Point pd1 = seq1.get(seq1.GetNoComponents() - 1);
  const Point pd2 = seq2.get(seq2.GetNoComponents() - 1);
  return
      euclideanDistance(po1, po2, geoid) + euclideanDistance(pd1, pd2, geoid);
}

ValueMapping dist_origin_and_destination_functions[] = {
  EndPointDistValueMap<
      PointSeq,  /*HAS_GEOID*/ false, dist_origin_and_destination>,
  EndPointDistValueMap<
      PointSeq,  /*HAS_GEOID*/ true,  dist_origin_and_destination>,
  EndPointDistValueMap<
      TPointSeq, /*HAS_GEOID*/ false, dist_origin_and_destination>,
  EndPointDistValueMap<
      TPointSeq, /*HAS_GEOID*/ true,  dist_origin_and_destination>,
  nullptr
};

struct DistOriginAndDestinationInfo : OperatorInfo
{
  DistOriginAndDestinationInfo() : OperatorInfo()
  {
    name      = "dist_origin_and_destination";
    signature = PointSeq::BasicType() + " x " + PointSeq::BasicType()
                + " -> " + CcReal::BasicType();
    appendSignature(
                PointSeq::BasicType() + " x " + PointSeq::BasicType() + " x "
                + Geoid::BasicType() + " -> " + CcReal::BasicType());
    appendSignature(
                TPointSeq::BasicType() + " x " + TPointSeq::BasicType()
                + " -> " + CcReal::BasicType());
    appendSignature(
                TPointSeq::BasicType() + " x " + TPointSeq::BasicType() + " x "
                + Geoid::BasicType() + " -> " + CcReal::BasicType());
    syntax    = "dist_origin_and_destination(_, _[, _])";
    meaning   = "Arithmetic mean of the Euclidean distances between the two "
                "first points and the two last points of the sequences. "
                "The geoid is taken into account, if specified. "
                "If any of the sequences is not defined or empty, the result "
                "is undefined.\n"
                "The time complexity is O(1).";
  }
};


/*
3.5 Common Implementation

*/
const mappings::VectorTypeMaps end_point_dist_maps = {
  /*0*/ {{PointSeq::BasicType(), PointSeq::BasicType()},
    /* -> */ {CcReal::BasicType()}},
  /*1*/ {{PointSeq::BasicType(), PointSeq::BasicType(), Geoid::BasicType()},
    /* -> */ {CcReal::BasicType()}},
  /*2*/ {{TPointSeq::BasicType(), TPointSeq::BasicType()},
    /* -> */ {CcReal::BasicType()}},
  /*3*/ {{TPointSeq::BasicType(), TPointSeq::BasicType(), Geoid::BasicType()},
    /* -> */ {CcReal::BasicType()}}
};

ListExpr EndPointDistTypeMap(ListExpr args)
{ return mappings::vectorTypeMap(end_point_dist_maps, args); }

int EndPointDistSelect(ListExpr args)
{ return mappings::vectorSelect(end_point_dist_maps, args); }

template<class SEQ, bool HAS_GEOID, end_point_op_type<SEQ> FUNC>
int EndPointDistValueMap(
    Word* args, Word& result, int /*message*/, Word& /*local*/, Supplier s)
{
  const SEQ& seq1 = *static_cast<SEQ*>(args[0].addr);
  const SEQ& seq2 = *static_cast<SEQ*>(args[1].addr);
  const Geoid* geoid = HAS_GEOID ? static_cast<Geoid*>(args[2].addr) : nullptr;
  result = qp->ResultStorage(s);    // CcReal
  CcReal& dist = *static_cast<CcReal*>(result.addr);

/*
Require defined and non-empty sequences.

*/
  if (seq1.GetNoComponents() == 0 || seq2.GetNoComponents() == 0) {
    dist.SetDefined(false);
    return 0;
  }

  dist.Set(FUNC(seq1, seq2, geoid));
  return 0;
}

void TrajectorySimilarityAlgebra::addEndPointDistOp()
{
  AddOperator(
      DistOriginInfo(), dist_origin_functions,
      EndPointDistSelect, EndPointDistTypeMap);
  AddOperator(
      DistDestinationInfo(), dist_destination_functions,
      EndPointDistSelect, EndPointDistTypeMap);
  AddOperator(
      DistOriginAndDestinationInfo(), dist_origin_and_destination_functions,
      EndPointDistSelect, EndPointDistTypeMap);
}


} //-- namespace tsa

/*
\begin{thebibliography}{ABCD99}

\bibitem[GNP+11]{GNP+11}
Fosca Giannotti, Mirco Nanni, Dino Pedreschi, Fabio Pinelli, Chiara Renso,
  Salvatore Rinzivillo, and Roberto Trasarti.
\newblock {Unveiling the complexity of human mobility by querying and mining
  massive trajectory data}.
\newblock {\em {VLDB} J.}, 20(5): 695--719, 2011,
  http://dx.doi.org/10.1007/s00778-011-0244-8;
  http://dblp.uni-trier.de/rec/bib/journals/vldb/GiannottiNPPRRT11.

\end{thebibliography}

*/
