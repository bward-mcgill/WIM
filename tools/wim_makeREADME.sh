#! /bin/bash 

# Create a detailed README in post-proc/case
# Look if inp file have been modified -> if so recreate readme else stay the same.

W3_REP_WRK=${1}
CI_REP_WRK=${2}
WIM_REP=${3}
WIM_REP_TOOLS=${4}
WIM_REP_PP=${5}
exp=${6}
year=${7}
month=${8}
day=${9}
sec=${10}
coupFreq=${11}
nts=${12}
coldstart=${13}

if [ ! -d "${WIM_REP_PP}/${exp}" ]; then
      mkdir -p "${WIM_REP_PP}/${exp}"
fi

echo "|------------Update ${exp}.README ! -------------|"

echo "# Detailled parameter of the simulation." > ${WIM_REP_PP}/${exp}/${exp}.README
echo "# Experience : ${exp}." >> ${WIM_REP_PP}/${exp}/${exp}.README
echo "# Start : ${year}-${month}-${day}-${sec}." >> ${WIM_REP_PP}/${exp}/${exp}.README
echo "# Coupling frequency : ${coupFreq}." >> ${WIM_REP_PP}/${exp}/${exp}.README
echo "# Number of timestep : ${nts}." >> ${WIM_REP_PP}/${exp}/${exp}.README
echo -e "# Last update : `date`. \n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ww3_grid---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${W3_REP_WRK}/ww3_grid_${exp}.out >> ${WIM_REP_PP}/${exp}/${exp}.README 
echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ww3_strt---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${W3_REP_WRK}/ww3_strt_${exp}.out >> ${WIM_REP_PP}/${exp}/${exp}.README
echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

#echo -e "#-------------------------------------------------ww3_prnc_ic*---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
#cat ${W3_REP_WRK}/ww3_prnc_ic1_${exp}.out >> ${WIM_REP_PP}/${exp}/${exp}.README
#echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ww3_shel---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${W3_REP_WRK}/ww3_shel_${exp}.out >> ${WIM_REP_PP}/${exp}/${exp}.README 
echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

#echo -e "#-------------------------------------------------ww3_ounf---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
#cat ${W3_REP_WRK}/ww3_ounf_${exp}.out >> ${WIM_REP_PP}/${exp}/${exp}.README 
#echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ice_in---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${CI_REP_WRK}/ice_in >> ${WIM_REP_PP}/${exp}/${exp}.README

echo '|------------Update cases.README ! -------------|'

header="Exp Start dtCoup ndt coldstart dtWW3 PRO SIC IC2VISC USECGICE IC4METHOD ICEDISP SIS IS2BACKSCAT IS2BREAK IS2CREEPB IS2ANDISB Init.Spec. dtCICE nx ny dx gridtype runtype ncat nfsd ice_data_type ice_data_conc ice_data_dist atm_data_type ocn_data_type"

dtWW3=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e 's/Maximum global time step      (s) ://p'`
PRO_WW3=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e '0,/PRO/{s/.*PRO//p}' | cut -c -1`
SIC_WW3=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e '0,/SIC/{s/.*SIC//p}' | cut -c -1`
SICVISC=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e 's/.*IC2VISC = //p' | cut -c -5`
USECGICE=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e 's/.*USECGICE =  //p' | cut -c -1`
IC4METHOD=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e 's/.*IC4METHOD=//p' | cut -c -1`
ICEDISP=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e 's/.*ICEDISP = //p' | cut -c -2`
SIS_WW3=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e '0,/SIS/{s/.*SIS//p}' | cut -c -1`
SIS2BS=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e 's/.*IS2BACKSCAT =//p' | cut -c -9`
SIS2BREAK=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e 's/.*IS2BREAK =//p' | cut -c -3`
SIS2CREEPB=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e 's/.*IS2CREEPB =//p' | cut -c -11`
SIS2ANDISB=`cat ${W3_REP_WRK}/ww3_grid_${exp}.out | sed -n -e 's/.*IS2ANDISB =//p' | cut -c -3`
spec=`cat ${W3_REP_WRK}/ww3_strt_${exp}.out | sed -n -e 's/.*Initial field ITYPE =//p'`

dtCICE=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    dt.*=//p'| cut -c -15`
nx=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    nx_global.*=//p'| cut -c -15`
ny=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ny_global.*=//p'| cut -c -15`
dx=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    dxrect.*=//p'| cut -c -15`
gridtype=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    grid_type.*=//p'| cut -c -15`
runtype=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    runtype.*=//p'| cut -c -15`
#bathy=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/   bathymetry_file.*=//p'| cut -c -15`
ncat=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ncat.*=//p'| cut -c -15`
nfsd=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    nfsd.*=//p'| cut -c -15`
ice_type=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ice_data_type.*=//p'| cut -c -15`
ice_conc=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ice_data_conc.*=//p'| cut -c -15`
ice_dist=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ice_data_dist.*=//p'| cut -c -15`
##wave_type=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    wave_spec_type.*=//p'| cut -c -14`
atm_type=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    atm_data_type.*=//p'| cut -c -15`
ocn_type=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ocn_data_type.*=//p'| cut -c -15`


if [ -z ${dtWW3} ]; then
   dtWW3='ND'
fi

if [ -z ${USECGICE} ]; then
   USECGICE='ND'
fi

if [ -z ${IC4METHOD} ]; then
   IC4METHOD='ND'
fi

if [ -z ${ICEDISP} ]; then
   ICEDISP='ND'
fi

if [ -z ${PRO_WW3} ]; then
   PRO_WW3='ND'
fi

if [ -z ${SICVISC} ]; then
   SICVISC='ND'
fi

if [ -z ${SIC_WW3} ]; then
   PRO_WW3='ND'
fi


if [ -z ${SIS_WW3} ]; then
   SIS_WW3='ND'
fi

if [ -z ${SIS2BS} ]; then
   SIS2BS='ND'
fi

if [ -z ${SIS2BREAK} ]; then
   SIS2BREAK='ND'
fi

if [ -z ${SIS2CREEPB} ]; then
   SIS2CREEPB='ND'
fi

if [ -z ${SIS2ANDISB} ]; then
   SIS2ANDISB='ND'
fi

if [ -z ${spec} ]; then
   spec='ND'
fi

if [ -z ${dtCICE} ]; then
   dtCICE='ND'
fi

if [ -z ${nx} ]; then
   nx='ND'
fi

if [ -z ${ny} ]; then
   ny='ND'
fi

params="${exp} ${year}-${month}-${day}-${sec} ${coupFreq} ${nts} ${coldstart} ${dtWW3} ${PRO_WW3} ${SIC_WW3} ${SICVISC} ${USECGICE} ${IC4METHOD} ${ICEDISP} ${SIS_WW3} ${SIS2BS} ${SIS2BREAK} ${SIS2CREEPB} ${SIS2ANDISB} ${spec} ${dtCICE} ${nx} ${ny} ${dx} ${gridtype} ${runtype} ND ${ncat} ${nfsd} ${ice_type} ${ice_conc} ${ice_dist} ${atm_type} ${ocn_type}" 

if [ ! -e ${WIM_REP}/cases.README ]; then
   echo "Wave Ice Model (WAVEWATCH III and CICE)." > ${WIM_REP}/cases.README
   echo "Summary of the parameters used in each run." >> ${WIM_REP}/cases.README
   echo "Benjamin Ward" >> ${WIM_REP}/cases.README
   echo "McGill University" >> ${WIM_REP}/cases.README
   printf '|%-14s' $header >> ${WIM_REP}/cases.README
   printf '|' $params >> ${WIM_REP}/cases.README
fi

bool_empty=`grep "|${exp}" ${WIM_REP}/cases.README`

if [ "$bool_empty" == "" ]; then
   printf '\n' >> ${WIM_REP}/cases.README
   printf '|%-14s' $params >> ${WIM_REP}/cases.README
   printf '|' >> ${WIM_REP}/cases.README
else
   sed -i "s/|${exp}.*/`printf '|%-14s' $params` | /g" ${WIM_REP}/cases.README
fi
