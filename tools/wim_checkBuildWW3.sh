#! /bin/bash

#If source code changed, 
#or
#if work directory don't exist,
#or
#if executable are not there,
#need to recompile.

W3_REP_MOD=${1}
WIM_REP_TOOLS=${2}
W3_REP_WRK=${3}
exp=${4}

if [ ! -d ${W3_REP_WRK} ]; then
   mkdir -p ${W3_REP_WRK}
fi

i=1
for arg in $@
do
if [ $i -le 4 ];then
   ((i=i+1))
   continue
else
    w3listProg="$w3listProg $arg"
fi
done

w3_list_src=`ls ${W3_REP_MOD}/ftn/*.ftn`
rm -f $W3_REP_WRK/checkListMD5_WW3.txt

for file in $w3_list_src
do
   md5sum $file >> ${W3_REP_WRK}/checkListMD5_WW3.txt 
done

if [ ! -e ${W3_REP_WRK}/listMD5_WW3.txt ]; then
   echo '|------------WW3 first build-------------|'
   bash ${WIM_REP_TOOLS}/wim_buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
   for file in $w3_list_src
   do
      md5sum $file >> ${W3_REP_WRK}/listMD5_WW3.txt 
   done
elif ! $(cmp -s "${W3_REP_WRK}/listMD5_WW3.txt" "${W3_REP_WRK}/checkListMD5_WW3.txt"); then
   echo '|------------WW3 source code has changed, build again.-------------|'
   bash ${WIM_REP_TOOLS}/wim_buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
   cat ${W3_REP_WRK}/checkListMD5_WW3.txt > ${W3_REP_WRK}/listMD5_WW3.txt
elif [ ! -d ${W3_REP_WRK} ]; then
   echo '|------------Work directory dont exist, build again.-------------|'
   bash ${WIM_REP_TOOLS}/wim_buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
   cat ${W3_REP_WRK}/checkListMD5_WW3.txt > ${W3_REP_WRK}/listMD5_WW3.txt
elif [ ! "$(ls -A ${W3_REP_MOD}/exe)" ] || [ ! "$(ls -A ${W3_REP_MOD}/mod)" ] || [ ! "$(ls -A ${W3_REP_MOD}/obj)" ]; then
   echo '|------------WW3 Executable missing, build again.-------------|'
   bash ${WIM_REP_TOOLS}/wim_buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
   cat ${W3_REP_WRK}/checkListMD5_WW3.txt > ${W3_REP_WRK}/listMD5_WW3.txt
fi

