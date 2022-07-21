#! /bin/bash 

# Create a detailed README in post-proc/case
# Look if inp file have been modified -> if so recreate readme else stay the same.

W3_REP_INP=${1}
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

echo -e "#-------------------------------------------------ww3_grid.inp---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${W3_REP_INP}/ww3_grid_${exp}.inp >> ${WIM_REP_PP}/${exp}/${exp}.README 
echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ww3_strt.inp---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${W3_REP_INP}/ww3_strt_${exp}.inp >> ${WIM_REP_PP}/${exp}/${exp}.README
echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ww3_shel.inp---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${W3_REP_INP}/ww3_shel_${exp}.inp >> ${WIM_REP_PP}/${exp}/${exp}.README 
echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ice_in---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${CI_REP_WRK}/ice_in >> ${WIM_REP_PP}/${exp}/${exp}.README

echo '|------------Update cases.README ! -------------|'

header="Exp Start dtCoup ndt coldstart dtWW3 PRO_WW3 SIC_WW3 SIS_WW3 spec dtCICE nx ny dx gridtype runtype bathymetry_file ncat nfsd ice_data_type ice_data_conc ice_data_dist atm_data_type ocn_data_type"

dtWW3=`sed -n '8p' < ${W3_REP_INP}/ww3_grid_${exp}.inp | cut -c 3-5`
PRO_WW3=`cat ${W3_REP_INP}/ww3_grid_${exp}.inp | sed -n -e 's/.*PRO//p' | cut -c -1`
SIC_WW3=`cat ${W3_REP_INP}/ww3_grid_${exp}.inp | sed -n -e 's/.*SIC//p' | cut -c -1`
SIS_WW3=`cat ${W3_REP_INP}/ww3_grid_${exp}.inp | sed -n -e 's/.*SIS//p' | cut -c -1`
spec=`sed -n '3p' < ${W3_REP_INP}/ww3_strt_${exp}.inp`
dtCICE=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    dt.*=//p'| cut -c -15`
nx=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    nx_global.*=//p'| cut -c -15`
ny=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ny_global.*=//p'| cut -c -15`
dx=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    dxrect.*=//p'| cut -c -15`
gridtype=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    grid_type.*=//p'| cut -c -15`
runtype=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    runtype.*=//p'| cut -c -15`
bathy=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    bathymetry_file.*=//p'| cut -c -15`
ncat=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ncat.*=//p'| cut -c -15`
nfsd=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    nfsd.*=//p'| cut -c -15`
ice_type=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ice_data_type.*=//p'| cut -c -15`
ice_conc=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ice_data_conc.*=//p'| cut -c -15`
ice_dist=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ice_data_dist.*=//p'| cut -c -15`
#wave_type=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    wave_spec_type.*=//p'| cut -c -14`
atm_type=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    atm_data_type.*=//p'| cut -c -15`
ocn_type=`cat ${CI_REP_WRK}/ice_in | sed -n -e 's/    ocn_data_type.*=//p'| cut -c -15`

params="${exp} ${year}-${month}-${day}-${sec} ${coupFreq} ${nts} ${coldstart} ${dtWW3} ${PRO_WW3} ${SIC_WW3} ${SIS_WW3} ${spec} ${dtCICE} ${nx} ${ny} ${dx} ${gridtype} ${runtype} ${bathy} ${ncat} ${nfsd} ${ice_type} ${ice_conc} ${ice_dist} ${atm_type} ${ocn_type}" 

if [ ! -e ${WIM_REP}/cases.README ]; then
   echo "Summary of the parameter used in each run." > ${WIM_REP}/cases.README
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
