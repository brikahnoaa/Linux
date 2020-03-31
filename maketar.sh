#!/bin/bash
Lnx=~/Linux
Kahn=".bash* .dir_colors .minttyrc .gitconfig .k .ssh/authorized_keys .vim bin"
cd
echo "rm $Lnx/tar/*.tar"
rm $Lnx/tar/*.tar
echo "tar cf $Lnx/tar/kahn.tar $Kahn"
tar cf $Lnx/tar/kahn.tar $Kahn
echo "tar cf $Lnx/tar/notes.tar notes"
tar cf $Lnx/tar/notes.tar notes
echo "cd $Lnx/opt; tar cf $Lnx/tar/opt.tar ."
cd $Lnx/opt; tar cf $Lnx/tar/opt.tar .
echo "cd $Lnx/etc; tar cf $Lnx/tar/etc.tar ."
cd $Lnx/etc; tar cf $Lnx/tar/etc.tar .
echo "cd $Lnx/usr/local; tar cf $Lnx/tar/usrlocal.tar ."
cd $Lnx/usr/local; tar cf $Lnx/tar/usrlocal.tar .
echo "cd $Lnx/servers; tar cf $Lnx/tar/servers.tar ."
cd $Lnx/servers; tar cf $Lnx/tar/servers.tar .
