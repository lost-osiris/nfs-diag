#!/bin/bash
repo="$(echo -e $1)repo/.git"
remote=$(git --git-dir=$repo remote update &> /dev/null)
remote_status=$(git --git-dir=$repo status -uno)
rm -f $(echo -e $1)current/*.pyo
rm -f $(echo -e $1)current/*.pyc
rm -f $(echo -e $1)repo/*.pyo
rm -f $(echo -e $1)repo/*.pyc
echo "blah"
if [[ "$(echo -e $remote_status | grep "behind")" != "" ]]; then
   git --git-dir=$repo pull --force
   #git --git-dir=$repo fetch --all --force
   #git --git-dir=$repo reset --hard
   #git --git-dir=$repo rebase origin/master
   src="$(echo -e $1)repo/*"
   dest="$(echo -e $1)current/"
   cp $src $dest
else
   echo -e "Already up-to-date"
fi   

