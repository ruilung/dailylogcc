#/bin/bash
if [[ $# -ne 2 ]]; then
 echo "ERROR!!! Need 2 paramenter"
 echo "i.g. dailylogcc /log 15"
 echo "first one is log folder, second is clean gzip file days ago"
 exit 1
fi


v_logfolder=$1
v_ago=$2

find ${v_logfolder} -name *.log -mtime +1 | xargs -r gzip
find ${v_logfolder} -name *.log.gz -mtime +${v_ago} | xargs -r rm -rf
