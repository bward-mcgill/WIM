#! /bin/bash

. ${HOME}/wim/wim_launcher.cfg
source ${HOME}/miniconda3/bin/activate wim
#conda deactivate

#Constants
W3_REP_OUT=${W3_REP_MOD}/out/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
WIM_REP_PP=${WIM_REP}/post-proc
WIM_REP_TOOLS=${WIM_REP}/tools

#Define stuff
if ${bool_CoupledWW3} && ${bool_CoupledCICE} ;then 
   bool_Coupled=true
elif ! ${bool_CoupledWW3} && ! ${bool_CoupledCICE} ;then
   echo "You can't do uncoupled simulation of both CICE and WW3 at the same time"
   exit 1
else
   bool_Coupled=false
fi

#Create required folders
if [ ! -d "${WIM_REP_PP}/${exp}/avg" ]; then
      mkdir -p "${WIM_REP_PP}/${exp}/avg"
fi

if [ ${bool_addVector} == "true" ] && [ ! -d "${WIM_REP_PP}/${exp}/interp" ]; then
    mkdir "${WIM_REP_PP}/${exp}/interp"
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

#Make plot (avg or hourly) + (normal or anomalies)
echo '|------------Post-Processing-------------|'
if [ ! -z ${ice_init} ] && [ ! -z ${rep_ice_init} ] && [ ${bool_Coupled} == "false" ] ;
then
    ${WIM_REP_TOOLS}/wim_plotWaveIce.py ${pp_prod} ${exp} ${ndtOutPP} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutPP} ${dtOutPP_u} ${bool_CoupledWW3} ${bool_CoupledCICE} ${bool_addContour} ${contourVar} ${bool_addVector} ${vectorVars} --iceIc ${ice_init} --repIceIc ${rep_ice_init} ${pp_listVar}
elif [ ${pp_prod} == 'hourly' ]; then
   echo "Plot hourly field."
   if [ ${pp_type} == 'case' ]; then
   	${WIM_REP_TOOLS}/wim_plotWaveIce.py ${pp_prod} ${exp} ${ndtOutH} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutH} ${dtOutH_u} ${bool_CoupledWW3} ${bool_CoupledCICE} ${bool_addContour} ${contourVar} ${bool_addVector} ${vectorVars} ${pp_listVar}
   elif [ ${pp_type} == 'anom' ]; then
        echo "TEST anom hourly"
   fi
#   ${WIM_REP_TOOLS}/wim_plotChangeFSD.py ${exp} ${ndtOutPP} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutPP} ${dtOutPP_u} ${bool_CoupledWW3} ${bool_CoupledCICE}
elif [ ${pp_prod} == 'avg' ]; then
   echo "Create and plot avg field."
   if [ ${pp_type} == 'case' ]; then
       if [ ! -d "${WIM_REP_PP}/${exp}/avg" ]; then
          mkdir -p "${WIM_REP_PP}/${exp}/avg"
       fi
       ${WIM_REP_TOOLS}/wim_avgOut.py ${exp} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${ndtOutA} ${dtOutA} ${dtOutA_u} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}/avg" ${couplingVar} ${listVarOutCICE}
       ${WIM_REP_TOOLS}/wim_plotWaveIce.py ${pp_prod} ${exp} ${ndtOutA} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} "${WIM_REP_PP}/${exp}/avg" "${WIM_REP_PP}/${exp}/avg" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutA} ${dtOutA_u} ${bool_CoupledWW3} ${bool_CoupledCICE} ${bool_addContour} ${contourVar} ${bool_addVector} ${vectorVars} ${pp_region} ${pp_listVar}
   elif [ ${pp_type} == 'anom' ]; then
	echo "Write the name of an other case to compute anomalies"
        read -r expAnom
        w3_repOut_anom=${W3_REP_MOD}/out/${expAnom}
        ci_repOut_anom=${CI_REP_MOD}/out/${expAnom}

        if [ ! -d ${w3_repOut_anom} ] || [ ! -d ${ci_repOut_anom} ]; then
	   echo "This other case don't exist"
           exit
        fi

        if [ ! -d "${WIM_REP_PP}/${expAnom}/avg" ]; then
          mkdir -p "${WIM_REP_PP}/${expAnom}/avg"
        fi
         ${WIM_REP_TOOLS}/wim_avgOut.py ${exp} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${ndtOutA} ${dtOutA} ${dtOutA_u} ${W3_REP_OUT} "${CI_REP_OUT}/history" "${WIM_REP_PP}/${exp}/avg" ${couplingVar} ${listVarOutCICE}
         ${WIM_REP_TOOLS}/wim_avgOut.py ${expAnom} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} ${ndtOutA} ${dtOutA} ${dtOutA_u} ${w3_repOut_anom} "${ci_repOut_anom}/history" "${WIM_REP_PP}/${expAnom}/avg" ${couplingVar} ${listVarOutCICE}
         ${WIM_REP_TOOLS}/wim_plotAnom.py ${pp_prod} ${exp} ${expAnom} ${ndtOutA} ${dtCICE} ${year_init_out} ${month_init_out} ${day_init_out} ${sec_init_out} "${WIM_REP_PP}/${exp}/avg" "${WIM_REP_PP}/${exp}/avg" "${WIM_REP_PP}/${expAnom}/avg" "${WIM_REP_PP}/${expAnom}/avg" "${WIM_REP_PP}/${exp}" ${default_exp} ${dtOutA} ${dtOutA_u} ${bool_CoupledWW3} ${bool_CoupledCICE} ${bool_addContour} ${contourVar} ${bool_addVector} ${vectorVars} ${pp_region} ${pp_listVar}
   fi
else
   echo 'Unknown post-proc option.'
   exit 1
fi
