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
cd ~
dots=.bash* .dir_colors .minttyrc .gitconfig .k .ssh/authorized_keys .vim/
tar cf $Lnx/tar/dots.tar $dots
tar cf $Lnx/tar/bin.tar bin
#
echo "git clone git@github.com:brikahnoaa/Linux.git"
