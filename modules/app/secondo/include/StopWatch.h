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

Small class for time measurement. Elapsed (real) time and used CPU time can
be computed according to a reference time defined by creation of the object or
by the start method. Times can be returnd as a double value representing seconds
or formatted as a string.

July 2004, M. Spiekermann. The class was created as replacement for calss TimeTest.
An instance could be used as a clock to measure time differences.

*/

#ifndef STOPWATCH_H
#define STOPWATCH_H

#include <string>
#include "SecondoConfig.h"


#ifndef SECONDO_WIN32
#include <sys/times.h>
#include <sys/time.h>
#else
#include <time.h>
#endif

#include "SecondoConfig.h"


#ifdef THREAD_SAFE
#include <boost/thread.hpp>
#endif


class StopWatch {


  public:
    StopWatch();
    StopWatch(const StopWatch& src);
    StopWatch& operator=(const StopWatch& src);
    ~StopWatch();

    // Reset the start time. Differences are computed with respect to this time
    void start();

    // return the real time difference (now-start) formatted as string
    const std::string diffReal();

    // return used CPU time since start formatted as string
    const std::string diffCPU();

    // return both times
    const std::string diffTimes();

    // return the time in format HH:MM:SS
    static const std::string timeStr(const time_t& inTime = 0);

    // return times in seconds
    double diffSecondsReal();
    double diffSecondsCPU();

    std::string minutesAndSeconds(const double seconds);

    static std::string currentTime();

  private:

#ifdef SECONDO_WIN32
    time_t startReal;
    time_t stopReal;
    clock_t cstartCPU;
    clock_t cstopCPU;
#else
    timeval startReal;
    timeval stopReal;
    struct tms startCPU;
    struct tms stopCPU;
#endif

#ifdef THREAD_SAFE
boost::mutex mtx;
#endif



};

#endif

