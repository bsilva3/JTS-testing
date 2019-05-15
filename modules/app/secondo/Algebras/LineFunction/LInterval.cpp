
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

*/


#include "LInterval.h"

/*
1 C++ Classes (Implementation)

1.1 LInterval

1.1.1 Constructors

1.1.1.1 Copy constructor

*/

LInterval::LInterval( const LInterval& linterval ):
    start(linterval.start), end(linterval.end),
    lc( linterval.lc ), rc( linterval.rc )
{ }

/*
1.1.1.2 Setting constructor

*/

LInterval::LInterval( const CcReal& start1, const CcReal& end1,
                      const bool lc1, const bool rc1 ):
    start(start1), end(end1), lc( lc1 ), rc( rc1 )
{ }

/*
1.1.2 Member functions

1.1.2.1. Is Valid

*/

bool LInterval::IsValid() const
{
    if( !start.IsDefined() || !end.IsDefined() )
        return false;

    int cmp = start.Compare( &end );
    if( cmp < 0 ) // start < end
        return true;
    else if( cmp == 0 ) // start == end
        return rc && lc;
    // start > end
    return false;
}

/*
1.1.2.2 Disjoint

*/

bool LInterval::R_Disjoint( const LInterval& i ) const
{
    bool res= ((end.Compare( &i.start ) < 0) ||
              ((end.Compare( &i.start ) == 0) && !( rc && i.lc )));
    return( res );
}

bool LInterval::Disjoint( const LInterval& i ) const
{
    assert( IsValid() && i.IsValid() );
    bool res=( R_Disjoint( i ) || i.R_Disjoint( *this ) );
    return( res );
}

/*
1.1.2.3 Before

*/

bool LInterval::Before( const LInterval& i ) const
{
    assert( IsValid() && i.IsValid() );

    if( Before( i.start ) )
        return true;

    return end.Compare( &i.start ) == 0 && i.lc == false;
}

bool LInterval::Before( const CcReal& i ) const
{
    assert( IsValid() && i.IsDefined() );

    return ( end.Compare( &i ) < 0 ||
           ( end.Compare( &i ) == 0 && rc == false ) );
}
/*
1.1.2.4 After

*/

bool LInterval::After( const CcReal& i ) const
{
    assert( IsValid() && i.IsDefined() );

    return ( start.Compare( &i ) > 0 ||
           ( start.Compare( &i ) == 0 && lc == false ) );
}


bool LInterval::After( const LInterval& iv ) const
{
    assert( IsValid() && iv.IsValid() );

    return (iv.end < start) ||
           ((iv.end == start) && (!iv.rc || !lc));
}

/*
1.1.2.5 CompareTo

*/

int  LInterval::CompareTo( const LInterval& i) const
{
    int cmp = start.Compare( &(i.start) );
    if( cmp != 0 )
        return cmp;
    if(!lc && i.lc)
        return 1;
    if(lc && !i.lc)
        return -1;

    cmp = end.Compare( &(i.end) );
    if( cmp != 0 )
        return cmp;
    if(rc && !i.rc)
        return 1;

    if(!rc && i.rc)
        return -1;

    return 0;
}

/*
1.1.2.6 Contains

*/

bool LInterval::Contains( const CcReal& a,
                          const bool ignoreCloseness ) const
{
    assert(this->IsValid());
    assert(a.IsDefined());

    bool lc = this->lc || ignoreCloseness;
    bool rc = this->rc || ignoreCloseness;
    return ( ( start.Compare( &a ) < 0 ||
             ( start.Compare( &a ) == 0 && lc ) ) &&
             ( end.Compare( &a ) > 0 ||
             ( end.Compare( &a ) == 0 && rc ) ) );
}


bool LInterval::Contains( const LInterval& i,
                          const bool ignoreCloseness ) const
{
    int cmp1 = start.Compare(&(i.start));
    int cmp2 = end.Compare(&(i.end));
    if(cmp1>0)    // i starts before this
        return false;
    if((cmp1==0) &&  !lc && i.lc && !ignoreCloseness) // i starts before this
        return false;
    // start is ok
    if(cmp2<0) // this ends before i
        return false;
    if(cmp2==0 && !rc && i.rc && !ignoreCloseness)
        return false;
    return true;
}

/*
1.1.3 Operator Redefinitions

1.1.3.1 Operation ~copy~

*/

LInterval& LInterval::operator=( const LInterval& i )
{
    assert( i.IsValid() );

    start.CopyFrom( &i.start );
    end.CopyFrom( &i.end );
    lc = i.lc;
    rc = i.rc;
    return *this;
}

/*
1.1.3.2 Operation $=$ (~equal~)

*/

bool LInterval::operator==( const LInterval& i ) const
{
    assert( IsValid() && i.IsValid() );

    return( ( start.Compare( &i.start ) == 0 && lc == i.lc &&
            end.Compare( &i.end ) == 0 && rc == i.rc ) ||
            ( start.Compare( &i.start ) == 0 && lc == i.lc &&
            end.Compare( &i.end ) != 0 &&
            end.Adjacent( &i.end ) && ( !rc || !i.rc ) ) ||
            ( end.Compare( &i.end ) == 0 && rc == i.rc &&
            start.Compare( &i.start ) != 0 && start.Adjacent( &i.start ) &&
            ( !lc || !i.lc ) ) ||
            ( start.Compare( &i.start ) != 0 && start.Adjacent( &i.start )
            && (!lc || !i.lc) &&
            end.Compare( &i.end ) != 0 && end.Adjacent( &i.end ) &&
            ( !rc || !i.rc ) ) );
}

/*
1.1.3.3 Operation $\neq$ (~not equal~)

*/

bool LInterval::operator!=( const LInterval& i ) const
{
    return !( *this == i );
}

/*
1.1.3.4 Operation $<$ (~smaller~)

*/

bool LInterval::operator<( const LInterval& i ) const
{
    return CompareTo(i) <0;
}

/*
1.1.3.5 Operation $\>$ (~greater~)

*/

bool LInterval::operator>( const LInterval& i ) const
{
    return CompareTo(i) >0;
}

/*
1.1.4 Functions to be part of relations

1.1.4.1 Adjacent

*/

bool LInterval::R_Adjacent( const LInterval& i ) const
{
    bool res=( (Disjoint( i ) &&
             ( end.Compare( &i.start ) == 0 && (rc || i.lc) )) ||
             ( ( end.Compare( &i.start ) < 0 && rc && i.lc ) &&
             end.Adjacent( &i.start ) ) );
    return( res );
}

bool LInterval::Adjacent( const LInterval& i ) const
{
    assert( IsValid() && i.IsValid() );
    bool res= ( R_Adjacent( i ) || i.R_Adjacent( *this ) );
    return( res );
}

/*
1.1.4.2 CopyFrom

*/

void LInterval::CopyFrom( const LInterval& i )
{
    start.CopyFrom( &i.start );
    end.CopyFrom( &i.end );
    lc = i.lc;
    rc = i.rc;
}

/*
2 Output Operator

*/

std::ostream& operator<<(std::ostream& o, const LInterval& u)
{
   return u.Print(o);
}
