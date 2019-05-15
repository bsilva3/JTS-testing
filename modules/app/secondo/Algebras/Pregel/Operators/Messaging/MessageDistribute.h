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

This header file contains the definition of the class MessageDistribute

2 Defines and includes

*/

#ifndef SECONDO_MESSAGEDISTRIBUTE_H
#define SECONDO_MESSAGEDISTRIBUTE_H

#include <Operator.h>
#include <boost/log/trivial.hpp>
#include "../../MessageBroker/MessageBroker.h"
#include "../../../Stream/Stream.h"

namespace pregel {
class MessageDistribute {
public:
 static ListExpr typeMapping(ListExpr args);

  static int valueMapping(Word *args,
                          Word &result,
                          int ignored,
                          Word &local,
                          void *s);

  static void distributeMessages(Stream<Tuple>, MessageBroker &);

  static OperatorSpec operatorSpec;

  static Operator messageDistribute;
};
}


#endif //SECONDO_MESSAGEDISTRIBUTE_H
