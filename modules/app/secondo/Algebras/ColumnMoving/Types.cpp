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

1 Types.cpp

*/

#include "Types.h"

namespace ColumnMovingAlgebra {

/*
In this file we define the static strings for the description of our
attribut array types.

*/

  char iintsName[] = "iints"; 
  char iintsInfo[] = "(ai*) where ai is a iint";
  char iintsExample[] = "((\"2001-10-10\" 5) (\"2002-10-10\" 7)) \n";

  char mintsName[] = "mints"; 
  char mintsInfo[] = "(ai*) where ai is a mint";
  char mintsExample[] = 
    "( \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) 1) \n"
    "    ((\"2003-10-10\" \"2004-10-10\" TRUE TRUE) 2) \n"
    "  ) \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) 5) \n"
    "    ((\"2002-10-10\" \"2007-10-10\" FALSE TRUE) 9) \n"
    "  ) \n"
    ") \n";

  char ipointsName[] = "ipoints"; 
  char ipointsInfo[] = "(ai*) where ai is a ipoint";
  char ipointsExample[] = "((\"2001-10-10\" (1.0 2.0)) "
                          "(\"2002-10-10\" (3.0 4.0))) \n";

  char mpointsName[] = "mpoints"; 
  char mpointsInfo[] = "(ai*) where ai is a mpoint";
  char mpointsExample[] = 
    "( \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) (1.0 2.0 3.0 4.0)) \n"
    "    ((\"2003-10-10\" \"2004-10-10\" TRUE TRUE) (6.0 7.0 3.0 4.0)) \n"
    "  ) \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) (1.5 8.0 3.0 4.0)) \n"
    "    ((\"2002-10-10\" \"2007-10-10\" FALSE TRUE) (6.7 2.0 5.0 8.0)) \n"
    "  ) \n"
    ") \n";

  char iregionsName[] = "iregions"; 
  char iregionsInfo[] = "(ai*) where ai is a iregion";
  char iregionsExample[] = 
    "(( \"2001-10-10\" ((((0.0 0.0) (1.0 0.0) (0.0 1.0)))) ) \n"
    " ( \"2001-10-10\" ((((1.0 1.0) (1.0 0.0) (0.0 1.0)))) ))";

  char mregionsName[] = "mregions"; 
  char mregionsInfo[] = "(ai*) where ai is a mregion";
  char mregionsExample[] = 
    "( \n"
    "  ( \n"
    "    ( (\"2001-10-10\" \"2002-10-10\" TRUE TRUE) \n"
    "      ((((0.0 0.0 0.5 0.5) (1.0 0.0 1.5 0.5) (0.0 1.0 0.5 1.5)))) ) \n"
    "    ( (\"2002-10-10\" \"2003-10-10\" FALSE TRUE) \n"
    "      ((((0.5 0.5 0.5 0.5) (1.5 0.5 1.5 0.5) (0.5 1.5 0.5 1.5)))) ) \n"
    "  ) \n"
    "  ( \n"
    "    ( (\"2001-10-10\" \"2002-10-10\" TRUE TRUE) \n"
    "      ((((0.0 0.0 0.5 0.5) (2.0 0.0 2.5 0.5) (0.0 2.0 0.5 2.5)))) ) \n"
    "    ( (\"2002-10-10\" \"2003-10-10\" FALSE TRUE) \n"
    "      ((((0.5 0.5 0.5 0.5) (2.5 0.5 2.5 0.5) (0.5 2.5 0.5 2.5)))) ) \n"
    "  ) \n"
    ") \n";

  char irealsName[] = "ireals"; 
  char irealsInfo[] = "(ai*) where ai is a ireal";
  char irealsExample[] = "((\"2001-10-10\" 5.1) (\"2002-10-10\" 7.5)) \n";

  char mrealsName[] = "mreals"; 
  char mrealsInfo[] = "(ai*) where ai is a mreal";
  char mrealsExample[] = 
    "( \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) (2.0 3.0 4.0 FALSE)) \n"
    "    ((\"2003-10-10\" \"2004-10-10\" TRUE TRUE) (4.0 5.0 3.0 FALSE)) \n"
    "  ) \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) (5.0 3.0 8.0 TRUE)) \n"
    "    ((\"2002-10-10\" \"2007-10-10\" FALSE TRUE) (2.0 6.0 3.0 FALSE)) \n"
    "  ) \n"
    ") \n";

  char iboolsName[] = "ibools"; 
  char iboolsInfo[] = "(ai*) where ai is a ibool";
  char iboolsExample[] = "((\"2001-10-10\" TRUE) (\"2002-10-10\" FALSE)) \n";

  char mboolsName[] = "mbools"; 
  char mboolsInfo[] = "(ai*) where ai is a mbool";
  char mboolsExample[] = 
    "( \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) TRUE) \n"
    "    ((\"2003-10-10\" \"2004-10-10\" TRUE TRUE) TRUE) \n"
    "  ) \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) TRUE) \n"
    "    ((\"2002-10-10\" \"2007-10-10\" FALSE TRUE) FALSE) \n"
    "  ) \n"
    ") \n";

  char istringsName[] = "istrings"; 
  char istringsInfo[] = "(ai*) where ai is a istring";
  char istringsExample[] = "((\"2001-10-10\" \"abc\") "
                           "(\"2002-10-10\" \"test\")) \n";

  char mstringsName[] = "mstrings"; 
  char mstringsInfo[] = "(ai*) where ai is a mstring";
  char mstringsExample[] = 
    "( \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) \"abc\") \n"
    "    ((\"2003-10-10\" \"2004-10-10\" TRUE TRUE) \"def\") \n"
    "  ) \n"
    "  ( \n"
    "    ((\"2001-10-10\" \"2002-10-10\" TRUE TRUE) \"test\") \n"
    "    ((\"2002-10-10\" \"2007-10-10\" FALSE TRUE) \"abc\") \n"
    "  ) \n"
    ") \n";

}

