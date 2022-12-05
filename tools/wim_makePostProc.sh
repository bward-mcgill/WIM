#! /bin/bash

. ${HOME}/wim/wim_launcher.cfg

#Constants
W3_REP_OUT=${W3_REP_MOD}/out/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
WIM_REP_PP=${WIM_REP}/post-proc
WIM_REP_TOOLS=${WIM_REP}/tools

if ${bool_CoupledWW3} && ${bool_CoupledCICE} ;then 
   bool_Coupled=true
elif ! ${bool_CoupledWW3} && ! ${bool_CoupledCICE} ;then
   echo "You can't do uncoupled simulation of both CICE and WW3 at the same time"
   exit 1
else
   bool_Coupled=false
fi

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
if [ -z ${ndtOutH} ];
then
    ndtOutPP=${ndtCoup}
fi
if [ -z ${dtOutH} ];
then
    dtOutPP=${dtCoup}
fi

echo '|------------Post-Processing-------------|'

if [ ! -z ${ice_init} ] && [ ! -z ${rep_ice_init} ] && [ ${bool_Coupled} == "false" ] ;
then
    ${WIM_REP_TOOLS}/wim_plotWaveIce.py ${pp_prod} ${exp} ${ndtOutPP} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutPP} ${dtOutPP_u} ${bool_CoupledWW3} ${bool_CoupledCICE} --iceIc ${ice_init} --repIceIc ${rep_ice_init}
elif [ ${pp_prod} == 'hourly' ]; then
   echo "Plot hourly field."
   ${WIM_REP_TOOLS}/wim_plotWaveIce.py ${pp_prod} ${exp} ${ndtOutH} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutH} ${dtOutH_u} ${bool_CoupledWW3} ${bool_CoupledCICE}
#   ${WIM_REP_TOOLS}/wim_plotChangeFSD.py ${exp} ${ndtOutPP} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutPP} ${dtOutPP_u} ${bool_CoupledWW3} ${bool_CoupledCICE}
elif [ ${pp_prod} == 'avg' ]; then
   #${WIM_REP_TOOLS}/wim_outAvg.py
   echo "Create and plot avg field."
   if [ ! -d "${WIM_REP_PP}/${exp}/avg" ]; then
      mkdir "${WIM_REP_PP}/${exp}/avg"
   fi
#   rm -rf ${WIM_REP_PP}/${exp}/avg/*
#   ${WIM_REP_TOOLS}/wim_avgOut.py ${exp} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${ndtOutA} ${dtOutA} ${dtOutA_u} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}/avg"
   ${WIM_REP_TOOLS}/wim_plotWaveIce.py ${pp_prod} ${exp} ${ndtOutA} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${WIM_REP_PP}/${exp}/avg" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutA} ${dtOutA_u} ${bool_CoupledWW3} ${bool_CoupledCICE}
else
   echo 'Unknown post-proc option.'
   exit 1
fi

