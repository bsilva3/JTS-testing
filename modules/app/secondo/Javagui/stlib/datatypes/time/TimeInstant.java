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

package stlib.datatypes.time;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Objects;
import java.util.TimeZone;

import stlib.datatypes.GeneralType;
import stlib.interfaces.time.TimeInstantIF;

/**
 * Class for representation of the 'Instant' data type.<br>
 * Internally the 'java.time.Instant' class is used to store the date time
 * value.
 * <p>
 * Stores date time values down to one nanosecond.<br>
 * Objects of this class are immutable.
 * 
 * @author Markus Fuessel
 */
public class TimeInstant extends GeneralType implements TimeInstantIF {

   /**
    * The minimum supported {@code TimeInstant}, '-1000000000-01-01T00:00Z'.<br>
    * <br>
    * 
    * @see java.time.Instant.MIN
    */
   public static final TimeInstantIF MIN = new TimeInstant(Instant.MIN);
   /**
    * The maximum supported {@code TimeInstant},
    * '1000000000-12-31T23:59:59.999999999Z'.<br>
    * <br>
    * 
    * @see java.time.Instant.MAX
    */
   public static final TimeInstantIF MAX = new TimeInstant(Instant.MAX);

   /**
    * Static attribute to store date time format which is used for all instant
    * values by default
    */
   private static DateTimeFormatter defaultDateTimeFormat;

   /**
    * Static attribute to store the time zone id which is used for all instant
    * values by default
    */
   private static ZoneId defaultTimeZoneId;

   /**
    * Initialize the static attributes
    */
   static {
      defaultDateTimeFormat = DateTimeFormatter.ISO_LOCAL_DATE_TIME;
      defaultTimeZoneId = TimeZone.getDefault().toZoneId();
   }

   /**
    * The Instant value<br>
    * Uses java.time.Instant to store the date time value
    * 
    * @see java.time.Instant
    */
   private final Instant instant;

   /**
    * Setter for the default date time format
    * 
    * @param format
    *           - DateTimeFormatter to use as default
    * 
    * @see java.time.format.DateTimeFormatter
    */
   public static void setDefaultDateTimeFormat(final DateTimeFormatter format) {
      defaultDateTimeFormat = format;
   }

   /**
    * Setter for the default zone id
    * 
    * @param zoneId
    *           - ZoneId to use as default
    * 
    * @see java.time.ZoneId
    */
   public static void setDefaultTimeZoneId(final ZoneId zoneId) {
      defaultTimeZoneId = zoneId;
   }

   /**
    * Simple constructor, creates an undefined 'TimeInstant' object
    */
   public TimeInstant() {
      this.instant = Instant.EPOCH;
   }

   /**
    * Constructor, create an defined 'TimeInstant' object from an Instant value
    * 
    * @param instant
    *           - the instant value
    */
   public TimeInstant(final Instant instant) {
      Objects.requireNonNull(instant, "'instant' must not be null");

      this.instant = instant;
      setDefined(true);

   }

   /**
    * Constructor, create an defined 'TimeInstant' object
    * 
    * @param dateTime
    *           - date time string
    * @param dateTimeFormat
    *           - DateTimeFormatter to use to parse the date time string
    * @param timeZoneId
    *           - ZoneId to use for the passed date time string
    */
   public TimeInstant(final String dateTime, final DateTimeFormatter dateTimeFormat, final ZoneId timeZoneId) {
      Objects.requireNonNull(dateTime, "'dateTime' must not be null");
      Objects.requireNonNull(dateTimeFormat, "'dateTimeFormat' must not be null");
      Objects.requireNonNull(timeZoneId, "'timeZoneId' must not be null");

      LocalDateTime localDateTime = LocalDateTime.parse(dateTime, dateTimeFormat);
      ZonedDateTime zonedDateTime = localDateTime.atZone(timeZoneId);
      this.instant = zonedDateTime.toInstant();

      setDefined(true);

   }

   /**
    * Constructor, create an defined 'TimeInstant' object <br>
    * Uses the default date time format and time zone id to parse the passed date
    * time string
    * 
    * @param dateTime
    *           - date time string
    */
   public TimeInstant(final String dateTime) {
      this(dateTime, defaultDateTimeFormat, defaultTimeZoneId);
   }

   /**
    * Constructor, create an defined 'TimeInstant' object <br>
    * Uses the defaul time zone id to parse the passed date time string with the
    * passed date time format
    * 
    * @param dateTime
    * @param dateTimeFormat
    */
   public TimeInstant(final String dateTime, final String dateTimeFormat) {
      this(dateTime, DateTimeFormatter.ofPattern(dateTimeFormat), defaultTimeZoneId);
   }

   /**
    * Copy constructor
    * 
    * @param original
    *           - the 'TimeInstant' object to copy
    */
   public TimeInstant(final TimeInstant original) {

      this.instant = original.getValue();
      setDefined(original.isDefined());
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.time.TimeInstantIF#plusMillis(long)
    */
   @Override
   public TimeInstantIF plusMillis(final long millisToAdd) {
      Instant newInstant = instant.plusMillis(millisToAdd);
      TimeInstant newTimeInstant = new TimeInstant(newInstant);
      newTimeInstant.setDefined(this.isDefined());

      return newTimeInstant;
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.time.TimeInstantIF#plusNanos(long)
    */
   @Override
   public TimeInstantIF plusNanos(final long nanosToAdd) {
      Instant newInstant = instant.plusNanos(nanosToAdd);
      TimeInstant newTimeInstant = new TimeInstant(newInstant);
      newTimeInstant.setDefined(this.isDefined());

      return newTimeInstant;
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.time.TimeInstantIF#minusMillis(long)
    */
   @Override
   public TimeInstantIF minusMillis(final long millisToSubtract) {
      Instant newInstant = instant.minusMillis(millisToSubtract);
      TimeInstant newTimeInstant = new TimeInstant(newInstant);
      newTimeInstant.setDefined(this.isDefined());

      return newTimeInstant;
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.time.TimeInstantIF#minusNanos(long)
    */
   @Override
   public TimeInstantIF minusNanos(final long nanosToSubtract) {
      Instant newInstant = instant.minusNanos(nanosToSubtract);
      TimeInstant newTimeInstant = new TimeInstant(newInstant);
      newTimeInstant.setDefined(this.isDefined());

      return newTimeInstant;
   }

   /*
    * (non-Javadoc)
    * 
    * @see java.lang.Comparable#compareTo(java.lang.Object)
    */
   @Override
   public int compareTo(final TimeInstantIF otherTimeInstant) {

      return instant.compareTo(otherTimeInstant.getValue());
   }

   /*
    * (non-Javadoc)
    * 
    * @see java.lang.Object#hashCode()
    */
   @Override
   public int hashCode() {
      return instant.hashCode();
   }

   /*
    * (non-Javadoc)
    * 
    * @see java.lang.Object#equals(java.lang.Object)
    */
   @Override
   public boolean equals(final Object obj) {
      if (!(obj instanceof TimeInstantIF)) {
         return false;
      }

      if (this == obj) {
         return true;
      }

      TimeInstantIF otherInstant = (TimeInstantIF) obj;

      return compareTo(otherInstant) == 0;
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.features.Orderable#before(java.lang.Object)
    */
   @Override
   public boolean before(final TimeInstantIF otherTimeInstant) {

      return (this.compareTo(otherTimeInstant) < 0);
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.features.Orderable#after(java.lang.Object)
    */
   @Override
   public boolean after(final TimeInstantIF otherTimeInstant) {

      return (this.compareTo(otherTimeInstant) > 0);
   }

   /**
    * If other 'TimeInstant' object is adjacent to this.<br>
    * Always returns false because time is considered as a continuous value and
    * there is always another instant between two instants.
    * 
    * @see stlib.interfaces.features.Orderable#adjacent(java.lang.Object)
    */
   @Override
   public boolean adjacent(final TimeInstantIF otherTimeInstant) {

      return false;
   }

   /*
    * (non-Javadoc)
    * 
    * @see java.lang.Object#toString()
    */
   @Override
   public String toString() {
      return "TimeInstant [instant=" + instant.atZone(defaultTimeZoneId) + ", isDefined()=" + isDefined() + "]";
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.time.TimeInstantIF#getValue()
    */
   @Override
   public Instant getValue() {
      return instant;
   }

   /*
    * (non-Javadoc)
    * 
    * @see stlib.interfaces.time.TimeInstantIF#toMilliseconds()
    */
   @Override
   public long toMilliseconds() {
      return instant.toEpochMilli();
   }

}
