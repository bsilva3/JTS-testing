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

//paragraph [1] Title: [{\Large \bf \begin {center}] [\end {center}}]
//[TOC] [\tableofcontents]

Started July 2014, Fabio Vald\'{e}s

*/
#include  "Tools.h"

#ifdef RECODE
#include <recode.h>
#endif

using namespace std;
using namespace datetime;

using namespace temporalalgebra;
namespace stj {
 
/*
\section{Implementation of class ~Tools~}

\subsection{Function ~recode~}

*/
#ifdef RECODE
bool Tools::recode(const string &src, const string &from, const string &to,
                   string &result) {
  string rs = trim(from)+".."+trim(to);
  // use recode lib

  RECODE_OUTER outer = recode_new_outer(true);
  RECODE_REQUEST request = recode_new_request(outer);

  bool success = recode_scan_request(request, rs.c_str());
  if (!success) {
    recode_delete_request(request);
    recode_delete_outer(outer);
    result.clear();
    return false;
  }
  char* recoded = recode_string(request, src.c_str());

  // make clean
  recode_delete_request(request);
  recode_delete_outer(outer);
  if (recoded == 0) {
    result.clear();
    return false;
  }
  result = recoded;
  free(recoded);
  return true;
}
#endif

/*
\subsection{Function ~intersect~}

*/
void Tools::intersect(const vector<set<TupleId> >& tidsets,
                      set<TupleId>& result) {
  result.clear();
  if (tidsets.empty()) {
    return;
  }
  vector<set<TupleId>::iterator> it;
  for (unsigned int i = 0; i < tidsets.size(); i++) { // initialize iterators
//     cout << "size of set " << i << " is " << tidsets[i].size() << endl;
    set<TupleId>::iterator iter = tidsets[i].begin();
    it.push_back(iter);
    if (iter == tidsets[i].end()) { // empty set
      return;
    }
  }
  while (true) {
    unsigned int min(UINT_MAX), max(0);
    for (unsigned int i = 0; i < tidsets.size(); i++) {
      if (*(it[i]) < min) {
        min = *(it[i]);
      }
      if (*(it[i]) > max) {
        max = *(it[i]);
      }
    }
    if (min == max) {
      result.insert(min);
      for (unsigned int i = 0; i < tidsets.size(); i++) {
        it[i]++;
        if (it[i] == tidsets[i].end()) {
          return;
        }
      }
    }
    else { // min < max
      for (unsigned int i = 0; i < tidsets.size(); i++) {
        while (*it[i] < max) {
          it[i]++;
          if (it[i] == tidsets[i].end()) {
            return;
          }
        }
      }
    }
  }
}

void Tools::intersectPairs(vector<set<pair<TupleId, int> > >& posVec, 
                           set<pair<TupleId, int> >*& result) {
  result->clear();
  if (posVec.empty()) {
    return;
  }
  if (posVec.size() == 1) {
    result = &(posVec[0]);
    return;
  }
  vector<set<pair<TupleId, int> >::iterator> it;
  for (unsigned int i = 0; i < posVec.size(); i++) { // initialize iterators
//     cout << "size of set " << i << " is " << posVec[i].size() << endl;
    set<pair<TupleId, int> >::iterator iter = posVec[i].begin();
    it.push_back(iter);
    if (iter == posVec[i].end()) { // empty set
      return;
    }
  }
  while (true) {
    pair<TupleId, int> min = make_pair(UINT_MAX, INT_MAX);
    pair<TupleId, int> max = make_pair(0, INT_MIN);
    for (unsigned int i = 0; i < posVec.size(); i++) {
      if (*(it[i]) < min) {
        min = *(it[i]);
      }
      if (*(it[i]) > max) {
        max = *(it[i]);
      }
    }
    if (min == max) {
      result->insert(min);
      for (unsigned int i = 0; i < posVec.size(); i++) {
        it[i]++;
        if (it[i] == posVec[i].end()) {
          return;
        }
      }
    }
    else { // min < max
      for (unsigned int i = 0; i < posVec.size(); i++) {
        while (*it[i] < max) {
          it[i]++;
          if (it[i] == posVec[i].end()) {
            return;
          }
        }
      }
    }
  }
}

void Tools::uniteLast(unsigned int size, vector<set<TupleId> >& tidsets) {
  if (tidsets.size() < size) {
    return;
  }
  for (unsigned int i = tidsets.size() - size + 1; i < tidsets.size(); i++) {
    tidsets[tidsets.size() - size].insert(tidsets[i].begin(), tidsets[i].end());
  }
  for (unsigned int i = 1; i < size; i++) {
    tidsets.pop_back();
  }
}

void Tools::uniteLastPairs(unsigned int size,
                           vector<set<pair<TupleId, int> > >& posVec) {
  if (posVec.size() < size) {
    return;
  }
  for (unsigned int i = posVec.size() - size + 1; i < posVec.size(); i++) {
    posVec[posVec.size() - size].insert(posVec[i].begin(), posVec[i].end());
  }
  for (unsigned int i = 1; i < size; i++) {
    posVec.pop_back();
  }
}

void Tools::filterPairs(set<pair<TupleId, int> >* pairs,
                   const set<TupleId>& pos, set<pair<TupleId, int> >*& result) {
  if (pos.empty() || pairs->empty()) {
    result = pairs;
    return;
  }
  set<pair<TupleId, int> >::iterator ip = pairs->begin();
  set<TupleId>::iterator it = pos.begin();
  set<pair<TupleId, int> >::iterator ir = result->begin();
  while ((ip != pairs->end()) && (it != pos.end())) {
    if (ip->first == *it) {
      ir = result->insert(ir, *ip);
      ip++;
      it++;
    }
    else if (ip->first < *it) {
      ip++;
    }
    else {
      it++;
    }
  }
  if (it == pos.end()) {
    while (ip != pairs->end()) {
      ir = result->insert(ir, *ip);
      ip++;
    }
  }
}

string Tools::int2String(int i) {
  stringstream result;
  result << i;
  return result.str();
}

int Tools::str2Int(string const &text) {
  int result;
  stringstream ss(text);
  if((ss >> result).fail())
    result = 0;
  return result;
}

void Tools::deleteSpaces(string &text) {
  size_t pos = 0;
  while ((pos = text.find(' ', pos)) != string::npos)
    text.erase(pos, 1);
}

/*
\subsection{Function ~convert~}

Converts a string into a char[*].

*/
char* Tools::convert(string arg) {
  return strdup(arg.c_str());
}

/*
\subsection{Function ~eraseQM~}

Deletes enclosing quotation marks from a string.

*/
void Tools::eraseQM(string& arg) {
  if (arg.at(0) == '"') {
    arg = arg.substr(1, arg.length() - 2);
  }
}

void Tools::addQM(string& arg) {
  if (arg.at(0) != '"') {
    arg.insert(0, "\"");
    arg.append("\"");
  }
}

void Tools::simplifyRegEx(string &regEx) {
  for (unsigned int i = 0; i < regEx.length(); i++) {
    switch (regEx[i]) {
      case '*': {
        regEx[i] = '?';
        break;
      }
      case '+': {
        regEx.erase(i, 1);
        break;
      }
      default: {
        break;
      }
    }
  }
}

/*
function ~setToString~

*/
string Tools::setToString(const set<string>& input) {
  set<string>::iterator i;
  stringstream result;
  if (input.size() == 1) {
    result << *(input.begin());
  }
  else if (input.size() > 1) {
    result << "{";
    for (i = input.begin(); i != input.end(); i++) {
      if (i != input.begin()) {
        result << ", ";
      }
      result << *i;
    }
    result << "}";
  }
  return result.str();
}

/*
function ~createSetMatrix~

Creates and returns a twodimensional array that is used to store the matching
positions.

*/

set<unsigned int>** Tools::createSetMatrix(unsigned int dim1,unsigned int dim2){
  set<unsigned int>** result = new set<unsigned int>*[dim1];
  for (unsigned int i = 0; i < dim1; i++) {
    result[i] = new set<unsigned int>[dim2];
  }
  return result;
};

/*
function ~deleteSetMatrix~

Deletes a twodimensional array.

*/

void Tools::deleteSetMatrix(set<unsigned int>** &victim, unsigned int dim1) {
  if (victim) {
    for (unsigned int i = 0; i < dim1; i++) {
      if (victim[i]) {
        delete[] victim[i];
      }
    }
    delete[] victim;
    victim = 0;
  }
}

/*
function ~prefixCount~

Returns the number of strings from which ~str~ is a prefix. This is needed in
MLabel::buildIndex.

*/
int Tools::prefixCount(string str, set<string> strings) {
  set<string>::iterator it;
  int result = 0;
  for (it = strings.begin(); it != strings.end(); it++) {
    if ((it->substr(0, str.length()) == str) && (*it != str)) {
      result++;
    }
  }
  return result;
}

void Tools::splitPattern(string& input, vector<string>& result) {
  result.clear();
  if (input.empty()) {
    return;
  }
  size_t pos = input.find('{');
  if (pos == 0) { // ({2012, 2013}, ...)
    result.push_back(input.substr(0, input.find('}') + 1));
    if (input.find('{', 1) != string::npos) { // ({2012, 2013}, {a, b, c})
      result.push_back(input.substr(input.find('{', 1)));
    }
    else { // ({2012, 2013} a)
      result.push_back(input.substr(input.find('}') + 1));
    }
  }
  else if (pos == string::npos) { // no curly brackets
    if (input.find(' ') == string::npos) { // * or +
      result.push_back(input);
    }
    else { // (2012 a)
      result.push_back(input.substr(0, input.find(' ')));
      result.push_back(input.substr(input.find(' ')));
    }
  }
  else { // (2012 {a, b, c})
    result.push_back(input.substr(0, input.find(' ')));
    result.push_back(input.substr(input.find(' ')));
  }
}

/*
function ~extractVar~

Takes an assignment string like ~time:=Z.time~ and returns the variable string.

*/
string Tools::extractVar(const string& input) {
  int posEq = input.find('=');
  int posDot = input.find('.');
  return input.substr(posEq + 1, posDot - posEq - 1);
}

int Tools::getKey(const string& type, Tuple *tuple /* = 0 */, 
                  ListExpr tupleType /* = 0 */) {
  if (type.empty()) {
    cout << "Error: empty string after variable" << endl;
    return -1;
  }
  if (type == "label")       return 0;
  if (type == "place")       return 1;
  if (type == "time")        return 2;
  if (type == "start")       return 3;
  if (type == "end")         return 4;
  if (type == "leftclosed")  return 5;
  if (type == "rightclosed") return 6;
  if (type == "card")        return 7;
  if (type == "labels")      return 8;
  if (type == "places")      return 9;
  if (tuple) {
    if (tupleType == 0) {
      cout << "Error: no tuple type found" << endl;
      return -1;
    }
    if (nl->ListLength(tupleType) != 2) {
      cout << "Error: list length must be 2" << endl;
      return -1;
    }
    if (!IsTupleDescription(nl->Second(tupleType))) {
      cout << "Error: list is not a tuple description" << endl;
      return -1;
    }
    ListExpr aType;
    int pos = FindAttribute(nl->Second(tupleType), type, aType);
    if (pos == 0) {
      cout << "Attribute " << type << " not found" << endl;
      return -1;
    }
    return pos + 99;
  }
  else {
    cout << "Error: type " << type << " is invalid without tuple" << endl;
  }
  return -1; // should not occur
}

string Tools::getDataType(const int key) {
  switch (key) {
    case -2: return MBool::BasicType();
    case -1: return CcBool::BasicType();
    case 0: return Label::BasicType();
    case 1: return Place::BasicType();
    case 2: return SecInterval::BasicType();
    case 3: 
    case 4: return Instant::BasicType();
    case 5:
    case 6: return CcBool::BasicType();
    case 7: return CcInt::BasicType();
    case 8: return Labels::BasicType();
    case 9: return Places::BasicType();
    default: return "error";
  }
}

DataType Tools::getDataType(const string& type) {
  if (type == "mlabel") return MLABEL;
  if (type == "mlabels") return MLABELS;
  if (type == "mplace") return MPLACE;
  return MPLACES;
}

DataType Tools::getDataType(TupleType *ttype, const int attrno) {
  SecondoCatalog* sc = SecondoSystem::GetCatalog();
  AttributeType attrType = ttype->GetAttributeType(attrno);
  string typeName = sc->GetTypeName(attrType.algId, attrType.typeId);
  return getDataType(typeName);
}

string Tools::getTypeName(TupleType *ttype, const int attrno) {
  SecondoCatalog* sc = SecondoSystem::GetCatalog();
  AttributeType attrType = ttype->GetAttributeType(attrno);
  return sc->GetTypeName(attrType.algId, attrType.typeId);
}

int Tools::getNoComponents(Relation *rel, const TupleId tid, const string &type,
                           const int attrno) {
  Tuple *tuple = rel->GetTuple(tid, true);
  if (type == "mreal") {
    ((MReal*)tuple->GetAttribute(attrno))->GetNoComponents();
  }
  else if (type == "mint") {
    ((MInt*)tuple->GetAttribute(attrno))->GetNoComponents();
  }
  else if (type == "mpoint") {
    ((MPoint*)tuple->GetAttribute(attrno))->GetNoComponents();
  }
  else if (type == "mregion") {
    ((MRegion*)tuple->GetAttribute(attrno))->GetNoComponents();
  }
  else if (type == "mbool") {
    ((MBool*)tuple->GetAttribute(attrno))->GetNoComponents();
  }
  tuple->DeleteIfAllowed();
  return -1;
}

bool Tools::isSymbolicType(ListExpr type) {
  return ((nl->ToString(type) == "mlabel") || (nl->ToString(type) == "mlabels")
     || (nl->ToString(type) == "mplace") || (nl->ToString(type) ==  "mplaces"));
}

/*
function ~extendDate~

Takes a datetime string and extends it to the format YYYY-MM-DD-HH:MM:SS.MMM,
the variable ~start~ decides on the values.

*/
string Tools::extendDate(string input, const bool start) {
  string result, mask;
  int month, daysInMonth, year;
  if (start) {
    mask.assign("-01-01-00:00:00");
  }
  else {
    mask.assign("-12-31-23:59:59.999");
  }
  if (input[input.size() - 1] == '-') { // handle case 2011-04-02-
    input.resize(input.size() - 1);
  }
  result.assign(input);
  size_t pos = 1;
  if ((pos = input.find('-', pos)) == string::npos) {
    result.append(mask.substr(0));
    return result;
  }
  pos++;
  if ((pos = input.find('-', pos)) == string::npos) {
    if (!start) {
      stringstream yearStream(input.substr(0, input.find('-')));
      stringstream monthStream(input.substr(input.find('-') + 1));
      stringstream dayStream;
      if ((monthStream >> month).fail()) {
        cout << "month stringstream error" << endl;
        return input + mask.substr(3);
      }
      else {
        switch (month){
          case 1:
          case 3:
          case 5:
          case 7:
          case 8:
          case 10:
          case 12:
            daysInMonth = 31;
            break;
          case 4:
          case 6:
          case 9:
          case 11:
            daysInMonth = 30;
            break;
          case 2:
            if ((yearStream >> year).fail()) {
              cout << "year stringstream error" << endl;
              return input + mask.substr(3);
            }
            else {
              if (((year % 4 == 0) && (year % 100 != 0))
                || (year % 400 == 0)) {
                daysInMonth = 29;
              }
              else {
                daysInMonth = 28;
              }
            }
            break;
          default: // should not occur
            cout << "month " << month << " does not exist" << endl;
            return input + mask.substr(3);
        }
      }
      dayStream << "-" << daysInMonth;
      result.append(dayStream.str());
      result.append(mask.substr(6));
      return result;
    }
  }
  pos = input.find('-') + 1;
  if ((pos = input.find('-', pos)) == string::npos) {
    result.append(mask.substr(3));
    return result;
  }
  pos++;
  if ((pos = input.find('-', pos)) == string::npos) {
    result.append(mask.substr(6));
    return result;
  }
  pos++;
  if ((pos = input.find(':', pos)) == string::npos) {
    result.append(mask.substr(9));
    return result;
  }
  pos++;
  if ((pos = input.find(':', pos)) == string::npos) {
    result.append(mask.substr(12));
    return result;
  }
  pos++;
  if ((pos = input.find('.', pos)) == string::npos) {
    result.append(mask.substr(15));
    return result;
  }
  return input;
}

/*
function ~checkSemanticDate~
Checks whether ~text~ is a valid semantic date string or a valid database object
of type ~Periods~ and contains the time interval defined by ~uIv~. If the
parameter ~resultNeeded~ is ~false~, the function will only check the validity
of ~text~.

*/
bool Tools::checkSemanticDate(const string &text, const SecInterval &uIv,
                              const bool eval) {
  std::string weekdays[7] = {"monday", "tuesday", "wednesday", "thursday", 
                             "friday", "saturday", "sunday"};
  std::string months[12] = {"january", "february", "march", "april", "may", 
      "june", "july", "august", "september", "october", "november", "december"};
  std::string daytimes[4] = {"morning", "afternoon", "evening", "night"};
  Instant uStart = uIv.start;
  Instant uEnd = uIv.end;
  bool isSemanticDate = false;
  for (int i = 0; i < 12; i++) {
    if (!text.compare(months[i])) {
      isSemanticDate = true;
    }
    else if (i < 7) {
      if (!text.compare(weekdays[i])) {
        isSemanticDate = true;
      }
      else if (i < 4) {
        if (!text.compare(daytimes[i])) {
          isSemanticDate = true;
        }
      }
    }
  }
  if (isSemanticDate && !eval) {
    return true;
  }
  else if (isSemanticDate && eval) {
    if ((uStart.GetYear() == uEnd.GetYear()) // year and month of start and end
         && (uStart.GetMonth() == uEnd.GetMonth())) { //must coincode for match
      for (int i = 0; i < 12; i++) { // handle months
        if (!text.compare(months[i])) {
          return (i == uStart.GetMonth() - 1);
        }
      } // for weekdays and daytimes, start and end day have to coincide
      if (uStart.GetGregDay() == uEnd.GetGregDay()) {
        for (int i = 0; i < 7; i++) { // handle weekdays
          if (!text.compare(weekdays[i])) {
            return (i == uStart.GetWeekday());
          }
        }
        for (int i = 0; i < 4; i++) { // handle daytimes
          if (!text.compare(daytimes[i])) {
            switch (i) {
              case 0:
                return (uStart.GetHour() >= 0) && (uEnd.GetHour() <= 11);
              case 1:
                return (uStart.GetHour() >= 12) && (uEnd.GetHour() <= 16);
              case 2:
                return (uStart.GetHour() >= 17) && (uEnd.GetHour() <= 20);
              case 3:
                return (uStart.GetHour() >= 21) && (uEnd.GetHour() <= 23);
              default: // cannot occur
                cout << "daytime error" << endl;
                return false;
            }
          }
        }
      }
    } // different months => match impossible
  }
  else {
    SecondoCatalog* sc = SecondoSystem::GetCatalog();
    const int errPos = 0;
    ListExpr errInfo;
    bool ok;
    if (Periods::checkType(sc->GetObjectTypeExpr(text)) ||
        SecInterval::checkType(sc->GetObjectTypeExpr(text))) {
      Word pWord = sc->InObject(sc->GetObjectTypeExpr(text),
                                sc->GetObjectValue(text), errPos, errInfo, ok);
      if (!ok) {
        cout << "Error: InObject failed." << endl;
        return false;
      }
      else {
        if (Periods::checkType(sc->GetObjectTypeExpr(text))) {
          Periods* period = static_cast<Periods*>(pWord.addr);
          return (eval ? period->Contains(uIv) : true);
        }
        else {
          SecInterval* interval = static_cast<SecInterval*>(pWord.addr);
          return (eval ? interval->Contains(uIv) : true);
        }
      }
    }
    cout << text << " is not a periods / interval object." << endl;
    return false;
  }
  return false;
}

/*
function ~checkDaytime~

Checks whether the daytime interval resulting from text (e.g., 0:00[~]8:00)
contains the one from the unit label.

*/
bool Tools::checkDaytime(const string& text, const SecInterval& uIv) {
  if ((uIv.start.GetYear() == uIv.end.GetYear())
       && (uIv.start.GetMonth() == uIv.end.GetMonth())
       && (uIv.start.GetGregDay() == uIv.end.GetGregDay())) {
    string startString, endString;
    stringstream startStream;
    startStream << uIv.start.GetYear() << "-" << uIv.start.GetMonth() << "-"
                << uIv.start.GetGregDay() << "-";
    startString.assign(startStream.str());
    endString.assign(startString);
    startString.append(text.substr(0, text.find('~')));
    endString.append(text.substr(text.find('~') + 1));
    Instant pStart(instanttype);
    Instant pEnd(instanttype);
    if (!pStart.ReadFrom(extendDate(startString, true))) {
      cout << "error: ReadFrom " << extendDate(startString, true) << endl;
      return false;
    }
    if (!pEnd.ReadFrom(extendDate(endString, false))) {
      cout << "error: ReadFrom " << extendDate(endString, false) << endl;
      return false;
    }
    SecInterval pInterval(pStart, pEnd, true, true);
    return pInterval.Contains(uIv);
  } // no match possible in case of different days
  return false;
}

/*
\subsection{Function ~isInterval~}

*/
bool Tools::isInterval(const string& str) {
  if (str.empty()) {
    return false;
  }
  if ((str[0] > 96) && (str[0] < 123)) { // 1st case: semantic date/time
    return false;
  }
  if (isDaytime(str)) {
    return false;
  }
  return true;
}

/*
\subsection{Function ~isDaytime~}

*/
bool Tools::isDaytime(const string& str) {
  if ((str.find('-') == string::npos) // 2nd case: 19:09~22:00
          && ((str.find(':') < str.find('~')) // on each side of [~],
              || (str[0] == '~')) // there has to be either xx:yy or nothing
          && ((str.find(':', str.find('~')) != string::npos)
              || str[str.size() - 1] == '~' || str.find('~') == string::npos)) {
    return true;
  }
  return false;
}

/*
\subsection{Function ~semanticToTimePer~}

*/
void Tools::semanticToTimePer(const string& spec, 
                      const NewPair<int64_t, int64_t> limits, Periods& result) {
  std::string weekdays[7] = {"monday", "tuesday", "wednesday", "thursday", 
                             "friday", "saturday", "sunday"};
  std::string months[12] = {"january", "february", "march", "april", "may", 
      "june", "july", "august", "september", "october", "november", "december"};
  std::string daytimes[4] = {"morning", "afternoon", "evening", "night"};
  Periods tempResult(true);
  Instant leftLimit(limits.first), rightLimit(limits.second);
  Instant startTemp(instanttype), endTemp(instanttype);
  Interval<Instant> limitsIv(leftLimit, rightLimit, true, true);
//   cout << "limits from multi-index are " << leftLimit << ", " << rightLimit
//        << endl;
  bool found = false;
  for (int i = 0; i < 7 && !found; i++) {
    if (spec == weekdays[i]) {
      found = true;
      int firstDay;
      if (i >= leftLimit.GetWeekday()) {
        firstDay = leftLimit.GetDay() + i - leftLimit.GetWeekday();
      }
      else {
        firstDay = leftLimit.GetDay() + 7 - (leftLimit.GetWeekday() - i);
      }
      for (int d = firstDay; d <= rightLimit.GetDay(); d = d + 7) {
        Instant startTmp(d, 0, instanttype), endTmp(d, 86399999, instanttype);
        Interval<Instant> ivTemp(startTmp, endTmp, true, true);
        tempResult.MergeAdd(ivTemp);
      }
    }
  }
  for (int i = 0; i < 12 && !found; i++) {
    if (spec == months[i]) {
      found = true;
      for (int y = leftLimit.GetYear(); y <= rightLimit.GetYear(); y++) {
        startTemp.Set(y, i + 1, 1, 0, 0, 0, 0);
        endTemp.Set(y, i + 1, 31, 23, 59, 59, 999);
        if (endTemp.GetGregDay() < 31) {
          endTemp.Set(y, i + 1, 31 - endTemp.GetGregDay(), 23, 59, 59, 999);
        }
        Interval<Instant> ivTemp(startTemp, endTemp, true, true);
        tempResult.MergeAdd(ivTemp);
      }
    }
  }
  for (int i = 0; i < 4 && !found; i++) {
    if (spec == daytimes[i]) {
      int startHours[5] = {0, 12, 17, 20, 24};
      found = true;
      for (int d = leftLimit.GetDay(); d <= rightLimit.GetDay(); d++) {
        Instant startTmp(d, 0, instanttype), endTmp(d, 0, instanttype);
        startTmp.Set(startTmp.GetYear(), startTmp.GetMonth(), 
                     startTmp.GetGregDay(), startHours[i], 0, 0, 0);
        endTmp.Set(endTmp.GetYear(), endTmp.GetMonth(), endTmp.GetGregDay(),
                   startHours[i + 1] - 1, 59, 59, 999);
        Interval<Instant> ivTemp(startTmp, endTmp, true, true);
        tempResult.MergeAdd(ivTemp);
      }
    }
  }
  if (!found) {
    result.SetDefined(false);
  }
  else {
    tempResult.Intersection(limitsIv, result);
//     cout << "sTTP result: " << result << endl;
  }
}

/*
\subsection{Function ~specToPeriods~}

*/
void Tools::specToPeriods(const string& spec, 
                      const NewPair<int64_t, int64_t> limits, Periods& result) {
//   cout << "start sTP with |" << spec << "|" << endl;
  result.Clear();
  Instant first(limits.first), last(limits.second);
  if (spec.empty()) {
    result.SetDefined(false);
  }
  else if (isInterval(spec)) {
    result.SetDefined(true);
    SecInterval iv(first, last, true, true);
    stringToInterval(spec, iv);
    result.Add(iv);
  }
  else if (isDaytime(spec)) {
    result.SetDefined(true);
    stringToDaytimePer(spec, limits, result);
  }
  else {
    semanticToTimePer(spec, limits, result);
  }
}

/*
\subsection{Function ~stringToInterval~}

*/
void Tools::stringToInterval(const string& str, SecInterval& result) {
  if (!isInterval(str)) {
    result.SetDefined(false);
    return;
  }
  Instant pStart(instanttype);
  Instant pEnd(instanttype);
  if (str[0] == '~') { // 3rd case: ~2012-05-12
    pStart.ToMinimum();
    pEnd.ReadFrom(extendDate(str.substr(1), false));
  }
  else if (str[str.size() - 1] == '~') { // 4th case: 2011-04-02-19:09~
    pStart.ReadFrom(extendDate(str.substr(0, str.size() - 1), true));
    pEnd.ToMaximum();
  }
  else if (str.find('~') == string::npos) { // 5th case: no [~] found
    pStart.ReadFrom(extendDate(str, true));
    pEnd.ReadFrom(extendDate(str, false));
  }
  else { // sixth case: 2012-05-12-20:00~2012-05-12-22:00
    pStart.ReadFrom(extendDate(str.substr(0, str.find('~')), true));
    pEnd.ReadFrom(extendDate(str.substr(str.find('~') + 1), false));
  }
  result.Set(pStart, pEnd, true, true);
}

/*
\subsection{Function ~setDaytime~}

*/
void Tools::setDaytime(const string& str, const bool isStart, Instant& result) {
//   cout << "setDaytime(" << str << ", " << isStart << ")" << endl;
  string src(str);
  size_t pos = 0;
  int hour(-1), minute(-1), second(-1), millisecond(-1);
  pos = src.find(":");
  if (pos != string::npos) {
    istringstream istr(src.substr(0, pos));
    istr >> hour;
//     cout << "found hour. " << hour << endl;
    src = src.substr(pos + 1);
    pos = src.find(':');
    if (pos != string::npos) {
      istr.clear();
      istringstream istr(src.substr(0, pos));
      istr >> minute;
//       cout << "found minute. " << minute << endl;
      src = src.substr(pos + 1);
      pos = src.find('.');
      if (pos != string::npos) { // all values given, 19:09:09.009
        istr.clear();
        istringstream istr(src.substr(0, pos));
        istr >> second;
//         cout << "found second. " << second << endl;
        istringstream iistr(src.substr(pos + 1));
        iistr >> millisecond;
//         cout << "found millisecond " << millisecond << endl;
      }
      else { // no millisecond, 19:09:09
        istr.clear();
        istringstream istr(src.substr(0, src.find('~')));
        istr >> second;
//         cout << "found second " << second << endl;
        millisecond = (isStart ? 0 : 999);
      }
    }
    else { // no second, 19:09
      istringstream istr(src.substr(0, src.find('~')));
      istr >> minute;
//       cout << "found minute " << minute << endl;
      second = (isStart ? 0 : 59);
      millisecond = (isStart ? 0 : 999);
    }
  }
  else {
    istringstream istr(src.substr(0, src.find('~')));
    istr >> hour;
//     cout << "found hour " << hour << endl;
    minute = (isStart ? 0 : 59);
    second = (isStart ? 0 : 59);
    millisecond = (isStart ? 0 : 999);
  }
  result.Set(result.GetYear(), result.GetMonth(), result.GetGregDay(), hour, 
             minute, second, millisecond);
//   cout << "result of setDaytime: " << result << endl;
}

/*
\subsection{Function ~stringToDaytmePer~}

*/
void Tools::stringToDaytimePer(const string& str, 
                      const NewPair<int64_t, int64_t> limits, Periods& result) {
  Instant leftLimit(limits.first), rightLimit(limits.second);
  Interval<Instant> limitsIv(leftLimit, rightLimit, true, true);
  Instant leftDummy(leftLimit), rightDummy(rightLimit);
  leftDummy.Set(leftLimit.GetYear(), leftLimit.GetMonth(), 
                leftLimit.GetGregDay(), 0, 0, 0, 0);
  rightDummy.Set(rightLimit.GetYear(), rightLimit.GetMonth(),
                 rightLimit.GetGregDay(), 23, 59, 59, 999);
  size_t pos = str.find('~');
  if (pos == 0) { // ~19:09; left limit remains unchanged
    setDaytime(str.substr(1), false, rightDummy);
  }
  else if (pos == string::npos) { // 19:09
    setDaytime(str, true, leftDummy);
    setDaytime(str, false, rightDummy);
  }
  else if (pos == str.length() - 1) { // 19:09~ ; right limit remains unchanged
    setDaytime(str.substr(0, pos), true, leftDummy);
  }
  else { // 19:09~20:15
    setDaytime(str.substr(0, pos), true, leftDummy);
    setDaytime(str.substr(pos + 1), false, rightDummy);
  }
  int startDay = std::floor(leftDummy.ToDouble());
  int endDay = std::floor(rightDummy.ToDouble());
  double startDaytime = leftDummy.ToDouble() - std::floor(leftDummy.ToDouble());
  double endDaytime = rightDummy.ToDouble() - std::floor(rightDummy.ToDouble());
  Periods tempResult(true);
  for (int i = startDay; i <= endDay; i++) {
    Instant startTemp(startDaytime + i);
    Instant endTemp(endDaytime + i);
    Interval<Instant> iv(startTemp, endTemp, true, true);
    tempResult.MergeAdd(iv);
  }
  tempResult.Intersection(limitsIv, result);
}

/*
\subsection{Function ~orderCheckInsert~}

*/
bool Tools::orderCheckInsert(Range<CcReal> *range, const Interval<CcReal> &iv) {
  set<Interval<CcReal>, ivCmp> ivSet;
  Interval<CcReal> ivTemp;
  for (int i = 0; i < range->GetNoComponents(); i++) {
    range->Get(i, ivTemp);
    ivSet.insert(ivTemp);
  }
  ivSet.insert(iv); // intervals are ordered in ivSet
  range->Clear();
  for (set<Interval<CcReal>, ivCmp>::iterator it = ivSet.begin(); 
       it != ivSet.end(); it++) {
    range->MergeAdd(*it);
  }
  return range->IsValid();
}

/*
\subsection{Function ~parseInterval~}

*/
bool Tools::parseInterval(const string& input, bool &isEmpty, int &pos, 
                          int &endpos, Word &value) {
  double left(0.0), right(0.0);
  bool lc(true), rc(true);
  endpos = input.find(' ', pos);
  stringstream leftss(input.substr(pos + 1, endpos));
  leftss >> left;
  if (input[pos] == '<') { // interval
    pos = input.find_first_not_of(' ', endpos);
    endpos = input.find(' ', pos);
    stringstream rightss(input.substr(pos, endpos - 1));
    rightss >> right;
    if (right < left) {
      cout << "invalid interval" << endl;
      return false;
    }
    if (input.find('>', pos) > input.find(' ', pos)) { // <x y lc rc>
      if (input[pos] != 't' && input[pos] != 'f') {
        cout << "\"t\" or \"f\" expected for interval, instead of \"" 
            << input[pos] << "\"" << endl;
        return false;
      }
      lc = (input[pos] == 't');
      pos = input.find_first_not_of(' ', pos + 1);
      rc = (input[pos] == 't');
      pos = input.find('>', pos) + 1;
    }
    endpos = input.find(' ', pos);
    pos = input.find_first_not_of(' ', endpos);
  }
  else { // single value
    right = left;
    pos = input.find_first_not_of(' ', endpos);
  }
  CcReal ccleft(left);
  CcReal ccright(right);
  Interval<CcReal> iv(ccleft, ccright, lc, rc);
  if (isEmpty) {
    value.addr = new Range<CcReal>(true);
    ((Range<CcReal>*)value.addr)->Add(iv);
    isEmpty = false;
  }
  else {
    if (!Tools::orderCheckInsert((Range<CcReal>*)value.addr, iv)) {
      cout << "error: interval " << input << " cannot be inserted" << endl;
      return false;
    }
  }
//   cout << "interval " << (lc ? "[" : "(") << left << ", " << right
//       << (rc ? "]" : ")") << " inserted" << endl;
  endpos = pos - 1;
  pos = input.find_first_not_of(' ', pos);
  return true;
}

/*
\subsection{Function ~isSetRel~}

*/
bool Tools::isSetRel(const string& input, int &pos, int &endpos,
                     SetRel &setrel) {
  if (input.substr(pos, 8) == "disjoint") {
    setrel = DISJOINT;
  }
  else if (input.substr(pos, 8) == "superset") {
    setrel = SUPERSET;
  }
  else if (input.substr(pos, 5) == "equal") {
    setrel = EQUAL;
  }
  else if (input.substr(pos, 9) == "intersect") {
    setrel = INTERSECT;
  }
  if (setrel != STANDARD) {
    pos = input.find_first_of('{', pos);
    return true;
  }
  else {
    return false;
  }
}

/*
\subsection{Function ~parseBoolorObj~}

*/
bool Tools::parseBoolorObj(const string& input, bool &isEmpty, int &pos,
                           int &endpos, Word &value, std::string& type) {
  if (!stringutils::isLetter(input[pos])) {
    return false;
  }
  endpos = input.find_first_of(" ,)}", pos) - 1;
  if (input.substr(pos, 4) == "TRUE") {
    if (isEmpty) {
      value.addr = new CcBool(true, true);
    }
    else {
      ((CcBool*)value.addr)->Set(true, true);
    }
    type = CcBool::BasicType();
  }
  else if (input.substr(pos, 5) == "FALSE") {
    if (isEmpty) {
      value.addr = new CcBool(true, false);
    } // no else required; false remains false; true remains true
    type = CcBool::BasicType();
  }
  else {
    SecondoCatalog* sc = SecondoSystem::GetCatalog();
    string name = input.substr(pos, endpos - pos + 1);
    if (!sc->IsObjectName(name)) {
      cout << name << " is not an object name" << endl;
      return false;
    }
    Word valuePart;
    bool defined;
    if (!sc->GetObject(name, valuePart, defined)) {
      cout << "object " << name << " could not be read" << endl;
      return false;
    }
    type = nl->ToString(sc->GetObjectTypeExpr(name));
    if (type == "rect") {
      type = "region";
      if (isEmpty) {
        value.addr = new Region(*((Rectangle<2>*)valuePart.addr));
        ((Rectangle<2>*)valuePart.addr)->DeleteIfAllowed();
      }
      else {
        Region rect(*((Rectangle<2>*)valuePart.addr));
        ((Rectangle<2>*)valuePart.addr)->DeleteIfAllowed();
        Region res(true);
        ((Region*)value.addr)->Union(rect, res);
        ((Region*)value.addr)->DeleteIfAllowed();
        ((Region*)value.addr)->CopyFrom(&res);
//         ((Region*)value.addr)->Print(cout); cout << endl;
      }
    }
    else if (type == "region") {
      if (isEmpty) {
        value.addr = valuePart.addr;
      }
      else {
        Region res(true);
        ((Region*)value.addr)->Union(*((Region*)valuePart.addr), res);
        ((Region*)valuePart.addr)->DeleteIfAllowed();
        ((Region*)value.addr)->CopyFrom(&res);
      }
    }
    else if (type == "line") {
      Region res(true);
      if (isEmpty) {
        Region emptyReg(true);
        emptyReg.Union(*((Line*)valuePart.addr), res);
        ((Line*)valuePart.addr)->DeleteIfAllowed();
        value.addr = new Region(res);
      }
      else {
        ((Region*)value.addr)->Union(*((Line*)valuePart.addr), res);
      }
    }
    else if (type == "label") {
      if (isEmpty) {
        value.addr = new Labels(true);
        ((Labels*)value.addr)->Append(*((Label*)valuePart.addr));
        ((Label*)valuePart.addr)->DeleteIfAllowed();
      }
      else {
        ((Labels*)value.addr)->Append(*((Label*)valuePart.addr));
        ((Label*)valuePart.addr)->DeleteIfAllowed();
      }
    }
    else if (type == "labels") {
      if (isEmpty) {
        value.addr = valuePart.addr;
      }
      else {
        set<string> labels;
        ((Labels*)valuePart.addr)->GetValues(labels);
        ((Labels*)value.addr)->Append(labels);
      }
    }
    else if (type == "place") {
      // TODO.
    }
    else if (type == "places") {
      // TODO.
    }
    else if (type == "interval") {
      if (isEmpty) {
        value.addr = new Range<CcReal>(true);
        ((Range<CcReal>*)value.addr)->Add((*(Interval<CcReal>*)valuePart.addr));
        delete (Interval<CcReal>*)valuePart.addr;
      }
      else {
        orderCheckInsert((Range<CcReal>*)value.addr, 
                         *((Interval<CcReal>*)valuePart.addr));
        delete (Interval<CcReal>*)valuePart.addr;
      }
    }
    else if (type == "bool") {
      if (isEmpty) {
        value.addr = valuePart.addr;
      }
      else {
        ((CcBool*)value.addr)->Set(true, ((CcBool*)value.addr)->GetValue() ||
                                        ((CcBool*)valuePart.addr)->GetValue());
        ((CcBool*)valuePart.addr)->DeleteIfAllowed();
      }
    }
    else {
      cout << "type " << type << " is invalid" << endl;
      return false;
    }
  }
  pos = input.find_first_not_of(' ', endpos + 1);
  isEmpty = false;
  return true;
}

/*
\subsection{Function ~checkAttrType~}

*/
bool Tools::checkAttrType(const string& typeName, const Word &value) {
  if (value.addr == 0) {
    return true;
  }
  else {
    if (typeName == "mlabel" || typeName == "mlabels") {
      return ((Labels*)value.addr)->IsDefined();
    }
    else if (typeName == "mplace" || typeName == "mplaces") {
      return ((Places*)value.addr)->IsDefined();
    }
    else if (typeName == "mpoint" || typeName == "mregion") {
      return ((Region*)value.addr)->IsDefined();
    }
    else if (typeName == "mbool") {
      return ((CcBool*)value.addr)->IsDefined();
    }
    else if (typeName == "mint" || typeName == "mreal") {
      return ((Range<CcReal>*)value.addr)->IsDefined();
    }
  }
  cout << "invalid type " << typeName << endl;
  return false;
}

/*
\subsection{Function ~isRelevantAttr~}

*/
bool Tools::isRelevantAttr(const string& name) {
  set<string> relevantAttrTypes;
  relevantAttrTypes.insert("mbool");
  relevantAttrTypes.insert(relevantAttrTypes.end(), "mint");
  relevantAttrTypes.insert(relevantAttrTypes.end(), "mlabel");
  relevantAttrTypes.insert(relevantAttrTypes.end(), "mlabels");
  relevantAttrTypes.insert(relevantAttrTypes.end(), "mplace");
  relevantAttrTypes.insert(relevantAttrTypes.end(), "mplace");
  relevantAttrTypes.insert(relevantAttrTypes.end(), "mpoint");
  relevantAttrTypes.insert(relevantAttrTypes.end(), "mreal");
  relevantAttrTypes.insert(relevantAttrTypes.end(), "mregion");
  return relevantAttrTypes.find(name) != relevantAttrTypes.end();
}

/*
\subsection{Function ~isMovingAttr~}

*/
bool Tools::isMovingAttr(const ListExpr ttype, const int attrno) {
  if (!nl->HasLength(ttype, 2)) {
    return false;
  }
  if (attrno < 1 || attrno > nl->ListLength(nl->Second(ttype))) {
    return false;
  }
  if (!nl->HasLength(nl->Nth(attrno, nl->Second(ttype)), 2)) {
    return false;
  }
  return isRelevantAttr(nl->ToString(nl->Second(nl->Nth(attrno, 
                                                        nl->Second(ttype)))));
}

/*
\subsection{Function ~getRelevantAttrs~}

*/
vector<pair<int, string> > Tools::getRelevantAttrs(TupleType *ttype,
                                     const int majorAttrNo, int& majorValueNo) {
  vector<pair<int, string> > result;
  SecondoCatalog* sc = SecondoSystem::GetCatalog();
  for (int i = 0; i < ttype->GetNoAttributes(); i++) {
    AttributeType attrType = ttype->GetAttributeType(i);
    string typeName = sc->GetTypeName(attrType.algId, attrType.typeId);
    if (i == majorAttrNo) {
      majorValueNo = result.size();
    }
    if (isRelevantAttr(typeName)) {
      result.push_back(make_pair(i, typeName));
    }
  }
  return result;
}

/*
\subsection{Function ~deleteValue~}

*/
void Tools::deleteValue(Word &value, const string &type) {
  if (value.addr == 0) {
    return;
  }
  if (type == "mlabel" || type == "mlabels") {
    ((Labels*)value.addr)->DeleteIfAllowed();
  }
  else if (type == "mplace" || type == "mplaces") {
    ((Places*)value.addr)->DeleteIfAllowed();
  }
  else if (type == "mpoint" || type == "mregion") {
    ((Region*)value.addr)->DeleteIfAllowed();
  }
  else if (type == "mbool") {
    ((CcBool*)value.addr)->DeleteIfAllowed();
  }
  else if (type == "mint" || type == "mreal") {
    ((Range<CcReal>*)value.addr)->DeleteIfAllowed();
  }
  else { // cannot occur
    cout << "cannot delete invalid type " << type << endl;
  }
}

/*
\subsection{Function ~timesMatch~}

Checks whether the time interval ~uIv~ is completely enclosed by each of the
intervals specified in ~ivs~. If ~ivs~ is empty, the result is ~true~.

*/
bool Tools::timesMatch(const Interval<Instant>& iv, const set<string>& ivs) {
  if (ivs.empty()) {
    return true;
  }
  bool elementOk(false);
  SecInterval pIv(true);
  for (set<string>::iterator j = ivs.begin(); j != ivs.end(); j++) {
    if (((*j)[0] > 96) && ((*j)[0] < 123)) { // 1st case: semantic date/time
      elementOk = checkSemanticDate(*j, iv, true);
    }
    else if (((*j).find('-') == string::npos) // 2nd case: 19:09~22:00
          && (((*j).find(':') < (*j).find('~')) // on each side of [~],
              || ((*j)[0] == '~')) // there has to be either xx:yy or nothing
          && (((*j).find(':', (*j).find('~')) != string::npos)
              || (*j)[(*j).size() - 1] == '~')) {
      elementOk = checkDaytime(*j, iv);
    }
    else {
      stringToInterval(*j, pIv);
      elementOk = pIv.Contains(iv);
    }
    if (!elementOk) { // all intervals have to match
      return false;
    }
  }
  return true;
}

/*
\subsection{Function ~processQueryStr~}

Invoked by ~initOpTrees~ and others.

*/
pair<QueryProcessor*, OpTree> Tools::processQueryStr(string query, int type) {
  pair<QueryProcessor*, OpTree> result;
  result.first = 0;
  result.second = 0;
  SecParser parser;
  string qParsed;
  ListExpr qList, rType;
  bool correct(false), evaluable(false), defined(false), isFunction(false);
  if (parser.Text2List(query, qParsed)) {
    cout << "Text2List(" << query << ") failed" << endl;
    return result;
  }
  if (!nl->ReadFromString(qParsed, qList)) {
    cout << "ReadFromString(" << qParsed << ") failed" << endl;
    return result;
  }
  result.first = new QueryProcessor(nl, am);
  try {
    result.first->Construct(nl->Second(qList), correct, evaluable, defined,
                            isFunction, result.second, rType);
  }
  catch (...) {
    delete result.first;
    result.first = 0;
    result.second = 0;
  }
  if (!correct || !evaluable || !defined) {
    cout << "correct:   " << (correct ? "TRUE" : "FALSE") << endl
         << "evaluable: " << (evaluable ? "TRUE" : "FALSE") << endl
         << "defined:   " << (correct ? "TRUE" : "FALSE") << endl;
    delete result.first;
    result.first = 0;
    result.second = 0;
    return result;
  }
  if (nl->ToString(rType) != getDataType(type)) {
    if (nl->ToString(rType) != getDataType(-2)) {
      cout << "incorrect result type: " << nl->ToString(rType) << "; should be "
           << getDataType(type) << " or " << getDataType(-2) << endl;
      delete result.first;
      result.first = 0;
      result.second = 0;
    }
  }
  return result;
}

/*
\subsection{Function ~evaluate~}

The string ~input~ is evaluated by Secondo. The result is returned as a Word.

*/
// Word evaluate(string input) {
//   SecParser qParser;
//   string query, queryStr;
//   ListExpr queryList;
//   Word queryResult;
//   input.insert(0, "query ");
//   if (!qParser.Text2List(input, queryStr)) {
//     if (nl->ReadFromString(queryStr, queryList)) {
//       if (!nl->IsEmpty(nl->Rest(queryList))) {
//         query = nl->ToString(nl->First(nl->Rest(queryList)));
//         if (qp->ExecuteQuery(query, queryResult)) {
//           return queryResult;
//         }
//       }
//     }
//   }
//   return queryResult;
// }



bool Tools::createTransitions(const bool dortmund,
                              map<string, set<string> >& transitions) {
  if (dortmund) {
    map<string, set<string> >::iterator im;
    set<string>::iterator it;
    transitions["Aplerbeck"].insert("Hörde");
    transitions["Aplerbeck"].insert("Innenstadt-Ost");
    transitions["Aplerbeck"].insert("Brackel");
    transitions["Brackel"].insert("Innenstadt-Nord");
    transitions["Brackel"].insert("Innenstadt-Ost");
    transitions["Brackel"].insert("Scharnhorst");
    transitions["Eving"].insert("Huckarde");
    transitions["Eving"].insert("Innenstadt-Nord");
    transitions["Eving"].insert("Mengede");
    transitions["Eving"].insert("Scharnhorst");
    transitions["Hörde"].insert("Hombruch");
    transitions["Hörde"].insert("Innenstadt-Ost");
    transitions["Hombruch"].insert("Innenstadt-Ost");
    transitions["Hombruch"].insert("Innenstadt-West");
    transitions["Hombruch"].insert("Lütgendortmund");
    transitions["Huckarde"].insert("Innenstadt-Nord");
    transitions["Huckarde"].insert("Innenstadt-West");
    transitions["Huckarde"].insert("Lütgendortmund");
    transitions["Huckarde"].insert("Mengede");
    transitions["Innenstadt-Nord"].insert("Innenstadt-Ost");
    transitions["Innenstadt-Nord"].insert("Innenstadt-West");
    transitions["Innenstadt-Nord"].insert("Scharnhorst");
    transitions["Innenstadt-Ost"].insert("Innenstadt-West");
    transitions["Innenstadt-West"].insert("Lütgendortmund");
    for (im = transitions.begin(); im != transitions.end(); im++) {
      for (it = im->second.begin(); it != im->second.end(); it++) {
        transitions[*it].insert(im->first); // add symmetric transitions
      }
      transitions[im->first].insert(im->first); // remaining in the same area
    }
  }
  else {
    Word kreis, kreisrtree;
    bool defined;
    SecondoCatalog* sc = SecondoSystem::GetCatalog();
    if (!sc->GetObject("Kreis", kreis, defined)) {
      cout << "Error: GetObject Kreis failed" << endl;
      return false;
    }
    if (!defined) {
      cout << "Error: object Kreis undefined" << endl;
      return false;
    }
    if (!sc->GetObject("Kreisrtree", kreisrtree, defined)) {
      cout << "Error: GetObject Kreisrtree failed" << endl;
      return false;
    }
    if (!defined) {
      cout << "Error: object Kreisrtree undefined" << endl;
      return false;
    }
    Relation *rel = (Relation*)(kreis.addr);
    R_Tree<2, TupleId> *rtree = (R_Tree<2, TupleId>*)(kreisrtree.addr);
    RelationIterator *it1 = new RelationIterator(*rel);
    Tuple *tuple1 = it1->GetNextTuple();
    R_TreeLeafEntry<2, TupleId> leaf;
    Tuple *tuple2 = 0;
    while (tuple1) {
      string name1 = ((CcString*)(tuple1->GetAttribute(0)))->GetValue();
      Region *r1 = (Region*)(tuple1->GetAttribute(4));
      Rectangle<2> bbox = r1->BoundingBox();
      if (rtree->First(bbox, leaf)) {
        tuple2 = rel->GetTuple(leaf.info, true);
        string name2 = ((CcString*)(tuple2->GetAttribute(0)))->GetValue();
        transitions[name1.substr(3)].insert(name2.substr(3));
        tuple2->DeleteIfAllowed();
        while (rtree->Next(leaf)) {
          tuple2 = rel->GetTuple(leaf.info, true);
          string name2 = ((CcString*)(tuple2->GetAttribute(0)))->GetValue();
          transitions[name1.substr(3)].insert(name2.substr(3));
          tuple2->DeleteIfAllowed();
        }
      }
      tuple1->DeleteIfAllowed();
      tuple1 = it1->GetNextTuple();
    }
    delete it1;
    delete rtree;
    delete rel;
  }
  return true;
}

/*
\subsection{Function ~createLabelSequence~}

Creates a vector of string containing either districts of Dortmund or German
counties in a random but sensible order.

*/
bool Tools::createLabelSequence(const int size, const int number,
                    const bool dortmund, map<string, set<string> >& transitions,
                    vector<string>& result) {
  time_t t;
  time(&t);
  srand((unsigned int)t);
  map<string, set<string> >::iterator im;
  set<string>::iterator it;
  for (int i = 0; i < number; i++) {
    im = transitions.begin();
    int choice = rand() % transitions.size();
    advance(im, choice);
    string name = im->first;
    result.push_back(name);
    for (int j = 1; j < size; j++) {
      it = transitions[name].begin();
      choice = rand() % transitions[name].size();
      advance(it, choice);
      name = *it;
      result.push_back(name);
    }
  }
  return result.size() == (unsigned int)(size * number);
}

void Tools::printNfa(vector<map<int, int> > &nfa, set<int> &finalStates) {
  map<int, int>::iterator it;
  for (unsigned int i = 0; i < nfa.size(); i++) {
    cout << (finalStates.count(i) ? " * " : "   ") << "state " << i << ":  ";
    for (it = nfa[i].begin(); it != nfa[i].end(); it++) {
      cout << "---" << it->first << "---> " << it->second << "    ";
    }
    cout << endl << endl;
  }
}

void Tools::makeNFApersistent(vector<map<int, int> > &nfa,set<int> &finalStates,
   DbArray<NFAtransition> &trans, DbArray<int> &s2p, map<int, int> &state2Pat) {
  NFAtransition tr;
  map<int, int>::iterator im;
  for (unsigned int i = 0; i < nfa.size(); i++) {
    tr.oldState = i;
    for (im = nfa[i].begin(); im != nfa[i].end(); im++) {
      tr.trigger = im->first;
      tr.newState = im->second;
      trans.Append(tr);
    }
    s2p.Append(state2Pat[i]);
  }
}

void Tools::createNFAfromPersistent(DbArray<NFAtransition> &trans, 
        DbArray<int> &s2p, vector<map<int, int> > &nfa, set<int> &finalStates) {
  nfa.clear();
  finalStates.clear();
  map<int, int> emptymap;
  NFAtransition tr;
  for (int i = 0; i < trans.Size(); i++) {
    trans.Get(i, tr);
    while (tr.oldState >= (int)nfa.size()) {
      nfa.push_back(emptymap);
    }
    nfa[tr.oldState][tr.trigger] = tr.newState;
  }
  int pat = INT_MAX;
  for (int i = 1; i < s2p.Size(); i++) {
    s2p.Get(i, pat);
    if ((pat != INT_MAX) && (pat >= 0)) {
      finalStates.insert(i);
    }
  }
}

double Tools::distance(const string& str1, const string& str2, 
                       const LabelFunction lf /* = TRIVIAL */) {
  if (lf == TRIVIAL) {
    return (str1 == str2 ? 0.0 : 1.0);
  }
  if (str1.empty() && str2.empty()) {
    return 0.0;
  }
  if (str1.empty() || str2.empty()) {
    return 1.0;
  }
  double ld = 1.0;
  if (lf == EDIT) {
    ld = stringutils::ld(str1, str2);
  }
  return ld / max(str1.length(), str2.length());
}

double Tools::distance(const pair<string, unsigned int>& val1, 
                       const pair<string, unsigned int>& val2, 
                       const LabelFunction lf /* = TRIVIAL */) {
  double ld = Tools::distance(val1.first, val2.first, lf);
  return ld / 2 + (val1.second == val2.second ? 0 : 0.5);
}

double Tools::distance(const set<string>& values1, const set<string>& values2,
                       const LabelFunction lf) {
  if (values1.empty() && values2.empty()) {
    return 0;
  }
  if (values1.empty() || values2.empty()) {
    return 1;
  }
  set<string>::iterator i1(values1.begin()), i2(values2.begin());
  int m(values1.size()), n(values2.size());
  double distsum = 0.0;
  double dist;
  int i1count(0), i2count(0);
  while (i1 != values1.end() && i2 != values2.end()) {
    dist = Tools::distance(*i1, *i2, lf);
    if (dist < 1) {
//       cout << "  " << *i1 << " = " << *i2 << endl;
      i1++;
      i1count++;
      i2++;
      i2count++;
      distsum += dist;
    }
    else {
      if (*i1 < *i2) {
//         cout << "  " << *i1 << " < " << *i2 << endl;
        i1++;
        i1count++;
      }
      else {
//         cout << "  " << *i1 << " > " << *i2 << endl;
        i2++;
        i2count++;
      }
      distsum += 1.0;
    }
  }
  distsum += std::max(m - i1count, n - i2count);
  return distsum / (m + n);
}

double Tools::distance(set<pair<string, unsigned int> >& values1, 
                       set<pair<string, unsigned int> >& values2, 
                       const LabelFunction lf /* = TRIVIAL */) {
  if (values1.empty() && values2.empty()) {
    return 0;
  }
  if (values1.empty() || values2.empty()) {
    return 1;
  }
  set<pair<string, unsigned int> >::iterator i1, i2;
  double distsum = 0;
  for (i1 = values1.begin(); i1 != values1.end(); i1++) {
    for (i2 = values2.begin(); i2 != values2.end(); i2++) {
      double dist = Tools::distance(i1->first, i2->first, lf);
      distsum += dist / 2 + (i1->second == i2->second ? 0 : 0.5);
    }
  }
  return distsum / (values1.size() * values2.size());
}

DistanceFunSym Tools::getDistanceFunSym(std::string funName) {
  std::transform(funName.begin(), funName.end(), funName.begin(),
            (int (*)(int))::tolower);
  if (funName == "equallabels") {
    return EQUALLABELS;
  }
  else if (funName == "prefix") {
    return PREFIX;
  }
  else if (funName == "suffix") {
    return SUFFIX;
  }
  else if (funName == "prefixsuffix") {
    return PREFIXSUFFIX;
  }
  else {
    return ERROR;
  }
}

bool Tools::getGeoFromORel(const std::string& relName, const unsigned int ref,
                           const bool bbox, Word& geo, std::string& type) {
  if (ref == 0) {
    geo.addr = new Rectangle<2>(true);
    ((Rectangle<2>*)(geo.addr))->SetDefined(false);
    return true;
  }
  SecondoCatalog* sc = SecondoSystem::GetCatalog();
  Word orelPtr;
  bool defined;
  if (!sc->GetObject(relName, orelPtr, defined)) {
    cout << "Error: cannot find relation 'Places'" << endl;
    return false;
  }
  if (!defined) {
    cout << "Error: relation 'Places' is undefined" << endl;
    return false;
  }
  OrderedRelation *orel = static_cast<OrderedRelation*>(orelPtr.addr);
  vector<void*> attributes(1);
  vector<SmiKey::KeyDataType> attrTypes(1);
  attrTypes[0] = SmiKey::Integer;
  attributes[0] = new CcInt(true, ref);
  CompositeKey fromKey(attributes, attrTypes, false);
  CompositeKey toKey(attributes, attrTypes, true);
  OrderedRelationIterator *rit = 
                  (OrderedRelationIterator*)orel->MakeRangeScan(fromKey, toKey);
  Tuple *pt = rit->GetNextTuple();
  if (bbox) {
    geo.addr = pt->GetAttribute(5);
    type = Rectangle<2>::BasicType();
  }
  else {
    if (pt->GetAttribute(1)->IsDefined()) {
      geo.addr = pt->GetAttribute(1)->Copy(); // point
      type = Point::BasicType();
    }
    else if (pt->GetAttribute(2)->IsDefined()) {
      geo.addr = pt->GetAttribute(2)->Copy(); // line
      type = Line::BasicType();
    }
    else if (pt->GetAttribute(3)->IsDefined()) {
      geo.addr = pt->GetAttribute(3)->Copy(); // region
      type = Region::BasicType();
    }
    else {
      geo.addr = 0;
      cout << "Error: no defined geometry for reference " << ref << endl;
    }
  }
  ((CcInt*)attributes[0])->DeleteIfAllowed();
//   pt->DeleteIfAllowed();
  return (geo.addr != 0);
}

bool Tools::getRectFromOrel(const std::string& relName, const unsigned int ref,
                            Rectangle<2>& box) {
  Word geo;
  std::string type;
  if (!getGeoFromORel(relName, ref, true, geo, type)) {
    return false;
  }
  box.CopyFrom((Rectangle<2>*)(geo.addr));
  return true;
}

}
