/*
----
This file is part of SECONDO.

Copyright (C) 2004-2009, University in Hagen, Faculty of Mathematics
and Computer Science, Database Systems for New Applications.

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

*/

#include "MPoints.h"

using namespace std;

namespace ColumnMovingAlgebra
{
/*
1.1.3 CRel Algebra Interface

the following functions are required by the crel algebra for all attribute 
arrays.

~Filter~ returns a duplicate of this attribut array with the speficied filter.

 
*/
  CRelAlgebra::AttrArray* MPoints::Filter(
    CRelAlgebra::SharedArray<const uint64_t> filter) const
  {
    return new MPoints(*this, filter);
  }

/*
~GetCount~ returns the number of entries in the attribut array.

*/
  uint64_t MPoints::GetCount() const
  {
    return m_MPointsData->rowCount();
  }

/*
~GetSize~ returns the amount of space needed to save this attribut array
to persistant storage.

*/
  uint64_t MPoints::GetSize() const
  {
    return m_MPointsData->savedSize() +
           m_DefTimes->savedSize() +
           sizeof(m_Mbr) +
           sizeof(bool) +
           (m_GridIndex.get() != 0 ? m_GridIndex->savedSize() : 0);
  }

/*
~Save~ saves this attribut array
to persistant storage.

*/
  void MPoints::Save(CRelAlgebra::Writer &target, bool includeHeader) const
  {
    m_MPointsData->save(target);
    m_DefTimes->save(target);
    
    GridIndex::Mbr m = m_Mbr;
    target.WriteOrThrow(reinterpret_cast<char*>(&m), sizeof(m));

    bool hasGrid = m_GridIndex.get() != 0;
    target.WriteOrThrow(reinterpret_cast<char*>(&hasGrid), sizeof(bool));
    if (hasGrid)
      m_GridIndex->save(target);
  }

/*
~Append~ adds the moving point at index ~row~ of the attribut array ~array~

*/
  void MPoints::Append(const CRelAlgebra::AttrArray & array, uint64_t row)
  {
    MPoints mpoints = static_cast<const MPoints &>(array);
    
    if (m_MPointsData->rowCount() == 0) {
      if (m_GridIndex.get() == 0 && mpoints.m_GridIndex.get() != 0) {
        GridIndex & g = *mpoints.m_GridIndex;
        m_GridIndex = std::make_shared<GridIndex>(g.offset(), g.cellSize(), 
                                                  g.splits());
      }
    }

    addRow();

    MPointsData::UnitIterator i = mpoints.m_MPointsData->unitIterator(row);
    while (i.hasNext()) {
      MPointsData::Unit u = i.next();
      addUnit(u.interval, u.x0, u.y0, u.x1, u.y1);
    }
  }

/*
~Append~ adds the row orientied MPoint ~value~

*/
  void MPoints::Append(Attribute & value)
  {
    temporalalgebra::MPoint & a = static_cast<temporalalgebra::MPoint&>(value);

    addRow();

    if (a.IsDefined()) {
      for (int i = 0; i < a.GetNoComponents(); i++) {
        temporalalgebra::UPoint c;
        a.Get(i, c);
        Interval interval(c.timeInterval);
        addUnit(interval, c.p0.GetX(), c.p0.GetY(), c.p1.GetX(), c.p1.GetY());
      }
    }
  }

/*
~Remove~ removes the last added moving point

*/
  void MPoints::Remove()
  {
    m_MPointsData->removeRow();
    m_DefTimes->removeRow();

    if (m_GridIndex.get() != 0)
      m_GridIndex->removeRow();
  }

/*
~Clear~ removes all moving points

*/
  void MPoints::Clear()
  {
    m_MPointsData->clear();
    m_DefTimes->clear();

    if (m_GridIndex.get() != 0)
      m_GridIndex->clear();
  }

/*
~IsDefined~ returns true, iff the moving point with index ~row~ has any units

*/
  bool MPoints::IsDefined(uint64_t row) const
  {
    return m_MPointsData->unitCount(row) > 0;
  }

/*
~Compare~ compares the moving point at index ~rowA~ with the moving point
at index ~rowB~ in ~arrayB~

*/
  int MPoints::Compare(uint64_t rowA, const CRelAlgebra::AttrArray &arrayB,
    uint64_t rowB) const
  {
    const MPoints & mpointsB = static_cast<const MPoints&>(arrayB);
    int iDiff;
    double dDiff;

    int unitCountA = m_MPointsData->unitCount(rowA);
    int unitCountB = mpointsB.m_MPointsData->unitCount(rowB);

    iDiff = unitCountA - unitCountB;
    if (iDiff != 0)
      return iDiff < 0 ? -1 : 1;

    MPointsData::UnitIterator iA = m_MPointsData->unitIterator(rowA);
    MPointsData::UnitIterator iB = mpointsB.m_MPointsData->unitIterator(rowB);

    while (iA.hasNext()) {
      checkrv(iB.hasNext(), "comparison logical error", 0);

      MPointsData::Unit a = iA.next();
      MPointsData::Unit b = iB.next();

      Interval & intervalA = a.interval;
      Interval & intervalB = b.interval;
      
      iDiff = intervalA.compare(intervalB);
      if (iDiff != 0)
        return iDiff < 0 ? -1 : 1;

      dDiff = a.x0 - b.x0;
      if (dDiff != 0)
        return dDiff < 0 ? -1 : 1;

      dDiff = a.x1 - b.x1;
      if (dDiff != 0)
        return dDiff < 0 ? -1 : 1;

      dDiff = a.y0 - b.y0;
      if (dDiff != 0)
        return dDiff < 0 ? -1 : 1;

      dDiff = a.y1 - b.y1;
      if (dDiff != 0)
        return dDiff < 0 ? -1 : 1;
    }

    return 0;
  }

/*
~Compare~ compares the moving point at index ~rowA~ with the row oriented
attribute ~value~

*/
  int MPoints::Compare(uint64_t row, Attribute &value) const
  {
    auto mpointB = static_cast<temporalalgebra::MPoint&>(value);

    if (!mpointB.IsDefined())
      return IsDefined(row) ? 1 : 0;

    int iDiff;
    double dDiff;

    int unitCountA = m_MPointsData->unitCount(row);
    int unitCountB = mpointB.GetNoComponents();

    iDiff = unitCountA - unitCountB;
    if (iDiff != 0)
      return iDiff < 0 ? -1 : 1;

    MPointsData::UnitIterator iA = m_MPointsData->unitIterator(row);
    int iB = 0;

    while (iA.hasNext()) {
      checkrv(iB < unitCountB, "comparison logical error", 0);
      temporalalgebra::UPoint b;

      MPointsData::Unit a = iA.next();
      mpointB.Get(iB, b);

      Interval & intervalA = a.interval;
      Interval intervalB(b.timeInterval);

      iDiff = intervalA.compare(intervalB);
      if (iDiff != 0)
        return iDiff < 0 ? -1 : 1;

      dDiff = a.x0 - b.p0.GetX();
      if (dDiff != 0)
        return dDiff < 0 ? -1 : 1;

      dDiff = a.x1 - b.p1.GetX();
      if (dDiff != 0)
        return dDiff < 0 ? -1 : 1;

      dDiff = a.y0 - b.p0.GetY();
      if (dDiff != 0)
        return dDiff < 0 ? -1 : 1;

      dDiff = a.y1 - b.p1.GetY();
      if (dDiff != 0)
        return dDiff < 0 ? -1 : 1;
    }

    return 0;
  }

/*
~GetHash~ returns a hash value for the moving point at index ~row~

*/
  uint64_t MPoints::GetHash(uint64_t row) const
  {
    if (m_MPointsData->unitCount(row) == 0)
      return 0;

    MPointsData::UnitIterator i = m_MPointsData->unitIterator(row);
    checkrv(i.hasNext(), "hash logical error", 0);
    MPointsData::Unit u = i.next();
    return (uint64_t)(u.interval.s ^ u.interval.e);
  }

/*
~GetAttribute~ converts the moving point 
in ~row~ to an MPoint as defined in the temporal algebra for row oriented
relations and returns it.

*/
  Attribute * MPoints::GetAttribute(uint64_t row, bool clone) const
  {
    temporalalgebra::MPoint * attribute = 
      new temporalalgebra::MPoint(m_MPointsData->unitCount(row));
      
    attribute->StartBulkLoad();

    MPointsData::UnitIterator i = m_MPointsData->unitIterator(row);
    while (i.hasNext()) {
      MPointsData::Unit u = i.next();
      Interval & interval = u.interval;
      attribute->Add(temporalalgebra::UPoint(
        temporalalgebra::Interval<Instant>(interval.s, interval.e, 
                                           interval.lc, interval.rc),
        u.x0, u.y0, u.x1, u.y1));
    }

    attribute->EndBulkLoad();
    return attribute;
  }

}
