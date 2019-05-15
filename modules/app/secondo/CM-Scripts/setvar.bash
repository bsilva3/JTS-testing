# bash Script for setting up a secondo environment
#
# The first argument is interpreted as SECONDO_BUILD_DIR
# copy this file to an apropriate location and set up
# an shell alias in your .bashrc file:

if [ -z $SETVAR_FIRST_CALL ]; then

  export SETVAR_FIRST_CALL="true"
  export COPY_OF_PATH=$PATH
  export COPY_OF_LD_PATH=$LD_LIBRARY_PATH
fi

PATH=$COPY_OF_PATH
LD_LIBRARY_PATH=$COPY_OF_LD_PATH

if [ "$1" != "" ]; then
  export SECONDO_BUILD_DIR=$1
else
  export SECONDO_BUILD_DIR=$PWD
fi

export SECONDO_CONFIG=${SECONDO_BUILD_DIR}/bin/SecondoConfig.ini

sdk=$SECONDO_SDK
binPaths=""
libPaths=""
incPaths=""
for dir in gcc dep bison flex; do
  binPaths=$binPaths"$sdk/$dir/bin:"
  libPaths=$libPaths"$sdk/$dir/lib:"
  incPaths=$incPaths"$sdk/$dir/include:"
done 
echo $libPaths
echo $binPaths
echo $incPaths


# Path declarations for the GCC
export CPLUS_INCLUDE_PATH=$incPaths
export LIBRARY_PATH=$libPaths:${SECONDO_BUILD_DIR}/lib

# Bison
export BISON_SIMPLE=${SECONDO_SDK}/bison/share/bison/bison.simple

# JNI
export JNI_INIT=${SECONDO_BUILD_DIR}/bin/JNI.ini

## Extend the search path
PATH=.:${J2SDK_ROOT}/bin:$binPaths:${PATH}
echo $PATH

# The runtime linker uses different variables on linux and windows
if [ $SECONDO_PLATFORM != "win32" ]; then

   pathList=${J2SDK_ROOT}/jre/lib/i386
   pathList=${pathList}:${J2SDK_ROOT}/jre/lib/i386/client
   pathList=${pathList}:$libPaths
   pathList=${pathList}:${BERKELEY_DB_DIR}/lib
   pathList=${pathList}:${PL_LIB_DIR}
   pathList=${pathList}:${LD_LIBRARY_PATH}

   LD_LIBRARY_PATH=.:${pathList}

else

   pathList=${J2SDK_ROOT}/jre/bin/client
   pathList=${pathList}:${MINGW_DIR}
   pathList=${pathList}:${SECONDO_BUILD_DIR}/lib
   pathList=${pathList}:${SECONDO_SDK}/lib
   pathList=${pathList}:${SECONDO_SDK}/pl/bin

   PATH=${PATH}:${pathList}
fi

# Some general extensions
PATH=${PATH}:${SECONDO_BUILD_DIR}/Tools/pd
PATH=${PATH}:${SECONDO_BUILD_DIR}/CM-Scripts
PATH=${PATH}:${SECONDO_BUILD_DIR}/bin

export PATH LD_LIBRARY_PATH

export PD_HEADER=${SECONDO_BUILD_DIR}/Tools/pd/pd.header
