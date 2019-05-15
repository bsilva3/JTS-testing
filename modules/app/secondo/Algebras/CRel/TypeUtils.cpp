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
along with SECONDO; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
----

*/

#include "TypeUtils.h"

#include <algorithm>
#include "AlgebraManager.h"
#include "ListUtils.h"
#include "Algebras/Standard-C++/LongInt.h"
#include "SecondoException.h"
#include "SecondoSystem.h"
#include "StandardTypes.h"
#include "Symbols.h"

using namespace CRelAlgebra;

using listutils::emptyErrorInfo;
using listutils::isStream;
using std::max;
using std::string;

extern AlgebraManager *am;
extern NestedList *nl;

bool CRelAlgebra::ResolveType(const ListExpr typeExpr, int &algebraId,
                              int &typeId)
{
  ListExpr firstAtom = typeExpr,
    list = nl->Empty();

  while (!nl->IsAtom(firstAtom))
  {
    if (nl->IsEmpty(firstAtom))
    {
      return false;
    }

    list = firstAtom;
    firstAtom = nl->First(firstAtom);
  }

  const NodeType atomType = nl->AtomType(firstAtom);

  if (atomType == IntType)
  {
    if (!nl->HasLength(list, 2))
    {
      return false;
    }

    const ListExpr secondAtom = nl->Second(list);
    if (!nl->IsNodeType(IntType, secondAtom))
    {
      return false;
    }

    algebraId = nl->IntValue(firstAtom);
    typeId = nl->IntValue(secondAtom);

    return true;
  }

  std::string name;
  switch (atomType)
  {
    case StringType:
      name = nl->StringValue(firstAtom);
      break;
    case SymbolType:
      name = nl->SymbolValue(firstAtom);
      break;
    default:
      return false;
  }

  return SecondoSystem::GetCatalog()->GetTypeId(name, algebraId, typeId);
}

bool CRelAlgebra::ResolveType(const ListExpr typeExpr, string &name)
{
  ListExpr firstAtom = typeExpr,
    list = nl->Empty();

  while (!nl->IsAtom(firstAtom))
  {
    if (nl->IsEmpty(firstAtom))
    {
      return false;
    }

    list = firstAtom;
    firstAtom = nl->First(firstAtom);
  }

  switch (nl->AtomType(firstAtom))
  {
    case IntType:
    {
      if (!nl->HasLength(list, 2))
      {
        return false;
      }

      const ListExpr secondAtom = nl->Second(list);
      if (!nl->IsNodeType(IntType, secondAtom))
      {
        return false;
      }

      name = SecondoSystem::GetCatalog()->GetTypeName(nl->IntValue(firstAtom),
                                                      nl->IntValue(secondAtom));

      return true;
    }
    case StringType:
    {
      name = nl->StringValue(firstAtom);
      return true;
    }
    case SymbolType:
    {
      name = nl->SymbolValue(firstAtom);
      return true;
    }
  }

  return false;
}

bool CRelAlgebra::ResolveType(const ListExpr typeExpr, string &name,
                              int &algebraId, int &typeId)
{
  ListExpr firstAtom = typeExpr,
    list = nl->Empty();

  while (!nl->IsAtom(firstAtom))
  {
    if (nl->IsEmpty(firstAtom))
    {
      return false;
    }

    list = firstAtom;
    firstAtom = nl->First(firstAtom);
  }

  const NodeType atomType = nl->AtomType(firstAtom);

  if (atomType == IntType)
  {
    if (!nl->HasLength(list, 2))
    {
      return false;
    }

    const ListExpr secondAtom = nl->Second(list);
    if (!nl->IsNodeType(IntType, secondAtom))
    {
      return false;
    }

    algebraId = nl->IntValue(firstAtom);
    typeId = nl->IntValue(secondAtom);

    name = SecondoSystem::GetCatalog()->GetTypeName(nl->IntValue(firstAtom),
                                                    nl->IntValue(secondAtom));

    return true;
  }

  switch (atomType)
  {
    case StringType:
      name = nl->StringValue(firstAtom);
      break;
    case SymbolType:
      name = nl->SymbolValue(firstAtom);
      break;
    default:
      return false;
  }

  return SecondoSystem::GetCatalog()->GetTypeId(name, algebraId, typeId);
}

void CRelAlgebra::ResolveTypeOrThrow(const ListExpr typeExpr, int &algebraId,
                                     int &typeId)
{
  if (!ResolveType(typeExpr, algebraId, typeId))
  {
    throw SecondoException("Failed to resolve algebraId and typeId for (" +
                           nl->ToString(typeExpr) + ")");
  }
}

void CRelAlgebra::ResolveTypeOrThrow(const ListExpr typeExpr, string &name)
{
  if (!ResolveType(typeExpr, name))
  {
    throw SecondoException("Failed to resolve typeName for (" +
                           nl->ToString(typeExpr) + ")");
  }
}

void CRelAlgebra::ResolveTypeOrThrow(const ListExpr typeExpr, string &name,
                                     int &algebraId, int &typeId)
{
  if (!ResolveType(typeExpr, name, algebraId, typeId))
  {
    throw SecondoException("Failed to resolve typeName, algebraId and typeId "
                           "for (" + nl->ToString(typeExpr) + ")");
  }
}

ListExpr CRelAlgebra::GetStreamType(const ListExpr typeExpr,
                                    bool allowNonStream)
{
  return (allowNonStream && !isStream(typeExpr)) ? typeExpr :
                                                   nl->Second(typeExpr);
}

ListExpr CRelAlgebra::GetNumericType(const string &name)
{
  int algebraId,
    typeId;

  if (!SecondoSystem::GetCatalog()->GetTypeId(name, algebraId, typeId))
  {
    return nl->Empty();
  }

  return nl->TwoElemList(nl->IntAtom(algebraId), nl->IntAtom(typeId));
}

TypeConstructor *CRelAlgebra::GetTypeConstructor(const ListExpr typeExpr)
{
  int algebraId,
    typeId;

  if (ResolveType(typeExpr, algebraId, typeId))
  {
    return am->GetTC(algebraId, typeId);
  }

  return nullptr;
}

bool CRelAlgebra::CheckKind(const std::string &kind, const ListExpr typeExpr)
{
  ListExpr error = emptyErrorInfo();

  return am->CheckKind(kind, typeExpr, error);
}

InObject CRelAlgebra::GetInFunction(const ListExpr typeExpr)
{
  int algebraId,
    typeId;

  if (ResolveType(typeExpr, algebraId, typeId))
  {
    return am->InObj(algebraId, typeId);
  }

  return nullptr;
}

OutObject CRelAlgebra::GetOutFunction(const ListExpr typeExpr)
{
  int algebraId,
    typeId;

  if (ResolveType(typeExpr, algebraId, typeId))
  {
    return am->OutObj(algebraId, typeId);
  }

  return nullptr;
}
