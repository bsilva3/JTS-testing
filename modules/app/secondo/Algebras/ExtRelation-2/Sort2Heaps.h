
/*
----
This file is part of SECONDO.

Copyright (C) 2016,
Faculty of Mathematics and Computer Science,
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


//[<] [\ensuremath{<}]
//[>] [\ensuremath{>}]

*/


#ifndef SORT2HEAPS_H
#define SORT2HEAPS_H

#include "NestedList.h"

ListExpr Sort2HeapsTM(ListExpr args);

ListExpr SortBy2HeapsTM(ListExpr args);

int Sort2HeapsVM(Word* args, Word& result, int message,
          Word& local, Supplier s);

ListExpr sortattrTM(ListExpr args);

int sortattrVM(Word* args, Word& result, int message,
          Word& local, Supplier s);

#endif



