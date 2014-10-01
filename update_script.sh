#!/bin/bash
repo="$(echo -e $1)repo/.git"
remote=$(git --git-dir=$repo remote update &> /dev/null)
remote_status=$(git --git-dir=$repo status -uno)
rm -f $(echo -e $1)current/*.pyo
rm -f $(echo -e $1)current/*.pyc
rm -f $(echo -e $1)repo/*.pyo
rm -f $(echo -e $1)repo/*.pyc

if [[ "$(echo -e $remote_status | grep "behind")" != "" ]]; then
   rm -f $(echo -e $1)repo/*
   rm -rf $(echo -e $1)repo/.git
   echo -e "*** Update in process ***\nDO NOT EXIT!"
   git clone https://github.com/lost-osiris/nfs-diag.git $1/repo &> /dev/null
   #git --git-dir=$repo fetch --all --force
   #git --git-dir=$repo reset --hard
   #git --git-dir=$repo rebase origin/master
   src="$(echo -e $1)repo/*"
   dest="$(echo -e $1)current/"
   cp $src $dest
   echo -e "*** Successfully Updated ***"
else
   echo -e "Already up-to-date"
fi   

