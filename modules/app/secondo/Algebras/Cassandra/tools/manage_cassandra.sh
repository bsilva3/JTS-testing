#!/bin/bash
#
# This script starts and stops cassandra
# on multiple nodes. The script can also
# create the default keyspaces.
#
# Jan Kristof Nidzwetzki
#
#######################################

# Scriptname and Path
pushd `dirname $0` > /dev/null
scriptpath=`pwd`
scriptname=$(basename $0)
popd > /dev/null

# Include functions
. $scriptpath/functions.sh

# Set language to default
LANG=C

# Cassandra Nodes
nodes=$DSECONDO_SN

if [ -z "$nodes" ]; then
   echo "Your environment variable \$(DSECONDO_SN) is empty. Please check your .secondorc"
   exit -1
fi

# Cassandra dir
cassandrapath="/opt/psec/nidzwetzki/cassandra"
cassandradir=$cassandrapath/current
cassandraconfig=$cassandradir/conf/cassandra.yaml

# Cassandra version and download URL
cassandra_version="2.2.5"
cassandra_url="http://artfiles.org/apache.org/cassandra/${cassandra_version}/apache-cassandra-${cassandra_version}-bin.tar.gz"

##
# Configuration
##

# Number of nodes for one physical system
cassandra_vnodes=64

# Path for data
cassandra_data_dir=$cassandrapath/data

# Path for commit logs
cassandra_commitlog_dir=/mnt/diskb/psec2/nidzwetzki/cassandra/commitlog

# Cassandra seed master
cassandra_seed="132.176.69.181"

# Start cassandra
start() {

commitlogs=$(ls -l $cassandra_commitlog_dir | wc -l)

if [ $commitlogs -le 1 ]; then
   firststart=1
else
   firststart=0
fi

script=$(readlink -f $0)

counter=0
for node in $nodes; do
   
   echo -n "Starting Cassandra on Node $node " 
   ssh $node "source .secondorc; $script start_local > /dev/null" 
   res=$?
   
   sleep 5

   if [ $counter -eq 0 ]; then
      echo -n "(first node) "
      sleep 10
   fi

   if [ $res -ne 0 ]; then
       echo -e $failed 
   else
     if [ $counter -ne 0 ]; then
       if [ $firststart -eq 1 ]; then
          # Wait for node to connect 
          while [ true ]; do
             if [ $($cassandradir/bin/nodetool ring | grep Joining | wc -l) -ne 0 ]; then
                break
             fi 
             echo -n "."
          done

          echo -n "-"
          
          # Wait for join
          while [ true ]; do
             if [ $($cassandradir/bin/nodetool ring | grep Joining | wc -l) -eq 0 ]; then
                break
             fi 
             echo -n "."
          done
       fi
     fi
 
     echo -e $done
   fi

   let counter=counter+1
done


echo "All cassandra nodes are ready...."
}

start_local() {
  # Set max filehandles
  ulimit -n 32768 > /dev/null 2>&1
  
  if [ $? -ne 0 ]; then
     echo "Unable to set max filehandles to 32768"
     echo "Contact your system administrator for assistance"
     exit -1
  fi

  $cassandradir/bin/cassandra > /dev/null 
}

# Stop cassandra
stop() {
   execute_parallel "ps ux | grep cassandra.jmx.local.port | grep -v grep | awk {'print \$2'} | xargs kill 2> /dev/null" "Stopping Cassandra" "$nodes" $max_pending
}

# Delete the data and the commit log of cassandra
delete_old_data() {
    
    if [ -d $cassandra_data_dir ]; then
        rm -r $cassandra_data_dir
    fi

    if [ -d $cassandra_commitlog_dir ]; then
        rm -r $cassandra_commitlog_dir
    fi

    mkdir -p $cassandra_data_dir
    mkdir -p $cassandra_commitlog_dir
}

# Download and install cassandra
install_cassandra_local() {
    if [ ! -d $cassandrapath ]; then
       echo "$cassandrapath does not exist, creating"
       mkdir -p $cassandrapath
    fi

    delete_old_data

    cd $cassandrapath
    
    if [ ! -f apache-cassandra-${cassandra_version}-bin.tar.gz ]; then
        wget $cassandra_url
    else
        rm -r apache-cassandra-${cassandra_version}
    fi
       
    tar zxvf apache-cassandra-${cassandra_version}-bin.tar.gz > /dev/null
 
    if [ -d current ]; then
       rm current
    fi

    ln -s apache-cassandra-${cassandra_version} current
   
    ip=$(getIp)

    sed -i "s/num_tokens: .*/num_tokens: $cassandra_vnodes/" $cassandraconfig
    sed -i "s/# commitlog_directory/commitlog_directory/" $cassandraconfig
    sed -i "s|commitlog_directory: .*|commitlog_directory: $cassandra_commitlog_dir|" $cassandraconfig
    sed -i "s/# data_file_directories/data_file_directories/" $cassandraconfig
    sed -i "s|#     -.*|     - $cassandra_data_dir|" $cassandraconfig
    sed -i "s/listen_address:.*/listen_address: $ip/" $cassandraconfig
    sed -i "s/rpc_address:.*/rpc_address: $ip/" $cassandraconfig
   
#    if [ $cassandra_seed != $ip ]; then
        sed -i "s|seeds: \"127.0.0.1\"|seeds: \"127.0.0.1,$cassandra_seed\"|" $cassandraconfig
#    fi 
}

# Install cassandra on all nodes
install_cassandra() {
script=$(readlink -f $0)

for node in $nodes; do
   echo -n "Install Cassandra on Node $node " 
   ssh $node "source .secondorc; $script install_local > /dev/null" 
   echo -e $done
done

}

# Init cassandra keyspaces
init_cassandra() {
	tmpfile=$(mktemp)
	ip=$(getIp)

        for i in $(seq 1 6); do
            echo -n "Creating keyspace keyspace_r$i "
            echo "" > $tmpfile
            echo "CREATE KEYSPACE keyspace_r$i WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : $i};" >> $tmpfile
            echo "USE keyspace_r$i;" >> $tmpfile
            echo "CREATE TABLE IF NOT EXISTS system_queries (id INT, query TEXT, version BIGINT, PRIMARY KEY(id));" >> $tmpfile
            echo "CREATE TABLE IF NOT EXISTS system_state (ip TEXT, node TEXT, cputype TEXT, memory INT, threads INT, heartbeat BIGINT, lastquery INT, PRIMARY KEY(ip));" >> $tmpfile
            echo "CREATE TABLE IF NOT EXISTS system_progress (queryid INT, ip TEXT, begintoken TEXT, endtoken TEXT, queryuuid TEXT, PRIMARY KEY(queryid, begintoken));" >> $tmpfile
            echo "CREATE TABLE IF NOT EXISTS system_pending (queryid INT, ip TEXT, begintoken TEXT, endtoken TEXT, PRIMARY KEY(queryid, begintoken, ip));" >> $tmpfile
            echo "CREATE TABLE IF NOT EXISTS system_tokenranges (begintoken TEXT, endtoken TEXT, ip TEXT, PRIMARY KEY(begintoken));" >> $tmpfile
	    
            $cassandradir/bin/cqlsh $ip < $tmpfile
            echo -e $done
        done

	rm $tmpfile
}

case "$1" in 

start)
   start
   ;;
stop)
   stop
   ;;
start_local)
   start_local
   ;;
install)
   install_cassandra
   ;;
install_local)
   install_cassandra_local
   ;;
init)
   init_cassandra
   ;;
*)
   echo "Usage $0 {start|stop|init|install}"
   ;;
esac

exit 0

