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

This header file defines the class LoopbackProxy

2 Defines and includes

*/

#ifndef SECONDO_MESSAGECLIENTLOOPBACKPROXY_H
#define SECONDO_MESSAGECLIENTLOOPBACKPROXY_H

#include "MessageClient.h"
#include "../Helpers/RemoteEndpoint.h"
#include <functional>

namespace pregel {
 class LoopbackProxy : public MessageClient {
 private:
  const std::function<void(std::shared_ptr<MessageWrapper> )> sendCallback;

 public:
  LoopbackProxy(std::function<void(std::shared_ptr<MessageWrapper> )> callback);

  ~LoopbackProxy() override;

  void sendMessage(std::shared_ptr<MessageWrapper> message) const override;

  void healthReport(std::stringstream &sstream) const override;
 };
}


#endif //SECONDO_MESSAGECLIENTLOOPBACKPROXY_H
