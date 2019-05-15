/*
This file is part of SECONDO.

Copyright (C) 2011, University in Hagen, Department of Computer Science,
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

2012, November Simone Jandt

1 Defines and Includes

*/

#ifndef JNETWORKADAPTER_H
#define JNETWORKADAPTER_H

#include "MapMatchingNetworkInterface.h"
#include "Algebras/JNet/JNetwork.h"


namespace mapmatch{

/*
1 class JNetworkAdapter

Implements IMMNetwork for JNetwork class to enable Mpatmatching to JNetwork
objects.

*/

class JNetworkAdapter : public IMMNetwork
{

public:

/*
1.1. Constructors and Deconstructor

*/

    JNetworkAdapter(jnetwork::JNetwork* jnet = NULL);
    JNetworkAdapter(const JNetworkAdapter& other);
    virtual ~JNetworkAdapter();

/*
1.1. Get Networkinformations

*/
    virtual bool GetSections(const Rectangle<2>& rBBox,
            std::vector<std::shared_ptr<IMMNetworkSection> >& 
                                                     vecSections) const;
    virtual Rectangle<2> GetBoundingBox() const;
    virtual double GetNetworkScale() const;
    virtual bool IsDefined() const;
    virtual bool CanGetRoadType() const;

    jnetwork::JNetwork* GetNetwork() const;
private:
    jnetwork::JNetwork* pJNet;
};

} // end of namespace mapmatch

#endif // JNETWORKADAPTER_H
