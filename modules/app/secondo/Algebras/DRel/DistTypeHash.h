/*
----
This file is part of SECONDO.

Copyright (C) 2015,
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


//[$][\$]

*/
#ifndef _DistTypeHash_h_
#define _DistTypeHash_h_

#include "DistTypeBasic.h"

namespace drel {
/*
1 Class ~DistType~

This class represents the distirbution type informations for the class
drel. The supported types are represented by the enum distributionType.
This type is used for hash distribution.

*/
    class DistTypeHash : public DistTypeBasic {
    public:
/*
1.1 Methods

*/
        DistTypeHash( distributionType _type, int _attr );

        DistTypeHash( const DistTypeHash& _distType );
        DistTypeHash &operator=( const DistTypeHash &_distType );
        virtual ~DistTypeHash( );

        virtual bool isEqual( DistTypeBasic* _distType );
        int getAttr( );

        virtual DistTypeBasic* copy( );

        static bool checkType( ListExpr list );

        virtual bool save( SmiRecord& valueRecord, size_t& offset, 
            const ListExpr typeInfo );
        virtual ListExpr toListExpr( ListExpr typeInfo );
        virtual void print( );
        static bool computeNewAttrPos( ListExpr attrPosList, int& attrPos );

/*
1.2 Members

1.2.1 ~attr~

The number of used attribute to distribute the relation. The numbering
starts with 0.

*/
        int attr;
    };

} // end of namespace drel

#endif // _DistTypeHash_h_