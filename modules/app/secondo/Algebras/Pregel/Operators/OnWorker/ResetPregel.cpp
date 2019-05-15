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

//paragraph [1] Title: [{\Large \bf \begin {center}] [\end {center}}]
//[TOC] [\tableofcontents]

[1] Header File of the class ~PregelAlgebra~

November 2018, J. Mende


[TOC]

1 Overview

This file contains definitions of the members of class ResetPregel

*/

#include <ListUtils.h>
#include "ResetPregel.h"
#include "../../PregelAlgebra.h"

namespace pregel {
 ListExpr ResetPregel::typeMapping(ListExpr args) {
  if (!nl->IsEmpty(args)) {
   return listutils::typeError("You must provide no arguments.");
  }

  return listutils::basicSymbol<CcBool>();
 }

 int ResetPregel::valueMapping(Word *args, Word &result, int message,
                               Word &local, Supplier s) {
  result = qp->ResultStorage(s);

  PregelAlgebra::getAlgebra()->reset(true);

  ((CcBool *) result.addr)->Set(true, true);
  return 0;
 }

 OperatorSpec ResetPregel::operatorSpec(
  "() -> bool",
  "#",
  "This operator resets the runtime state of the Pregel system. It does so "
  "recursively for all connected workers.",
  "query resetPregel();",
  "This operator belongs to the Pregel API."
  "It may require knowledge of the system to effectively understand and "
  "use all the operators that are provided."
 );

 Operator ResetPregel::resetPregel(
  "resetPregel",
  ResetPregel::operatorSpec.getStr(),
  ResetPregel::valueMapping,
  Operator::SimpleSelect,
  ResetPregel::typeMapping
 );
}
