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

//characters [1] verbatim:  [\verb@]         [@]
//paragraph  [1] title:     [{\Large \bf ]   [}]


[1] GameOps.hpp

1 Defines and includes

*/

#ifndef SECONDO_ALGEBRAS_CHESS_GAMEOPS_HPP
#define SECONDO_ALGEBRAS_CHESS_GAMEOPS_HPP

#include <string>
#include <functional>
#include <boost/assert.hpp>
#include "Algebras/Relation-C++/RelationAlgebra.h"
#include "TypeMapping.hpp"
#include "ListStream.hpp"
#include "Game.hpp"
#include "MoveOps.hpp"


/*
2. operator definitions - for operating on Game objects

    Basic functionality is to get moves, positions and
    the history of a chess match.

    See ChessAlgebra.examples for further information

*/


struct getkey_op : std::binary_function< Game, CcString, std::string >
{
    std::string operator()( const Game& g, const CcString& s ) const
    {
        const std::string& key = s.GetValue();
        for( int i = 0; i < g.tags.Size(); ++i )
        {
            std::string tmp = g.get_tag( i ).first.GetValue();
            if ( key == tmp )
                return g.get_tag( i ).second.GetValue();
        }
        throw std::runtime_error( "Key not found" );
    }
};

struct getposition_op : std::binary_function< Game, CcInt, Position* >
{
    Position* operator() ( const Game& g, const CcInt& ccn ) const
    {
        int n = ccn.GetValue();
        if ( g.moves.Size() < n || n < 0 )
            throw std::runtime_error( "Move number out of bounds" );
        Position* pos = new Position( INITIAL_POSITION );
        for( int i = 0; i < n; ++i )
        {
            const Ply& p = g.get_move( i );
            delete apply_ply_op()( *pos, p );
        }
        return pos;
    }
};

struct getmove_op : std::binary_function< Game, CcInt, Ply* >
{
    Ply* operator() ( const Game& g, const CcInt& ccn ) const
    {
        int n = ccn.GetValue() - 1;
        if ( g.moves.Size() <= n || n < 0 )
            throw std::runtime_error( "Move number out of bounds" );
        return new Ply( g.get_move(n) );
    }
};

struct lastmove_op : std::unary_function< Game, int >
{
    int operator() ( const Game& g ) const
    {
        return g.moves.Size();
    }
};

struct moves_op : std::unary_function< Game, std::pair<bool, Ply*> >
{
    moves_op( const Game&, ListExpr type ) : current_(0) {}

    std::pair<bool, Ply*> operator()( const Game& g )
    {
        if ( current_ < g.moves.Size() )
            return std::make_pair( true, new Ply( g.get_move( current_++ ) ) );
        return std::make_pair( false, new Ply(UNDEF) );
    }

private:
    int current_;
};

struct positions_op : std::unary_function< Game, std::pair<bool, Position*> >
{
    positions_op( const Game&, ListExpr type )
        : current_(-1), pos_(INITIAL_POSITION) {}

    std::pair<bool, Position*> operator()( const Game& g )
    {
        if ( ++current_ < g.moves.Size() )
        {
            delete apply_ply_op()( pos_, g.get_move( current_ ) );
            return std::make_pair( true, new Position( pos_ ) );
        }
        return std::make_pair( false, new Position(UNDEF) );
    }

private:
    int current_;
    Position pos_;
};

struct history_op : std::unary_function< Game, std::pair<bool, Tuple*> >
{
    history_op( const Game&, ListExpr type )
        : type_(type), current_(0), pos_(INITIAL_POSITION){}

    std::pair<bool, Tuple*> operator()( const Game& g )
    {
        TupleType type( type_ );
        if ( current_ < g.moves.Size() )
        {
            const Ply& ply = g.get_move( current_++ );
            delete apply_ply_op()( pos_, ply );

            TupleType* tt = new TupleType(type_);
            Tuple* result = new Tuple( tt );
            tt->DeleteIfAllowed();
            result->PutAttribute( 0, new CcInt(true, current_) );
            result->PutAttribute( 1, new Position(pos_) );
            result->PutAttribute( 2, new Ply(ply) );
            return std::make_pair( true, result );
        }
        TupleType* tt = new TupleType(type_);
        std::pair<bool,Tuple*> res = std::make_pair( false, new Tuple( tt ) );
        tt->DeleteIfAllowed(); // free the local reference
        return res;
    }

    static list_ostream type( ListExpr )
    {
        return list_ostream()
           << ( list_ostream() << ChessBSymbol("No")
                               << ChessBSymbol("int") )
           << ( list_ostream() << ChessBSymbol("Pos")
                               << ChessBSymbol("position") )
           << ( list_ostream() << ChessBSymbol("Move")
                               << ChessBSymbol("chessmove") );
    }

private:
    ListExpr type_;
    int current_;
    Position pos_;
};

#endif // SECONDO_ALGEBRAS_CHESS_GAMEOPS_HPP
