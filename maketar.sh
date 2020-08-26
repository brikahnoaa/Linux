#!/bin/bash
Lnx=~/Linux
Kahn=".bash* .dir_colors .minttyrc .gitconfig .k .ssh/authorized_keys .vim bin"
cd
echo "rm $Lnx/tar/*.tar"
rm $Lnx/tar/*.tar
echo "cd ~; tar cf $Lnx/tar/kahn.tar $Kahn"
cd ~; tar cf $Lnx/tar/kahn.tar $Kahn
echo "cd ~; tar cf $Lnx/tar/notes.tar Notes"
cd ~; tar cf $Lnx/tar/notes.tar Notes
echo "cd $Lnx/opt; tar cf $Lnx/tar/opt.tar ."
cd $Lnx/opt; tar cf $Lnx/tar/opt.tar .
echo "cd $Lnx/etc; tar cf $Lnx/tar/etc.tar ."
cd $Lnx/etc; tar cf $Lnx/tar/etc.tar .
echo "cd $Lnx/usr/local; tar cf $Lnx/tar/usrlocal.tar ."
cd $Lnx/usr/local; tar cf $Lnx/tar/usrlocal.tar .
echo "cd $Lnx/servers; tar cf $Lnx/tar/servers.tar ."
cd $Lnx/servers; tar cf $Lnx/tar/servers.tar .
#
echo "git clone git@github.com:brikahnoaa/Linux.git"
