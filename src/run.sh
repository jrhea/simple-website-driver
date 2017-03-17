#!/bin/bash
#Usage:
# ./run.sh [input file]
#Example:
# ./run.sh /path/to/data/login.txt

#add phantomjs to path if it doesn't exist
PHANTOMJS_PATH="/home/jrhea/3rd-party/phantomjs-2.1.1-linux-x86_64"
[[ ":$PATH:" != *":$PHANTOMJS_PATH:"* ]] && PATH="$PHANTOMJS_PATH/bin:${PATH}"

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

#execute script

if [ $# -eq 0 ]; then
  ./websiteDriver.py
else
  ./websiteDriver.py < $1
fi