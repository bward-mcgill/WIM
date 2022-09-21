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

if [ -z ${ndtOutPP} ];
then
    ndtOutPP=${ndtCoup}
fi

if [ -z ${dtOutPP} ];
then
    dtOutPP=${dtCoup}
fi


echo '|------------Post-Processing-------------|'

if [ ! -z ${ice_init} ] && [ ! -z ${rep_ice_init} ] && [ ${bool_Coupled} == "false" ] ;
then
    ${WIM_REP_TOOLS}/wim_plotWaveIce.py ${exp} ${ndtOutPP} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutPP} ${dtOutPP_u} ${bool_CoupledWW3} ${bool_CoupledCICE} --iceIc ${ice_init} --repIceIc ${rep_ice_init}
else
   ${WIM_REP_TOOLS}/wim_plotWaveIce.py ${exp} ${ndtOutPP} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutPP} ${dtOutPP_u} ${bool_CoupledWW3} ${bool_CoupledCICE}
#   ${WIM_REP_TOOLS}/wim_plotChangeFSD.py ${exp} ${ndtOutPP} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutPP} ${dtOutPP_u} ${bool_CoupledWW3} ${bool_CoupledCICE}

fi

