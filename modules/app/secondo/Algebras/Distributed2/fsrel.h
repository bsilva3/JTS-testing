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

#ifndef FSREL_H
#define FSREL_H

#include <string>
#include <vector>
#include "NestedList.h"
#include "SecondoSMI.h"

union Word;

namespace distributed2{

class fsrel{

public:
  fsrel();
  fsrel(const fsrel& src);
  explicit fsrel(const std::vector<std::string>& names);

  void set(const std::vector<std::string>& values);

  inline size_t size() const{
    return values.size();
  }

  inline const std::string& operator[](const size_t i) {
    return values[i];
  }

  inline void append(const std::string& s) {
     assert(defined);
     values.push_back(s);
  }

  inline  void clear(){
     values.clear();
     defined = true; 
  }


 
  // secondo support 
  static inline std::string BasicType(){return "fsrel";}
  static bool checkType(const ListExpr list);
  static ListExpr Property();
  static Word In(const ListExpr typeInfo, const ListExpr instance,
                 const int errorPos, ListExpr& errorInfo, bool& correct);
  static ListExpr Out(ListExpr typeInfo, Word value);
  static Word Create(const ListExpr typeInfo);
  static void Delete(const ListExpr typeInfo, Word& w);
  static bool Open(SmiRecord& valueRecord,
                   size_t& offset, const ListExpr typeInfo,
                   Word& value);
  static bool Save(SmiRecord& valueRecord, size_t& offset,
                   const ListExpr typeInfo, Word& value);
  static void Close(const ListExpr typeInfo, Word& w);
  static Word Clone(const ListExpr typeInfo, const Word& v);
  static void* Cast(void* addr);
  static bool TypeCheck(ListExpr type, ListExpr& errorInfo);
  static int SizeOf();
  inline bool IsDefined()const{ return defined;}
  inline std::vector<std::string> GetValue()const{ return values;}
  inline void SetDefined(const bool _def){ defined = _def;}
  

private:
  explicit fsrel(const int __attribute__((unused)) dummy) {}
  std::vector<std::string> values;
  bool defined;

};

} // end of namespace distributed2

#endif
