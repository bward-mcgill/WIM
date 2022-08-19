#! /bin/bash

. ${HOME}/wim/wim_launcher.cfg

#Constants
W3_REP_OUT=${W3_REP_MOD}/out/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
WIM_REP_PP=${WIM_REP}/post-proc
WIM_REP_TOOLS=${WIM_REP}/tools
REP_CDO="/opt/cdo/bin/"

#Set default value, if output variables are undefined.
if [ -z ${year_init_out} ];
then
    year_init_out=${year_init}
fi

if [ -z ${year_init_out} ];
then
    month_init_out=${month_init}
fi

if [ -z ${year_init_out} ];
then
    day_init_out=${day_init}
fi

if [ -z ${year_init_out} ];
then
    sec_init_out=${sec_init}
fi

if [ -z ${ndt_out} ];
then
    ndt_out=${ndt}
fi

if [ -z ${dt_out} ];
then
    dt_out=${dt}
fi

#Change name of longitude and latitude variable (required for xarray):
#if ${bool_Coupled}; then
#   list_files=`ls ${W3_REP_OUT}/ww3.????????.nc`
#else
#   list_files=`ls ${W3_REP_OUT}/ww3.????????????.nc`
#fi
#
#for file in ${list_files}
#do
#    name=`echo ${file} | rev | cut -c 4- | rev`
#    ${REP_CDO}/cdo chname,latitude,lat,longitude,lon ${file} ${file}_temp>/dev/null 2>&1 ; rm -f ${file} ; mv ${file}_temp ${file}
#done


echo '|------------Post-Processing-------------|'
if [ ! -z ${ice_init} ] && [ ! -z ${rep_ice_init} ] && [ ${bool_Coupled} == "false" ] ;
then
    ${WIM_REP_TOOLS}/wim_plotWaveIce.py ${exp} ${ndt_out} ${dt} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} ${CI_REP_OUT}/history ${WIM_REP_PP}/${exp} ${default_exp} ${dt_out} ${bool_Coupled} --iceIc ${ice_init} --repIceIc ${rep_ice_init}
else
   ${WIM_REP_TOOLS}/wim_plotWaveIce.py ${exp} ${ndt_out} ${dt} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} ${CI_REP_OUT}/history ${WIM_REP_PP}/${exp} ${default_exp} ${dt_out} ${bool_Coupled}
fi


