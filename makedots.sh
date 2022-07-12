#!/bin/bash
Lnx=~/Linux
cd ~
dots=".bash* .dir_colors .minttyrc .gitconfig .k .ssh/auth* .ssh/config .vim"
echo tar cf $Lnx/dots.tar bin $dots 
tar cf $Lnx/dots.tar bin $dots
#
echo "git clone git@github.com:brikahnoaa/Linux.git"
