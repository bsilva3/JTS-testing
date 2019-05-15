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


1 QueryExecutor for Distributed-SECONDO


1.1 Includes

*/

#include <string>
#include <iostream>
#include <map>
#include <algorithm>

#include <unistd.h>
#include <stdlib.h>
#include <time.h>

#include "SecondoInterface.h"
#include "NestedList.h"
#include "NList.h"
#include "qelogger.h"
#include "CassandraAdapter.h"
#include "CassandraResult.h"
#include "heartbeat.h"
#include "workerqueue.h"
#include "qeutils.h"
#include "secondoworker.h"
#include "state.h"
#include "cassandrainfo.h"

/*
1.1 Defines

*/

// Enum for ownership of a token range
// Local Tokenrange   - We have to process the data in the range
// Foreign Tokenrange - An other worker process has to process the data
enum RANGE_MODE {LOCAL_TOKENRANGE, FOREIGN_TOKENRANGE};

#define CMDLINE_CASSANDRA_NODE          1<<0
#define CMDLINE_CASSANDRA_KEYSPACE      1<<1
#define CMDLINE_SECONDO_HOST            1<<2
#define CMDLINE_SECONDO_PORT            1<<3

/*
1.2 Usings

*/
using namespace std;
using namespace cassandra;

/*
1.3 Structs

*/
struct cmdline_args_t {
  string cassandraNodeIp;
  string cassandraKeyspace;
  string secondoHost;
  vector<string> secondoPorts;
};


class Queryexecutor {

public:
   
   Queryexecutor(vector<SecondoWorker*> *myWorker, 
         CassandraAdapter *myCassandra,
         cmdline_args_t *myCmdline_args, string myInstanceUuid, 
         QueryexecutorState *myQueryExecutorState) 
         : worker(myWorker), cassandra(myCassandra), 
           cmdline_args(myCmdline_args), instanceUuid(myInstanceUuid), 
           queryExecutorState(myQueryExecutorState) {
             
   }
   
   /*
   2.1 Update last executed command in cassandra system table

   */
   bool updateLastCommand(size_t lastCommandId) {
  
     // Build CQL query
     stringstream ss;
     ss << "UPDATE system_state set lastquery = ";
     ss << lastCommandId;
     ss << " WHERE ip = '";
     ss << cmdline_args->cassandraNodeIp;
     ss << "';";

     // Update last executed command
     bool result = cassandra -> executeCQLSync(
       ss.str(),
       CASS_CONSISTENCY_ONE 
     );
 
     if(! result) {
        LOG_ERROR("Unable to update last executed query "
          << "in system_state table" << endl
          << "CQL Statement: " << ss.str() << endl);
        return false;
     }

     return true;
   }
   

   /*
   2.2 Determine the CPU type of the system
   
   */
   string getCpuType() {
           string line;
           string result = "---";
           ifstream file("/proc/cpuinfo");

           while(getline(file,line)) {
                   if(line.find("model name") != string::npos) {
                           size_t pos = line.find(":");
                           pos = pos + 2; // ignore ": "
                           result = line.substr(pos, line.size());
                           break;
                   }   
           }   

           file.close();
           return result;
   }

   /*
   2.2 Determine the amount of memory of the system
   
   */
   int getMemory() {
      string token;
      ifstream file("/proc/meminfo");
      while(file >> token) {
         if(token == "MemTotal:") {
             long mem;
             if(file >> mem) {
                 return mem / 1024;
              } else {
                 return 0;
              }
         }
         file.close();
      }
      return 0;
   }

   /*
   2.2 Update UUID Entry in global state table

   */
   bool updateSystemState() {  
      
     // Build CQL query
     stringstream ss;
     ss << "UPDATE system_state set node = '";
     ss << instanceUuid;
     ss << "', threads = ";
     ss << cmdline_args->secondoPorts.size();
     ss << ", cputype = '";
     ss << getCpuType();
     ss << "', memory=";
     ss << getMemory();
     ss << " WHERE ip = '";
     ss << cmdline_args->cassandraNodeIp;
     ss << "';";
  
     bool result = cassandra -> executeCQLSync(
         ss.str(),
         CASS_CONSISTENCY_ONE
     );
  
     if(! result) {
       cout << "[Error] Unable to update heartbeat in system_state table" 
            << endl;
       cout << "CQL Statement: " << ss.str() << endl;
       return false;
     }
  
     return true;
   }

   /*
   2.2 Find the first local token range in the logical ring and 
       return its position

   */
   size_t findFirstLocalTokenrange(vector<TokenRange> &allTokenRanges, 
                                 string &ip) {
         size_t offset = 0;
         for( ; offset < allTokenRanges.size(); ++offset) {
           TokenRange tryTokenRange = allTokenRanges[offset];
           
           if(tryTokenRange.isLocalTokenRange(ip)) {
             break;
           }
         }
      
         return offset;
   }

   /*
   2.2 Print total and processed tokens and sleep some time
    
   */
   void printStatusMessage(CassandraInfo *cassandraInfo) {
        
        const vector<TokenRange> &allTokenRanges 
           = cassandraInfo -> getAllTokenRanges();
        
        const vector<TokenRange> &processedTokenRanges 
           = cassandraInfo -> getProcessedTokenRanges();
        
         cout << "[Info] RESULT: " << processedTokenRanges.size() << " of "
              << allTokenRanges.size() << " token ranges processed" << endl;
      
         if(processedTokenRanges.size() != allTokenRanges.size()) {
           cout << "[Info] Sleep 5 seconds and check the ring again" << endl;
           sleep(5);
         }
   }

   /*
   2.2 Execute a query for a tokenrange range, only if it's not 
       already processed 

   */
   bool executeQueryForTokenrangeIfNeeded(string &query, size_t queryId,
                                   CassandraInfo *cassandraInfo,
                                   TokenRange tokenrange) {
           
           cassandraInfo -> refreshDataOrExit(queryId);
                                      
           const vector<TokenRange> &processedTokenRanges 
                = cassandraInfo -> getProcessedTokenRanges();
  
           // Its query already processed for tokenrange?
           if( binary_search(processedTokenRanges.begin(), 
                             processedTokenRanges.end(), tokenrange))  {
          
             LOG_DEBUG("Skipping already processed range: " << tokenrange);
             return false;
           } else {
             LOG_DEBUG("Executing query for range: " << tokenrange);
             WorkerQueue *tokenQueue = (worker->front()) -> getTokenQueue();
             tokenQueue->push(tokenrange);
             return true;
           }
   }

   /*
   2.2 Execute the given query for all local token ranges

   */
   void executeQueryForLocalTokenranges(string &query, 
                                   size_t queryId, string &ip,
                                   CassandraInfo *cassandraInfo) {
  
       vector<TokenRange> allTokenRanges 
            = cassandraInfo -> getAllTokenRanges();
                                         
       // Generate token range queries for local tokenranges;
       for(vector<TokenRange>::iterator 
           iter = allTokenRanges.begin();
           iter != allTokenRanges.end(); ++iter) {
 
         TokenRange tokenrange = *iter;
    
         // It's a local token range
         if(tokenrange.isLocalTokenRange(ip)) {
           executeQueryForTokenrangeIfNeeded(query, queryId,
                cassandraInfo, tokenrange);
         }
       }  
   }
   
   /*
   2.3 Execute the given query for all responsible token ranges

   */
   void executeQueryForResponsibleTokenranges(string &query, 
                                   size_t queryId, string &ip,
                                   CassandraInfo *cassandraInfo) {
                                      
      cassandraInfo->refreshDataOrExit(queryId);
      vector<TokenRange> allTokenRanges = cassandraInfo->getAllTokenRanges();
         
      // Find start offset
      size_t offset = findFirstLocalTokenrange(allTokenRanges, ip);
      
      RANGE_MODE mode = LOCAL_TOKENRANGE;
      
      for(size_t position = 0; position < allTokenRanges.size(); 
                ++position) {
             
         size_t realPos = (position + offset) % allTokenRanges.size();
         TokenRange range = allTokenRanges[realPos];              
        
         if(range.isLocalTokenRange(ip)) {
            mode = LOCAL_TOKENRANGE;
            continue;
         } 
       
         if(mode == LOCAL_TOKENRANGE) {
            if(cassandraInfo->isNodeAlive(range.getIp())) {
               LOG_DEBUG("Set to foreign: " << range);
               mode = FOREIGN_TOKENRANGE;
              continue;
           } 
           
           LOG_DEBUG("Treat range as local, because node is dead: " << range);
           executeQueryForTokenrangeIfNeeded(
               query, queryId, cassandraInfo, range);
         }
      }

// Uncomment this block to use the old algorithem with 2 phases
// and without work unit reasignment      
//      while( ! cassandraInfo->isQueryExecutedCompletely() ) {
//            printStatusMessage(cassandraInfo);
//            cassandraInfo->refreshDataOrExit(queryId);
//      }
      
   }

/*
2.3 Get a vector with all unprocessed tokenranges for a queryid
   
*/   
   void getUnprocessedTokenRanges(CassandraInfo *cassandraInfo, 
        vector<TokenRange> *unprocessedTokenRange) {
           
         const vector<TokenRange> &allTokenRanges 
                = cassandraInfo -> getAllTokenRanges();
           
         const vector<TokenRange> &processedTokenRanges 
                = cassandraInfo -> getProcessedTokenRanges();
           
         for(vector<TokenRange>::const_iterator iter = allTokenRanges.begin(); 
              iter != allTokenRanges.end(); iter++) {
                 
         TokenRange tokenrange = *iter;

         // Is query already processed for tokenrange?
         if( ! binary_search(processedTokenRanges.begin(), 
                    processedTokenRanges.end(), tokenrange)) {
                       
            unprocessedTokenRange->push_back(tokenrange);
         }
      }
   }
   
   /*
   2.3 Execute the given query for all responsible token ranges

   */
   void executeQueryForOtherTokenranges(string &query, 
                                   size_t queryId, string &ip,
                                   CassandraInfo *cassandraInfo) {
      
      cassandraInfo->refreshDataOrExit(queryId);
      vector<TokenRange> processedTokenRanges = vector<TokenRange>();
      
      while( ! cassandraInfo->isQueryExecutedCompletely() ) {

            vector<TokenRange> unprocessedTokenRanges = vector<TokenRange>();
            getUnprocessedTokenRanges(cassandraInfo, &unprocessedTokenRanges);
            WorkerQueue *tokenQueue = (worker->front()) -> getTokenQueue();
            
            while(tokenQueue->isEmpty() && unprocessedTokenRanges.size() > 0) {

                // Choose one random work unit 
                int tokenPos = rand() % unprocessedTokenRanges.size();
                
                TokenRange tokenrange = unprocessedTokenRanges.at(tokenPos);
                unprocessedTokenRanges.erase(
                   unprocessedTokenRanges.begin()+tokenPos);
                
                string ip;
     
                // Is the work unit already assigned to an other QPN?
                if(cassandra -> getNodeForPendingTokenRange(ip, 
                     queryId, &tokenrange)) {
                        
                   if(cassandraInfo->isNodeAlive(ip)) {
                      continue;
                   }
                   
                   if(find(processedTokenRanges.begin(), 
                           processedTokenRanges.end(), 
                           tokenrange) != processedTokenRanges.end()) {
                      continue;
                   }
                }
                
                executeQueryForTokenrangeIfNeeded(
                    query, queryId, cassandraInfo, tokenrange);
                processedTokenRanges.push_back(tokenrange);
                cassandra->insertPendingTokenRange(queryId, ip, &tokenrange);
            }
  
            printStatusMessage(cassandraInfo);
            cassandraInfo->refreshDataOrExit(queryId);
      }
   }

   void waitForSecondoWorker() {
      // Wait for query execution
      for(vector<SecondoWorker*>::iterator it = worker->begin(); 
         it != worker->end(); ++it) {
         SecondoWorker *worker = *it;
         worker->waitForQueryCompletion();
      }
   }

   /*
   2.2 Handle a multitoken query (e.g. query ccollectrange('192.168.1.108', 
        'secondo', 'relation2', 'ONE',__TOKENRANGE__);

   */
   void handleTokenQuery(string &query, size_t queryId, string &ip) {

       // Determine cassandra ring configuration
       CassandraInfo cassandraInfo(cassandra);
       cassandraInfo.refreshDataOrExit(queryId);
       queryExecutorState -> setQuery(query);
    
       // Part 1: Execute query for all local token ranges
       executeQueryForLocalTokenranges(query, queryId, ip, &cassandraInfo);

       // Part 2: Process responsible token ranges
       executeQueryForResponsibleTokenranges(query, queryId, ip, 
           &cassandraInfo);
       
       // Part 3: Process othertoken ranges
       executeQueryForOtherTokenranges(query, queryId, ip, &cassandraInfo);
       
       // Execution is complete, empty queue and notify secondo worker
       printStatusMessage(&cassandraInfo);
       WorkerQueue *tokenQueue = (worker->front()) -> getTokenQueue();
       tokenQueue -> clear();

       // Add Termination token for worker and cancel running queries
       for(size_t i = 0; i < worker->size(); ++i) {
          tokenQueue->push(TokenRange(0, 0, ip));
          if(! (worker->at(i))->isQueryComplete()) {
             (worker->at(i))->cancelRunningQuery();
          }
       }

       waitForSecondoWorker();
   } 

   void executeSecondoCommand(string command, size_t queryId, 
       bool wait = true) {
   
      // Execute query on all worker
      for(vector<SecondoWorker*>::iterator it = worker->begin(); 
        it != worker->end(); ++it) {
        
         SecondoWorker *worker = *it;
         worker->submitQuery(command, queryId);
      }
   
      if(wait) {
         waitForSecondoWorker();
      }
   }
   
   /*
   2.3 Replace placeholder in the command and execute it

   */
   void prepareAndExecuteCommand(string &command, size_t commandId) {
      QEUtils::replaceShortcuts(command);
 
      QEUtils::replacePlaceholder(
         command, "__NODEID__", instanceUuid);
      QEUtils::replacePlaceholder(
         command, "__CASSANDRAIP__", cmdline_args -> cassandraNodeIp);
      QEUtils::replacePlaceholder(
         command, "__KEYSPACE__", cmdline_args -> cassandraKeyspace);
   
      // Simple query or token based query?
      if(QEUtils::containsPlaceholder(command, "__TOKENRANGE__")) {
        executeSecondoCommand(command, commandId, false);
        handleTokenQuery(command, commandId, 
             cmdline_args -> cassandraNodeIp);
      } else {
         executeSecondoCommand(command, commandId);
      }
   }

   /*
   2.3 Execute a GEP reset 
   
   */
   void executeGEPReset(size_t &lastCommandId, time_t &version, 
      time_t newVersion) {
         
      cout << "Detected a new GEP (our version: " << version
           << " / new: " << newVersion << ")" << endl;
      
      executeSecondoCommand(string("close database"), 
          lastCommandId + 1);
          
      lastCommandId = 0;
      
      // Wait for system tables to be recreated
      sleep(5); 
    
      updateLastCommand(lastCommandId);
      updateSystemState();
        
      cout << "[Info] Reset complete, waiting for new queries" << endl;
   }

   /*
   2.3 This is the main loop of the query executor. This method fetches
     queries from cassandra and forward them to secondo.

   */
   void mainLoop() {
 
     size_t lastCommandId = 0;
     time_t version = 0;
     
     updateLastCommand(lastCommandId);
     updateSystemState();
  
     while(true) {
           cout << "Waiting for commands...." << endl;
        
           vector<CassandraQuery> result;
           cassandra->getQueriesToExecute(result);
           
           for(vector<CassandraQuery>::iterator iter = result.begin(); 
              iter != result.end(); iter++) {
                 
             CassandraQuery &query = *iter;
   
             size_t id = query.getQueryId();
             string command = query.getQuery();
             
             // This is the first command, store QEP version
             if(id == 1 && lastCommandId == 0) {
                version = query.getVersion();
             }
             
             // A new version of the query plan was submitted
             // => cqueryreset is executed,
             // clear secondo state and reset lastCommandId
             if(id == 1 && version < query.getVersion()) {
               executeGEPReset(lastCommandId, version, query.getVersion());
               break;
             }
             
             // Skip already processed queries of the GEP
             if(id <= lastCommandId) {
                continue;
             }
          
             // Execute next query
             prepareAndExecuteCommand(command, id);
             lastCommandId = id;
             updateLastCommand(lastCommandId);
         }
         sleep(4);
      }
   }
   
private:
   vector<SecondoWorker*> *worker;
   CassandraAdapter *cassandra;
   cmdline_args_t *cmdline_args;
   string instanceUuid;
   QueryexecutorState *queryExecutorState;
};


/*
2.1 Init the cassandra adapter, the 1st parameter
 is the initial contact point to the cassandra cluter.
 The 2nd parameter is the keyspace.

*/
CassandraAdapter* getCassandraAdapter(string &cassandraHostname, 
                                      string &cassandraKeyspace) {
  
  CassandraAdapter* cassandra = 
     new CassandraAdapter(cassandraHostname, cassandraKeyspace);
  
  cassandra -> connect(true);
  
  // Connection successfully?
  if(cassandra == NULL) {
    return NULL;
  }
  
  return cassandra;
}

/*
2.4 start the heartbeat thread

*/
void* startHeartbeatThreadInternal(void *ptr) {
  HeartbeatUpdater* hu = (HeartbeatUpdater*) ptr;
  hu -> run();
  
  return NULL;
}

/*
2.5 start the heartbeat thread

*/
HeartbeatUpdater* startHeartbeatThread(string cassandraIp, 
                         string cassandraKeyspace,
                         pthread_t &targetThread) {
  
   HeartbeatUpdater* heartbeatUpdater 
     = new HeartbeatUpdater(cassandraIp, cassandraKeyspace);
     
   pthread_create(&targetThread, NULL, 
                  &startHeartbeatThreadInternal, heartbeatUpdater);
  
  return heartbeatUpdater;
}

/*
2.6 Print help and exiting

*/
void printHelpAndExit(char *progName) {
  cerr << "Usage: " << progName 
       << " -i <cassandra-ip> -k <keyspace> -s <secondo-ip> -p <secondo-port>" 
       << endl;
          
  cerr << endl;
  cerr << "-i <IP-Address> - The cassandra node to connect to" << endl;
  cerr << "-k <Keyspace>   - The keyspace to open" << endl;
  cerr << "-s <IP-Address> - The IP of the SECONDO Server" << endl;
  cerr << "-p <Port>       - The SECONDO Server port to connect to" << endl;
  exit(EXIT_FAILURE);
}

/*
2.7 parse commandline args

*/
void parseCommandline(int argc, char* argv[], 
                     cmdline_args_t &cmdline_args) {
  
  unsigned int flags = 0;
  int option = 0;
  char* pch;
  
  while ((option = getopt(argc, argv,"i:k:s:p:")) != -1) {
     switch (option) {
      case 'i':
           cmdline_args.cassandraNodeIp = string(optarg);
           flags |= CMDLINE_CASSANDRA_NODE;
           break;
      case 'k':
           cmdline_args.cassandraKeyspace = string(optarg);
           flags |= CMDLINE_CASSANDRA_KEYSPACE;
           break;
      case 's':
           cmdline_args.secondoHost = string(optarg);
           flags |= CMDLINE_SECONDO_HOST;
           break;
      case 'p':
           
           pch = strtok (optarg, ":");
           while (pch != NULL) {
              cmdline_args.secondoPorts.push_back(string(pch));
              pch = strtok (NULL, ":");
           }
        
           flags |= CMDLINE_SECONDO_PORT;
           break;
      default:
        printHelpAndExit(argv[0]);
     }
  }
  
  unsigned int requiredFalgs = CMDLINE_CASSANDRA_NODE | 
                               CMDLINE_CASSANDRA_KEYSPACE |
                               CMDLINE_SECONDO_HOST | 
                               CMDLINE_SECONDO_PORT;
                               
  if(requiredFalgs != flags) {
    printHelpAndExit(argv[0]);
  }
}

/*
2.7 Disconnect from cassandra

*/
void disconnectFromCassandra(CassandraAdapter* cassandra) {
   if(cassandra != NULL) {
     cassandra -> disconnect();
     delete cassandra;
     cassandra = NULL;
   }
}

/*
2.8 Start n SECONDO worker

*/
void startSecondoWorker(vector<SecondoWorker*> &worker, 
   QueryexecutorState &queryExecutorState, 
   cmdline_args_t &cmdline_args, WorkerQueue &tokenQueue, 
   CassandraAdapter* cassandra) {
   
   size_t workerId = 0;
      
   for(vector<string>::iterator it = cmdline_args.secondoPorts.begin(); 
        it != cmdline_args.secondoPorts.end(); it++) {
          
       SecondoWorker *secondoWorker = new SecondoWorker(
            cassandra, cmdline_args.secondoHost, *it, 
            cmdline_args.cassandraNodeIp,
            &tokenQueue, workerId, &queryExecutorState);
      
       startSecondoWorkerThread(secondoWorker);
       worker.push_back(secondoWorker);
       
       workerId++;
   }
}

/*
2.9 Stop all SECONDO worker

*/
void stopSeconcoWorker(vector<SecondoWorker*> &worker) {
   for(vector<SecondoWorker*>::iterator it = worker.begin(); 
        it != worker.end(); it++) {
     
           // Stop and delete worker
           (*it)->stop();
           delete *it;
   }
   worker.clear();
}

/*
2.8 Main method

*/
int main(int argc, char* argv[]){
    
  WorkerQueue tokenQueue(1);
  cmdline_args_t cmdline_args;
  vector<SecondoWorker*> worker;
  QueryexecutorState queryExecutorState;
  Logger::open();
  srand (time(NULL));
  
  parseCommandline(argc, argv, cmdline_args);
  
  CassandraAdapter* cassandra = 
     getCassandraAdapter(cmdline_args.cassandraNodeIp, 
                         cmdline_args.cassandraKeyspace);
  
  if(cassandra == NULL) { 
    cerr << "Could not connect to cassandra, exiting" << endl;
    exit(EXIT_FAILURE);
  }
  
  // Start SECONDO worker
  startSecondoWorker(worker, queryExecutorState, cmdline_args, 
     tokenQueue, cassandra);

  // Gernerate UUID
  string instanceUuid;
  QEUtils::createUUID(instanceUuid);
  
  // Main Programm
  pthread_t heartbeatThread;
  HeartbeatUpdater* heartbeatUpdater;
  
  heartbeatUpdater = startHeartbeatThread(cmdline_args.cassandraNodeIp, 
                       cmdline_args.cassandraKeyspace, heartbeatThread);


  Queryexecutor queryexecutor(&worker, cassandra, &cmdline_args, 
                instanceUuid, &queryExecutorState);
  queryexecutor.mainLoop();
  
  // Stop SECONDO worker
  stopSeconcoWorker(worker);
   
  // Stop heatbeat thread
  heartbeatUpdater->stop();
  pthread_join(heartbeatThread, NULL);
  delete heartbeatUpdater;
  heartbeatUpdater = NULL;
  
  disconnectFromCassandra(cassandra);
  Logger::close();
   
  return 0;
}
