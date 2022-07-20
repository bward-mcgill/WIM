#! /bin/bash 

# Create a detailed README in post-proc/case
# Look if inp file have been modified -> if so recreate readme else stay the same.

W3_REP_INP=${1}
CI_REP_WRK=${2}
WIM_REP=${HOME}/wim
WIM_REP_TOOLS=${3}
WIM_REP_PP=${4}
exp=${5}
year=${6}
month=${7}
day=${8}
sec=${9}
coupFreq=${10}
nts=${11}

#w3_list_src=`ls ${W3_REP_INP}/*.inp`
#ci_list_src=`ls ${CI_REP_WRK}/ice_in`
#list_src="${w3_list_src} ${ci_list_src}"

#rm -f ${WIM_REP_TOOLS}/checkMD4Readme.txt

#for file in $list_src
#do
#   md5sum $file >> ${WIM_REP_TOOLS}/checkMD4Readme.txt 
#done

#if ! $(cmp -s "${WIM_REP_TOOLS}/MD4Readme.txt" "${WIM_REP_TOOLS}/checkMD4Readme.txt"); then
echo '|------------Make run => update README ! -------------|'
#   rm -f ${WIM_REP_TOOLS}/MD4Readme.txt
#
#   for file in $list_src
#   do
#      md5sum $file >> ${WIM_REP_TOOLS}/MD4Readme.txt 
#   done

   echo "# Detailled parameter of the simulation." > ${WIM_REP_PP}/${exp}.README
   echo "# Experience : ${exp}." >> ${WIM_REP_PP}/${exp}.README
   echo "# Start : ${year}-${month}-${day}-${sec}." >> ${WIM_REP_PP}/${exp}.README
   echo "# Coupling frequency : ${coupFreq}." >> ${WIM_REP_PP}/${exp}.README
   echo "# Number of timestep : ${nts}." >> ${WIM_REP_PP}/${exp}.README
   echo -e "# Last update : `date`. \n" >> ${WIM_REP_PP}/${exp}.README

#  echo "#-------------------------------------------------wim_launcher.cfg---------------------------------------------------#" >> ${WIM_REP_PP}/${exp}.README

#   cat ${WIM_REP}/wim_launcher.cfg >> ${WIM_REP_PP}/${exp}.README

   echo -e "#-------------------------------------------------ww3_grid.inp---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}.README

   cat ${W3_REP_INP}/ww3_grid_${exp}.inp >> ${WIM_REP_PP}/${exp}.README
 
   echo -e "\n" >> ${WIM_REP_PP}/${exp}.README

   echo -e "#-------------------------------------------------ww3_strt.inp---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}.README

   cat ${W3_REP_INP}/ww3_strt_${exp}.inp >> ${WIM_REP_PP}/${exp}.README
 
   echo -e "\n" >> ${WIM_REP_PP}/${exp}.README

   echo -e "#-------------------------------------------------ww3_shel.inp---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}.README

   cat ${W3_REP_INP}/ww3_shel_${exp}.inp >> ${WIM_REP_PP}/${exp}.README
 
   echo -e "\n" >> ${WIM_REP_PP}/${exp}.README

   echo -e "#-------------------------------------------------ice_in---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}.README

   cat ${CI_REP_WRK}/ice_in >> ${WIM_REP_PP}/${exp}.README
 
#else
#   echo 'Input files didnt change, dont update readme'
#fi

# Create a summary of the readme in cases.README (just one line).

# If detailled readme as been changed -> remove line and create a new one. 

# Else 
