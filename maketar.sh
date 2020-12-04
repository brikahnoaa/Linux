#!/bin/bash
Lnx=~/Linux
echo "cd $Lnx"
cd $Lnx
mkdir -p tar
echo "rm -f tar/*.tar"
rm -f tar/*.tar
for i in opt etc usr servers; do
  echo "tar cf tar/$i.tar $i"
  tar cf tar/$i.tar $i
done
#
echo "git clone git@github.com:brikahnoaa/Linux.git"
