/*
----
This file is part of SECONDO.

Copyright (C) 2017,
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
//[_][\_]

*/
#include "FileTransferKeywords.h"
#include "StringUtils.h"

using namespace std;

namespace distributed2
{

string FileTransferKeywords::FileTransferServer() {
    return "<FILETRANSFERSERVER>";
}
string FileTransferKeywords::FileTransferClient() {
    return "<FILETRANSFERCLIENT>";
}
string FileTransferKeywords::SendFile() {
    return "<SENDFILE>";
}
string FileTransferKeywords::ReceiveFile() {
    return "<RECEIVEFILE>";
}
string FileTransferKeywords::Data() {
    return "<DATA>";
}
string FileTransferKeywords::EndData() {
    return "</DATA>";
}
string FileTransferKeywords::FileNotFound() {
    return "<FILENOTFOUND>";
}
string FileTransferKeywords::Cancel() {
    return "<CANCEL>";
}
string FileTransferKeywords::OK() {
    return "<OK>";
}

bool FileTransferKeywords::isBool(string s) {
    stringutils::toLower(s);
    return (s == "true") || (s == "false");
}

bool FileTransferKeywords::getBool(string s) {
    stringutils::toLower(s);
    return s == "true";
}

}
