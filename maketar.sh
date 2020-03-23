#!/bin/bash
New=~/Linux
Kahn=".bash* .dir_colors .minttyrc .gitconfig .k .ssh/authorized_keys .vim"
cd
echo "rm $New/tar/*.tar"
rm $New/tar/*.tar
echo "tar cf $New/tar/kahn.tar $Kahn"
tar cf $New/tar/kahn.tar $Kahn
echo "tar cf $New/tar/notes.tar notes"
tar cf $New/tar/notes.tar notes
echo "cd $New/opt; tar cf $New/tar/opt.tar ."
cd $New/opt; tar cf $New/tar/opt.tar .
echo "cd $New/etc; tar cf $New/tar/etc.tar ."
cd $New/etc; tar cf $New/tar/etc.tar .
