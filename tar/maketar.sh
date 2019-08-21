#!/bin/bash
New=~/Linux
cd
tar cf $New/tar/kahn.tar .bashrc .dir_colors .minttyrc .gitconfig .k .ssh/authorized_keys .vim/ bin/
tar cf $New/tar/notes.tar notes/
cd $New
tar cf tar/opt.tar opt/
tar cf tar/etc.tar etc/
