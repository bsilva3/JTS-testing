/*
----
This file is part of SECONDO.

Copyright (C) 2004-2009, University in Hagen, Faculty of Mathematics
and Computer Science, Database Systems for New Applications.

SECONDO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

SECONDO is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
auint64_t with SECONDO; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
----

*/

#pragma once

#include "AttrArray.h"
#include <cstdint>
#include "LinesTC.h"
#include "NestedList.h"
#include "ReadWrite.h"
#include <string>
#include "TypeConstructor.h"

namespace CRelAlgebra
{
  class LinesTI
  {
  public:
    static bool Check(ListExpr typeExpr);

    static bool Check(ListExpr typeExpr, std::string &error);

    LinesTI(bool numeric);

    ListExpr GetTypeExpr() const;

  private:
    bool m_isNumeric;
  };

  class LinesTC : public AttrArrayTypeConstructor
  {
  public:
    static const std::string name;

    static ListExpr TypeProperty();

    static bool CheckType(ListExpr typeExpr, ListExpr &errorInfo);

    static Word In(ListExpr typeExpr, ListExpr value, int errorPos,
                   ListExpr &errorInfo, bool &correct);

    static ListExpr Out(ListExpr typeExpr, Word value);

    static Word Create(const ListExpr typeExpr);

    static void Delete(const ListExpr typeExpr, Word &value);

    static bool Open(SmiRecord &valueRecord, size_t &offset,
                     const ListExpr typeExpr, Word &value);

    static bool Save(SmiRecord &valueRecord, size_t &offset,
                     const ListExpr typeExpr, Word &value);

    static void Close(const ListExpr typeExpr, Word &w);

    static void *Cast(void *addr);

    static int SizeOf();

    static Word Clone(const ListExpr typeExpr, const Word &w);

    static ListExpr GetAttributeType(ListExpr typeExpr, bool numeric);

    static AttrArrayManager *CreateManager(ListExpr attributeType);

    LinesTC();
  };
}
