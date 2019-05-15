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

[1] Implementation of the Locality In-between Polylines (LIP) Operators

[2] LIPDistance.cpp

\tableofcontents

\noindent

1 Introduction

This file implements and registers distance operators for point sequences based
on the Locality In-between Polylines (LIP) measure defined in \cite{PKM+07}.

The basic idea of the LIP operators is to measure the area of the shape formed
by the two sequences, if their first points are connected and their last points
are connected to close the shape.

As \cite{PKM+07} points out, the LIP measures work correctly for point sequences
that follow a stable trend with no dramatic rotations. Below such pair of
sequences is called ~well-formed~. With other pairs of sequences the LIP
measures may yield self-intersecting polygons that can render the distance
measure meaningless or indefinite. The separate ~GenLIP~ algorithm searches a
pair of sequences for bad segments and feeds the ~well-formed~ parts into one of
the LIP operators.


1.1 Operators

1.1.1 ~dist\_lip~

The operator

        $dist\_lip : SEQ \times SEQ \rightarrow real$

with $SEQ \in \{pointseq,\ tpointseq\}$ determines the Locality In-between
Polylines distance for a pair of ~well-formed~ point sequences $P,\ Q$ of type
~SEQ~. If the pair of sequences is not ~well-formed~, the result is indefinite.

The LIP distance $D_{LIP}(P,\ Q)$ is defined as the sum of the weighted areas of
the polygons defined by the intersection points of the two sequences $P,\ Q$.

$$D_{LIP}(P,\ Q) = \sum_{\forall\ p\ \in\ Polygons} lip(p)$$

$$lip(p) = area(p) \cdot weight(p)$$

The weight of a polygon is defined as the length of the portions of the
sequences $P,\ Q$ that participate in the construction of the polygon divided by
the total length of the sequences.

$$weight(p) = \frac{length(Q|_{p}) + length(P|_{p})}{length(Q) + length(P)}$$

The temporal components of ~tpointseq~ objects are ignored. If any of the two
sequences is ~undefined~ or contains less than two points, the result is
~undefined~.

The worst-case time complexity of the operator in the present implementation is
$\mathcal{O}(n^2)$ and the space complexity is $\mathcal{O}(n)$, where $n$ is
the total number of points in the sequences. The time complexity can be improved
to $\mathcal{O}(n \log n)$ according to \cite{PKM+07}.


1.1.2 ~dist\_stlip~

The operator

        $dist\_stlip : tpointseq \times tpointseq \times real \times duration
        \rightarrow real$

with $dist\_stlip(P, Q, st\_factor, \delta)$ determines the Spatio-temporal
Locality In-between Polylines (STLIP) distance for a pair of ~well-formed~
~tpointseq~ objects $P,\ Q$, a non-negative ~st\_factor~, and a non-negative
duration $\delta$. If the pair of sequences is not ~well-formed~, the result is
indefinite.

STLIP extends LIP by multiplying each weighted polygon area with a factor that
measures the temporal dissimilarity of the two portions of the two sequences
that contribute to the polygon.

$$D_{STLIP}(P,\ Q,\ \delta) = \sum_{\forall\ p\ \in\ Polygons}
stlip(p, \delta)$$

$$stlip(p,\ \delta) = lip(p) \cdot (1 + st\_factor \cdot tlip(p, \delta))$$

$$tlip(p,\ \delta) = \left| 1 - \frac{2 \cdot mdi(p, \delta)}{duration(P) +
duration(Q)} \right|$$

$mdi(p, \delta)$ is the maximum duration of the temporal element that is the
outcome of the intersection between $P|_p$ and either

  * $Q|_p$,

  * $Q|_p$ extended towards the future by $\delta$, or

  * $Q|_p$ extended towards the past by $\delta$.

If the portions of $P, Q$ that contribute to a polygon $p$ cover the same time
interval within the tolerance $\delta$, they have highest similarity and thus
a low $tlip(p)$. $st\_factor$ controls how much the temporal dissimilarity
affects the result. With $st\_factor = 0$, STLIP yields the same result as LIP.

If any of the sequences is undefined or has less than two points or if
~st\_factor~ or $\delta$ is negative, the result is ~undefined~.

\cite{PKM+07} defines that STLIP first restricts the original sequences to the
common temporal element and then uses the ~GenLIP~ algorithm to filter out bad
segments. This is not implemented here.

Time and space complexity are the same as for the operator ~dist\_lip~ with
higher constants for the time complexity.


1.1.3 ~dist\_spstlip2~

The operator

        $dist\_spstlip2 : tpointseq \times tpointseq \times real \times duration
        \times real \rightarrow real$

with $dist\_spstlip2(P, Q, st\_factor, \delta, sp\_factor)$ determines the
experimental Speed-pattern Spatio-temporal Locality In-between Polylines
(SPSTLIP2) distance for a pair of ~well-formed~ ~tpointseq~ objects $P,\ Q$, a
non-negative ~st\_factor~, a non-negative duration $\delta$, and a non-negative
~sp\_factor~. If the pair of sequences is not ~well-formed~, the result is
indefinite.

SPSTLIP2 extends STLIP by multiplying each STLIP polygon value with a factor
that measures the dissimilarity in the velocity of the two sequences on the
polygon. ~sp\_factor~ controls how much the differences in the velocities affect
the result.

$$D_{SPSTLIP2}(P,\ Q,\ \delta) = \sum_{\forall\ p\ \in\ Polygons} spstlip2(p,
\delta)$$

$$spstlip2(p,\ \delta) = stlip(p, \delta) \cdot (1 + sp\_factor \cdot
splip2(p))$$

$$splip2(p) = \left| 1 - \frac{2 \cdot speed(P|_p)}{speed(P|_p) + speed(Q|_p)}
\right|$$

$speed(P|_p)$ measure the speed of the portion of sequence $P$ that contributes
to the polygon $p$. With $sp\_factor = 0$, SPSTLIP2 yields the same result as
STLIP.

If any of the sequences is ~undefined~ or has less than two points or if
~st\_factor~, or $\delta$, or ~sp\_factor~ is negative, the result is
~undefined~.

\cite{PKM+07} defines a measure called SPSTLIP that also factors the speed
pattern into the calculation, but that measure is only useful if the sequences
have a common temporal element per polygon. In contrast, the experimental
measure SPSTLIP2 implemented here, is not affected by temporal shifts of the
sequences.

In addition, SPSTLIP would use the ~GenLIP~ algorithm to filter out bad
segments. This is not implemented here.

Time and space complexity are the same as for the operator ~dist\_stlip~ with
higher constants for the time complexity.


1.1.4 ~genlip~

The operator

        $genlip : SEQ \times SEQ \times int \times (SEQ \times SEQ \rightarrow
        real) \rightarrow real$

with $genlip(P, Q, max\_gap\_size, function)$ and $SEQ \in \{pointseq,\
tpointseq\}$ performs the ~GenLIP~ algorithm on the two sequences. It searches
the point sequences for series of $max\_gap\_size$ or more bad segments and
feeds only the remaining (~well-formed~) parts into the $function$. The
accumulated results of the $function$ are returned. If the two sequences contain
no ~well-formed~ part, the result is ~undefined~.

As the original ~GenLIP~ algorithm, this operator processes only the minimum
number of segments of both sequences and ignores additional segments of the
longer sequence.

The time complexity of the ~GenLIP~ algorithm itself is $\mathcal{O}(n)$ (not
including the runtime of the $function$), where $n$ is the total number of
points in the sequences.


1.1.5 ~genlip2~

The operator

        $genlip2 : SEQ \times SEQ \times int \times (SEQ \times SEQ \rightarrow
        real) \rightarrow real$

is a variant of the $genlip$ operator. Deviating from the original specification
of the ~GenLIP~ algorithm, $genlip2$ also processes additional segments of the
longer sequence.


2 Includes

*/

#include <memory>

#include "PointSeq.h"
#include "Segment.h"
#include "TrajectorySimilarity.h"
#include "VectorTypeMapUtils.h"

#include "DateTime.h"         // DateTime, Instant
#include "Algebras/Spatial/RegionTools.h" 
#include "Algebras/Spatial/SpatialAlgebra.h"  
#include "Algebras/Temporal/TemporalAlgebra.h"  


namespace tsa {

/*
3 LIP Algorithms

3.1 Struct ~Polygon~

Struct representing a polygon with some properties needed for the calculation of
LIP and STLIP measures.

*/
struct Polygon
{
  Polygon(const Region &&region, const double length)
    : region(region), length(length) { }

/*
A ~Region~ object of the SpatialAlgebra representing the polygon's shape.

*/
  const Region region;

/*
The length of the portions of the original sequences that participate in the
construction of the polygon.

*/
  const double length;

/*
For STLIP: Maximum duration of the temporal element of the polygon as defined in
\cite[sect.\ 4]{PKM+07}.

*/
  datetime::DateTime mdi{datetime::durationtype};

/*
For SPSTLIP2: Dissimilarity of velocities of the two sequences on the polygon.

*/
  double splip = 0.0;
};


/*
3.2 Function Template ~dist\_lip~

This function template implements the LIP measures for two point sequences, each
with at least two points (i.\ e.\ one segment).

The aggregator ~agg~ of class ~AGG~ performs the operations that are specific
to the LIP, STLIP, or SPSTLIP2 distance measure. It maintains two lists of
points, $list1$ and $list2$, and a list of polygons.

*/
template<class SEQ, class AGG>
double dist_lip(AGG&& agg, const SEQ& seq1, const SEQ& seq2)
{
/*
The first segment on the second sequence that has not yet been included in a
polygon.

*/
  SegmentIt<SEQ> sit2mark = SegmentIt<SEQ>::begin(seq2);

/*
One past the end segment iterators for the sequences.

*/
  const SegmentIt<SEQ> sit1end = SegmentIt<SEQ>::end(seq1);
  const SegmentIt<SEQ> sit2end = SegmentIt<SEQ>::end(seq2);

/*
Iterate all segments of the first sequence.

*/
  for (SegmentIt<SEQ> sit1 = SegmentIt<SEQ>::begin(seq1);
       sit1 != sit1end; ++sit1)
  {
/*
Add the start point of the current segment of the first sequence to $list1$.

*/
    agg.list1Add(sit1->getStart());

/*
Iterate the segments of the second sequence starting at $sit2mark$.

*/
    for (SegmentIt<SEQ> sit2 = sit2mark; sit2 != sit2end; ++sit2)
    {
/*
Test if the current segments intersect and if so, determine the point where they
cross.

*/
      Point cross(0.0, 0.0);
      if (agg.testIntersection(*sit1, *sit2, cross)) {
/*
The segments intersect at $cross$. First, add the start point of each segment
between $sit2mark$ and the current segment on the second sequence to $list2$.

*/
        for (SegmentIt<SEQ> sit2b = sit2mark; sit2b != sit2 + 1; ++sit2b)
          agg.list2Add(sit2b->getStart());

/*
Determine the ~Point~ or ~TPoint~ objects where the segments meet and add them
to the point lists. For LIP $cross1$ and $cross2$ are the same as $cross$. For
STLIP the instants of $cross1$ and $cross2$ indicate when the segment passes the
intersection.

*/
        const auto cross1 = agg.getCross(*sit1, cross);
        const auto cross2 = agg.getCross(*sit2, cross);
        agg.list1Add(cross1);
        agg.list2Add(cross2);
/*
Close the polygon and add it to the list of polygons. Clear the point lists and
start a new polygon at the intersection points. Move $sit2mark$ just after the
last segment of the second sequence that was processed. Leave the inner loop.

*/
        agg.addPolygon(agg.closePolygon());
        agg.reset();
        agg.list1Add(cross1);
        agg.list2Add(cross2);
        sit2mark = sit2 + 1;
        break;
      }
    }
  }

/*
There were no more intersections. Add the start points of the remaining segments
between $sit2mark$ and the end of the second sequence to $list2$. Add the end
points of the two sequences to the point lists. Close the last polygon and add
it to the list of polygons.

*/
  for (SegmentIt<SEQ> sit2b = sit2mark; sit2b != sit2end; ++sit2b)
    agg.list2Add(sit2b->getStart());
  agg.list1Add((sit1end-1)->getEnd());
  agg.list2Add((sit2end-1)->getEnd());
  agg.addPolygon(agg.closePolygon());

/*
Perform final computations.

*/
  agg.finalize();

/*
If the total length of the two sequences on the polygons is 0, we cannot weight
the areas of the polygons. Instead, we return a LIP distance of 0, assuming that
the polygon areas are also empty.

*/
  if (agg.empty())
    return 0.0;

/*
Sum up the distance values of the polygons.

*/
  double dist = 0.0;
  for (const Polygon &polygon : agg.getPolygons())
    dist += agg.getDist(polygon);
  return dist;
}


/*
3.2 Aggregator Class for LIP

*/
template<class SEQ>
class LIPAggregator
{
public:
  using segment_t = Segment<typename SEQ::point_t>;

  LIPAggregator() { }

  void list1Add(const Point& pt)
  {
    if (!list1.empty())
      len1 += euclideanDistance(list1.back(), pt);
    list1.push_back(pt);
  }

  void list2Add(const Point& pt)
  {
    if (!list2.empty())
      len2 += euclideanDistance(list2.front(), pt);
    list2.push_front(pt);
  }

  static bool testIntersection(
      const segment_t& seg1, const segment_t& seg2, Point& cross)
  { return intersection(seg1, seg2, cross); }

  const Point getCross(const segment_t& /*seg*/, const Point& cross)
  { return cross; }

  std::unique_ptr<Polygon> closePolygon()
  {
    const double length = len1 + len2;
    total_length += length;

    list1.splice(list1.end(), list2);
    std::unique_ptr<Region> region = createRegion(list1);
    if (!region)
      return nullptr;

    return std::unique_ptr<Polygon>(new Polygon(std::move(*region), length));
  }

  void addPolygon(std::unique_ptr<Polygon> polygon)
  {
    if (polygon)
      polygons.push_back(std::move(*polygon.release()));
  }

  void reset()
  {
    list1.clear();
    list2.clear();
    len1 = 0.0;
    len2 = 0.0;
  }

  void finalize() { }

  bool empty() const
  { return total_length == 0.0; }

  const std::list<Polygon>& getPolygons() const
  { return polygons; }

  inline double getDist(const Polygon& polygon) const
  {
    const double area = polygon.region.Area();
    const double weight = polygon.length / total_length;
    const double lip = area * weight;
    return lip;
  }

private:
/*
Create a ~Region~ object from a list of points.

*/
  static std::unique_ptr<Region> createRegion(const std::list<Point> &points)
  {
/*
Create a cycle of points. In the worst case, that cycle has one more point than
the original list of points, where the additional point is used to close the
cycle. ~std::list::size()~ has $\mathcal{O}(1)$ complexity in C++11.

*/
    std::vector<::Point> cycle;
    cycle.reserve(points.size() + 1);

/*
Copy the points to the cycle, but skip duplicates.

*/
    for (const Point &tsa_pt : points) {
      const ::Point pt(tsa_pt.toSAPoint());
      if (cycle.size() != 0 && AlmostEqual(pt, cycle.back()))
        continue;
      cycle.push_back(pt);
    }

/*
Close the cycle, if needed.

*/
    if (cycle.size() > 1 && !AlmostEqual(cycle.front(), cycle.back()))
      cycle.push_back(cycle.front());

/*
Do not keep a polygon, whose area is apparently empty. The first and the last
point of the cycle are always the same. Therefore at least four points are
needed to make up a non-empty area.

*/
    if (cycle.size() < 4)
      return nullptr;

/*
Force clockwise order of cycle, so that it makes a face of the region.

*/
    if (!getDir(cycle))
      reverseCycle(cycle);

/*
Create and return the region.

The LIP algorithm can produce a list of points that wrongly appears as a hole to
the ~RegionCreator~ and triggers an exception in its method
~findLeftNearestOuter()~ (throwing a ~std::string~). Therefore exception
handling is used to silently ignore such cases.

*/
    std::vector<std::vector<::Point>> cycles;
    cycles.push_back(std::move(cycle));
    try {
      std::unique_ptr<Region> region(buildRegion(cycles));
      return region;
    }
    catch (const std::string& str) {
      return nullptr;
    }
  }

protected:
  std::list<Point> list1;
  std::list<Point> list2;
  double len1 = 0.0;
  double len2 = 0.0;

private:
  double total_length = 0.0;
  std::list<Polygon> polygons;
};


/*
3.3 Aggregator Class for STLIP

*/
class STLIPAggregator : public LIPAggregator<TPointSeq>
{
public:
  using Base = LIPAggregator<TPointSeq>;
  using Interval = temporalalgebra::Interval<Instant>;
  using DateTime = datetime::DateTime;

  STLIPAggregator(const double st_factor, const DateTime& delta)
    : LIPAggregator(),
      st_factor(st_factor), delta(delta)
  { }

  void list1Add(const TPoint& pt)
  {
    if (list1.empty()) {
      list1_iv.start = pt.getInstant();
      if (getPolygons().empty())
        seq1_iv.start = pt.getInstant();
    }
    list1_iv.end = pt.getInstant();
    seq1_iv.end = pt.getInstant();
    Base::list1Add(pt);
  }

  void list2Add(const TPoint& pt)
  {
    if (list2.empty()) {
      list2_iv.start = pt.getInstant();
      if (getPolygons().empty())
        seq2_iv.start = pt.getInstant();
    }
    list2_iv.end = pt.getInstant();
    seq2_iv.end = pt.getInstant();
    Base::list2Add(pt);
  }

  const TPoint getCross(const Segment<TPoint>& seg, const Point& cross)
  {
    const double bc = seg.baryCoord(cross);
    const DateTime duration =
        seg.getEnd().getInstant() - seg.getStart().getInstant();
    const Instant t = seg.getStart().getInstant() + (duration * bc);
    return TPoint(t, cross);
  }

  std::unique_ptr<Polygon> closePolygon()
  {
    std::unique_ptr<Polygon> polygon = Base::closePolygon();
    if (!polygon)
      return nullptr;

    if (st_factor != 0.0) {
      Interval iv_a = list2_iv;
      Interval iv_b(list2_iv.start,         list2_iv.end + delta, true, false);
      Interval iv_c(list2_iv.start - delta, list2_iv.end,         true, false);

      DateTime mdi(datetime::durationtype, 0);
      if (iv_a.Intersects(list1_iv)) {
        iv_a.IntersectionWith(list1_iv);
        mdi = iv_a.end - iv_a.start;
      }
      if (iv_b.Intersects(list1_iv)) {
        iv_b.IntersectionWith(list1_iv);
        mdi = std::max(mdi, iv_b.end - iv_b.start);
      }
      if (iv_c.Intersects(list1_iv)) {
        iv_c.IntersectionWith(list1_iv);
        mdi = std::max(mdi, iv_c.end - iv_c.start);
      }

      polygon->mdi = mdi;
    }

    return polygon;
  }

  void finalize()
  {
    total_duration =
        (seq1_iv.end - seq1_iv.start) + (seq2_iv.end - seq2_iv.start);
  }

  inline double getDist(const Polygon& polygon) const
  {
    const double lip = Base::getDist(polygon);
    if (st_factor != 0.0) {
      const double tlip =
          fabs(1.0 - (2.0 *
              (polygon.mdi.ToDouble() / total_duration.ToDouble())));
      const double stlip = lip * (1.0 + (st_factor * tlip));
      return stlip;
    }
    else
      return lip;
  }

protected:
  Interval list1_iv{Instant(), Instant(), /*lc*/ true, /*rc*/ false};
  Interval list2_iv{Instant(), Instant(), /*lc*/ true, /*rc*/ false};

private:
  const double st_factor;
  const DateTime& delta;

  Interval seq1_iv{Instant(), Instant(), /*lc*/ true, /*rc*/ false};
  Interval seq2_iv{Instant(), Instant(), /*lc*/ true, /*rc*/ false};

  DateTime total_duration{datetime::durationtype};
};


/*
3.4 Aggregator Class for SPSTLIP2

*/
class SPSTLIP2Aggregator : public STLIPAggregator
{
public:
  using Base = STLIPAggregator;

  SPSTLIP2Aggregator(
      const double st_factor, const DateTime& delta, const double sp_factor)
    : STLIPAggregator(st_factor, delta), sp_factor(sp_factor)
  { }

  std::unique_ptr<Polygon> closePolygon()
  {
    std::unique_ptr<Polygon> polygon = Base::closePolygon();
    if (!polygon)
      return nullptr;

    if (sp_factor != 0.0) {
      const double speed1 = len1 / (list1_iv.end - list1_iv.start).ToDouble();
      const double speed2 = len2 / (list2_iv.end - list2_iv.start).ToDouble();
      const double splip = fabs(1.0 - (2.0 * speed1 / (speed1 + speed2)));
      polygon->splip = splip;
    }

    return polygon;
  }

  inline double getDist(const Polygon& polygon) const
  {
    const double stlip = Base::getDist(polygon);
    if (sp_factor != 0.0)
      return stlip * (1.0 + (sp_factor * polygon.splip));
    else
      return stlip;
  }

private:
  const double sp_factor;
};



/*
4 GenLIP Algorithm

4.1 LIP Criterion

Test if the segment between two two end points crosses any of the preceding
segments.

*/
template<class SEQ>
static bool bad_end_segment(
    const SegmentIt<SEQ> &sit1begin, const SegmentIt<SEQ> &sit1last,
    const SegmentIt<SEQ> &sit2begin, const SegmentIt<SEQ> &sit2last)
{
/*
If both sequences contain just one segment, there is nothing the segment
between the end points could intersect.

*/
  if (sit1begin == sit1last && sit2begin == sit2last)
    return false;

/*
According to \cite{PKM+07}, "the effect of the bad segments is local and can be
treated by testing only a small number of segments for intersection." This
implementation arbitrarily uses 3 as that small number.

*/
  const std::size_t max_look_back = 3;

/*
Create the segment that is defined by the end points of the two sequences.

*/
  const Segment<typename SEQ::point_t> seg(
      sit1last->getEnd(), sit2last->getEnd());

/*
Iterate segments in reverse order starting at the next to the last segment of
each sequence. If the end segment crosses any the the preceding segments, report
the end segment as ~bad~.

*/
  SegmentIt<SEQ> sit1 = sit1last - 1;
  SegmentIt<SEQ> sit2 = sit2last - 1;

  for (std::size_t look_back = 0;
       look_back < max_look_back;
       ++look_back, --sit1, --sit2)
  {
    Point cross(0.0, 0.0);
    if (intersection(seg, *sit1, cross) ||
        intersection(seg, *sit2, cross))
    {
      return true;
    }

    if (sit1 == sit1begin || sit2 == sit2begin)
      break;
  }

/*
No intersection found. Report the end segment as ~good~.

*/
  return false;
}


/*
4.2 Call Function

Call the specified function for the two subsequences.

*/
template<class SEQ>
bool call_function(
    const SegmentIt<SEQ>& sit1begin, const SegmentIt<SEQ>& sit1end,
    const SegmentIt<SEQ>& sit2begin, const SegmentIt<SEQ>& sit2end,
    void* function, double& res)
{
  SEQ seq1(sit1begin, sit1end);
  SEQ seq2(sit2begin, sit2end);

  ArgVector& args = *qp->Argument(function);
  args[0].setAddr(&seq1);
  args[1].setAddr(&seq2);

  Word w;
  qp->Request(function,w);
  const CcReal& cc_real = *static_cast<CcReal*>(w.addr);

  const bool defined = cc_real.IsDefined();
  if (defined)
    res += cc_real.GetValue();

  return defined;
}


/*
4.3 GenLIP

This implementation of the ~GenLIP~ algorithm unwinds the recursion (line 23)
and the inner loop (lines 9-14) of the original algorithm. To do this it keeps
track of subsequences of ~good~ segments and of the size of the current gap.
Once the current gap exceeds the maximum gap size, the $function$ is calculated
for the subsequences and new subsequences are started just after the gap.

As the original ~GenLIP~ algorithm, by default this implementation processes
only the minimum number of segments of both sequences and ignores additional
segments of the longer sequence. If the template parameter ~PROCESS\_ALL~ is set
to ~true~, additional segments of the longer sequence are also processed.

*/
template<class SEQ, bool PROCESS_ALL=false>
void genlip(
    const SEQ& seq1, const SEQ& seq2, const std::size_t max_gap_size,
    void* function, CcReal& result)
{
  result.SetDefined(false);

  SegmentIt<SEQ> sit1 = SegmentIt<SEQ>::begin(seq1);
  SegmentIt<SEQ> sit2 = SegmentIt<SEQ>::begin(seq2);
  const SegmentIt<SEQ> sit1end = SegmentIt<SEQ>::end(seq1);
  const SegmentIt<SEQ> sit2end = SegmentIt<SEQ>::end(seq2);

/*
If any of the sequences is empty, there are no ~well-formed~ parts to find.

*/
  if (sit1 == sit1end || sit2 == sit2end)
    return;

/*
Iterators for the current subsequences of ~good~ segments.

*/
  SegmentIt<SEQ> sub1begin = sit1;
  SegmentIt<SEQ> sub2begin = sit2;
  SegmentIt<SEQ> sub1end = sit1;
  SegmentIt<SEQ> sub2end = sit2;

/*
Current size of gap.

*/
  std::size_t gap_size = 0;

/*
Keep track whether at least one subsequence of ~good~ parts exists and has a
defined result value.

*/
  bool defined = false;

/*
Accumulator for result values.

*/
  double acc = 0.0;

  do {
/*
(GenLIP lines 1-2, 19)

Check for exceeded maximum gap size.

*/
    if (gap_size > max_gap_size) {
/*
(GenLIP lines 15-17, 20-23)

Add the result for the subsequences of ~good~ segments just before the gap and
start new subsequences just after the gap.

*/
      defined |= call_function(
          sub1begin, sub1end, sub2begin, sub2end, function, acc);
/*
(lines 21-22)

*/
      sub1begin = sit1;
      sub2begin = sit2;
      sub1end = sit1;
      sub2end = sit2;
/*
(line 23)

*/
      gap_size = 0;
    }

/*
Check the current pair of segments.

*/
    if (gap_size == 0) {
/*
(GenLIP lines 3-8)

Iterating ~good~ segments, so far.

*/
      Point cross(0.0, 0.0);
      if (intersection(*sit1, *sit2, cross) ||
          !bad_end_segment(sub1begin, sit1, sub2begin, sit2))
      {
/*
(GenLIP lines 3-6)

Current segments contribute to subsequnces of ~good~ segments.

*/
        sub1end = sit1 + 1;
        sub2end = sit2 + 1;

      } else {
/*
(GenLIP lines 7-8)

The begin of a gap was found.

*/
        gap_size = 1;
      }

    } else {
/*
(GenLIP lines 9-14)

Iterating ~bad~ segments in a gap.

*/
      if (!bad_end_segment(sub1begin, sit1, sub2begin, sit2))
      {
/*
(GenLIP lines 10-13)

Current segments finish the gap, so the gap segments contribute to subsequnces
of ~good~ segments.

*/
        sub1end = sit1 + 1;
        sub2end = sit2 + 1;
        gap_size = 0;

      } else {
/*
(GenLIP lines 9, 14)

Current segments are ~bad~ and contribute to the gap.

*/
        ++gap_size;
      }
    }

  } while (++sit1 != sit1end && ++sit2 != sit2end);


/*
Variant ~PROCESS\_ALL~: Also process additional segments of the longer sequence.

*/
  if (PROCESS_ALL) {
    sub1end = sit1end;
    sub2end = sit2end;
  }

/*
(GenLIP lines 20)

Add the result for the last subsequence of ~good~ segments.

*/
  defined |= call_function(
      sub1begin, sub1end, sub2begin, sub2end, function, acc);

  if (defined)
    result.Set(acc);
}



/*
5 Registration of Operators

5.1 ~dist\_lip~

*/
template<class SEQ>
int LIPDistValueMap(
    Word* args, Word& result, int /*message*/, Word& /*local*/, Supplier s)
{
  const SEQ& seq1 = *static_cast<SEQ*>(args[0].addr);
  const SEQ& seq2 = *static_cast<SEQ*>(args[1].addr);
  result = qp->ResultStorage(s);    // CcReal
  CcReal& dist = *static_cast<CcReal*>(result.addr);

/*
Require defined sequences with at least two points each.

*/
  if (seq1.GetNoComponents() < 2 || seq2.GetNoComponents() < 2) {
    dist.SetDefined(false);
    return 0;
  }

  LIPAggregator<SEQ> agg;
  dist.Set(dist_lip(agg, seq1, seq2));
  return 0;
}

ValueMapping dist_lip_functions[] = {
  LIPDistValueMap<PointSeq>,
  LIPDistValueMap<TPointSeq>,
  nullptr
};

struct DistLIPInfo : OperatorInfo
{
  DistLIPInfo() : OperatorInfo()
  {
    name      = "dist_lip";
    signature = PointSeq::BasicType() + " x " + PointSeq::BasicType()
                + " -> " + CcReal::BasicType();
    appendSignature(
                TPointSeq::BasicType() + " x " + TPointSeq::BasicType()
                + " -> " + CcReal::BasicType());
    syntax    = "dist_lip(_, _[, _])";
    meaning   = "Locality In-between Polylines (LIP) distance of a well-formed "
                "pair of point sequences. LIP is defined as the sum of the "
                "weighted areas of the polygons defined by the intersection "
                "points of the two sequences. If the pair of sequences is not "
                "well-formed, the result is indefinite.\n"
                "If any of the sequences is undefined or has less than two "
                "points, the result is undefined.\n"
                "The worst-case time complexity of the operator in the present "
                "implementation is O(n^2) and the space complexity is O(n), "
                "where n is the total number of points in the sequences.";
  }
};

const mappings::VectorTypeMaps dist_lip_maps = {
  /*0*/ {{PointSeq::BasicType(), PointSeq::BasicType()},
    /* -> */ {CcReal::BasicType()}},
  /*1*/ {{TPointSeq::BasicType(), TPointSeq::BasicType()},
    /* -> */ {CcReal::BasicType()}}
};

ListExpr DistLIPTypeMap(ListExpr args)
{ return mappings::vectorTypeMap(dist_lip_maps, args); }

int DistLIPSelect(ListExpr args)
{ return mappings::vectorSelect(dist_lip_maps, args); }


/*
5.2 ~dist\_stlip~

*/
int STLIPDistValueMap(
    Word* args, Word& result, int /*message*/, Word& /*local*/, Supplier s)
{
  const TPointSeq& seq1 = *static_cast<TPointSeq*>(args[0].addr);
  const TPointSeq& seq2 = *static_cast<TPointSeq*>(args[1].addr);
  const CcReal& cc_st_factor = *static_cast<CcReal*>(args[2].addr);
  const datetime::DateTime& delta =
      *static_cast<datetime::DateTime*>(args[3].addr);
  result = qp->ResultStorage(s);    // CcReal
  CcReal& dist = *static_cast<CcReal*>(result.addr);

/*
Require defined sequences with at least two points each and a defined
$st\_factor$ and defined duration $delta$.

*/
  if (seq1.GetNoComponents() < 2 || seq2.GetNoComponents() < 2 ||
      !cc_st_factor.IsDefined() ||
      !delta.IsDefined() || delta.GetType() != datetime::durationtype)
  {
    dist.SetDefined(false);
    return 0;
  }

/*
Require a $st\_factor \ge 0$ and a $delta \ge 0$.

*/
  const double st_factor = cc_st_factor.GetValue();
  if (st_factor < 0.0 || delta.ToDouble() < 0.0) {
    dist.SetDefined(false);
    return 0;
  }

  STLIPAggregator agg(st_factor, delta);
  dist.Set(dist_lip(agg, seq1, seq2));
  return 0;
}

ValueMapping dist_stlip_functions[] = {
  STLIPDistValueMap,
  nullptr
};

struct DistSTLIPInfo : OperatorInfo
{
  DistSTLIPInfo() : OperatorInfo()
  {
    name      = "dist_stlip";
    signature = TPointSeq::BasicType() + " x " + TPointSeq::BasicType()
                + " x " + CcReal::BasicType() + " x " + Duration::BasicType()
                + " -> " + CcReal::BasicType();
    syntax    = "dist_stlip(_, _, _, _)";
    meaning   = "Spatio-temporal Locality In-between Polylines distance "
                "STLIP(P, Q, st_factor, delta) of a well-formed pair of "
                "tpointseq objects, a non-negative st_factor and a "
                "non-negative duration delta.\n"
                "STLIP extends LIP (operator dist_lip) by multiplying each "
                "weighted polygon area with a factor that measures the "
                "temporal dissimilarity of the two portions of the two "
                "sequences that contribute to the polygon. Portions that cover "
                "the same time interval within the tolerance delta, have "
                "highest similarity. st_factor controls how much the temporal "
                "dissimilarity affects the result. With an st_factor of 0, "
                "STLIP yields the same result as LIP.\n"
                "If the pair of sequences is not well-formed, the result is "
                "indefinite. If any of the sequences is undefined or has less "
                "than two points or if st_factor or delta is negative, the "
                "result is undefined.\n"
                "Time and space complexity are the same as for dist_lip with "
                "higher constants for the time complexity.";
  }
};

const mappings::VectorTypeMaps dist_stlip_maps = {
  /*0*/ {{TPointSeq::BasicType(), TPointSeq::BasicType(),
    CcReal::BasicType(), Duration::BasicType()}, /* -> */ {CcReal::BasicType()}}
};

ListExpr DistSTLIPTypeMap(ListExpr args)
{ return mappings::vectorTypeMap(dist_stlip_maps, args); }

int DistSTLIPSelect(ListExpr args)
{ return mappings::vectorSelect(dist_stlip_maps, args); }


/*
5.3 ~dist\_spstlip2~

*/
int SPSTLIP2DistValueMap(
    Word* args, Word& result, int /*message*/, Word& /*local*/, Supplier s)
{
  const TPointSeq& seq1 = *static_cast<TPointSeq*>(args[0].addr);
  const TPointSeq& seq2 = *static_cast<TPointSeq*>(args[1].addr);
  const CcReal& cc_st_factor = *static_cast<CcReal*>(args[2].addr);
  const datetime::DateTime& delta =
      *static_cast<datetime::DateTime*>(args[3].addr);
  const CcReal& cc_sp_factor = *static_cast<CcReal*>(args[4].addr);
  result = qp->ResultStorage(s);    // CcReal
  CcReal& dist = *static_cast<CcReal*>(result.addr);

/*
Require defined sequences with at least two points each, a defined
$st\_factor$ and $sp\_factor$, and a defined duration $delta$.

*/
  if (seq1.GetNoComponents() < 2 || seq2.GetNoComponents() < 2 ||
      !cc_st_factor.IsDefined() ||
      !delta.IsDefined() || delta.GetType() != datetime::durationtype ||
      !cc_sp_factor.IsDefined())
  {
    dist.SetDefined(false);
    return 0;
  }

/*
Require $st\_factor \ge 0$, $delta \ge 0$, and $sp\_factor \ge 0$.

*/
  const double st_factor = cc_st_factor.GetValue();
  const double sp_factor = cc_sp_factor.GetValue();
  if (st_factor < 0.0 || delta.ToDouble() < 0.0 || sp_factor < 0.0) {
    dist.SetDefined(false);
    return 0;
  }

  SPSTLIP2Aggregator agg(st_factor, delta, sp_factor);
  dist.Set(dist_lip(agg, seq1, seq2));
  return 0;
}

ValueMapping dist_spstlip2_functions[] = {
  SPSTLIP2DistValueMap,
  nullptr
};

struct DistSPSTLIP2Info : OperatorInfo
{
  DistSPSTLIP2Info() : OperatorInfo()
  {
    name      = "dist_spstlip2";
    signature = TPointSeq::BasicType() + " x " + TPointSeq::BasicType()
                + " x " + CcReal::BasicType() + " x " + Duration::BasicType()
                + " x " + CcReal::BasicType() + " -> " + CcReal::BasicType();
    syntax    = "dist_spstlip2(_, _, _, _, _)";
    meaning   = "Experimental Speed-pattern Spatio-temporal Locality "
                "In-between Polylines distance SPSTLIP2(P, Q, st_factor, "
                "delta, sp_factor) of a well-formed pair of tpointseq objects, "
                "a non-negative st_factor, a non-negative duration delta, and "
                "a non-negative sp_factor.\n"
                "SPSTLIP2 extends STLIP (operator dist_stlip) by multiplying "
                "each STLIP polygon value with a factor that measures the "
                "dissimilarity in the velocity of the two sequences on the "
                "polygon. sp_factor controls how much the differences in the "
                "velocities affect the result. With an sp_factor of 0, "
                "SPSTLIP2 yields the same result as STLIP.\n"
                "If the pair of sequences is not well-formed, the result is "
                "indefinite. If any of the sequences is undefined or has less "
                "than two points, or if st_factor, delta, or sp_factor is "
                "negative, the result is undefined.\n"
                "Time and space complexity are the same as for dist_stlip with "
                "higher constants for the time complexity.";
  }
};

const mappings::VectorTypeMaps dist_spstlip2_maps = {
  /*0*/ {{TPointSeq::BasicType(), TPointSeq::BasicType(),
    CcReal::BasicType(), Duration::BasicType(), CcReal::BasicType()},
    /* -> */ {CcReal::BasicType()}}
};

ListExpr DistSPSTLIP2TypeMap(ListExpr args)
{ return mappings::vectorTypeMap(dist_spstlip2_maps, args); }

int DistSPSTLIP2Select(ListExpr args)
{ return mappings::vectorSelect(dist_spstlip2_maps, args); }


/*
5.4 ~genlip~

*/
template<class SEQ, bool PROCESS_ALL=false>
int GenLIPDistValueMap(
    Word* args, Word& result, int /*message*/, Word& /*local*/, Supplier s)
{
  const SEQ& seq1 = *static_cast<SEQ*>(args[0].addr);
  const SEQ& seq2 = *static_cast<SEQ*>(args[1].addr);
  const CcInt cc_max_gap_size = *static_cast<CcInt*>(args[2].addr);
  void* function = args[3].addr;
  result = qp->ResultStorage(s);    // CcReal
  CcReal& res = *static_cast<CcReal*>(result.addr);

/*
Require defined sequences with at least two points each.

*/
  if (seq1.GetNoComponents() < 2 || seq2.GetNoComponents() < 2) {
    res.SetDefined(false);
    return -1;
  }

/*
Require a defined and non-negative maximum gap size.

*/
  if (!cc_max_gap_size.IsDefined() || cc_max_gap_size.GetValue() < 0) {
    res.SetDefined(false);
    return -1;
  }

  genlip<SEQ, PROCESS_ALL>(
      seq1, seq2, cc_max_gap_size.GetValue(), function, res);
  return -1;
}

ValueMapping genlip_functions[] = {
  GenLIPDistValueMap<PointSeq>,
  GenLIPDistValueMap<TPointSeq>,
  nullptr
};

struct GenLIPInfo : OperatorInfo
{
  GenLIPInfo() : OperatorInfo()
  {
    name      = "genlip";
    signature = PointSeq::BasicType() + " x " + PointSeq::BasicType()
                + " x " + CcInt::BasicType() + " x (" + PointSeq::BasicType()
                + " x " + PointSeq::BasicType() + " -> " + CcReal::BasicType()
                + ") -> " + CcReal::BasicType();
    appendSignature(
                TPointSeq::BasicType() + " x " + TPointSeq::BasicType()
                + " x " + CcInt::BasicType() + " x (" + TPointSeq::BasicType()
                + " x " + TPointSeq::BasicType() + " -> " + CcReal::BasicType()
                + ") -> " + CcReal::BasicType());
    syntax    = "genlip(_, _, _, _)";
    meaning   = "Calculate GenLIP(P, Q, max_gap_size, function) for a pair of "
                "point sequences. The algorithm searches the point sequences "
                "for series of max_gap_size or more bad segments and feeds "
                "only the remaining (well-formed) parts into the function. The "
                "accumulated results of the function are returned. If the two "
                "sequences contain no well-formed part, the result is "
                "undefined.\n"
                "As the original GenLIP algorithm, this operator processes "
                "only the minimum number of segments of both sequences and "
                "ignores additional segments of the longer sequence.\n"
                "The time complexity of the ~GenLIP~ algorithm itself is O(n), "
                "where n is the total number of points in the sequences.";
  }
};

const mappings::NVectorTypeMaps GenLIPMaps()
{
  const mappings::NVectorTypeMaps maps = {
    /*0*/ {NList(
            NList(PointSeq::BasicType()), NList(PointSeq::BasicType()),
            NList(CcInt::BasicType()), NList(NList(Symbols::MAP()),
              NList(PointSeq::BasicType()), NList(PointSeq::BasicType()),
              NList(CcReal::BasicType()))
          ), /* -> */ NList(CcReal::BasicType())},
    /*1*/ {NList(
            NList(TPointSeq::BasicType()), NList(TPointSeq::BasicType()),
            NList(CcInt::BasicType()), NList(NList(Symbols::MAP()),
              NList(TPointSeq::BasicType()), NList(TPointSeq::BasicType()),
              NList(CcReal::BasicType()))
          ), /* -> */ NList(CcReal::BasicType())}
  };
  return maps;
}

ListExpr GenLIPTypeMap(ListExpr args)
{ return mappings::vectorTypeMap(GenLIPMaps(), args); }

int GenLIPSelect(ListExpr args)
{ return mappings::vectorSelect(GenLIPMaps(), args); }


/*
5.5 ~genlip2~

*/
ValueMapping genlip2_functions[] = {
  GenLIPDistValueMap<PointSeq,  /*PROCESS_ALL*/ true>,
  GenLIPDistValueMap<TPointSeq, /*PROCESS_ALL*/ true>,
  nullptr
};

struct GenLIP2Info : OperatorInfo
{
  GenLIP2Info() : OperatorInfo()
  {
    name      = "genlip2";
    signature = PointSeq::BasicType() + " x " + PointSeq::BasicType()
                + " x " + CcInt::BasicType() + " x (" + PointSeq::BasicType()
                + " x " + PointSeq::BasicType() + " -> " + CcReal::BasicType()
                + ") -> " + CcReal::BasicType();
    appendSignature(
                TPointSeq::BasicType() + " x " + TPointSeq::BasicType()
                + " x " + CcInt::BasicType() + " x (" + TPointSeq::BasicType()
                + " x " + TPointSeq::BasicType() + " -> " + CcReal::BasicType()
                + ") -> " + CcReal::BasicType());
    syntax    = "genlip2(_, _, _, _)";
    meaning   = "Variant of the genlip operator. Deviating from the original "
                "specification of the GenLIP algorithm, genlip2 also processes "
                "additional segments of the longer sequence.";
  }
};


void TrajectorySimilarityAlgebra::addLIPDistOp()
{
  AddOperator(
      DistLIPInfo(), dist_lip_functions,
      DistLIPSelect, DistLIPTypeMap);
  AddOperator(
      DistSTLIPInfo(), dist_stlip_functions,
      DistSTLIPSelect, DistSTLIPTypeMap);
  AddOperator(
      DistSPSTLIP2Info(), dist_spstlip2_functions,
      DistSPSTLIP2Select, DistSPSTLIP2TypeMap);
  AddOperator(
      GenLIPInfo(), genlip_functions,
      GenLIPSelect, GenLIPTypeMap);
  AddOperator(
      GenLIP2Info(), genlip2_functions,
      GenLIPSelect, GenLIPTypeMap);
}

} //-- namespace tsa

/*
\begin{thebibliography}{ABCD99}

\bibitem[PKM+07]{PKM+07}
Nikos Pelekis, Ioannis Kopanakis, Gerasimos Marketos, Irene Ntoutsi, Gennady L.
  \ Andrienko, and Yannis Theodoridis.
\newblock {Similarity Search in Trajectory Databases}.
\newblock In {\em {14th International Symposium on Temporal Representation and
  Reasoning {(TIME} 2007), 28-30 June 2007, Alicante, Spain}}, pages 129--140.
  {IEEE} Computer Society, 2007, http://dx.doi.org/10.1109/TIME.2007.59;
  http://dblp.uni-trier.de/rec/bib/conf/time/PelekisKMNAT07.

\end{thebibliography}

*/
