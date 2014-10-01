#!/bin/bash

remote=$(git --git-dir=$1 remote update &> /dev/null)
remote_status=$(git --git-dir=$1 status -uno)
rm -f $(echo -e $1)current/*.pyo
rm -f $(echo -e $1)current/*.pyc
rm -f $(echo -e $1)repo/*.pyo
rm -f $(echo -e $1)repo/*.pyc

if [[ "$(echo -e $remote_status | grep "behind")" != "" ]]; then
   git --git-dir=$1 fetch --all --force
   git --git-dir=$1 reset --hard
   git --git-dir=$1 rebase origin/master
   cp $(echo -e $1)repo/* $(echo -e $1)current/
else
   echo -e "Already up-to-date"
fi   

