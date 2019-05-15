//This file is part of SECONDO.

//Copyright (C) 2004, University in Hagen, Department of Computer Science,
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

package util.domain.enums;

import util.domain.ComplexToken;

/**
 * ErrorTyes are used to describe semantic errors within querys.
 * Used in {@link ComplexToken} to record errors which occurred while analysing a query.
 * @author D.Merle
 */
public enum ErrorType {
	MISSING_BRACKET,
	UNFINISHED_BRACKET,
	WRONG_BRACKET,
	MISSING_PREFIX_ARGUMENTS,
	MISSING_POSTFIX_ARGUMENTS,
	TOO_MANY_POSTFIX_ARGUMENTS,
	PARAMETER_FUNCTION_AT_ILLEGEAL_POSITION,
	PARAMETER_FUNCTION_REFERS_TO_ILLEGAL_PREFIX,
	PARAMETER_FUNCTION_REFERS_TO_ILLEGAL_ATTRIBUTE
}