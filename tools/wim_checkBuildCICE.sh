#! /bin/bash

#If case exist, but source code has changed, 
#or
#if executable is not there
#then
#need to recompile.

CI_REP_MOD=${1}
WIM_REP_TOOLS=${2}
CI_REP_WRK=${3}
CI_REP_OUT=${4}

ci_list_src=`find ${CI_REP_MOD}/cicecore/ -name "*.F90"` 
ip_list_src=`find ${CI_REP_MOD}/icepack/columnphysics/ -name "*.F90"`
ci_list_src="${ci_list_src} ${ip_list_src}"

rm -f ${CI_REP_WRK}/checkListMD5_CICE.txt

for file in $ci_list_src
do
   md5sum $file >> ${CI_REP_WRK}/checkListMD5_CICE.txt 
done

if [ ! -e ${CI_REP_WRK}/listMD5_CICE.txt ]; then
   echo '|------------CICE first build-------------|'
   cd ${CI_REP_WRK}
   csh ${CI_REP_WRK}/cice.build
   for file in $ci_list_src
   do
      md5sum $file >> ${CI_REP_WRK}/listMD5_CICE.txt 
   done
elif ! $(cmp -s "${CI_REP_WRK}/listMD5_CICE.txt" "${CI_REP_WRK}/checkListMD5_CICE.txt"); then
   echo '|------------CICE source code has changed build again.-------------|'
   cd ${CI_REP_WRK}
   csh ${CI_REP_WRK}/cice.build
   cat ${CI_REP_WRK}/checkListMD5_CICE.txt > ${CI_REP_WRK}/listMD5_CICE.txt
elif [ ! -e ${CI_REP_OUT}/cice ] ; then
   echo '|------------CICE Executable missing, build again !-------------|'
   cd ${CI_REP_WRK}
   csh ${CI_REP_WRK}/cice.build
else
   echo "Everything is in order, no need to recompile"
fi

