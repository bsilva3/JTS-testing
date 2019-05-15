/*
----
This file is part of SECONDO.

Copyright (C) 2012, University in Hagen
Faculty of Mathematic and Computer Science,
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

#include "InvertedFile.h"
#include "NestedList.h"
#include "ListUtils.h"
#include "QueryProcessor.h"
#include "StandardTypes.h"
#include "Algebras/Relation-C++/RelationAlgebra.h"
#include "Algebras/FText/FTextAlgebra.h"
#include "Algebras/Stream/Stream.h"
#include "Progress.h"


extern NestedList* nl;
extern QueryProcessor* qp;

using namespace std;

namespace triealg{

/*

1.2 Type Constructor InvFile

*/


ListExpr InvfileProperty(){
  return nl->TwoElemList(
             nl->FiveElemList(
                 nl->StringAtom("Signature"),
                 nl->StringAtom("Example Type List"),
                 nl->StringAtom("List Rep"),
                 nl->StringAtom("Example List"),
                 nl->StringAtom("Remarks")),
             nl->FiveElemList(
                nl->TextAtom(" -> SIMPLE"),
                nl->TextAtom("invfile"),
                nl->TextAtom("invfile"),
                nl->TextAtom("( (a 1))"),
                nl->TextAtom("test type constructor"))
         );   
}


bool CheckInvfile(ListExpr type, ListExpr& ErrorInfo){
   return InvertedFile::checkType(type);
}

ListExpr OutInvfile(ListExpr typeInfo, Word value){
   return nl->TextAtom("An invfile");
}

Word InInvfile(ListExpr typeInfo, ListExpr value,
               int errorPos, ListExpr& errorInfo, bool& correct){
   Word w;
   w.addr = 0;
   correct = false;
   return w;
}

Word CreateInvfile(const ListExpr typeInfo){
   Word  res;
   res.addr = new InvertedFile();
   return res;
}

void DeleteInvfile( const ListExpr typeInfo, Word& w ){
  InvertedFile* t = (InvertedFile*) w.addr;
  t->deleteFiles();
  delete t;
  w.addr = 0;
}

void CloseInvfile( const ListExpr typeInfo, Word& w ){
  InvertedFile* t = (InvertedFile*) w.addr;
  delete t;
  w.addr = 0;
}

Word CloneInvfile(const ListExpr typeInfo, const Word& value){
  InvertedFile* src = (InvertedFile*) value.addr;
  return src->clone(); 
}

void* CastInvfile( void* addr) {
   return (InvertedFile*) addr;
}

int SizeOfInvfile(){
  return sizeof(InvertedFile);
}


TypeConstructor invfiletc( InvertedFile::BasicType(),
                        InvfileProperty,
                        OutInvfile,
                        InInvfile,
                        0,
                        0,
                        CreateInvfile,
                        DeleteInvfile,
                        OpenInvfile<uint32_t, uint32_t>,
                        SaveInvfile<uint32_t, uint32_t>,
                        CloseInvfile,
                        CloneInvfile,
                        CastInvfile,
                        SizeOfInvfile,
                        CheckInvfile );


/*
2.5 Operator createInvFile

2.5.1 Type Mapping

Signature is stream(tuple) x a1 x a2 -> invfile

a1 must be of type text
a2 must be of type tid

*/
ListExpr createInvFileTM(ListExpr args){
  string err = "stream(tuple) x a_i x a_j [ x bool x int x text"
               " [x string] ]expected";
  if(    !nl->HasLength(args,3) && !nl->HasLength(args,6) 
      && !nl->HasLength(args,7)){
    return listutils::typeError(err + " (wrong number of arguments)");
  }
  if(!Stream<Tuple>::checkType(nl->First(args))){
    return listutils::typeError(err + " (first arg is not a tuple stream)");
  }
  if(!listutils::isSymbol(nl->Second(args)) ||
     !listutils::isSymbol(nl->Third(args))){
    return listutils::typeError(err + 
                  " (one of the attribute names is not valid)");
  }
  ListExpr attrList = nl->Second(nl->Second(nl->First(args)));
  string a1 = nl->SymbolValue(nl->Second(args));
  string a2 = nl->SymbolValue(nl->Third(args));
  ListExpr t1;
  ListExpr t2;
  int i1 = listutils::findAttribute(attrList,a1,t1);
  if(i1==0){
    return listutils::typeError("Attribute " + a1 + 
                                " not known in the tuple");
  }
  int i2 = listutils::findAttribute(attrList,a2,t2);
  if(i2==0){
    return listutils::typeError("Attribute " + a2 + 
                                " not known in the tuple");
  }

  if(!FText::checkType(t1)){
    return listutils::typeError(a1 + " not of type text");
  } 

  if(!TupleIdentifier::checkType(t2)){
    return listutils::typeError(a2 + " not of type " + 
                             TupleIdentifier::BasicType());
  }

  ListExpr appendList = nl->TwoElemList( nl->IntAtom(i1-1),
                                          nl->IntAtom(i2-1));

  
  if(nl->HasLength(args,3)){
     ListExpr defaultParamList = nl->FourElemList(
                                nl->BoolAtom(false),
                                nl->IntAtom(1),
                                nl->TextAtom(""),
                                nl->TwoElemList(
                                    listutils::basicSymbol<CcString>(), 
                                    listutils::getUndefined())
                                );
      appendList = listutils::concat(defaultParamList, appendList);
  } else {
       ListExpr ignoreCase = nl->Fourth(args);
       ListExpr minLength = nl->Fifth(args);
       ListExpr stopWords = nl->Sixth(args);
       if(!CcBool::checkType(ignoreCase) ||
          !CcInt::checkType(minLength) ||
          !FText::checkType(stopWords)){
          return listutils::typeError(err);
       }
       if(nl->HasLength(args,7)){
          ListExpr separators = nl->Seventh(args);
          if(!CcString::checkType(separators)){
             return listutils::typeError(err + 
                                  " (7. arg is not of type string)");
          }
       } else {
          ListExpr defaultParamList = nl->OneElemList(
           nl->TwoElemList( listutils::basicSymbol<CcString>(), 
                            listutils::getUndefined()));
          appendList = listutils::concat(defaultParamList, appendList);
       }
  }

  return nl->ThreeElemList( nl->SymbolAtom(Symbols::APPEND()),
                            appendList,
                            nl->SymbolAtom(InvertedFile::BasicType()));

}


/*
2.5.2 Value Mapping

*/

int createInvFileVM(Word* args, Word& result, int message,
                  Word& local, Supplier s){

  switch(message){

    case OPEN:
    case CLOSE:
    case REQUEST: {      
       Stream<Tuple> stream(args[0]);
       int textIndex = ((CcInt*)args[7].addr)->GetValue();
       int tidIndex  = ((CcInt*)args[8].addr)->GetValue();
       result = qp->ResultStorage(s);
       InvertedFile* invFile = (InvertedFile*) result.addr;

       bool ignoreCase = false;
       CcBool* ic = (CcBool*) args[3].addr;
       if(ic->IsDefined()){
          ignoreCase = ic->GetValue();
       }
       int minWL = 1;
       CcInt* wl = (CcInt*) args[4].addr;
       if(wl->IsDefined() && wl->GetValue()>0){
           minWL = wl->GetValue();
       }
       string stopWords = "";
       FText* sw = (FText*) args[5].addr;
       if(sw->IsDefined()){
         stopWords = sw->GetValue();
       }
 
       CcString* separators = (CcString*) args[6].addr;
       if(separators->IsDefined()){
          invFile->setParams(ignoreCase, minWL, stopWords, 
                             separators->GetValue());
       } else {
          invFile->setParams(ignoreCase, minWL, stopWords, 
                             InvertedFile::getDefaultSeparators());
       }

       stream.open();
       Tuple* tuple;
     
       size_t maxMem = qp->GetMemorySize(s) * 1024*1024;

       size_t trieCacheSize = maxMem / 20;
       if(trieCacheSize < 4096){
          trieCacheSize = 4096;
       }
       size_t invFileCacheSize;
       if(trieCacheSize + 4096 > maxMem){
            invFileCacheSize = 4096;
       } else {
            invFileCacheSize = maxMem - trieCacheSize;
       }


       appendcache::RecordAppendCache* cache = 
                            invFile->createAppendCache(invFileCacheSize);

       TrieNodeCacheType* trieCache = 
                            invFile->createTrieCache(trieCacheSize);

       while( (tuple = stream.request())!=0){
          FText* text = (FText*) tuple->GetAttribute(textIndex);
          TupleIdentifier* tid = (TupleIdentifier*) 
                                  tuple->GetAttribute(tidIndex);

          if(text->IsDefined() && tid->IsDefined()){
             invFile->insertText(tid->GetTid() , text->GetValue(),
                                 cache, trieCache);
          }
          tuple->DeleteIfAllowed();
       }   
       stream.close();
       delete cache;
       delete trieCache;
       return 0;
     }
   case REQUESTPROGRESS: {
     ProgressInfo p1;
     ProgressInfo* pRes;

     pRes = (ProgressInfo*) result.addr;

     if ( qp->RequestProgress(args[0].addr, &p1) ) {    
        pRes->Copy(p1);
        return YIELD;
     } else {
        return CANCEL;
      }    
   }
   case CLOSEPROGRESS: {
      return 0;
   }  
  }
  return 0;
}


/*
2.5.3 Specification

*/

const string createInvFileSpec = 
   "( ( \"Signature\" \"Syntax\" \"Meaning\" "
   "\"Example\" \"Comment\" ) "
   "(<text> stream(tuple(...) x a_i x a_j "
   "[[ ignoreCase, minWordLength, stopWords], separators]-> invfile </text--->"
   "<text> _ createInvFile[_, _, _, _ , _,_] </text--->"
   "<text>creates an inverted file from a stream. "
   " a_i must be of type text, a_j must be of type tid."
   " The last three arguments are optionally."
   " If ignoreCase is set to true, upper and lower case is ignored."
   " minWordLength is of type int and describes the minimum word length"
   " for indexing (default 1)."
   "Stopwords is a text containing words which not should be indexed."
   "The separators argument specifies all characters which are to use as "
   "word separators. For the default, use the defaultInvFileSeparators "
   "operator."
   "</text--->"
   "<text>query SEC2OPERATORINFO feed addid "
   "createInvFile[Signature, TID] </text--->"
   "<text></text--->"
   ") )";


Operator createInvFile (
         "createInvFile" ,           // name
          createInvFileSpec,          // specification
          createInvFileVM,           // value mapping
          Operator::SimpleSelect, // trivial selection function
          createInvFileTM);
/*
\subsection{Operator insertInvFile}

\subsubsection{Type Mapping}

Signature is stream(tuple) x invfile x a1 x a2 -> stream(tuple)

a1 must be of type text
a2 must be of type tid

*/
ListExpr insertInvFileTM(ListExpr args){
  string err = "stream(tuple) x invfile x a_i x a_j   expected";
  if (!nl->HasLength(args, 4)) {
    return listutils::typeError(err + " (wrong number of arguments)");
  }
  if (!Stream<Tuple>::checkType(nl->First(args))) {
    return listutils::typeError(err + " (first arg is not a tuple stream)");
  }
  if (!InvertedFile::checkType(nl->Second(args))) {
    return listutils::typeError(err + " (second arg is not an inverted file)");
  }
  if (!listutils::isSymbol(nl->Third(args)) ||
      !listutils::isSymbol(nl->Fourth(args))) {
    return listutils::typeError(err +
                                " (one of the attribute names is invalid)");
  }
  ListExpr attrList = nl->Second(nl->Second(nl->First(args)));
  string a1 = nl->SymbolValue(nl->Third(args));
  string a2 = nl->SymbolValue(nl->Fourth(args));
  ListExpr t1;
  ListExpr t2;
  int i1 = listutils::findAttribute(attrList, a1, t1);
  if (i1==0) {
    return listutils::typeError("Attribute " + a1 + " not found in the tuple");
  }
  int i2 = listutils::findAttribute(attrList, a2, t2);
  if (i2==0) {
    return listutils::typeError("Attribute " + a2 + " not known in the tuple");
  }
  if(!FText::checkType(t1)){
    return listutils::typeError(a1 + " not of type text");
  } 
  if(!TupleIdentifier::checkType(t2)){
    return listutils::typeError(a2 + " not of type " + 
                                TupleIdentifier::BasicType());
  }
  return nl->ThreeElemList(nl->SymbolAtom(Symbols::APPEND()),
                           nl->TwoElemList(nl->IntAtom(i1 - 1), 
                                           nl->IntAtom(i2 - 1)),
                           nl->First(args));
}

/*
\subsubsection{Value Mapping}

*/

int insertInvFileVM(Word* args, Word& result, int message,
                    Word& local, Supplier s) {
  InvFileInsertLI *li = (InvFileInsertLI*)local.addr;
  switch (message) {
    case OPEN: {
      if (li) {
        delete li;
        local.addr = 0;
      }
      Stream<Tuple> stream = (Stream<Tuple>)args[0].addr;
      InvertedFile *inv = (InvertedFile*)args[1].addr;
      int textIndex = ((CcInt*)args[4].addr)->GetValue();
      int tidIndex  = ((CcInt*)args[5].addr)->GetValue();
      size_t maxMem = qp->GetMemorySize(s) * 1024*1024;
      li = new InvFileInsertLI(stream, inv, textIndex, tidIndex, maxMem);
      qp->SetModified(qp->GetSon(s, 1));
      local.addr = li;
      return 0;
    }
    case REQUEST: {
      result.addr = li ? li->nextTuple() : 0;
      return result.addr ? YIELD : CANCEL;
    }
    case CLOSE: {
      if (li) {
        delete li;
        local.addr = 0;
      }
    }
    case REQUESTPROGRESS: {
      ProgressInfo p1;
      ProgressInfo* pRes;
      pRes = (ProgressInfo*) result.addr;
      if (qp->RequestProgress(args[0].addr, &p1)) {
        pRes->Copy(p1);
        return YIELD;
      }
      else {
        return CANCEL;
      }
    }
    case CLOSEPROGRESS: {
      return 0;
    }
  }
  return 0;
}

/*
2.5.3 Specification

*/

const string insertInvFileSpec = 
    "( ( \"Signature\" \"Syntax\" \"Meaning\" "
    "\"Example\" \"Comment\" ) "
    "(<text> stream(tuple(...)) x invfile x a_i x a_j -> stream(tuple(...))"
    "</text--->"
    "<text> _ _ insertInvFile[ _, _ ] </text--->"
    "<text>inserts an attribute of a tuple stream into an inverted file."
    " a_i must be of type text, a_j must be of type tid."
    "</text--->"
    "<text></text--->"
    "<text></text--->"
    ") )";


Operator insertInvFile (
         "insertInvFile" ,           // name
          insertInvFileSpec,          // specification
          insertInvFileVM,           // value mapping
          Operator::SimpleSelect, // trivial selection function
          insertInvFileTM);

/*
2.6 Operator searchWord

2.6.1 Type Mapping

Signature : invfile x string -> 
            stream(tuple([Tid : tid, WordPos : int, CharPos : int]))

*/
ListExpr searchWordTM(ListExpr args){
   string err = "invfile x string expected" ;
   if(!nl->HasLength(args,2)){
     return listutils::typeError(err);
   }
   if(!InvertedFile::checkType(nl->First(args)) ||
      !CcString::checkType(nl->Second(args))){
     return listutils::typeError(err);
   }   
   ListExpr attrList = nl->ThreeElemList(
                    nl->TwoElemList( nl->SymbolAtom("Tid"), 
                    nl->SymbolAtom(TupleIdentifier::BasicType())),
                    nl->TwoElemList( nl->SymbolAtom("WordPos"),  
                                     nl->SymbolAtom(CcInt::BasicType())),
                    nl->TwoElemList( nl->SymbolAtom("CharPos"),  
                                     nl->SymbolAtom(CcInt::BasicType()))
                   );
   return nl->TwoElemList( nl->SymbolAtom(Stream<Tuple>::BasicType()),
                 nl->TwoElemList( nl->SymbolAtom(Tuple::BasicType()),
                     attrList));                                
}


/*
2.6.1 LocalInfo

*/

class searchWordLocalInfo{
   public:
      searchWordLocalInfo( InvertedFile* inv, string word, 
                           ListExpr typeList, size_t mem){
         tt = new TupleType(typeList);
         it = inv->getExactIterator(word, mem);
      } 
      ~searchWordLocalInfo(){
         tt->DeleteIfAllowed();
         delete it;
      }

      Tuple* next(){
         TupleId id;
         uint32_t wp;
         uint32_t cp;
         if(it->next(id,wp,cp)){
            Tuple* res = new Tuple(tt);
            res->PutAttribute(0, new TupleIdentifier(true,id));
            res->PutAttribute(1, new CcInt(true,wp));
            res->PutAttribute(2, new CcInt(true, cp));
            return res;
         }
         return 0;
      }


   private:
      TupleType* tt;
      InvertedFile::exactIterator* it; 
};

/*
2.6.2 Value Mapping

*/

int searchWordVM(Word* args, Word& result, int message,
                  Word& local, Supplier s){

   searchWordLocalInfo* li = (searchWordLocalInfo*) local.addr;
   switch(message){
      case OPEN : {
                   if(li){
                      delete li;
                   }
                   InvertedFile* iv = (InvertedFile*) args[0].addr;
                   CcString* cstr = (CcString*) args[1].addr;
                   ListExpr type = nl->Second(GetTupleResultType(s));
                   size_t memBuffer = 4096;
                   if(cstr->IsDefined()){
                       local.addr = new searchWordLocalInfo(iv, 
                                         cstr->GetValue(), type, memBuffer);
                   }
                   return 0;
                   }
     case REQUEST : {
                      if(!li){
                        return CANCEL;
                      }
                      result.addr=li->next();
                      return result.addr?YIELD:CANCEL;
                    }  
     case CLOSE  : {
                     if(li){
                       delete li;
                       local.addr = 0;
                     }
                   }                 

   }
   return -1;
}

/*
2.6.3 Specification

*/

const string searchWordSpec = 
    "( ( \"Signature\" \"Syntax\" \"Meaning\" "
    "\"Example\" \"Comment\" ) "
    "(<text> invfile x string -> stream(tuple([TID : tid, "
    "WordPos : int, CharPos : int)) </text--->"
    "<text> _ searchWord [_]  </text--->"
    "<text>Retrives the information stored in an inverted file "
    " for the give string"
    "</text--->"
    "<text>query SEC2OPERATORINFO feed addid createInvFile[Signature, TID] "
    " searchWord[\"string\"] count"
     "</text--->"
    "<text></text--->"
    ") )";


Operator searchWord (
         "searchWord" ,           // name
          searchWordSpec,          // specification
          searchWordVM,           // value mapping
          Operator::SimpleSelect, // trivial selection function
          searchWordTM);


/*
2.6 Operator searchPrefix

2.6.1 Type Mapping

Signature : invfile x string -> 
          stream(tuple([Word : text, Tid : tid, WordPos : int, CharPos : int]))

*/
ListExpr searchPrefixTM(ListExpr args){
   string err = "invfile x string expected" ;
   if(!nl->HasLength(args,2)){
     return listutils::typeError(err);
   }
   if(!InvertedFile::checkType(nl->First(args)) ||
      !CcString::checkType(nl->Second(args))){
     return listutils::typeError(err);
   }   
   ListExpr attrList = nl->FourElemList(
                     nl->TwoElemList( nl->SymbolAtom("Word"), 
                                 nl->SymbolAtom(FText::BasicType())),
                     nl->TwoElemList( nl->SymbolAtom("Tid"), 
                                 nl->SymbolAtom(TupleIdentifier::BasicType())),
                     nl->TwoElemList( nl->SymbolAtom("WordPos"),  
                                 nl->SymbolAtom(CcInt::BasicType())),
                     nl->TwoElemList( nl->SymbolAtom("CharPos"),  
                                 nl->SymbolAtom(CcInt::BasicType()))
                       );
   return nl->TwoElemList( nl->SymbolAtom(Stream<Tuple>::BasicType()),
                 nl->TwoElemList( nl->SymbolAtom(Tuple::BasicType()),
                     attrList));                                
}


/*
2.6.1 LocalInfo

*/

class searchPrefixLocalInfo{
   public:
      searchPrefixLocalInfo( InvertedFile* inv, string word, ListExpr typeList){
         tt = new TupleType(typeList);
         it = inv->getPrefixIterator(word);
      } 
      ~searchPrefixLocalInfo(){
         tt->DeleteIfAllowed();
         delete it;
      }

      Tuple* next(){
         string word;
         TupleId id;
         uint32_t wp;
         uint32_t cp;
         if(it->next(word,id,wp,cp)){
            Tuple* res = new Tuple(tt);
            res->PutAttribute(0, new FText(true,word));
            res->PutAttribute(1, new TupleIdentifier(true,id));
            res->PutAttribute(2, new CcInt(true,wp));
            res->PutAttribute(3, new CcInt(true, cp));
            return res;
         }
         return 0;
      }


   private:
      TupleType* tt;
      InvertedFile::prefixIterator* it;  
};

/*
2.6.2 Value Mapping

*/

int searchPrefixVM(Word* args, Word& result, int message,
                  Word& local, Supplier s){

   searchPrefixLocalInfo* li = (searchPrefixLocalInfo*) local.addr;
   switch(message){
      case OPEN : {
                   if(li){
                      delete li;
                   }
                   InvertedFile* iv = (InvertedFile*) args[0].addr;
                   CcString* cstr = (CcString*) args[1].addr;
                   ListExpr type = nl->Second(GetTupleResultType(s));
                   if(cstr->IsDefined()){
                       local.addr = new searchPrefixLocalInfo(iv, 
                                             cstr->GetValue(), type);
                   }
                   return 0;
                   }
     case REQUEST : {
                      if(!li){
                        return CANCEL;
                      }
                      result.addr=li->next();
                      return result.addr?YIELD:CANCEL;
                    }  
     case CLOSE  : {
                     if(li){
                       delete li;
                       local.addr = 0;
                     }
                   }                 

   }
   return -1;
}

/*
2.6.3 Specification

*/

const string searchPrefixSpec = 
    "( ( \"Signature\" \"Syntax\" \"Meaning\" "
    "\"Example\" \"Comment\" ) "
    "(<text> invfile x string -> stream(tuple([ Word : string, TID : tid, "
    "WordPos : int, CharPos : int)) </text--->"
    "<text> _ searchPrefix [_]  </text--->"
    "<text>Retrieves the information stored in an inverted file "
    " for the given prefix"
    "</text--->"
    "<text>query SEC2OPERATORINFO feed addid createInvFile[Signature, TID] "
    " searchPrefix[\"stri\"] count"
     "</text--->"
    "<text></text--->"
    ") )";


Operator searchPrefix (
         "searchPrefix" ,           // name
          searchPrefixSpec,          // specification
          searchPrefixVM,           // value mapping
          Operator::SimpleSelect, // trivial selection function
          searchPrefixTM);

/*
2.7 Operator getFileInfo

2.7.1 Type Mapping

The Signature is {trie, invfile} -> text 

*/
ListExpr getFileInfoTM(ListExpr args){
  string err = " invfile expected " ;
  if(!nl->HasLength(args,1)){
    return listutils::typeError(err);
  }
  ListExpr arg = nl->First(args);
  if(!InvertedFile::checkType(arg)){
    return listutils::typeError(err);
  }
  return listutils::basicSymbol<FText>();

}

/*
2.7.2 ValueMapping

*/
template<class T>
int getFileInfoVM(Word* args, Word& result, int message,
                  Word& local, Supplier s){

   T* t = (T*) args[0].addr;
   result = qp->ResultStorage(s);
   FText* res = (FText*) result.addr;
   SmiStatResultType r;
   t->getFileInfo(r);
   stringstream ss;
   for(unsigned int i=0; i< r.size() ; i++){
      ss << r[i].first << " : " << r[i].second << endl;
   }
   res->Set(true,ss.str());
   return 0;
}

/*
2.7.4 Specification

*/
OperatorSpec getFileInfoSpec(
           "{invfile} -> text",
           "getFileInfo(_)",
           "Returns information about the underlying files of"
           " an index structure",
           " query getFileInfo(iv1) " );

/*
2.7.5 Operator Instance

*/  


Operator getFileInfo
  (
  "getFileInfo",             //name
   getFileInfoSpec.getStr(),         //specification
   getFileInfoVM<InvertedFile>,        //value mapping
   Operator::SimpleSelect,   //trivial selection function
   getFileInfoTM        //type mapping
  );



/*
2.8 wordCount

This operator returns the amount of a certain word within the
whole indexed relation.

2.8.1 typeMapping

Signature : invfile x string -> int

*/

ListExpr wordCountTM(ListExpr args){
  string err ="invfile x string expected";
  if(!nl->HasLength(args,2)){
    return listutils::typeError(err);
  }
  if(!InvertedFile::checkType(nl->First(args))){
    return listutils::typeError(err);
  }
  if(!CcString::checkType(nl->Second(args))){
    return listutils::typeError(err);
  }
  return listutils::basicSymbol<CcInt>();  
}


/*
2.8.2 Value Mapping

*/

int wordCountVM(Word* args, Word& result, int message,
                  Word& local, Supplier s){

   InvertedFile* iv = (InvertedFile*) args[0].addr;
   CcString* str = (CcString*) args[1].addr;   
   result = qp->ResultStorage(s);
   CcInt* res = (CcInt*) result.addr;
   if(!str->IsDefined()){
      res->SetDefined(false);
   } else {
     res->Set(true, iv->wordCount(str->GetValue()));
  }
  return 0;
}


/*
2.8.3 Specification

*/

OperatorSpec wordCountSpec(
           "  invfile x string -> int",
           " _ wordCount[_]",
           " Returns how ofter a word is indexed.",
           " query iv wordCount[\"secondo\" " );

/*
2.8.4 Operator Instance

*/

Operator wordCount (
         "wordCount" ,           // name
          wordCountSpec.getStr(),          // specification
          wordCountVM,           // value mapping
          Operator::SimpleSelect, // trivial selection function
          wordCountTM);


/*
2.9 prefixCount

2.9.1 Type Mapping

Signature :  invfile x string -> stream(tuple([Word : text, Count : int]))

*/
ListExpr prefixCountTM(ListExpr args){
  string err ="invfile x string expected";
  if(!nl->HasLength(args,2)){
    return listutils::typeError(err);
  }
  if(!InvertedFile::checkType(nl->First(args))){
    return listutils::typeError(err);
  }
  if(!CcString::checkType(nl->Second(args))){
    return listutils::typeError(err);
  }

  ListExpr attrList = nl->TwoElemList(
                             nl->TwoElemList(
                                    nl->SymbolAtom("Word"),
                                    listutils::basicSymbol<FText>()),
                             nl->TwoElemList(
                                    nl->SymbolAtom("Count"),
                                    listutils::basicSymbol<CcInt>()));

  return  nl->TwoElemList(  
                 listutils::basicSymbol<Stream<Tuple> >(),
                 nl->TwoElemList(
                      listutils::basicSymbol<Tuple>(),
                      attrList)); 
                           
} 

/*
2.9.2 Value Mapping

*/

class prefixCountLI{
  public:
     prefixCountLI(InvertedFile* iv, CcString* str, ListExpr type): tt(0),it(0){
        if(str->IsDefined()){
           it = iv->getCountPrefixIterator(str->GetValue());
           tt = new TupleType(type);
        }
     }

    ~prefixCountLI(){
         if(it){
           delete it;
         } 
         if(tt){
           tt->DeleteIfAllowed();;
         }
     }

     Tuple* next(){
        string s;
        size_t c = 0;
        if(!it->next(s,c)){
           return 0;
        }
        Tuple* res = new Tuple(tt);
        res->PutAttribute(0, new FText(true,s));
        res->PutAttribute(1, new CcInt(true,c));
        return res; 
     }

  private:
     TupleType* tt;
     InvertedFile::countPrefixIterator* it;    

};

int prefixCountVM(Word* args, Word& result, int message,
                  Word& local, Supplier s){


   prefixCountLI* li = (prefixCountLI*) local.addr;
   switch(message){
      case OPEN : {
                      if(li){
                         delete li;
                      }
                      InvertedFile* iv = (InvertedFile*) args[0].addr;
                      CcString* str = (CcString*) args[1].addr;
                      local.addr = new prefixCountLI(iv,str, 
                                   nl->Second(GetTupleResultType(s)));
                      return 0;
                  } 
     case REQUEST : {
                      if(!li){
                        return CANCEL;
                      }
                      result.addr = li->next();
                      return result.addr?YIELD:CANCEL;
                   }

     case CLOSE : {
                      if(li){
                         delete li;
                         local.addr = 0;
                      }
                      return 0;
                  }
   }
   return -1;
}

/*
9.2.3 Specification

*/

OperatorSpec prefixCountSpec(
           "  invfile x string -> stream(tuple([Word : text, Count : int]))",
           " _ prefixCount[_]",
           " Returns how often word starting with a prefix are indexed.",
           " query iv prefixCountCount[\"secondo\" ] tconsume " );


/*
9.2.4 Operator instance

*/

Operator prefixCount (
         "prefixCount" ,           // name
          prefixCountSpec.getStr(),          // specification
          prefixCountVM,           // value mapping
          Operator::SimpleSelect, // trivial selection function
          prefixCountTM);


/*
9.3 Operator ~getInvFileSeparators~

Returns all characters used for tokenize the string within the 
InvFile data type.

*/
ListExpr getInvFileSeparatorsTM(ListExpr args){
  if(!nl->IsEmpty(args)){
    return listutils::typeError("no arguments expected");
  }
  return listutils::basicSymbol<CcString>();
}

int getInvFileSeparatorsVM(Word* args, Word& result, int message,
                  Word& local, Supplier s){
   result = qp->ResultStorage(s);
   CcString* res = (CcString*) result.addr;
   res->Set(true, InvertedFile::getDefaultSeparators());
   return 0;
}

OperatorSpec getInvFileSeparatorsSpec(
           "  -> string",
           " defaultInvFileSeparators()",
           " Returns all characters used by Inverted Files to "
          "tokenize texts as a single string by default",
           " query defaultInvFileSeparators()" );




Operator getInvFileSeparators (
         "defaultInvFileSeparators" ,           // name
          getInvFileSeparatorsSpec.getStr(),          // specification
          getInvFileSeparatorsVM,           // value mapping
          Operator::SimpleSelect, // trivial selection function
          getInvFileSeparatorsTM);


/*
9.4 getSeparators

*/
ListExpr getSeparatorsTM(ListExpr args){
  string err = "excpected " + InvertedFile::BasicType();
  if(!nl->HasLength(args,1)){
     return listutils::typeError(err);
  }
  if(!InvertedFile::checkType(nl->First(args))){
     return listutils::typeError(err);
  }
  return listutils::basicSymbol<CcString>();
}


int getSeparatorsVM(Word* args, Word& result, int message,
                  Word& local, Supplier s){
   result = qp->ResultStorage(s);
   CcString* res = (CcString*) result.addr;
   InvertedFile* arg = (InvertedFile*) args[0].addr;
   res->Set(true, arg->getSeparators());
   return 0;
}


OperatorSpec getSeparatorsSpec(
           "  invfile -> string",
           " getSeparators(_)",
           " Returns all characters used by the inverted file to "
          "tokenize texts as a single string",
           " query getSeparators(inv)" );




Operator getSeparators (
         "getSeparators" ,           // name
          getSeparatorsSpec.getStr(),          // specification
          getSeparatorsVM,           // value mapping
          Operator::SimpleSelect, // trivial selection function
          getSeparatorsTM);


/*
9.5 Operator ~containsWord~ and and ~containsPrefix~

These operators check whether a text or a string contains
a given word or a word prefix.

9.5.1 Type Mapping

These operators get two string or text values and optionally a
boolean value. It checks whether the first argument contains the
word or the word start given by the second argument. The boolean
argument specifies wether the check should be case sensitive. The
default value is false. For separating the first text into words, 
the default seperator of the inverted file are used.

*/
ListExpr containsWordOrPrefixTM(ListExpr args){
  string err = "{string,text} x {string, text} [ x bool] expected";
  if(!nl->HasLength(args,2) && !nl->HasLength(args,3)){
    return listutils::typeError(err);
  }
  if(   !CcString::checkType(nl->First(args)) 
     && !FText::checkType(nl->First(args))){
    return listutils::typeError(err);
  }
  if(   !CcString::checkType(nl->Second(args)) 
     && !FText::checkType(nl->Second(args))){
    return listutils::typeError(err);
  }
  if(nl->HasLength(args,2)){
     return nl->ThreeElemList( nl->SymbolAtom(Symbols::APPEND()),
                     nl->OneElemList(nl->BoolAtom(false)),
                     listutils::basicSymbol<CcBool>());
  }
  if(!CcBool::checkType(nl->Third(args))){
    return listutils::typeError(err);
  }
  return  listutils::basicSymbol<CcBool>();
}

/*
9.5.2 Value Mapping

*/
template<class T, class W, bool prefix>
int containsWordOrPrefixVM(Word* args, Word& result, int message,
                  Word& local, Supplier s){

   T* text = (T*) args[0].addr;
   W* word = (W*) args[1].addr;
   CcBool* cs = (CcBool*) args[2].addr;
   result = qp->ResultStorage(s);
   CcBool* res = (CcBool*) result.addr;
   if(!text->IsDefined() || !word->IsDefined() || !cs->IsDefined()){
     res->SetDefined(false);
     return 0;
   }
   string t = text->GetValue();
   string w = word->GetValue();

   bool c = cs->GetValue();
   if(!c){
     stringutils::toLower(t);
     stringutils::toLower(w);
     stringutils::trim(w);
   }
   res->Set(true,false);
   if(w.length()==0){ // stupid user found
     return 0;
   }

   

   stringutils::StringTokenizer st(t,InvertedFile::getDefaultSeparators());
   while(st.hasNextToken()){
     string nw = st.nextToken();
     if(prefix){
        if(stringutils::startsWith(nw,w)){
           res->Set(true,true);
           return 0;           
        }
     } else {
        if(nw==w){
          res->Set(true,true);
          return 0;
        }
     }
   }
   return 0;
}

/*
9.5.3 Value Mapping array and Selection

*/
ValueMapping containsWordVM[] = {
  containsWordOrPrefixVM<CcString,CcString,false>,
  containsWordOrPrefixVM<CcString,FText,false>,
  containsWordOrPrefixVM<FText,CcString,false>,
  containsWordOrPrefixVM<FText,FText,false>,
};

ValueMapping containsPrefixVM[] = {
  containsWordOrPrefixVM<CcString,CcString,true>,
  containsWordOrPrefixVM<CcString,FText,true>,
  containsWordOrPrefixVM<FText,CcString,true>,
  containsWordOrPrefixVM<FText,FText,true>,
};

int containsWordOrPrefixSelect(ListExpr args){
  int v1 = CcString::checkType(nl->Second(args))?0:1;
  int v2 = CcString::checkType(nl->First(args))?0:2;
  return v1+v2;
}

/*
9.5.4 Specififation

*/

OperatorSpec containsWordSpec(
           "  {string,text} x {string,text} [ x bool] -> bool",
           " containsWord(_,_,_)",
           " Checks whether the first argument contains a word given "
          " by the second argument. The optional third argument determines"
          " whether the checking is case sensitive.",
           " query containsWord('Secondo is great','Secondo',FALSE)" );

OperatorSpec containsPrefixSpec(
           "  {string,text} x {string,text} [ x bool] -> bool",
           " containsprefix(_,_,_)",
           " Checks whether the first argument contains a word starting with "
          " the second argument. The optional third argument determines"
          " whether the checking is case sensitive.",
           " query containsWord('Secondo is great','Secondo',FALSE)" );

/*
9.5.5 Operator instances

*/

Operator containsWordOp(
     "containsWord",                // operator's name
     containsWordSpec.getStr(),    // specification
     4,                     // number of Value Mappings
     containsWordVM,               // value mapping array
     containsWordOrPrefixSelect,           // selection function
     containsWordOrPrefixTM                // type mapping
);

Operator containsPrefixOp(
     "containsPrefix",                // operator's name
     containsPrefixSpec.getStr(),    // specification
     4,                     // number of Value Mappings
     containsPrefixVM,               // value mapping array
     containsWordOrPrefixSelect,           // selection function
     containsWordOrPrefixTM                // type mapping
);



} // end of namespace triealg




class TrieAlgebra : public Algebra {
  public:
     TrieAlgebra() : Algebra() {
     AddTypeConstructor( &triealg::invfiletc );
     triealg::insertInvFile.SetUsesMemory();
     
     AddOperator(&triealg::createInvFile);
     triealg::createInvFile.SetUsesMemory();
     
     AddOperator(&triealg::getFileInfo);
     AddOperator(&triealg::wordCount);
     AddOperator(&triealg::prefixCount);
     AddOperator(&triealg::searchWord);
     AddOperator(&triealg::searchPrefix);
     AddOperator(&triealg::getInvFileSeparators);
     AddOperator(&triealg::getSeparators);

     AddOperator(&triealg::containsWordOp);
     AddOperator(&triealg::containsPrefixOp);
     AddOperator(&triealg::insertInvFile);
     triealg::insertInvFile.SetUsesMemory();

#ifdef USE_PROGRESS
     triealg::createInvFile.EnableProgress();
     triealg::insertInvFile.EnableProgress();
#endif
   }
};


extern "C"
Algebra*
  InitializeTrieAlgebra( NestedList* nlRef, QueryProcessor* qpRef ) {
     nl = nlRef;
     qp = qpRef;
     return (new TrieAlgebra);
}



