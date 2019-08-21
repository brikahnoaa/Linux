#!/bin/bash
# trim - keep Last (3) backup sets

Last=3
Size=3000

Name=$( basename $0 )
Temp=/tmp/$Name

if [[ "$1" == [1-9] ]]; then Last=$1; fi

# exit if there is enough space free
if df -B1G /data/PCbackup/ | awk "END{if (\$4 < $Size) exit 1}"; then 
  echo no trim above $Size MB
  df -h /data0
  exit
fi

rm -f $Temp
for i in /data/PCbackup/*; do
  ls -td $i/*/Ba* 2> /dev/null | tail -n+$(( $Last + 1 )) >> $Temp
done


if [[ -s $Temp ]]; then
  echo "Trim: removing older backup sets (keeping last $Last)"
  df -h /data
  cat $Temp | while read i; do
    echo " = $i"
    /bin/rm -r "$i"
  done
  df -h /data
fi

