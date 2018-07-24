#!/bin/sh
# Script for quickly recompiling and testing the elasticsearch-aknn plugin.
set -e

ESBIN="$HOME/Downloads/elasticsearch-6.2.4/bin"
PLUGINPATH="file:build/distributions/elasticsearch-aknn-0.0.1-SNAPSHOT.zip"

# TODO: fix the code so that skipping these tasks is not necessary.
gradle clean build -x integTestRunner -x test 
$ESBIN/elasticsearch-plugin remove elasticsearch-aknn | true
$ESBIN/elasticsearch-plugin install -b $PLUGINPATH

export ES_HEAP_SIZE=12g
sudo sysctl -w vm.max_map_count=262144
# most probably line above will cause an error on mac. The solution is following:
#
# run:
#
# screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
#
# If it asks you for a username and password, Log in with root and no password.
# If it just has a blank screen, press RETURN.
#
# Then configure the sysctl setting as you would for Linux:
# sysctl -w vm.max_map_count=262144
#
# Exit by Control-A Control-\

$ESBIN/elasticsearch


