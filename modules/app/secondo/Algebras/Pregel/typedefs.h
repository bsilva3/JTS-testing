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

This header file contains type and macro definitions

2 Defines and includes

*/

#ifndef SECONDO_TYPEDEFS_H
#define SECONDO_TYPEDEFS_H

#include <memory>
#include <functional>
#include "../Distributed2/ConnectionInfo.h"

namespace pregel {
 #define PRECONDITION(condition, message) \
 if (!(condition)) { \
  BOOST_LOG_TRIVIAL(error) << message; \
  ((CcBool *) result.addr)->Set(true, false); \
  return 0; \
 }

 using WorkerConnection = distributed2::ConnectionInfo;

 template<typename Type> using supplier = std::function<Type *()>;
 template<typename Type> using supplier2 
                         = std::function<std::shared_ptr<Type> ()>;
 template<typename Type> using consumer = std::function<void(Type *)>;
 template<typename Type> using consumer2 
                        = std::function<void(std::shared_ptr<Type> )>;
 using executable = std::function<void()>;
}

#endif //SECONDO_TYPEDEFS_H
