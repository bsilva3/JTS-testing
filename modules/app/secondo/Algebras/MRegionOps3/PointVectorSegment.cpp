/*
----
This file is part of SECONDO.

Copyright (C) 2008, University in Hagen, Department of Computer Science,
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
//[ue] [\"u]
//[ae] [\"a]
//[oe] [\"o]
//[x] [$\times $]
//[->] [$\rightarrow $]

[1] Implementation of the MRegionOps3Algebra

April - November 2008, M. H[oe]ger for bachelor thesis.
Mai - November 2017, U. Wiesecke for master thesis.

[TOC]

1 Introduction

2 Defines and Includes

*/

#include "PointVectorSegment.h"

using namespace std;

namespace temporalalgebra{
  namespace mregionops3 {   
    
    std::string toString(Predicate predicate){
      switch(predicate){
        case UNDEFINED: return "UNDEFINED";
        case LEFT_IS_INNER:   return "LEFT_IS_INNER";
        case RIGHT_IS_INNER:  return "RIGHT_IS_INNER";
        case INNER: return "INNER";
        case OUTER: return "OUTER";
        case INTERSECT: return "INTERSECT";
        case NO_INTERSECT: return "NO_INTERSECT";
        default: return "";
      }// switch
    }// toString
/*
3 Class Point3D

*/    
    Point3D::Point3D():x(0),y(0),z(0){
    }// Konstruktor
    
    Point3D::Point3D(const Point3D& point){
      set(point);
    }// Konstruktor
    
    Point3D::Point3D(const RationalPoint3D& point){
      set(point);
    }// Konstruktor

    Point3D::Point3D(double x, double y, double z){
      set(x,y,z);
    }// Konstruktor  
      
    void Point3D::set(const Point3D& point){
      this->x = point.x;
      this->y = point.y;
      this->z = point.z;      
    }// set
    
    void Point3D::set(const RationalPoint3D& point){
      this->x = point.getX().get_d();
      this->y = point.getY().get_d();
      this->z = point.getZ().get_d();      
    }// set
    
    void Point3D::set(double x, double y, double z){
      this->x = x;
      this->y = y;
      this->z = z;
    }// set
    
    double Point3D::getX() const{
      return x;
    }// getX
    
    double Point3D::getY() const{
      return y;
    }// getY
    
    double Point3D::getZ() const{
      return z;    
    }// getZ
    
    RationalPoint3D Point3D::getR() const{
      return RationalPoint3D(x,y,z);  
    }// get
    
    Rectangle<3> Point3D::getBoundingBox()const{
      double array[3] = {x,y,z};
      return Rectangle<3>(true,array,array);
    }// getBoundingBox 
    
    std::ostream& operator <<(std::ostream& os, const Point3D& point){
      os << "Point3D(" << point.x;
      os << ", " << point.y;
      os << ", " << point.z << ")";
      return os; 
    }// operator <<
    
    bool Point3D::operator !=(const Point3D& point) const{
      return !(*this == point);
    }// Operator !=
    
    bool Point3D::operator ==(const Point3D& point) const{
      return NumericUtil::nearlyEqual(this->x, point.x) && 
             NumericUtil::nearlyEqual(this->y, point.y) && 
             NumericUtil::nearlyEqual(this->z, point.z);
    }// Operator ==
    
    bool Point3D::nearlyEqual(const Point3D& other, double e)const{
      return NumericUtil::nearlyEqual(this->x, other.x, e) && 
             NumericUtil::nearlyEqual(this->y, other.y, e) && 
             NumericUtil::nearlyEqual(this->z, other.z, e);
    }// nearlyEqual
    
    bool Point3D::operator <(const Point3D& point) const {
      if (NumericUtil::lower(x, point.x))
        return true;
      if (NumericUtil::greater(x, point.x))
        return false;   
      if (NumericUtil::lower(y, point.y))
        return true;
      if (NumericUtil::greater(y, point.y))
        return false; 
      return NumericUtil::lower(z, point.z);
    }// Operatot <
    
    Point3D& Point3D::operator =(const Point3D& point){
      set(point);
      return *this;
    }// Operator =
/*
4 Class RationalPoint3D

*/      
    RationalPoint3D::RationalPoint3D():x(0),y(0),z(0){
    }// Konstruktor
    
    RationalPoint3D::RationalPoint3D(const Point3D& point){
      set(point);
    }// Konstruktor
    
    RationalPoint3D::RationalPoint3D(const RationalPoint3D& point){
      set(point);
    }// Konstruktor

    RationalPoint3D::RationalPoint3D(mpq_class x, mpq_class y, mpq_class z){
      set(x,y,z);
    }// Konstruktor  
      
    void RationalPoint3D::set(const Point3D& point){
      this->x = point.getX();
      this->y = point.getY();
      this->z = point.getZ();      
    }// set
    
    void RationalPoint3D::set(const RationalPoint3D& point){
      this->x = point.x;
      this->y = point.y;
      this->z = point.z;      
    }// set
    
    void RationalPoint3D::set(mpq_class x, mpq_class y, mpq_class z){
      this->x = x;
      this->y = y;
      this->z = z;
    }// set
    
    mpq_class RationalPoint3D::getX() const{
      return x;
    }// getX
    
    mpq_class RationalPoint3D::getY() const{
      return y;
    }// getY
    
    mpq_class RationalPoint3D::getZ() const{
      return z;    
    }// getZ
    
    Point3D RationalPoint3D::getD() const{
      return Point3D(x.get_d(),y.get_d(),z.get_d());  
    }// get
    
    std::ostream& operator <<(std::ostream& os, const RationalPoint3D& point){
      os << "RationalPoint3D(" << point.x.get_d();
      os << ", " << point.y.get_d();
      os << ", " << point.z.get_d() << ")";
      return os; 
    }// operator <<
    
    bool RationalPoint3D::operator !=(const RationalPoint3D& point) const{
      return !(*this == point);
    }// Operator !=
    
    bool RationalPoint3D::operator ==(const RationalPoint3D& point) const{
      return NumericUtil::nearlyEqual(this->x, point.x) && 
             NumericUtil::nearlyEqual(this->y, point.y) && 
             NumericUtil::nearlyEqual(this->z, point.z);
    }// Operator ==
    
    RationalPoint3D& RationalPoint3D::operator =(const RationalPoint3D& point){
      set(point);
      return *this;
    }// Operator =
      
    RationalPoint3D RationalPoint3D::operator +(
        const RationalVector3D& vector) const{
      RationalPoint3D point;
      point.x = (this->x + vector.getX());
      point.y = (this->y + vector.getY());
      point.z = (this->z + vector.getZ());
      return point;    
    }// Operator +
    
    RationalPoint3D RationalPoint3D::operator -(
        const RationalVector3D& vector) const{
      RationalPoint3D point;
      point.x = (this->x - vector.getX());
      point.y = (this->y - vector.getY());
      point.z = (this->z - vector.getZ());
      return point;
    }// Operator -
    
    RationalVector3D RationalPoint3D::operator -(
        const RationalPoint3D& point) const{
      RationalVector3D result;    
      return RationalVector3D(this->x - point.x, this->y - point.y, 
                               this->z - point.z);
    }// Operator -
         
    mpq_class RationalPoint3D::distance2(const RationalPoint3D& point)const{
      return (point - *this).length2();      
    }// distance2
      
    mpq_class RationalPoint3D::distance(const RationalPoint3D& point)const{
      return (point - *this).length();      
    }// distance     
/*
5 Class RationalVector3D

*/    
    RationalVector3D::RationalVector3D():x(0),y(0),z(0){
    }// Konstruktor
    
    RationalVector3D::RationalVector3D(const RationalVector3D& vector){
      set(vector);
    }// Konstruktor
    
    RationalVector3D::RationalVector3D(const mpq_class& x, const mpq_class& y,
                                       const mpq_class& z){
      set(x,y,z);
    }// Konstruktor
    
    void RationalVector3D::set(const RationalVector3D& vector){
      this->x = vector.x;
      this->y = vector.y;
      this->z = vector.z;
    }// set
    
    void RationalVector3D::set(const mpq_class& x, const mpq_class& y, 
                               const mpq_class& z){
      this->x = x;
      this->y = y;
      this->z = z;
    }// set
    
    mpq_class RationalVector3D::getX() const{
      return x;
    }// getX
    
    mpq_class RationalVector3D::getY() const{
      return y;
    }// GetY
    
    mpq_class RationalVector3D::getZ() const{
      return z;    
    }// getZ
    
    bool RationalVector3D::operator !=(const RationalVector3D& vector) const{
      return !(*this == vector);
    }// Operator !=
    
    bool RationalVector3D::operator ==(const RationalVector3D& vector) const{
      return NumericUtil::nearlyEqual(this->x, vector.x) && 
             NumericUtil::nearlyEqual(this->y, vector.y) && 
             NumericUtil::nearlyEqual(this->z, vector.z);
    }// Operator ==
    
    RationalVector3D& RationalVector3D::operator = (
        const RationalVector3D& vector){
      set(vector);
      return *this;
    }// Operator =  
    
    std::ostream& operator <<(std::ostream& os,const RationalVector3D& vector){
      os << "RationalVector3D( "<< vector.x.get_d();
      os << ", " << vector.y.get_d();
      os << ", " << vector.z.get_d()<<")";
      return os; 
    }// operator <<

    RationalVector3D operator *(const mpq_class& value, 
                                const RationalVector3D& vector){
      RationalVector3D result;
      result.x = value * vector.x;
      result.y = value * vector.y;
      result.z = value * vector.z;
      return result;
    }// Operator *
    
    RationalVector3D operator *(const RationalVector3D& vector, 
                                const mpq_class& value){
      RationalVector3D result;
      result.x = value * vector.x;
      result.y = value * vector.y;
      result.z = value * vector.z;
      return result;
    }// Operator *  
    
    RationalVector3D RationalVector3D::operator -() const{
      return RationalVector3D(-this->x, -this->y, -this->z);
    }// Operator -

    mpq_class RationalVector3D::operator *(
        const RationalVector3D& vector) const{
      return (this->x * vector.x + this->y * vector.y + this->z * vector.z);
    }// Operator *
       
    RationalVector3D RationalVector3D::operator ^(
        const RationalVector3D& vector) const{
      RationalVector3D result;
      result.x = this->y * vector.z - this->z * vector.y;
      result.y = this->z * vector.x - this->x * vector.z;
      result.z = this->x * vector.y - this->y * vector.x;
      return result;
    }// Operatopr ^ 
       
    void RationalVector3D::normalize(){
      mpf_class len2 = this->x * this->x + 
                       this->y * this->y + 
                       this->z * this->z;    
                       
      mpf_class len = sqrt(len2);                 
      if (len != 0.0) {
        x /= len;
        y /= len;
        z /= len;
      }// if
    }// normilize
    
    mpq_class RationalVector3D::length2() const{
      return x*x + y*y + z*z;
    }// length2
    
    mpq_class RationalVector3D::length() const{
      mpf_class tmp = length2();
      return mpq_class(sqrt(tmp));     
    }// length  
/*
6 Class Segment3D

*/      
    Segment3D::Segment3D(){   
    }// Konstruktor    
    
    Segment3D::Segment3D(const Point3D& tail, const Point3D& head){
      this->tail = tail;
      this->head = head; 
    }// Konstruktor
    
    Segment3D::Segment3D(const Segment3D& segment){
      set(segment);
    }// konstruktor
    
    Segment3D::Segment3D(const RationalSegment3D& segment){
      this->tail = segment.getTail();
      this->head = segment.getHead(); 
    }// konstruktor    
    
    void Segment3D::set(const Segment3D& segment){
      this->tail = segment.tail;
      this->head = segment.head; 
    }// konstruktor   

    Point3D Segment3D::getHead() const{
      return this->head;
    }// getHead
    
    Point3D Segment3D::getTail() const{
      return this->tail;
    }// getTail 

    RationalSegment3D Segment3D::getR()const {
      return RationalSegment3D(tail,head);
    }// getR
          
    std::ostream& operator <<(std::ostream& os, const Segment3D& segment){
      os << "Segment3D(" << segment.tail << ", " << segment.head << ")";
      return os; 
    }// operator <<
    
    bool Segment3D::operator ==(const Segment3D& segment) const{
      return (this->head == segment.head && this->tail == segment.tail);
    }// operator == 
    
    Segment3D&  Segment3D::operator =(const Segment3D& segment){
      set(segment);
      return *this;      
    }// Operator =    
/*
7 Class RationalSegment3D

*/
    RationalSegment3D::RationalSegment3D(){
    }// Konstruktor
    
    RationalSegment3D::RationalSegment3D(const RationalSegment3D& segment){
      set(segment);
    }// Konstruktor
    
    RationalSegment3D::RationalSegment3D(const Segment3D& segment){
      this->tail = segment.getTail();
      this->head = segment.getHead();
    }// Kostruktor
    
    RationalSegment3D::RationalSegment3D(const RationalPoint3D& tail, 
                                         const RationalPoint3D& head){
      this->tail = tail;
      this->head = head;
    }// konstruktor

    void RationalSegment3D::set(const RationalSegment3D& segment){
      this->tail = segment.tail;
      this->head = segment.head;
    }// set
    
    RationalPoint3D RationalSegment3D::getHead() const{
      return head;
    }// getHead
    
    RationalPoint3D RationalSegment3D::getTail() const{
      return tail;
    }// getTail
    
    Segment3D RationalSegment3D::getD() const{
      return Segment3D(tail.getD(), head.getD());
    }// get
    
    std::ostream& operator <<(std::ostream& os, 
                              const RationalSegment3D& segment){
       os << "RationalSegment3D(" << segment.tail << ", ";
       os << segment.head << ")";
      return os; 
    }// Operator << 

    bool RationalSegment3D::operator ==(
        const RationalSegment3D& segment) const{
      return (this->head == segment.head && this->tail == segment.tail);
    }// operator == 
    
    RationalSegment3D& RationalSegment3D::operator =(
        const RationalSegment3D& segment){
      set(segment);
      return *this;
    }// operator =
/*
8 Class Point2D

*/      
    Point2D::Point2D():x(0),y(0){
    }// Konstruktor
    
    Point2D::Point2D(const Point2D& point){
      set(point);    
    }// Konstruktor
    
    Point2D::Point2D(const RationalPoint2D& point){
      set(point.getX().get_d(),point.getY().get_d());  
    }// konstruktor
    
    Point2D::Point2D(double x, double y){
      set(x,y);
    }// Konstriktor
    
    void  Point2D::set(const Point2D& point){
      this->x = point.x;
      this->y = point.y;
    }// set
    
    void  Point2D::set(double x, double y){
      this->x = x;
      this->y = y;
    }// set
    
    double  Point2D::getX() const{
      return x;
    }// getX
    
    double  Point2D::getY() const{
      return y;
    }// getY
            
    RationalPoint2D Point2D::getR()const{
      return RationalPoint2D(x,y);
    }// getR
    
    bool Point2D::operator ==(const Point2D& point) const{
      return NumericUtil::nearlyEqual(this->x, point.x) && 
             NumericUtil::nearlyEqual(this->y, point.y);
    }// Operator ==
    
    Point2D&  Point2D::operator =(const Point2D& point){
      set(point);
      return *this;      
    }// Operator =
         
    std::ostream& operator <<(std::ostream& os, const Point2D& point){
      os << "Point2D(" << point.x;
      os << ", " << point.y << ")";
      return os; 
    }// Operator <<
    
    bool Point2D::operator <(const Point2D& point) const {
      if (NumericUtil::lower(x, point.x))
        return true;
      if (NumericUtil::greater(x, point.x))
        return false;           
      return NumericUtil::lower(y, point.y);
    }// Operator <
/*
9 Class RationalPoint2D

*/     
    RationalPoint2D::RationalPoint2D():x(0),y(0){
    }// Konstruktor
    
    RationalPoint2D::RationalPoint2D(const RationalPoint2D& point){
      set(point);
    }// Konstruktor
    
    RationalPoint2D::RationalPoint2D(const Point2D& point){
      set(point.getX(),point.getY());
    }// konstruktor
    
    RationalPoint2D::RationalPoint2D(const mpq_class& x, 
                                     const mpq_class& y){
      set(x,y);
    }// Konstruktor
    
    void RationalPoint2D::set(const RationalPoint2D& point){
      this->x = point.x;
      this->y = point.y;
    }// set
    
    void RationalPoint2D::set(const mpq_class& x, const mpq_class& y){
      this->x = x;
      this->y = y;
    }// set
    
    mpq_class RationalPoint2D::getX() const{
      return x;
    }// getX
    
    mpq_class RationalPoint2D::getY() const{
      return y;
    }// getY
    
    Point2D RationalPoint2D::getD()const{
      return (Point2D(x.get_d(),y.get_d()));
    }// getD

    bool RationalPoint2D::operator ==(const RationalPoint2D& point) const{
      return NumericUtil::nearlyEqual(this->x, point.x) && 
      NumericUtil::nearlyEqual(this->y, point.y);
    }// Operator ==

    RationalPoint2D& RationalPoint2D::operator =(const RationalPoint2D& point){
      set(point);
      return *this;  
    }// Operator =
    
    std::ostream& operator <<(std::ostream& os, const RationalPoint2D& point){
      os << "RationalPoint2D(" << point.x.get_d();
      os << ", " << point.y.get_d() << ")";
      return os; 
    }// Oparator <<
    
    bool RationalPoint2D::operator <(const RationalPoint2D& point) const {
      if (NumericUtil::lower(x, point.x))
        return true;
      if (NumericUtil::greater(x, point.x))
        return false;           
      return NumericUtil::lower(y, point.y);
    }// Operator <
    
    RationalVector2D RationalPoint2D::operator -(
        const RationalPoint2D& point) const{
      return RationalVector2D(x - point.x, y - point.y);
    }// Operator -  
/*
10 Class RationalVector2D

*/     
    RationalVector2D::RationalVector2D():x(0),y(0){
    }// Konstruktor
    
    RationalVector2D::RationalVector2D(const RationalVector2D& vector){
      set(vector);
    }// Konstruktor  
    
    RationalVector2D::RationalVector2D(const mpq_class& x, 
                                       const mpq_class& y){
      set(x,y);
    }// Konstruktor
    
    void RationalVector2D::set(const RationalVector2D& vector){
      this->x = vector.x;
      this->y = vector.y;
    }// set
    
    void RationalVector2D::set(const mpq_class& x, const mpq_class& y){
      this->x = x;
      this->y = y;
    }// set
    
    mpq_class RationalVector2D::getX() const{
      return x;
    }// getX
    
    mpq_class RationalVector2D::getY() const{
      return y;
    }// getY


    bool RationalVector2D::operator ==(const RationalVector2D& point) const{
      return NumericUtil::nearlyEqual(this->x, point.x) && 
      NumericUtil::nearlyEqual(this->y, point.y);
    }// Operator ==

    RationalVector2D& RationalVector2D::operator =(
        const RationalVector2D& vector){
      set(vector);
      return *this;  
    }// Operator =
    
    std::ostream& operator <<(std::ostream& os, 
                              const RationalVector2D& vector){
      os << "RationalVector2D(" << vector.x.get_d();
      os << ", " << vector.y.get_d() << ")";
      return os; 
    }// Oparator <<
    
    void RationalVector2D::normalize(){
      mpf_class len2 = this->x * this->x + 
                       this->y * this->y;                       
      mpf_class len = sqrt(len2);
      if (len != 0.0) {
        x /= len;
        y /= len;
      }// if
    }// normalize

     mpq_class RationalVector2D::operator |(
         const RationalVector2D& vector) const{
       return (x * vector.y - y * vector.x);    
     }// operator |
     
     mpq_class RationalVector2D::length() const{
      mpf_class len2 = this->x * this->x + 
                       this->y * this->y; 
      return mpq_class(sqrt(len2));                        
    }// length2
/*
11 Class Segment2D

*/      
    Segment2D::Segment2D(){
    }// Konstruktor
    
    Segment2D::Segment2D(const RationalSegment2D& segment){
      this->tail = segment.getTail();
      this->head = segment.getHead(); 
    }// konstruktor
      
    Segment2D::Segment2D(const Point2D& tail, const Point2D& head){
      this->tail = tail;
      this->head = head;
    }// Konstruktor 

    Point2D Segment2D::getHead() const{
      return this->head;
    }// getHead
      
    Point2D Segment2D::getTail() const{
      return this->tail;
    }// getTail      
    
    RationalSegment2D Segment2D::getR()const {
      return RationalSegment2D(tail,head);
    }// getR
      
    std::ostream& operator <<(std::ostream& os, const Segment2D& segment){
      os << "Segment2D(" << segment.tail << ", " << segment.head << ")";
      return os; 
    }// Opaerator 
    
     bool Segment2D::operator ==(const Segment2D& segment) const{
      return (this->head == segment.head && this->tail == segment.tail);
    }// operator == 
/*
12 Class RationalSegment2D

*/      
    RationalSegment2D::RationalSegment2D(){
    }// Konstruktor
      
    RationalSegment2D::RationalSegment2D(const RationalPoint2D& tail, 
                                         const RationalPoint2D& head){
      this->tail = tail;
      this->head = head;
    }// Konstruktor 
    
    RationalSegment2D::RationalSegment2D(const Segment2D& segment){
      this->tail = segment.getTail();
      this->head = segment.getHead(); 
    }// konstruktor

      
    RationalPoint2D RationalSegment2D::getHead() const{
      return this->head;
    }// getHead
      
    RationalPoint2D RationalSegment2D::getTail() const{
      return this->tail;
    }// getTail      
      
    Segment2D RationalSegment2D::getD()const {
      return Segment2D(tail,head);
    }// getR  
      
    std::ostream& operator <<(std::ostream& os, 
                              const RationalSegment2D& segment){
      os << "RationalSegment2D (" << segment.tail;
      os << ", " << segment.head << ")";
      return os; 
    }// Opaerator 
    
     bool RationalSegment2D::operator ==(
         const RationalSegment2D& segment) const{
      return (this->head == segment.head && this->tail == segment.tail);
    }// operator == 
        
    bool RationalSegment2D::intersection(const 
        RationalSegment2D& other, 
        RationalPoint2D& intersectionPoint)const{
      mpq_class relDistanceFromTail = 0; 
      mpq_class x00 = this->tail.getX();
      mpq_class y00 = this->tail.getY();
      mpq_class x01 = this->head.getX();
      mpq_class y01 = this->head.getY(); 
      mpq_class x10 = other.tail.getX();
      mpq_class y10 = other.tail.getY();
      mpq_class x11 = other.head.getX();
      mpq_class y11 = other.head.getY(); 
      mpq_class denominator= (x00-x01)*(y10-y11) -(y00-y01)*(x10-x11);
      if (NumericUtil::nearlyEqual(denominator, 0)) return false;
      mpq_class x = (x00*y01-y00*x01)*(x10-x11)-(x00-x01)*(x10*y11-y10*x11);
      mpq_class y = (x00*y01-y00*x01)*(y10-y11)-(y00-y01)*(x10*y11-y10*x11);
      x=x/denominator;
      y=y/denominator;
      if (!NumericUtil::lowerOrNearlyEqual(min(x00,x01),x)) return false;
      if (!NumericUtil::lowerOrNearlyEqual(min(x10,x11),x)) return false;
      if (!NumericUtil::lowerOrNearlyEqual(min(y00,y01),y)) return false;       
      if (!NumericUtil::lowerOrNearlyEqual(min(y10,y11),y)) return false;
      if (!NumericUtil::lowerOrNearlyEqual(x,max(x00,x01))) return false;
      if (!NumericUtil::lowerOrNearlyEqual(x,max(x10,x11))) return false;
      if (!NumericUtil::lowerOrNearlyEqual(y,max(y00,y01))) return false;
      if (!NumericUtil::lowerOrNearlyEqual(y,max(y10,y11))) return false;
      intersectionPoint = RationalPoint2D(x,y);
      if((x01-x00)!=0){
        relDistanceFromTail = (x-x00)/(x01-x00);
      }// if
      else if ((y01-y00)!=0){
        relDistanceFromTail = (y-y00)/(y01-y00);
      }// else if
      else {
        relDistanceFromTail = 0;
      }// else
      return true;
    }// intersection
    
    mpq_class RationalSegment2D::whichSide(const RationalPoint2D& point)const{
      // This is the fast version:
      // value = (start.x - x) * (end.y - y) - (end.x - x) * (start.y - y);
      // This is slower, but numerical more stable:
      RationalVector2D vector1 = head  - tail;
      RationalVector2D vector2 = point - tail;      
      vector1.normalize();
      vector2.normalize();
      mpq_class value = vector1 | vector2;     
      return value; 
    }// isLeft
    
    bool RationalSegment2D::isLeft(const RationalPoint2D& point)const{
      return NumericUtil::greater(whichSide(point), 0.0); 
    }// isLeft  
/*
13 Class Point3DContainer

*/       
    Point3DContainer::Point3DContainer():pointsTree(4, 8){
    }// Konstruktor

    Point3DContainer::Point3DContainer(
       const Point3DContainer& other):pointsTree(4, 8){
      set(other);
    }// Konstruktor  
    
    void Point3DContainer::set(const Point3DContainer& other){
      this->points     = other.points;
      this->pointsTree = other.pointsTree;
    }// set
              
    Point3D Point3DContainer::get(size_t index)const{
      if(index >= points.size()){
        NUM_FAIL("point index is out of range.");
      }// if  
      return points[index];
    } // get
    
    size_t Point3DContainer::add( 
        const Point3D& point){
      Rectangle<3> bbox=point.getBoundingBox(); 
      bbox.Extend(NumericUtil::eps);
      std::unique_ptr<mmrtree::RtreeT<3, size_t>::iterator> 
        it(pointsTree.find(bbox));
      size_t const* index;
      while((index = it->next()) != 0){
        if(points[*index] == point) return *index;
      }// while
      size_t newIndex = points.size();
      points.push_back(point);
      pointsTree.insert(bbox, newIndex);
      return newIndex;
    }// add
    
    size_t Point3DContainer::size()const{
      return points.size();
    } // size

    std::ostream& Point3DContainer::print(
        std::ostream& os, std::string prefix)const{ 
      os << "Point3DContainer(" << endl;
      for(size_t i = 0; i< points.size(); i++){
        os << prefix + "  Index:="<< i<<", " << points[i] << endl; 
      }// for
      os << prefix << ")" << endl;
      return os;
    }// print
       
    bool Point3DContainer::operator==(
        const Point3DContainer& other)const{
      if(this->points.size() != other.points.size()) return false;
      for(size_t i = 0; i < points.size(); i++){
        if(other.points[i] != this->points[i]) {
           cerr << "Faile on Index:=" << i << ", ";
           cerr << this->points[i] << ", ";
           cerr << other.points[i] << endl;
          return false;
        }// if
      }// for
      return true;
    }// Operator ==
    
    Point3DContainer& Point3DContainer::operator=(
        const Point3DContainer& points){
      set(points);
      return *this;
    }// Operator =
    
    std::ostream& operator<<(
        std::ostream& os, const Point3DContainer& container){
      return container.print(os,"");
    }// Operator << 
/*
14 class Segment

*/      
    Segment::Segment (){
      this->head       = 0;
      this->tail       = 0;
      this->predicate  = UNDEFINED;
    }// Konstruktor    
    
    Segment::Segment (size_t tail, size_t head, 
                      const Predicate& predicate /* = UNDEFINED */){
      this->head       = head;
      this->tail       = tail;
      this->predicate  = predicate;
    }// Konstruktor
    
    Segment::Segment (const Segment& segment){
      set(segment);
    }// KOnstruktor
    
    void Segment::set(const Segment& segment){
      this->head       = segment.head;
      this->tail       = segment.tail;
      this->predicate  = segment.predicate;
    }// set
    
    size_t Segment::getHead()const{
      return this->head;
    }// getHead
    
    size_t Segment::getTail()const{
      return this->tail;
    }// getTail
      
    Predicate Segment::getPredicate() const{
      return this->predicate;
    }// getPredicate

    void Segment::setPredicate(Predicate predicate){
      this->predicate = predicate;
    }// setPredicate
    
    std::ostream& operator <<(std::ostream& os, const Segment& segment){
      os << "Segment(" << segment.getTail() << ", " << segment.getHead();
      os << ", ";
      os << toString(segment.getPredicate()) <<")";
      return os;
    }// operator <<

    bool Segment::operator ==(const Segment& segment) const{
      if(this->head       == segment.head &&
         this->tail       == segment.tail &&
         this->predicate  == segment.predicate) return true;
      return false;
    }// Operator ==

    Segment& Segment::operator =(const Segment& segment){
      set(segment);
      return *this;
    }// Operator = 
/*
15 class SegmentContainer

*/      
    SegmentContainer::SegmentContainer():
       segmentBuckets(vector<vector<size_t>>(buckets,vector<size_t>())){
    }// Konstruktor
      
    SegmentContainer::SegmentContainer(const SegmentContainer& other){
      set(other);
    }// Konstruktor
    
    void SegmentContainer::clear(){
      this->segmentBuckets = vector<vector<size_t>>(buckets,vector<size_t>());
      this->segments       = vector<Segment>();    
    }// clear
    
    void SegmentContainer::set(const SegmentContainer& other){
      this->segmentBuckets = other.segmentBuckets;
      this->segments       = other.segments; 
    }// set
    
    size_t SegmentContainer::size()const {
      return segments.size(); 
    }// size    
    
    size_t SegmentContainer::getHash(const Segment& segment)const{
      return (segment.getTail() + 
             this->buckets * segment.getHead()) % this->buckets;
    }// getHash

    size_t SegmentContainer::add(const Segment& segment, 
                                 bool pFaceIsCritical /* = false*/){
      size_t hash = getHash(segment);
      for(size_t i = 0; i< segmentBuckets[hash].size();i++){
        size_t j = segmentBuckets[hash][i];
        Segment other = segments[j];
        // Two segments with equal tail und head
        if( other.getTail() == segment.getTail() &&
            other.getHead() == segment.getHead()){          
          // cout << other << endl;
          // cout << segment << endl; 
          // In the case of a noncritical intersection, 
          // the old and the new predicate are distinguishable.
          if(!pFaceIsCritical){
            if((segment.getPredicate() == RIGHT_IS_INNER && 
                other.getPredicate()   == LEFT_IS_INNER) || 
               (segment.getPredicate() == LEFT_IS_INNER && 
                other.getPredicate()   == RIGHT_IS_INNER)){             
              segments[j].setPredicate(UNDEFINED);  
              return j;
            }//if
            // Old predicate is undefined
            else if (other.getPredicate() == UNDEFINED) {
              segments[j] = segment;
              return j; 
            }// else if 
            // Old and new predicates are the same
            else if (other.getPredicate() == segment.getPredicate()){
              return j;
            }// else if                 
            cerr << "old segment:=" << other << endl;
            cerr << "new segment:=" << segment << endl;
            NUM_FAIL("Predicates from non critical segments don't combinable");
          }// if            
          else {
            // Start or end point have an intersection
            if (other.getPredicate()   == UNDEFINED && (
                segment.getPredicate() == RIGHT_IS_INNER ||
                segment.getPredicate() == LEFT_IS_INNER)){
              segments[j].setPredicate(INTERSECT);
              return j; 
            }// if
            // Cut within the critical segment
            // Take the predicate.
            else if (other.getPredicate()   == NO_INTERSECT && 
                    (segment.getPredicate() == RIGHT_IS_INNER ||
                     segment.getPredicate() == LEFT_IS_INNER)){
              segments[j] = segment;
              return j;
            }// else if
            // Old and new predecate are the same 
            else if (other.getPredicate() == segment.getPredicate()){
              return j;
            }// else if 
            // Segment is added one more time
            else if (other.getPredicate()   == UNDEFINED && (
                     segment.getPredicate() == INNER ||
                     segment.getPredicate() == OUTER||
                     segment.getPredicate() == INTERSECT)){
              segments[j] = segment;
              return j; 
            }// if  
            // Segment with contradictory predicate is to be set.
            else if (other.getPredicate()   == INTERSECT && (
                     segment.getPredicate() == INNER ||
                     segment.getPredicate() == OUTER)){
              return j;
            }// if            
            cerr << "old segment:=" << other << endl;
            cerr << "new segment:=" << segment << endl;
            cerr << *this;
            NUM_FAIL("Predicates from critical segments don't combinable.");
          }// else - segments form critical pface
        }// if - two equal segments 
      }// for
      size_t index = segments.size();
      segments.push_back(segment);
      segmentBuckets[hash].push_back(index);
      return index;
    }// add
      
    void SegmentContainer::set(size_t index, Predicate predicate){
      if(index < segments.size()){
        Predicate oldPredicate = segments[index].getPredicate();
        if(segments[index].getPredicate() == predicate) return;
        else if(oldPredicate == UNDEFINED || oldPredicate == NO_INTERSECT){
          if(predicate != UNDEFINED && predicate != NO_INTERSECT) {
            segments[index].setPredicate(predicate);
          }// if
        }// else if
        else if ((oldPredicate == INNER && predicate == OUTER) ||
                 (oldPredicate == OUTER && predicate == INNER)) { 
          segments[index].setPredicate(INTERSECT);
        }// else
      }// if
      else NUM_FAIL("Index is out of range.");        
    }// set
      
    Segment SegmentContainer::get(size_t index)const{
      if(index < segments.size()){
        return segments[index];
      }// if
      else {
        cerr << *this;
        cerr << "Index is:=" << index << endl;
        NUM_FAIL("Index is out of range."); 
        return segments[0];
      }// else
    }// get
      
    std::ostream& SegmentContainer::print(std::ostream& os, 
                                          std::string prefix)const{
      os <<  "SegmentContainer(" << endl;
      for(size_t i = 0; i < segments.size(); i++){
        os << prefix + "  Index:=" << i << ", " << segments[i] << endl;
      }// for
      //for(size_t i = 0; i < segmentBuckets.size(); i++){
      //  os << prefix << "  Bucket:=" << i << "( ";
      //  std::list<size_t>::const_iterator iterator;
      //  for(iterator  = segmentBuckets[i].begin(); 
      //      iterator != segmentBuckets[i].end();){  
      //    os << *iterator;
      //     iterator++;
      //    if(iterator != segmentBuckets[i].end()) os << ", "; 
      //  }// for
      //  os << ")" << endl;
      //}// for
      os << prefix << ")" << endl;
      return os;
    }// print
      
    std::ostream& operator<<( std::ostream& os,
                              const SegmentContainer& container){
      return container.print(os,"");
    }// Operator <<
      
    bool SegmentContainer::operator == (const SegmentContainer& other)const{
      if(this->segments.size() != other.segments.size()) return false;
      for(size_t i = 0; i < this->segments.size(); i++){
        if(!(other.segments[i] == this->segments[i])) {
          // cout << "Faile on Index:=" << i << ", ";
          // cout << this->segments[i] << ", ";
          // cout << other.segments[i] << endl;
          return false;
        }// if
      }// for
      return true;
    }// Operator ==
      
    SegmentContainer& SegmentContainer::operator = (
        const SegmentContainer& segments){
      set(segments);
      return *this;
    }// Operator =    

  } // end of namespace mregionops3
} // end of namespace temporalalgebra
