#! /bin/bash 

# Create a detailed README in post-proc/case
# Look if inp file have been modified -> if so recreate readme else stay the same.

WIM_REP=${1}
. ${WIM_REP}/wim_launcher.cfg

#Constants
W3_REP_BIN=${W3_REP_MOD}/bin
W3_REP_INP=${W3_REP_MOD}/inp/${exp}
W3_REP_WRK=${W3_REP_MOD}/work/${exp}
W3_REP_OUT=${W3_REP_MOD}/out/${exp}

CI_REP_WRK=${CI_REP_MOD}/work/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
CI_REP_RST=${CI_REP_OUT}/restart

WIM_REP_PP=${WIM_REP}/post-proc
WIM_REP_TOOLS=${WIM_REP}/tools


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
cat ${W3_REP_INP}/ww3_grid_${exp}.inp >> ${WIM_REP_PP}/${exp}/${exp}.README 
echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ww3_strt---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${W3_REP_INP}/ww3_strt_${exp}.inp >> ${WIM_REP_PP}/${exp}/${exp}.README
echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

#echo -e "#-------------------------------------------------ww3_prnc_ic*---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
#cat ${W3_REP_WRK}/ww3_prnc_ic1_${exp}.out >> ${WIM_REP_PP}/${exp}/${exp}.README
#echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ww3_shel---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${W3_REP_INP}/ww3_shel_${exp}.inp >> ${WIM_REP_PP}/${exp}/${exp}.README 
echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

#echo -e "#-------------------------------------------------ww3_ounf---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
#cat ${W3_REP_WRK}/ww3_ounf_${exp}.out >> ${WIM_REP_PP}/${exp}/${exp}.README 
#echo -e "\n" >> ${WIM_REP_PP}/${exp}/${exp}.README

echo -e "#-------------------------------------------------ice_in---------------------------------------------------# \n" >> ${WIM_REP_PP}/${exp}/${exp}.README
cat ${CI_REP_WRK}/ice_in >> ${WIM_REP_PP}/${exp}/${exp}.README

echo '|------------Update cases.README ! -------------|'

header="exp year_init month_init day_init sec_init dtCoup ndtCoup description"

echo "Enter a brief description of the case: "
read -r description

if [ "$description" == "" ]; then
   description='none'
fi

params="${exp} ${year_init} ${month_init} ${day_init} ${sec_init} ${dtCoup}${dtCoup_u} ${ndtCoup}" 

if [ ! -e ${WIM_REP}/cases.README ]; then
   echo "Wave Ice Model (WAVEWATCH III and CICE)." > ${WIM_REP}/cases.README
   echo "Summary of the parameters used in each run." >> ${WIM_REP}/cases.README
   echo "Benjamin Ward" >> ${WIM_REP}/cases.README
   echo "McGill University" >> ${WIM_REP}/cases.README
   printf '|%-14s' $header >> ${WIM_REP}/cases.README
#   printf '|' $params >> ${WIM_REP}/cases.README
fi

bool_empty=`grep "|${exp}" ${WIM_REP}/cases.README`

if [ "$bool_empty" == "" ]; then
   printf '\n' >> ${WIM_REP}/cases.README
   printf '|%-14s' $params >> ${WIM_REP}/cases.README
   printf '|' >> ${WIM_REP}/cases.README
   printf "${description}" >> ${WIM_REP}/cases.README
else
   sed -i "s/|${exp}.*/`printf '|%-14s' $params` | /g" ${WIM_REP}/cases.README
   printf "${description}" >> ${WIM_REP}/cases.README
fi
