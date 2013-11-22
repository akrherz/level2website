#set echo
set nexrad=$1

cd /chinook/nexrd2/raw/$1

ls -l ${1}* | awk '{print $5 " " $9}' > dir2.list
cp dir2.list dir.list
rm -f dir2.list

#END