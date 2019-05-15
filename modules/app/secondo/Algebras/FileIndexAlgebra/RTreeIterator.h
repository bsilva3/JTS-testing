 
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

//paragraph [1] Title: [{\Large \bf \begin{center}] [\end{center}}]
//paragraph [10] Footnote: [{\footnote{] [}}]
//[->] [$\rightarrow$]
//[TOC] [\tableofcontents]
//[_] [\_]

RTree-Class

*/

#ifndef RTREEITERATOR_H
#define RTREEITERATOR_H


#include <vector>
#include "RTree.h"
#include "Algebras/Rectangle/RectangleAlgebra.h"


namespace fialgebra{
  
template <int dim>
class RTreeIterator{
public:
  //Constructor
  RTreeIterator (RTree<dim>* rtree, Rectangle<dim> rectArg);
  //Destructor
  ~RTreeIterator();
  //Suchmethode
  size_t Search();

private:
  std::vector<std::pair<size_t, unsigned int> > pathStack;
  RTree<dim>* rt;
  Rectangle<dim> rect;
}; 
}//end of namespace fialgebra
#endif // RTREEITERATOR_H


