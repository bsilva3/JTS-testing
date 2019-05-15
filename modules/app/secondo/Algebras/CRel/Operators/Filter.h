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

#pragma once

#include "AlgebraTypes.h"
#include <cstdint>
#include "Ints.h"
#include "NestedList.h"
#include "Operator.h"
#include "SecondoSMI.h"
#include "Algebras/Stream/Stream.h"
#include "../TBlock.h"
#include "../TypeConstructors/TBlockTC.h"
#include <vector>

namespace CRelAlgebra
{
  namespace Operators
  {
    template<bool project>
    class Filter : public Operator
    {
    public:
      Filter();

    private:
      class State
      {
      public:
        State(Supplier stream, Supplier filter, const TBlockTI &blockType,
              uint64_t *projection, double copyLimit);

        ~State();

        TBlock *Request();

      private:
        TBlock *m_sourceBlock,
          *m_targetBlock;

        LongInts *m_filteredIndices;

        const uint64_t m_desiredBlockSize;

        uint64_t m_filteredIndex;

        Stream<TBlock> m_stream;

        Supplier m_filter;

        Address &m_filterArg;

        const PTBlockInfo m_blockInfo;

        const uint64_t * const m_projection;

        const double m_copyLimit;
      };

      static const OperatorInfo info;

      static ListExpr TypeMapping(ListExpr args);

      static State *CreateState(ArgVector args, Supplier s);
    };
  }
}
