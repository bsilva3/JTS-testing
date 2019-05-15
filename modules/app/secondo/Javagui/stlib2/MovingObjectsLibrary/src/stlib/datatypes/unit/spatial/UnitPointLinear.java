//This file is part of SECONDO.

//Copyright (C) 2014, University in Hagen, Department of Computer Science,
//Database Systems for New Applications.

//SECONDO is free software; you can redistribute it and/or modify
//it under the terms of the GNU General Public License as published by
//the Free Software Foundation; either version 2 of the License, or
//(at your option) any later version.

//SECONDO is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU General Public License for more details.

//You should have received a copy of the GNU General Public License
//along with SECONDO; if not, write to the Free Software
//Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

package stlib.datatypes.unit.spatial;

import java.util.Objects;

import stlib.datatypes.interval.Period;
import stlib.datatypes.spatial.Point;
import stlib.datatypes.unit.UnitObject;
import stlib.interfaces.interval.PeriodIF;
import stlib.interfaces.spatial.PointIF;
import stlib.interfaces.spatial.util.RectangleIF;
import stlib.interfaces.time.TimeInstantIF;
import stlib.interfaces.unit.UnitObjectIF;
import stlib.interfaces.unit.spatial.UnitPointIF;

/**
 * This class represents 'UnitPointLinear' objects
 * <p>
 * It is used to represent a continuous linear movement of a point during a
 * certain period of time.
 * 
 * @author Markus Fuessel
 */
/**
 * @author Markus Fuessel
 *
 */
public class UnitPointLinear extends UnitObject<PointIF> implements UnitPointIF {

   /**
    * Point at the beginning of the unit period
    */
   private final PointIF startPoint;

   /**
    * Point at the end of the unit period
    */
   private final PointIF endPoint;

   /**
    * Constructor for an undefined 'UnitPointLinear' object
    */
   public UnitPointLinear() {
      this.startPoint = new Point();
      this.endPoint = new Point();
   }

   /**
    * Constructor for a 'UnitPointLinear' object
    * 
    * @param period
    *           - time period for which this unit is defined
    * @param startPoint
    *           - point at which the linear movement starts
    * @param endPoint
    *           - point at which the linear movement ends
    */
   public UnitPointLinear(final PeriodIF period, final PointIF startPoint, final PointIF endPoint) {

      super(period);
      this.startPoint = Objects.requireNonNull(startPoint, "'startPoint' must not be null");
      this.endPoint = Objects.requireNonNull(endPoint, "'endPoint' must not be null");

      setDefined(period.isDefined() && startPoint.isDefined() && endPoint.isDefined());

   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.unit.UnitObjectIF#getValue(java.time.Instant)
    */
   @Override
   public PointIF getValue(final TimeInstantIF instant) {
      return getValue(instant, false);
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.unit.UnitObjectIF#getValue(stlib.interfaces.time.
    * TimeInstantIF, boolean)
    */
   @Override
   public PointIF getValue(final TimeInstantIF instant, final boolean ignoreClosedFlags) {

      PeriodIF period = getPeriod();

      if (isDefined() && period.contains(instant, ignoreClosedFlags)) {
         if (instant.equals(period.getLowerBound())) {
            return getInitial();

         } else if (instant.equals(period.getUpperBound())) {
            return getFinal();

         } else {
            long durationMilli = period.getDurationInMilliseconds();
            long durationCurrent = Period.getDurationInMilliseconds(period.getLowerBound(), instant);

            double x = startPoint.getXValue() + (getDeltaX() / durationMilli) * (durationCurrent);
            double y = startPoint.getYValue() + (getDeltaY() / durationMilli) * (durationCurrent);

            return new Point(x, y);
         }
      } else {
         return new Point();
      }

   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.unit.UnitObjectIF#atPeriod(stlib.interfaces.interval.
    * PeriodIF)
    */
   @Override
   public UnitPointLinear atPeriod(PeriodIF period) {
      PeriodIF newPeriod = this.getPeriod().intersection(period);

      if (!newPeriod.isDefined()) {
         return new UnitPointLinear();
      }

      return new UnitPointLinear(newPeriod, getValue(newPeriod.getLowerBound(), true),
            getValue(newPeriod.getUpperBound(), true));
   }

   /**
    * Not implemented for 'UnitPointLinear' objects yet.
    * 
    * @see stlib.interfaces.unit.UnitObjectIF#equalValue(stlib.datatypes.unit.UnitObjectIF)
    */
   @Override
   public boolean equalValue(UnitObjectIF<PointIF> otherUnitObject) {

      return false;
   }

   /**
    * Get the delta between start and end point on the x axis
    * 
    * @return the x axis delta
    */
   private double getDeltaX() {
      return Point.getDeltaX(startPoint, endPoint);
   }

   /**
    * Get the delta between start and end point on the y axis
    * 
    * @return the y axis delta
    */
   private double getDeltaY() {
      return Point.getDeltaY(startPoint, endPoint);
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.unit.UnitObjectIF#getInitial()
    */
   @Override
   public PointIF getInitial() {
      return startPoint;
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.unit.UnitObjectIF#getFinal()
    */
   @Override
   public PointIF getFinal() {
      return endPoint;
   }

   /**
    * Getter for the projection bounding box of this 'UnitPointLinear' object
    * <p>
    * Combines the bounding box of the start point with the bounding box of the end
    * point
    */
   @Override
   public RectangleIF getProjectionBoundingBox() {

      RectangleIF startPointBB = startPoint.getBoundingBox();
      RectangleIF endPointBB = endPoint.getBoundingBox();

      return startPointBB.merge(endPointBB);
   }

   /*
    * (non-Javadoc)
    * 
    * @see
    * stlib.interfaces.unit.UnitObjectIF#finalEqualToInitialValue(stlib.interfaces.
    * unit .UnitObjectIF)
    */
   @Override
   public boolean finalEqualToInitialValue(UnitObjectIF<PointIF> otherUnitObject) {
      return getFinal().almostEqual(otherUnitObject.getInitial());
   }

}
