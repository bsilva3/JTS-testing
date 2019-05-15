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
    
Implementation of the Secondo Server Module

2002 U. Telle. 
 
2003-2004 M. Spiekermann. Minor modifications for messages,
binary encoded list transfer and error handling of socket streams.

December 2005, Victor Almeida deleted the deprecated algebra levels
(~executable~, ~descriptive~, and ~hybrid~). Only the executable
level remains.

February 2006. M. Spiekermann. Changes in the client server protocol. Now
the ~restore~ and ~save~ object/database commands work correctly. Moreover the
code was simplified and restructured. As a consequence protocol related procedures 
are implemented in class ~CSProtocol~ and can be used by inside the 
~TTYCS~ and the ~Server~ code. 



*/

#include <cstdlib>
#include <string>
#include <algorithm>
#include <map>
#include <climits>
#include <iostream>
#include <fstream>
#include <sstream>
#include <signal.h>

#include "Application.h"
#include "SocketIO.h"
#include "Messenger.h"
#include "AlgebraTypes.h"
#include "SecondoSystem.h"
#include "SecondoCatalog.h"
#include "SecondoInterface.h"
#include "SecondoInterfaceTTY.h"
#include "FileSystem.h"
#include "Profiles.h"
#include "LogMsg.h"
#include "StopWatch.h"
#include "StringUtils.h"
#include "FileSystem.h"

#include "CSProtocol.h"
#include "NList.h"
#include "satof.h"


using namespace std;


static string currentFolder  = ""; 
static string requestFolder  = "";
static string transferFolder = "";


//#define DEBUG_SERVER true
#define DEBUG_SERVER false

#define debug_server(a) if(DEBUG_SERVER){cout << "getline '"  << a \
                << "' in function '" << __PRETTY_FUNCTION__ << endl;}



void initTransferFolders(){
  if(!currentFolder.empty()){
    return;
  }
  currentFolder = SmiEnvironment::GetSecondoHome();
  requestFolder  = currentFolder + "/filetransfers";
  transferFolder =  (requestFolder +"/" ) 
                   + stringutils::int2str(WinUnix::getpid());
}


class SecondoServer;
typedef void (SecondoServer::*ExecCommand)();

class SecondoServer : public Application
{
 public:
  SecondoServer( const int argc, const char** argv ) : 
     Application( argc, argv ) 
  {};
  virtual ~SecondoServer() {
      if(si) delete si;
      if(csp) delete csp;
      if(client) delete client;
     // the nl pointer is free'd  during destruction of si
  };
  int Execute();
  void CallSecondo();
  void CallNumericType();
  void CallGetTypeId();
  void CallLookUpType();
  void CallDbSave();
  void CallObjectSave();
  void CallDbRestore();
  void CallObjectRestore();
  void CallFileTransfer();
  void CallRequestFile();
  void CallRequestFileFolder();
  void CallRequestFilePath();
  void CallSendFileFolder();
  void CallSendFilePath();
  void CallServerPid();
  void CallGetHome();
  void Connect();
  void Disconnect();
  void WriteResponse( const int errorCode, const int errorPos,
                      const string& errorMessage, ListExpr resultList );
  bool ReceiveFile( const string& clientFileName,
                    const string& serverFileName );
  void CallGetOperatorIndexes();
  void CallGetCosts();
  void CallGetLinearCostFun();
  void CallGetCostFun();
  void CallCancelQuery();
  void CallHeartbeat();
  
 private:

  void CallRestore(const string& tag, bool database=false);
  void CallSave(const string& tag, bool database=false);
  string CreateTmpName(const string& prefix);
  
  Socket*           client;
  SecondoInterface* si;
  NestedList*       nl;
  string            parmFile;
  string            dbDir;
  string            port; 
  bool              quit;
  string            registrar;
  string            user;
  string            pswd;

  CSProtocol* csp;
};


void
SecondoServer::WriteResponse( const int errorCode, const int errorPos,
                              const string& errorMessage, ListExpr resultList )
{
  ListExpr msg = nl->TextAtom();
  nl->AppendText( msg, errorMessage );
  
  ListExpr list = nl->FourElemList(
                    nl->IntAtom( errorCode ),
                    nl->IntAtom( errorPos ),
                    msg,
                    resultList );

  iostream& iosock = client->GetSocketStream();
 
  csp->IgnoreMsg(true); 
  iosock << "<SecondoResponse>" << endl;
  csp::sendList(iosock,nl, list);  
  iosock << "</SecondoResponse>" << endl;
  iosock.flush(); 
}

void
SecondoServer::CallSecondo()
{
  string line="", cmdText="", cmdEnd="";
  iostream& iosock = client->GetSocketStream();
  int type=0;
  iosock >> type;
  debug_server(type);
  csp->skipRestOfLine();
  csp->IgnoreMsg(false);
  bool ready=false;
  do
  {
    getline( iosock, line );
    debug_server(line);
    ready = (line == "</Secondo>");
    if ( !ready )
    {
      cmdText += line + "\n";
    }
  }
  while (!ready && !iosock.fail());
  ListExpr commandLE = nl->TheEmptyList();
  ListExpr resultList = nl->TheEmptyList();
  int errorCode=0, errorPos=0;
  string errorMessage="";
  si->Secondo( cmdText, commandLE, type, true, false, 
               resultList, errorCode, errorPos, errorMessage );
  NList::setNLRef(nl);
  WriteResponse( errorCode, errorPos, errorMessage, resultList );
}

void
SecondoServer::CallNumericType()
{
  string typeStr, cmdEnd;
  iostream& iosock = client->GetSocketStream();
  iosock.clear();
  getline( iosock, typeStr );
  debug_server(typeStr);
  getline( iosock, cmdEnd );
  debug_server(cmdEnd);
  if ( cmdEnd == "</NumericType>" )
  {
    ListExpr typeList = 0;
    nl->ReadFromString( "("+typeStr+")", typeList );
    ListExpr list = si->NumericTypeExpr( nl->First(typeList) );
    nl->WriteToString( typeStr, list );
    iosock << "<NumericTypeResponse>" << endl
           << typeStr << endl
           << "</NumericTypeResponse>" << endl;
    nl->Destroy(list);
    nl->Destroy(typeList);
  }
  else
  {
    iosock << "<SecondoError>" << endl
           << "SECONDO-0080 Protocol error: </NUMERICTYPE> expected." << endl
           << "</SecondoError>" << endl;
  }
  iosock.flush();
}


void SecondoServer::CallGetHome(){
   iostream& iosock = client->GetSocketStream();
   iosock << SmiEnvironment::GetSecondoHome() << endl;
   iosock.flush();
}

void SecondoServer::CallHeartbeat(){
  iostream& iosock = client->GetSocketStream();
  string line;
  getline(iosock,line);
  int heart1 = atoi(line.c_str());
  getline(iosock, line);
  int heart2 = atoi(line.c_str());
  getline(iosock,line);
  if(line!="</HEARTBEAT>"){
     cerr << "missing </HEARTBEAT>" << endl; 
     heart1 = -1;
     heart2 = -1;
  }
  bool ok = SecondoSystem::GetInstance()->SetHeartbeat(heart1,heart2);
  if(ok){
     iosock << "<YES>" << endl;
  } else {
     iosock << "<NO>" << endl;
  }
}


void
SecondoServer::CallGetTypeId()
{
  string name, cmdEnd;
  int algebraId, typeId;
  iostream& iosock = client->GetSocketStream();
  iosock.clear();
  iosock >> name;
  debug_server(name);
  csp->skipRestOfLine();
  getline( iosock, cmdEnd );
  debug_server(cmdEnd);
  if ( cmdEnd == "</GetTypeId>" )
  {
    bool ok = si->GetTypeId( name, algebraId, typeId );
    if ( ok )
    {
      iosock << "<GetTypeIdResponse>" << endl
             << algebraId << " " << typeId << endl
             << "</GetTypeIdResponse>" << endl;
    }
    else
    {
      iosock << "<GetTypeIdResponse>" << endl
             << 0 << " " << 0 << endl
             << "</GetTypeIdResponse>" << endl;
    }
  }
  else
  {
    iosock << "<SecondoError>" << endl
           << "SECONDO-0080 Protocol error: </GetTypeId> expected." << endl
           << "</SecondoError>" << endl;
  }
  iosock.flush();
}

void
SecondoServer::CallLookUpType()
{
  string name, typeStr, cmdEnd;
  int algebraId, typeId;
  iostream& iosock = client->GetSocketStream();
  getline( iosock, typeStr );
  debug_server(typeStr);
  getline( iosock, cmdEnd );
  debug_server(cmdEnd);
  if ( cmdEnd == "</LookUpType>" )
  {
    ListExpr typeList;
    nl->ReadFromString( "(" + typeStr + ")", typeList );
    si->LookUpTypeExpr( nl->First(typeList), name, algebraId, typeId );

    iosock << "<LookUpTypeResponse>" << endl
           << "((" << name << ") " << algebraId << " " << typeId << ")" << endl
           << "</LookUpTypeResponse>" << endl;
    nl->Destroy(typeList);
  }
  else
  {
    iosock << "<SecondoError>" << endl
           << "SECONDO-0080 Protocol error: </LookUpType> expected." << endl
           << "</SecondoError>" << endl;
  }
  iosock.flush();
}


void SecondoServer::CallGetOperatorIndexes(){

   string name;
   ListExpr args;
   iostream& iosock = client->GetSocketStream();
   getline(iosock,name);
   debug_server(name);
   AlgebraManager* am = SecondoSystem::GetAlgebraManager();
   //NestedList* nl = am->getListStorage();
   NestedList* nl1 = SecondoSystem::GetNestedList(); 

   nl1->ReadBinaryFrom(iosock, args);

   string cmdEnd;
   getline(iosock, cmdEnd);
   debug_server(cmdEnd);
   if(cmdEnd=="</REQUESTOPERATORINDEXES>"){
       iosock << "<OPERATORINDEXESRESPONSE>" << endl;
       int algId;
       int OpId;
       int funId;
       ListExpr resList;
    
       NList::setNLRef(nl1); 
       bool ok = am->findOperator(name,args,resList, algId, OpId,funId);
       NList::setNLRef(nl);
      
       stringstream ss;
       ss << (ok?"1":"0") << endl;
       ss << algId << endl << OpId << endl << funId << endl;
       iosock << ss.str();
       nl1->WriteBinaryTo(resList, iosock);
       iosock << endl;
       iosock << "</OPERATORINDEXESRESPONSE>" << endl;
   } else {
     
    iosock << "<SecondoError>" << endl
           << "SECONDO-0080 Protocol error: "
           << "</REQUESTOPERATORINDEXES> expected." << endl
           << " received '" << cmdEnd << "'" << endl
           << "</SecondoError>" << endl;
   }
  iosock.flush();
}

void SecondoServer::CallGetCosts(){

   AlgebraManager* am = SecondoSystem::GetAlgebraManager();
   iostream& iosock = client->GetSocketStream();
   string line;
   getline(iosock,line);
   debug_server(line);

   int noStreams = atoi(line.c_str());
   if((noStreams!=1) && (noStreams!=2)){
    iosock << "<SecondoError>" << endl
           << "SECONDO-0080 Protocol error: getCosts "
           << "can handle only 2 streams" << endl
           << "</SecondoError>" << endl;
     iosock.flush();
     return;
   }
   // operator identifier
   getline(iosock,line);
   debug_server(line);
   int algId = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int opId = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int funId = atoi(line.c_str());
   // informations about the first tuple stream
   // there is at least one
   getline(iosock,line);
   debug_server(line);
   int noTuples1 =  atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int sizeOfTuple1 = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int noAttributes1 = atoi(line.c_str());
   size_t costs;
   bool ok;
   if(noStreams==1){ // there is only 1 stream
      getline(iosock,line);
      debug_server(line);
      double selectivity = satof(line.c_str());
      getline(iosock,line);
      debug_server(line);
      int memoryMB = atoi(line.c_str());
      ok = am->getCosts(algId,opId,funId,
                        noTuples1,sizeOfTuple1, noAttributes1, 
                        selectivity,memoryMB,costs);
   } else {
      // get information about stream 2
      getline(iosock,line);
      debug_server(line);
      int noTuples2 = atoi(line.c_str());
      getline(iosock,line);
      debug_server(line);
      int sizeOfTuple2 = atoi(line.c_str());
      getline(iosock,line);
      debug_server(line);
      int noAttributes2 = satof(line.c_str());
      getline(iosock,line);
      debug_server(line);
      double selectivity = satof(line.c_str());
      getline(iosock,line);
      debug_server(line);
      int memoryMB = atoi(line.c_str());

      ok = am->getCosts(algId,opId,funId,
                        noTuples1,sizeOfTuple1, noAttributes1,
                        noTuples2,sizeOfTuple2, noAttributes2,
                        selectivity, memoryMB, costs);
   }
 
    
   getline(iosock,line);
   debug_server(line);
   if(line!="</GETCOSTS>"){
      iosock << "<SecondoError>" << endl
             << "SECONDO-0080 Protocol error: </GETCOSTS> "
             << " expected" << endl
             << " received '" << line << "'" << endl
             << "</SecondoError>" << endl;
      iosock.flush();
      return;
   }
   iosock << "<COSTRESPONSE>" << endl;
   stringstream ss;
   ss << (ok?"1":"0") << endl;
   ss << costs << endl;
   iosock << ss.str();
   iosock << "</COSTRESPONSE>" << endl;   
   iosock.flush();
}


void SecondoServer::CallGetLinearCostFun(){
   
   AlgebraManager* am = SecondoSystem::GetAlgebraManager();
   iostream& iosock = client->GetSocketStream();
   
   string line;
   getline(iosock,line);
   debug_server(line);
   int noStreams = atoi(line.c_str());
   if((noStreams!=1) && (noStreams!=2)){
    iosock << "<SecondoError>" << endl
           << "SECONDO-0080 Protocol error: getCosts "
           << "can handle only 2 streams" << endl
           << "</SecondoError>" << endl;
     iosock.flush();
     return;
   }
   getline(iosock,line);
   debug_server(line);
   int algId = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int opId = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int funId = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int noTuples1 =  atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int sizeOfTuple1 = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int noAttributes1 = atoi(line.c_str());
   
   




   bool ok;
   double sufficientMemory;
   double timeAtSuffMemory;
   double timeAt16MB;
   if(noStreams==1){
      getline(iosock,line);
      debug_server(line);
      double selectivity = satof(line.c_str());
      ok = am->getLinearParams(algId,opId,funId,
                               noTuples1,sizeOfTuple1, noAttributes1,
                                selectivity,
                               sufficientMemory,timeAtSuffMemory,timeAt16MB);
   } else {
      getline(iosock,line);
      debug_server(line);
      int noTuples2 = atoi(line.c_str());
      getline(iosock,line);
      debug_server(line);
      int sizeOfTuple2 = atoi(line.c_str());
      getline(iosock,line);
      debug_server(line);
      int noAttributes2 = atoi(line.c_str());
      getline(iosock,line);
      debug_server(line);
      double selectivity = satof(line.c_str());

      ok = am->getLinearParams(algId, opId, funId,
                               noTuples1, sizeOfTuple1, noAttributes1,
                               noTuples2, sizeOfTuple2, noAttributes2,
                               selectivity,
                               sufficientMemory,timeAtSuffMemory,timeAt16MB);
   }
   getline(iosock,line);
   debug_server(line);
   if(line!="</GETLINEARCOSTFUN>"){
      iosock << "<SecondoError>" << endl
             << "SECONDO-0080 Protocol error: </GETCOSTS> "
             << " expected" << endl
             << " received '" << line << "'" << endl
             << "</SecondoError>" << endl;
      iosock.flush();
      return;
   }
   stringstream ss;
   ss << "<LINEARCOSTFUNRESPONSE>" << endl;
   ss << (ok?"1":"0") << endl;
   ss << sufficientMemory << endl;
   ss << timeAtSuffMemory << endl;
   ss << timeAt16MB << endl;
   ss << "</LINEARCOSTFUNRESPONSE>" << endl;   
   iosock << ss.str();
   iosock.flush();
}

/*
 * Cancel a running query by sending SIGUSR1 to the query processor 

*/
void SecondoServer::CallCancelQuery() {
#ifdef SECONDO_WIN32
    // Canceling query is currently not supported on windows 
    iosock << "<NOT_SUPPORTED/>" << endl;
#else 
    iostream& iosock = client->GetSocketStream();
    string line;
    getline(iosock,line);
    debug_server(line);
    int pid = atoi(line.c_str());
    getline(iosock,line);
    debug_server(line);
    
    // Ensure that we only send the signal to SecondoBDB processes
    // Otherwise an attacker could send the signal to every process
    // on the server
    const char *secondoName = "SecondoBDB";
         
    stringstream ss;
    ss << "/proc/" << pid << "/cmdline";
    FILE* file = fopen(ss.str().c_str(), "r");

    // Pid still active?
    if(file) {
         char buffer[1024];
         
         fread(buffer, sizeof(char), 1024, file);
         fclose(file);
         
         if(strncmp(secondoName, buffer, strlen(secondoName)) == 0) {
             kill(pid, SIGUSR1);
         }
    }

    iosock << "<OK/>" << endl;
#endif
    
iosock.flush();
}

void SecondoServer::CallGetCostFun(){
   
   AlgebraManager* am = SecondoSystem::GetAlgebraManager();
   iostream& iosock = client->GetSocketStream();
   string line;
   getline(iosock,line);
   debug_server(line);
   int noStreams = atoi(line.c_str());
   if((noStreams!=1) && (noStreams!=2)){
    iosock << "<SecondoError>" << endl
           << "SECONDO-0080 Protocol error: getCosts "
           << "can handle only 2 streams" << endl
           << "</SecondoError>" << endl;
     iosock.flush();
     return;
   }
   getline(iosock,line);
   debug_server(line);
   int algId = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int opId = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int funId = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int noTuples1 =  atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int sizeOfTuple1 = atoi(line.c_str());
   getline(iosock,line);
   debug_server(line);
   int noAttributes1 = atoi(line.c_str());
   bool ok;
   int funType;
   double sufficientMemory;
   double timeAtSuffMemory;
   double timeAt16MB;
   double a;
   double b;
   double c;
   double d;
   if(noStreams==1){
      getline(iosock,line);
      debug_server(line);
      double selectivity  =  satof(line.c_str());
      ok = am->getFunction(algId, opId, funId,
                           noTuples1, sizeOfTuple1, noAttributes1,
                           selectivity,
                           funType,sufficientMemory,timeAtSuffMemory,timeAt16MB,
                           a,b,c,d);
   } else { // nostreams ==2
      getline(iosock,line);
      debug_server(line);
      int noTuples2 = atoi(line.c_str());
      getline(iosock,line);
      debug_server(line);
      int sizeOfTuple2 = atoi(line.c_str());
      getline(iosock,line);
      debug_server(line);
      int noAttributes2 = atoi(line.c_str());
      getline(iosock,line);
      debug_server(line);
      double selectivity = satof(line.c_str()); 

      ok = am->getFunction(algId, opId, funId,
                           noTuples1, sizeOfTuple1, noAttributes1,
                           noTuples2, sizeOfTuple2, noAttributes2,
                           selectivity,
                           funType,sufficientMemory,timeAtSuffMemory,timeAt16MB,
                           a,b,c,d);
   }
   getline(iosock,line);
   debug_server(line);
   if(line!="</GETCOSTFUN>"){
      iosock << "<SecondoError>" << endl
             << "SECONDO-0080 Protocol error: </GETCOSTS> "
             << " expected" << endl
             << " received '" << line << "'" << endl
             << "</SecondoError>" << endl;
      iosock.flush();
      return;
   }
   stringstream ss;
   ss << "<COSTFUNRESPONSE>" << endl;
   ss << (ok?"1":"0") << endl;
   ss << funType << endl;
   ss << sufficientMemory << endl;
   ss << timeAtSuffMemory << endl;
   ss << timeAt16MB << endl;
   ss << a << endl << b << endl << c << endl << d << endl;
   ss << "</COSTFUNRESPONSE>" << endl;   
   iosock << ss.str();
   iosock.flush(); 
}

string
SecondoServer::CreateTmpName(const string& prefix)
{
  ostringstream os;
  os << prefix << GetOwnProcessId();
  return os.str();
}       



void
SecondoServer::CallSave(const string& tag, bool database /*=false*/)
{

  //cout << "Begin CallSave()" << endl;
 
  // parameters for Secondo interface call
  SI_Error errorCode=ERR_NO_ERROR;
  int errorPos=0;
  string errorMessage="";
  ListExpr commandLE = nl->TheEmptyList();
  ListExpr resultList = nl->TheEmptyList();

  string cmdText="";
  string serverFileName = CreateTmpName(tag);
  // Read client message and construct Secondo command
  if (!database)
  {
    // read in object or database name
    iostream& iosock = client->GetSocketStream();
    string name = "";
    iosock >> name;
    debug_server(name);
    csp->skipRestOfLine();

    if(!csp->nextLine("</"+tag+">", errorMessage))
      errorCode = ERR_IN_SECONDO_PROTOCOL;
      
    cmdText= "(save " + name + " to " + serverFileName + ")";
  }
  else
  {
    cmdText = "(save database to " + serverFileName + ")";
  }  
  
  // create file on server 
  if (errorCode == ERR_NO_ERROR)
  {
   
    si->Secondo( cmdText, commandLE, 0, true, false, 
                 resultList, errorCode, errorPos, errorMessage );
    NList::setNLRef(nl); 

  } 

  // If successful create list from file
  if (errorCode == ERR_NO_ERROR)
  {
    nl->ReadFromFile( serverFileName, resultList );
  } 
   
  WriteResponse( errorCode, errorPos, errorMessage, resultList );
  //FileSystem::DeleteFileOrFolder( serverFileName );

  //cout << "End CallSave()" << endl;
}


void
SecondoServer::CallDbSave()
{
  CallSave("DbSave", true);
}


void
SecondoServer::CallObjectSave()
{
  CallSave("ObjectSave");
}


void
SecondoServer::CallRestore(const string& tag, bool database/*=false*/)
{
  // parameters for Secondo interface call
  SI_Error errorCode=0;
  int errorPos=0;
  string errorMessage="";
  ListExpr commandLE = nl->TheEmptyList();
  ListExpr resultList = nl->TheEmptyList();
  
  // read in object or database name
  iostream& iosock = client->GetSocketStream();
  string name = "";
  iosock >> name;
  debug_server(name);
  csp->skipRestOfLine();
  
  //cout << "Begin CallRestore()" << endl;
  
  string serverFileName= CreateTmpName(tag);
  if ( csp->ReceiveFile( serverFileName ) )
  {
    string cmdText="";

    // construct Secondo command
    if (database)
    {
      cmdText = "(restore database " + name +
                " from " + serverFileName + ")";
            
    }
    else
    {       
      cmdText= "(restore " + name +
               " from " + serverFileName + ")";
    } 
    
    si->Secondo( cmdText, commandLE, 0, true, false, 
                 resultList, errorCode, errorPos, errorMessage );
    NList::setNLRef(nl);
  }
  else
  {
    
    errorCode = ERR_IN_SECONDO_PROTOCOL;
    errorMessage = "Protocol-Error: File not received correctly."; 
    resultList = nl->TheEmptyList();
  }
  FileSystem::DeleteFileOrFolder(serverFileName);
  
  if (!csp->nextLine("</"+tag+">", errorMessage) )
  {
    errorCode = ERR_IN_SECONDO_PROTOCOL;
  }
  WriteResponse( errorCode, errorPos, errorMessage, resultList );
  //FileSystem::DeleteFileOrFolder( serverFileName );

  //cout << "End CallRestore()" << endl;
}


void
SecondoServer::CallObjectRestore()
{
  CallRestore("ObjectRestore");    
}       

void
SecondoServer::CallDbRestore()
{
  CallRestore("DbRestore",true);        
}       


bool isValidFileName(const string& name){
  if(name.empty()) return false;
  if(stringutils::startsWith(name, "/")) return false;
  if(name.find("..") != string::npos) return false;
  return true;
}

void
SecondoServer::CallFileTransfer() {
  // parameters for Secondo interface call
  initTransferFolders();
  SI_Error errorCode=0;
  int errorPos=0;
  string errorMessage="";
  ListExpr resultList = nl->TheEmptyList();
  
  // read in object or database name
  iostream& iosock = client->GetSocketStream();
  string serverFileName = "";
  iosock >> serverFileName;
  debug_server(serverFileName);
  csp->skipRestOfLine();
  string allowOverwriteS;
  getline(iosock, allowOverwriteS);
  debug_server(allowOverwriteS);
  bool allowOverwrite = allowOverwriteS == "<ALLOW_OVERWRITE>"; 
  
  stringutils::trim(serverFileName);
  if(!isValidFileName(serverFileName)){
     iosock << "<SecondoError>" << endl;
     iosock << stringutils::int2str(ERR_INVALID_FILE_NAME) << endl;
     iosock << "</SecondoError>" << endl;
     iosock.flush();
     return;
  }
  
  string fullFileName = transferFolder  + "/" + serverFileName; 

  if(!allowOverwrite){
     if(FileSystem::FileOrFolderExists(fullFileName)){
       iosock << "<SecondoError>" << endl;
       iosock << stringutils::int2str(ERR_FILE_EXISTS) << endl;
       iosock << "</SecondoError>" << endl;
       iosock.flush();
       return;
     }
  }

  if(FileSystem::IsDirectory(fullFileName)){ // overwriting impossible
       iosock << "<SecondoError>" << endl;
       iosock << stringutils::int2str(ERR_FILE_EXISTS) << endl;
       iosock << "</SecondoError>" << endl;
       iosock.flush();
       return;
  } 

   
  int lastPathSeparator = fullFileName.find_last_of("/");
  string path = fullFileName.substr(0,lastPathSeparator);
  if(!FileSystem::IsDirectory(path)){
    FileSystem::CreateFolderEx(path);
  }
  iosock << "<SecondoOK>" << endl;
  iosock.flush(); 

  if ( !csp->ReceiveFile( fullFileName) ) {
    errorCode = ERR_IN_SECONDO_PROTOCOL;
    errorMessage = "Protocol-Error: File not received correctly."; 
    resultList = nl->TheEmptyList();
  }
  
  if (!csp->nextLine(csp->endFileTransfer, errorMessage) )
  {
    errorCode = ERR_IN_SECONDO_PROTOCOL;
  }
  WriteResponse( errorCode, errorPos, errorMessage, resultList );
}




void SecondoServer::CallRequestFileFolder(){
  initTransferFolders();
  iostream& iosock = client->GetSocketStream();
  string res = requestFolder.substr(currentFolder.length()+1);
  iosock << res << endl;
  iosock.flush();
}

void SecondoServer::CallRequestFilePath(){
  initTransferFolders();
  iostream& iosock = client->GetSocketStream();
  string res = requestFolder;
  iosock << res << endl;
  iosock.flush();
}


void SecondoServer::CallSendFileFolder(){
  initTransferFolders();
  iostream& iosock = client->GetSocketStream();
  string res = transferFolder.substr(currentFolder.length()+1);
  iosock << res << endl;
  iosock.flush();
}

void SecondoServer::CallSendFilePath(){
  initTransferFolders();
  iostream& iosock = client->GetSocketStream();
  string res = transferFolder;
  iosock << res << endl;
  iosock.flush();
}

void SecondoServer::CallServerPid(){
  iostream& iosock = client->GetSocketStream();
  iosock << stringutils::int2str(WinUnix::getpid()) << endl;
  iosock.flush();
}

void 
SecondoServer::CallRequestFile(){
  initTransferFolders();
  iostream& iosock = client->GetSocketStream();
  string serverFileName = "";
  iosock >> serverFileName;
  debug_server(serverFileName);
  csp->skipRestOfLine();
  string errorMessage="";
  if(!csp->nextLine(csp->endRequestFile, errorMessage)){
     return;  // protocol error
  }
  // check validity of the file file, i.e. the name cannot
  // be empty, cannot start with a '/' and cannot
  // contain '..' . 
  stringutils::trim(serverFileName);
  if(!isValidFileName(serverFileName)){
     iosock << "<SecondoError>" << endl;
     iosock << stringutils::int2str(ERR_INVALID_FILE_NAME) << endl;
     iosock << "</SecondoError>" << endl;
     iosock.flush();
     return;
  }       
  string fullFileName = requestFolder + "/" + serverFileName; 

  // check wether file is present
  ifstream in(fullFileName.c_str());
  if(!in.good()){
     iosock << "<SecondoError>" << endl;
     iosock << stringutils::int2str(ERR_FILE_NOT_EXISTS) << endl;
     iosock << "</SecondoError>" << endl;
     iosock.flush();
     return;
  } 
  in.close();
  iosock << "<SecondoOK>" << endl;
  iosock.flush();
  csp->SendFile(fullFileName);  
  iosock.flush();
}



void
SecondoServer::Connect()
{
  iostream& iosock = client->GetSocketStream();
  string line;
  getline( iosock, user );
  debug_server(user);
  getline( iosock, pswd );
  debug_server(pswd);
  //cout << "user = " << user << endl;
  //cout << "passwd = " << pswd << endl;
  getline( iosock, line ); //eat up </USER> ?
  debug_server(line);
}

void
SecondoServer::Disconnect()
{
  quit = true;
}

int SecondoServer::Execute() {
  int rc = 0;
  parmFile = (GetArgCount() > 1) ? GetArgValues()[1] : "SecondoConfig.ini";
  dbDir = (GetArgCount() >2) ? GetArgValues()[2] : "";
  port = (GetArgCount() > 3) ? GetArgValues()[3] : "";
  registrar = SmiProfile::GetUniqueSocketName( parmFile , port);

  if(dbDir.empty()){
     dbDir = SmiProfile::GetParameter( "Environment", 
                                       "SecondoHome", 
                                       "", 
                                       parmFile );
  }

  si = new SecondoInterfaceTTY(true);

  cout << "Initialize the secondo interface " << endl;

  map<string,ExecCommand> commandTable;
  map<string,ExecCommand>::iterator cmdPos;
  commandTable["<Secondo>"]     = &SecondoServer::CallSecondo;
  commandTable["<NumericType>"] = &SecondoServer::CallNumericType;
  commandTable["<GetTypeId>"]   = &SecondoServer::CallGetTypeId;
  commandTable["<LookUpType>"]  = &SecondoServer::CallLookUpType;
  commandTable["<DbSave/>"]      = &SecondoServer::CallDbSave;
  commandTable["<ObjectSave>"]  = &SecondoServer::CallObjectSave;
  commandTable["<ObjectRestore>"]   = &SecondoServer::CallObjectRestore;
  commandTable["<DbRestore>"]   = &SecondoServer::CallDbRestore;
  commandTable["<FileTransfer>"]   = &SecondoServer::CallFileTransfer;
  commandTable["<RequestFile>"] = &SecondoServer::CallRequestFile;
  commandTable["<REQUEST_FILE_FOLDER>"] 
               = &SecondoServer::CallRequestFileFolder;
  commandTable["<REQUEST_FILE_PATH>"] 
               = &SecondoServer::CallRequestFilePath;
  commandTable["<SEND_FILE_FOLDER>"] 
               = &SecondoServer::CallSendFileFolder;
  commandTable["<SEND_FILE_PATH>"] 
               = &SecondoServer::CallSendFilePath;
  commandTable["<SERVER_PID>"] 
               = &SecondoServer::CallServerPid;
  commandTable["<Connect>"]     = &SecondoServer::Connect;
  commandTable["<Disconnect/>"] = &SecondoServer::Disconnect;
  commandTable["<REQUESTOPERATORINDEXES>"] = 
                                    &SecondoServer::CallGetOperatorIndexes;
  commandTable["<GETCOSTS>"] = &SecondoServer::CallGetCosts;
  commandTable["<GETLINEARCOSTFUN>"] = &SecondoServer::CallGetLinearCostFun;
  commandTable["<GETCOSTFUN>"] = &SecondoServer::CallGetCostFun;
  commandTable["<CANCEL_QUERY>"] = &SecondoServer::CallCancelQuery;
  commandTable["<GET_HOME>"] = &SecondoServer::CallGetHome;
  commandTable["<HEARTBEAT>"] = &SecondoServer::CallHeartbeat;
  
  string logMsgList = SmiProfile::GetParameter( "Environment", 
                                                "RTFlags", "", parmFile );
  RTFlag::initByString(logMsgList);


  client = GetSocket();
  if(!client){
    rc = -2;
  } else {
     ostream* traceInS = 0;
     ostream* traceOutS = 0;
     string traceIn = SmiProfile::GetParameter("Environment",
                                               "TraceServerIn",
                                                "", parmFile);           
     string traceOut = SmiProfile::GetParameter("Environment",
                                               "TraceServerOut",
                                                "", parmFile);
     if(!traceIn.empty()){
        string fn = traceIn+"_"+stringutils::int2str(WinUnix::getpid())+".log";
        traceInS = new ofstream(fn.c_str(),ios::binary);
     }         
     if(!traceOut.empty()){
         if(traceIn==traceOut){
             traceOutS = traceInS;
         } else {
           string fn = traceOut+"_"+ stringutils::int2str(WinUnix::getpid())
                     + ".log";
           traceOutS = new ofstream(fn.c_str(),ios::binary);
         }
     }
     if(traceInS || traceOutS){
        client->setTraceStreams(traceInS, traceOutS, true);
     }

    iostream& iosock = client->GetSocketStream();
    csp = new CSProtocol(nl, iosock, true);
    //si->SetProtocolPtr(csp);
    
    ios_base::iostate s = iosock.exceptions();
    iosock.exceptions(ios_base::failbit|ios_base::badbit|ios_base::eofbit);
    iosock << "<SecondoOk/>" << endl;
    quit = false;
    // first connect to get the user and password information
    try {
        string cmd;
        getline( iosock, cmd );
        debug_server(cmd); 
        cmdPos = commandTable.find( cmd );
        if ( cmdPos != commandTable.end() )
        {
           (*this.*(cmdPos->second))();
        }
        else
        {
          iosock << "<SecondoError>" << endl
                 << "SECONDO-0080 Protocol-Error: Start tag \"" 
                 << cmd << "\" unknown!" << endl
                 << "</SecondoError>" << endl;
        }
        if ( Application::Instance()->ShouldAbort() )
        {
          iosock << "<SecondoError>" << endl
                 << "SECONDO-9999 Server going down. Disconnecting." << endl
                 << "</SecondoError>" << endl;
          quit = true;
        }
    
      } catch (ios_base::failure) {
        cerr << endl 
             << "I/O error on socket stream object during initialization!" 
             << endl;
        if ( !client->IsOk() ) {
           cerr << "Socket Error: " << client->GetErrorText() << endl;  
         }
       quit = true; 
      }
    cout << "Try to initialize the secondo system " << endl; 
    string errorMsg("");
    if( si->Initialize( user, pswd, "", port, parmFile, dbDir,errorMsg, true ))
    {
       cout << "initialization successful" << endl;
       iosock << "<SecondoIntro>" << endl
              << "You are connected with a Secondo server." << endl
              << "</SecondoIntro>" << endl;
       //Messenger messenger( registrar );
       //string answer;
       //ostringstream os;
       //os << "LOGIN " << user << " " << GetOwnProcessId();
       //messenger.Send( os.str(), answer );
       SmiEnvironment::SetUser( user );

      // initialization successfull, send ok and wait for further requests



      nl = si->GetNestedList();
      NList::setNLRef(nl);


      do {
      try {
        string cmd;
        getline( iosock, cmd );
        debug_server(cmd); 
        cmdPos = commandTable.find( cmd );
        if ( cmdPos != commandTable.end() )
        {
           (*this.*(cmdPos->second))();
        }
        else
        {
          iosock << "<SecondoError>" << endl
                 << "SECONDO-0080 Protocol-Error: Start tag \"" 
                 << cmd << "\" unknown!" << endl
                 << "</SecondoError>" << endl;
        }
        if ( Application::Instance()->ShouldAbort() )
        {
          iosock << "<SecondoError>" << endl
                 << "SECONDO-9999 Server going down. Disconnecting." << endl
                 << "</SecondoError>" << endl;
          quit = true;
        }
    
      } catch (ios_base::failure) {
        cerr << endl 
             << "I/O error on socket stream object during processing commands!" 
             << endl;
        if ( !client->IsOk() ) {
           cerr << "Socket Error: " << client->GetErrorText() << endl;  
         }
       quit = true; 
      }

      } while (!iosock.fail() && !quit);

      if(iosock.fail()){
         cerr << "connection broken, terminate" << endl;
      }
      
      iosock.exceptions(s);

      client->Close();
      delete client;
      //os << "LOGOUT " << user << " " << GetOwnProcessId();
      //messenger.Send( os.str(), answer );
      client = 0;
    } else {
       iosock << "<SecondoError>" << endl
              << "Initialization failed (username, password correct?)" << endl
              << errorMsg  
              << "</SecondoError>" << endl;
      rc = -1;
    }
    //iosock.flush();
  }

  si->Terminate();
  delete si;
  si = 0;
  return (rc);
}

int SecondoServerMode( const int argc, const char* argv[] )
{
  string msgfolder = "server.msg";

  if(!FileSystem::FileOrFolderExists(msgfolder)){
     FileSystem::CreateFolder(msgfolder);
  }

  FileSystem::AppendItem(msgfolder, 
             "msg_"+ stringutils::int2str(WinUnix::getpid())+".txt");

  ofstream fmsg;
  fmsg.open(msgfolder.c_str(), ios::app);

  cout << "Redirecting server output to file " << msgfolder << endl;

  streambuf* backup1 = cout.rdbuf();   // back up cout's streambuf
  streambuf* backup2 = cerr.rdbuf();   
  streambuf* backup3 = clog.rdbuf();   

  cout.rdbuf(fmsg.rdbuf());   // assign streambuf to cout and cerr
  cerr.rdbuf(fmsg.rdbuf());
  clog.rdbuf(fmsg.rdbuf());

  freopen(msgfolder.c_str(),"a", stdout);
  freopen(msgfolder.c_str(),"a", stderr);

  SecondoServer* appPointer = new SecondoServer( argc, argv );
  int rc = appPointer->Execute();
  delete appPointer;

  cout.rdbuf(backup1);
  cerr.rdbuf(backup2);
  clog.rdbuf(backup3);
  fmsg.close();
  fclose(stdout);
  fclose(stderr);

  return (rc);
}

