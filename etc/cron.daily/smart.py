#!/bin/bash
# v3 smartctl disk check
# v4 set RAID in .conf
# v5 use different forms of smartctl, no .conf
Name=$( basename $0 )
#if [ -r $Name.conf ]; then . $Name.conf; else echo no $Name.conf; exit 1; fi

# ac: smartctl -A -d 3ware,1 /dev/twl0 # 9750 3w_sas
# note: megaraid sees all disks on each device e.g. sda sdb
# b3: cr: smartctl -A -d megaraid,9 /dev/sda # 9363 9269 megaraid_sas
# e2:  # 9361 megaraid_sas
# ve: smartctl -A -d 3ware,0 /dev/twa0 # 9650 9690 3w_9xxx
# ve: smartctl -A -d 3ware,0 /dev/twa1 # 9650 9690 3w_9xxx

# ac: LSI 9750-8i at 0:0:0:0: on /dev/sdb
# ac: driver 3w-sas rhel7.7
# b3: LSI MR9271-4i at 0:2:0:0: on /dev/sda
# b3: LSI MR9271-4i at 0:2:1:0: on /dev/sdb
# cr: AVAGO MR9363-4i at 0:2:0:0: on /dev/sda
# cr: AVAGO MR9363-4i at 0:2:1:0: on /dev/sdb
# e2: AVAGO MR9361-8i at 0:2:0:0: on /dev/sda
# e2: driver megaraid_sas rhel6.10
# ve: AMCC 9690SA-8I at 8:0:0:0: on /dev/sdb
# ve: AMCC 9650SE-12M at 9:0:0:0: on /dev/sdc
# ve: driver 3w_9xxx rhel6.10

# reporting
# 5=Reallocated_Sector_Ct 9=Power_On_Hours 10=Spin_Retry_Count
# 197=Current_Pending_Sector 198=Offline_Uncorrectable
awkS='
/^  5 /{if ($10 > 0) printf "%d=%s ", $10, $2 }
/^ 10 /{if ($10 > 0) printf "%d=%s ", $10, $2 }
/^194 /{if ($10 > 36) printf "%d=%s ", $10, $2 }
/^197 /{if ($10 > 0) printf "%d=%s ", $10, $2 }
/^198 /{if ($10 > 0) printf "%d=%s ", $10, $2 }
/^  9 /{x=$10/24/365; if (x > 4) printf "(%1.1f years) ", x }
'

# quickie
if [[ -n "$1" ]]; then
  echo "== $1"
  out=$( smartctl -d sat -A $1 | awk "$awkS" )
  if [[ -n $out ]]; then
    echo "  SATA disk $1"
    echo "$out"
  fi
  exit
fi
  

# figure out disks
# smartctl --scan for AT disks, dmesg scsi# for raid controllers
# could use lsblk

echo == smart: looking for sector errs on $( hostname )
sata=$( smartctl --scan-open | awk '/ sat /{print $1}')
if [[ -n "$sata" ]]; then echo SATA $sata; fi

## non-raid
for i in $sata; do
  out=$( smartctl -d sat -A $i | awk "$awkS" )
  if [[ -n $out ]]; then
    echo "  SATA disk $i"
    echo "$out"
  fi
done

## raid
tmp=/tmp/$Name.dmesg
# rhel7 dmesg leads with microtime stamp, strip that off
dmesg | sed 's/^\[ *[0-9\.]*\] //' > $tmp
cnt=0
egrep 'Direct-Access *(AMCC|LSI|AVAGO)' $tmp | \
  while read x scsi x vendor card x; do 
    if [ -n "$scsi" ]; then
      # get device using scsi tag, e.g  sd 8:0:0:0: [sdb] Attached SCSI disk
      dev=/dev/$(grep $scsi $tmp | sed -n '/^sd/{s/.*\[\(sd.\)\].*/\1/;p;q}')
      echo "$vendor $card at $scsi on $dev"
      vendors[$(( ++cnt ))]=$vendor
      cards[$cnt]=$card
      scsis[$cnt]=$scsi
      devs[$cnt]=$dev
    fi
  done
# scan raid
if [[ $cnt -gt 0 ]]; then 
  # for each
  for i in {1..$cnt}; do
    case ${cards[$i]} in
      *96[69]0*) driver=3ware; device=/dev/twa$i;;
      *9750*) driver=3ware; device=/dev/twl0;;
      *9[23]6*) driver=megaraid; device=${devs[$i]};;
    esac
    for j in {0..24}; do
      out=$( smartctl -d $driver,$j -A $device | awk "$awkS" )
      if [[ -n "$out" ]]; then
        echo "  raid disk $driver,$j $device"
        echo "$out"
      fi
    done
  done
fi
rm $tmp
