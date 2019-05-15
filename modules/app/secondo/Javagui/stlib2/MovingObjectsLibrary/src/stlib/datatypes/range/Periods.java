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

package stlib.datatypes.range;

import stlib.datatypes.interval.Period;
import stlib.datatypes.time.TimeInstant;
import stlib.interfaces.interval.PeriodIF;
import stlib.interfaces.range.PeriodsIF;
import stlib.interfaces.time.TimeInstantIF;

/**
 * Concrete class for representation of 'Periods' objects. That are 'Range'
 * objects with disjoint and non adjacent 'TimeInstant' intervals.
 * 
 * @author Markus Fuessel
 */
public class Periods extends Range<TimeInstantIF> implements PeriodsIF {

   /**
    * Simple constructor to create an empty 'Periods' object with the specified
    * initial capacity
    * 
    * @param size
    *           - initial capacity of this 'Periods' object
    */
   public Periods(final int size) {
      super(size);
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.range.PeriodsIF#first()
    */
   @Override
   public PeriodIF first() {
      return (PeriodIF) super.first();
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.range.PeriodsIF#last()
    */
   @Override
   public PeriodIF last() {
      return (PeriodIF) super.last();
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.range.PeriodsIF#get(int)
    */
   @Override
   public PeriodIF get(final int index) {

      PeriodIF period;

      if (index >= 0 && index < this.getNoComponents()) {
         period = (PeriodIF) super.get(index);
      } else {
         period = new Period();
      }

      return period;

   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.datatypes.range.Range#getUndefinedValue()
    */
   @Override
   protected TimeInstantIF getUndefinedObject() {

      return new TimeInstant();
   }

}
