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

package mmdb.data.attributes.standard;

import mmdb.data.attributes.MemoryAttribute;
import mmdb.data.features.Orderable;
import mmdb.data.features.Parsable;
import sj.lang.ListExpr;

/**
 * Object representation for database attributes of type 'string'.
 *
 * @author Alexander Castor
 */
public class AttributeString extends MemoryAttribute implements Orderable, Parsable {

	/**
	 * The attribute's value
	 */
	private String value;
	
	/**
	 * Explicit Standard Constructor
	 */
	public AttributeString() {}
	
	/**
	 * Create AttributeString from String
	 * 
	 * @param value
	 * 			The int value to encapsulate
	 */
	public AttributeString(String value) {
		this.value = value;
	}
	
	/*
	 * (non-Javadoc)
	 * 
	 * @see mmdb.data.attributes.MemoryAttribute#fromList(sj.lang.ListExpr)
	 */
	@Override
	public void fromList(ListExpr list) {
		setValue(list.stringValue());
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see mmdb.data.attributes.MemoryAttribute#toList()
	 */
	@Override
	public ListExpr toList() {
		return ListExpr.stringAtom(getValue());
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#equals(java.lang.Object)
	 */
	@Override
	public boolean equals(Object attribute) {
		if (attribute == null) {
			return false;
		}
		if (!(attribute instanceof AttributeString)) {
			return false;
		}
		String valueOther = ((AttributeString) attribute).getValue();
		if (getValue().equals(valueOther)) {
			return true;
		}
		return false;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#hashCode()
	 */
	@Override
	public int hashCode() {
		return getValue().hashCode();
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Comparable#compareTo(java.lang.Object)
	 */
	@Override
	public int compareTo(Orderable attribute) {
		String valueOther = ((AttributeString) attribute).getValue();
		return getValue().compareTo(valueOther);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see mmdb.data.features.Parseable#parse(java.lang.String)
	 */
	@Override
	public Parsable parse(String text) {
		if (text == null) {
			return null;
		}
		AttributeString result = new AttributeString();
		result.setValue(text);
		return result;
	}

	/**
	 * Getter for value.
	 * 
	 * @return the value
	 */
	public String getValue() {
		return value;
	}

	/**
	 * Setter for value.
	 * 
	 * @param value
	 *            the value to set
	 */
	public void setValue(String value) {
		this.value = value;
	}

	/**
	 * Retrieve a String representation of the attribute in nested list format.
	 * For testing purpose.
	 * 
	 * @return Nested list representation
	 */
	@Override
	public String toString() {
		if (this.value == null) {
			return "(string undefined)";
		} else {
			return "(string " + this.value + ")";
		}
	}

}
