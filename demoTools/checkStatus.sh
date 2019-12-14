#!/bin/bash
rem=`git config --get remote.origin.url`
echo $rem
git remote update &>/dev/null
st=`git status | awk 'NR==2'`
if [ `echo $st | grep -c 'branch is up to date'` -eq 1 ]; then
   echo 0
elif [ `echo $st | grep -c 'branch is behind'` -eq 1 ]; then
   echo 1
elif [ `echo $st | grep -c 'branch is ahead'` -eq 1 ]; then
   echo 2
else
   echo 3
fi
date
echo $st
