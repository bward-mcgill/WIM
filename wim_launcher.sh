#! /bin/bash
# --------------------------------------------------------------------------- #
# wim_launcher.sh : Launch an existing case. Run CICE and WW3 sequentially    #
#                   and exchange variables in the coupled WIM framework       #
#                                                                             #
# use  : ./wim_launcher.sh                                                    #
#                                                                             #
#                                                      Benjamin Ward          #
#                                                      June 2022              #
#                                                      McGill University      #
# --------------------------------------------------------------------------- #

#Source config file
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
CI_REP_INP=${CI_REP_MOD}/inp/CICE_data

WIM_REP_PP=${WIM_REP}/post-proc
WIM_REP_TOOLS=${WIM_REP}/tools


export WWATCH3_NETCDF=NC4
export NETCDF_CONFIG="/usr/bin/nc-config"

#if either bool_CoupledCICE or bool_CoupledWW3 are false, only one timestep is runned : it's an uncoupled simulation.
if ${bool_CoupledWW3} && ${bool_CoupledCICE} ;then 
   bool_Coupled=true
   ndtCICE=1
   dtCICEOut=1
   dtCICEOut_u=h
   ndtCICE_u=1
   echo "Coupled simulation."
elif ! ${bool_CoupledWW3} && ! ${bool_CoupledCICE} ;then
   echo "Error, you can't do an uncoupled simulation of both WW3 and CICE at the same time"
   exit 1
else
   bool_Coupled=false
   if [ ${dtCoup} -ne 0  ] || [ ${ndtCoup} -ne 0 ]; then
      echo "Coupling frequency and number of timestep need to be set to 0 for uncoupled simulation !"
      exit 1 
   fi
   if ! ${bool_CoupledWW3}; then
         echo "Uncoupled WW3 simulation."
         ndtCICE=1
         ndtCICE_u=1
         dtCICEOut=1
         dtCICEOut_u=h
   else
       echo "Uncoupled CICE simulation".
   fi
fi

if [ ${dtCICE_u} == 's' ]; then
    ((dtCICE=dtCICE*1))
elif [ ${dtCICE_u} == 'h' ]; then
    ((dtCICE=dtCICE*3600))
elif [ ${dtCICE_u} == 'd' ]; then
    ((dtCICE=dtCICE*3600*24))
else
     echo "dtCICE_u must be s, h or d"
     exit
fi

if [ ${dtCoup_u} == 's' ]; then
    ((dtCoup=dtCoup*1))
elif [ ${dtCoup_u} == 'h' ]; then
    ((dtCoup=dtCoup*3600))
elif [ ${dtCoup_u} == 'd' ]; then
    ((dtCoup=dtCoup*3600*24))
else
     echo "dtCoup_u must be s, h or d"
     exit
fi


if [ ${default_exp} == "wimgx3" ]; then
    grid="gx3"
elif [ ${default_exp} == "wim2p5" ]; then
    grid="g2p5"
elif [ ${default_exp} == "wimgx1" ]; then
    grid="gx1"
elif [ ${default_exp} == "wimtx1" ]; then
    grid="tx1"
else
   echo "Unknown grid"
   exit
fi

#rm -rf ${CI_REP_MOD}/caselist*
#rm -rf ${CI_REP_OUT}/cice.runlog*
#rm -rf ${W3_REP_INP}/ice_forcing*.nc

i=0
##----------------------Run the WIM-------------------#
listDateTs=`${WIM_REP_TOOLS}/wim_dateTime.py printListTs ${year_init} ${month_init} ${day_init} ${sec_init} ${dtCoup} ${ndtCoup}`

for dateTimeStep in ${listDateTs}
do
   timerStart=$SECONDS

   cd ${CI_REP_WRK}
   yyyy=`echo ${dateTimeStep} | cut -c -4`
   mm=`echo ${dateTimeStep} | cut -c 5-6` 
   dd=`echo ${dateTimeStep} | cut -c 7-8`
   ts=`echo ${dateTimeStep} | cut -c 9-`
   yyyy_int=$(echo $yyyy | sed 's/^0*//')
   mm_int=$(echo $mm | sed 's/^0*//')
   dd_int=$(echo $dd | sed 's/^0*//')

   # At some point need to remove ww3 restart file because they take to much place.
#   if [ $dd_int == "28" ]; then
#	old_mm=${mm}
#   fi
#
#   if [ ${mm} != ${month_init} ] && [ $dd_int == 2 ] && [ $bool_coupled ]; then
#	rm -rf ${W3_REP_WRK}/restart_????-${old_mm}-*.ww3
#	echo "Old ww3 restart file removed"
#   fi
#
   if [ $ts -eq "00000" ]; then
      ts_int=0
   else
      ts_int=$(echo $ts | sed 's/^0*//')
   fi
   ((tsp1_int=ts_int+dtCICE))
   dateTs=`${WIM_REP_TOOLS}/wim_dateTime.py printTs ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} 'CICE'`
   dateTsp1=`${WIM_REP_TOOLS}/wim_dateTime.py printTs ${yyyy_int} ${mm_int} ${dd_int} ${tsp1_int} 'CICE'`
   dateTsp1_w3=`echo "${dateTs//-}" | cut -c -8`
   dateTs_w3=`echo "${dateTsp1//-}" | cut -c -8`

   echo "Timestep $i : $dateTs"

   echo '|------------Run CICE-------------|'
   if ${bool_coldStart}; then
      # In the case of a cold start, timestep 0 : create a wave field and initiate FSD from internal.
      if [ $i -eq 0 ]; then
        echo "Cold start !"
        if ${tr_fsd}; then
            #Initiate FSD.
            ice_ic=${ice_ic_initFSD}
            wave_spec_file='unknown_wave_spec_file'
            wave_spec_type="none"
            CST_NDT=1
            CST_FREQ='h'
            CST_NDT_U=1
            bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${tr_fsd} ${CST_NDT} ${CST_NDT_U} ${CST_FREQ} ${CI_REP_WRK} ${couplingVar} ${listVarOutCICE}
            timerStartCI=$SECONDS
            ./cice.submit
            timerEndCI=$(( $SECONDS - ${timerStartCI} ))
            rm -f ${CI_REP_RST}/iced.fsd.nc ; ${REP_CDO}/cdo select,name=fsd001,fsd002,fsd003,fsd004,fsd005,fsd006,fsd007,fsd008,fsd009,fsd010,fsd011,fsd012 ${CI_REP_RST}/iced.${dateTsp1}.nc ${CI_REP_RST}/iced.fsd.nc > /dev/null 2>&1
            rm -f ${CI_REP_RST}/iced.${dateTs}_fsd.nc ; ${REP_CDO}/cdo merge ${CI_REP_RST}/iced.fsd.nc ${CI_REP_RST}/iced.${dateTs}.nc ${CI_REP_RST}/iced.${dateTs}_fsd.nc > /dev/null 2>&1 ;
            rm -f ${CI_REP_RST}/iced.${dateTsp1}.nc
        fi
        if [ ${default_exp} == "wimgx3" ] || [ ${default_exp} == "wimgx1" ] || [ ${default_exp} == "wimtx1" ]; then
           if ! ${bool_CoupledCICE}; then
               # If we want to launch an uncoupled simulation of CICE (change ndt)
 #              ice_ic='none'
 #              ice_ic=${CI_REP_RST}/iced.2014-11-01-00000.nc
               ice_ic=${CI_REP_RST}/iced.${dateTs}.nc
              #ice_ic=${ice_ic_initFSD}
               wave_spec_file='unknown_wave_spec_file'
               wave_spec_type="none"
               tr_fsd="false"
               bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${tr_fsd} ${ndtCICE} ${ndtCICE_u} ${dtCICEOut_u} ${CI_REP_WRK} ${couplingVar} ${listVarOutCICE}
               timerStartCI=$SECONDS
               ./cice.submit
               timerEndCI=$(( $SECONDS - ${timerStartCI} ))
               echo "Uncoupled CICE simulation done, exit loop."
               break # We want to run an uncoupled simulation, we don't event want to run WW3.
           else
               #If we want to launch a coupled simulation (keep ndt to 1).
               ice_ic=${CI_REP_RST}/iced.${dateTs}_fsd.nc
               wave_spec_file='unknown_wave_spec_file'
               wave_spec_type="none"
               bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${tr_fsd} ${ndtCICE} ${ndtCICE_u} ${dtCICEOut_u} ${CI_REP_WRK} ${couplingVar} ${listVarOutCICE}
               timerStartCI=$SECONDS
               ./cice.submit
               timerEndCI=$(( $SECONDS - ${timerStartCI} ))
           fi
       elif [ ${default_exp} == "wim2p5" ]; then
           mv ${CI_REP_RST}/iced.${dateTsp1}.nc ${CI_REP_RST}/iced.${dateTs}_fsd.nc
           if ! ${bool_CoupledCICE}; then
              ice_ic='internal'
              wave_spec_file=${wave_file_cst}
              wave_spec_type="random"
              bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${tr_fsd} ${ndtCICE} ${ndtCICE_u} ${dtCICEOut_u} ${CI_REP_WRK} ${couplingVar} ${listVarOutCICE}
              timerStartCI=$SECONDS
              ./cice.submit
              timerEndCI=$(( $SECONDS - ${timerStartCI} ))
              echo "Uncoupled CICE simulation done, exit loop."
              break
           else
               #If we want to launch a coupled simulation (keep ndt to 1).
               ice_ic=${CI_REP_RST}/iced.${dateTs}_fsd.nc
               wave_spec_file='unknown_wave_spec_file'
               wave_spec_type="none"
               bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${tr_fsd} ${ndtCICE} ${ndtCICE_u} ${dtCICEOut_u} ${CI_REP_WRK} ${couplingVar} ${listVarOutCICE}
               timerStartCI=$SECONDS
               ./cice.submit
               timerEndCI=$(( $SECONDS - ${timerStartCI} ))
           fi
        fi
     #Timestep 1 is special for the idealised case, we still need to start from internal. Might not be necessary.
     elif [ $i -eq 1 ]; then
        #Now we start simulation for real ! We redo the initial timestep, but now with a wave field an the fsd variables.
        if [ ${default_exp} == "wimgx3" ] || [ ${default_exp} == "wimgx1" ] || [ ${default_exp} == "wimtx1" ]; then
            ice_ic=${CI_REP_RST}/iced.${dateTs}_fsd.nc
            wave_spec_file=${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
            wave_spec_type="random"
        elif [ ${default_exp} == "wim2p5" ]; then
	 #   ice_ic='internal'
            ice_ic=${CI_REP_RST}/iced.${dateTs}_fsd.nc
            wave_spec_file=${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
            wave_spec_type="random"
        fi
        bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${tr_fsd} ${ndtCICE} ${ndtCICE_u} ${dtCICEOut_u} ${CI_REP_WRK} ${couplingVar} ${listVarOutCICE}
        timerStartCI=$SECONDS
        ./cice.submit
        timerEndCI=$(( $SECONDS - ${timerStartCI} ))
     else
        ice_ic=${CI_REP_RST}/iced.${dateTs}.nc
        wave_spec_file=${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
        wave_spec_type="random"

        bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${tr_fsd} ${ndtCICE} ${ndtCICE_u} ${dtCICEOut_u} ${CI_REP_WRK} ${couplingVar} ${listVarOutCICE}
        timerStartCI=$SECONDS
        ./cice.submit
        timerEndCI=$(( $SECONDS - ${timerStartCI} ))
        rm -rf ${CI_REP_RST}/iced.${dateTs}.nc
        rm -rf ${CI_REP_MOD}/out/${exp}/history/iceh_ic.${dateTs}.nc
      fi
   else
      #Hot start, skip time step 0.
      if [ $i -eq 0 ]; then
         echo "Hot Start"
         timerEndCI=0
      fi

      if ${bool_Coupled}; then
          if [ $i -ge 1 ]; then
              ice_ic=${CI_REP_RST}/iced.${dateTs}.nc
              wave_spec_file=${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
              wave_spec_type="random"
              bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${tr_fsd} ${ndtCICE} ${ndtCICE_u} ${dtCICEOut_u} ${CI_REP_WRK} ${couplingVar} ${listVarOutCICE}
              timerStartCI=$SECONDS
              ./cice.submit
              timerEndCI=$(( $SECONDS - ${timerStartCI} ))
          fi
          if [ $i -gt 1 ]; then
             rm -rf ${CI_REP_RST}/iced.${dateTs}.nc
             rm -rf ${CI_REP_MOD}/out/${exp}/history/iceh_ic.${dateTs}.nc
          fi
      fi
   fi

   echo '|------------Run WW3-------------|'
   if ${bool_coldStart}; then
      if [ $i -eq 0 ]; then
        if ${bool_CoupledWW3}; then
           bash ${WIM_REP_TOOLS}/wim_updateInpWW3.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${dtCoup} ${exp} ${bool_Coupled} ${W3_REP_INP} ${WIM_REP_TOOLS} ${grid}
           rm -rf ${W3_REP_INP}/ice_forcing.nc; ln -s ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc ${W3_REP_INP}/ice_forcing.nc
           timerStartW3=$SECONDS
           bash ${WIM_REP_TOOLS}/wim_runww3.sh ${W3_REP_MOD} ${exp} ${dateTs} ${w3listProg}
           timerEndW3=$(( $SECONDS - ${timerStartW3} ))
           mv ${W3_REP_WRK}/ww3.${dateTs_w3}_efreq.nc ${W3_REP_OUT}/ww3.${dateTs}_efreq.nc ;  mv ${W3_REP_WRK}/ww3.${dateTs_w3}.nc ${W3_REP_OUT}/ww3.${dateTs}.nc
           ${WIM_REP_TOOLS}/wim_updateIced.py ${exp} ${W3_REP_OUT} "ww3.${dateTs}.nc" ${W3_REP_OUT} "ww3.${dateTs}_efreq.nc" ${default_exp}
        else # We want to run an uncoupled simulation with only WW3.
           rm -rf ${W3_REP_INP}/ice_forcing.nc; ln -s ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc ${W3_REP_INP}/ice_forcing.nc
           timerStartW3=$SECONDS
           bash ${WIM_REP_TOOLS}/wim_runww3.sh ${W3_REP_MOD} ${exp} ${dateTs} ${w3listProg}
           timerEndW3=$(( $SECONDS - ${timerStartW3} ))
           mv ${W3_REP_WRK}/ww3.*.nc ${W3_REP_OUT}/
           echo "Uncoupled WW3 simulation done, exit loop"
           break
        fi
      else
        w3listProg="ww3_prnc ww3_shel ww3_ounf"
        bash ${WIM_REP_TOOLS}/wim_updateInpWW3.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${dtCoup} ${exp} ${bool_Coupled} ${W3_REP_INP} ${WIM_REP_TOOLS} ${grid}
        rm -rf ${W3_REP_INP}/ice_forcing-${dateTs}.nc; mv ${W3_REP_INP}/ice_forcing.nc ${W3_REP_INP}/ice_forcing-${dateTs}.nc; ln -s ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc ${W3_REP_INP}/ice_forcing.nc
        timerStartW3=$SECONDS
        bash ${WIM_REP_TOOLS}/wim_runww3.sh ${W3_REP_MOD} ${exp} ${dateTs} ${w3listProg}
        timerEndW3=$(( $SECONDS - ${timerStartW3} ))
        mv ${W3_REP_WRK}/ww3.${dateTsp1_w3}_efreq.nc ${W3_REP_OUT}/ww3.${dateTsp1}_efreq.nc ;  mv ${W3_REP_WRK}/ww3.${dateTsp1_w3}.nc ${W3_REP_OUT}/ww3.${dateTsp1}.nc
        ${WIM_REP_TOOLS}/wim_updateIced.py ${exp} ${W3_REP_OUT} "ww3.${dateTsp1}.nc" ${W3_REP_OUT} "ww3.${dateTsp1}_efreq.nc" ${default_exp}
        echo "Output are ${W3_REP_OUT}/ww3.${dateTsp1}_efreq.nc ${W3_REP_OUT}/ww3.${dateTsp1}.nc"
      fi
   else #Hot start, skip timestep 0.
      if ${bool_Coupled}; then
        if [ $i -eq 0 ]; then
           timerEndW3=0
        fi
        if [ $i -ge 1 ]; then
           if [ ! -e ${W3_REP_WRK}/mod_def.ww3 ]; then
               gridProg="ww3_grid"
           else
               gridProg=""
           fi

       	   w3listProg="${gridProg} ww3_prnc ww3_shel ww3_ounf"
           bash ${WIM_REP_TOOLS}/wim_updateInpWW3.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${dtCoup} ${exp} ${bool_Coupled} ${W3_REP_INP} ${WIM_REP_TOOLS} ${grid}
           rm -rf ${W3_REP_INP}/ice_forcing-${dateTs}.nc; mv ${W3_REP_INP}/ice_forcing.nc ${W3_REP_INP}/ice_forcing-${dateTs}.nc; ln -s ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc ${W3_REP_INP}/ice_forcing.nc
           timerStartW3=$SECONDS
           echo `ls /storage/bward/wim/ww3/model/inp/case95/ice_forcing.nc`
           bash ${WIM_REP_TOOLS}/wim_runww3.sh ${W3_REP_MOD} ${exp} ${dateTs} ${w3listProg}
           timerEndW3=$(( $SECONDS - ${timerStartW3} ))
           mv ${W3_REP_WRK}/ww3.${dateTsp1_w3}_efreq.nc ${W3_REP_OUT}/ww3.${dateTsp1}_efreq.nc ;  mv ${W3_REP_WRK}/ww3.${dateTsp1_w3}.nc ${W3_REP_OUT}/ww3.${dateTsp1}.nc
           ${WIM_REP_TOOLS}/wim_updateIced.py ${exp} ${W3_REP_OUT} "ww3.${dateTsp1}.nc" ${W3_REP_OUT} "ww3.${dateTsp1}_efreq.nc" ${default_exp}
           echo "Output are ${W3_REP_OUT}/ww3.${dateTsp1}_efreq.nc ${W3_REP_OUT}/ww3.${dateTsp1}.nc"
        fi
      fi
   fi
   ((i=i+1))
   timerEnd=$(( $SECONDS - ${timerStart} ))
   echo "Computing time for the time step : ${timerEnd}"
   echo "Computing time for CICE : ${timerEndCI}"
   echo "Computing time for W3 : ${timerEndW3}"
   timerEndRest=$(( $timerEnd - ${timerEndCI} - ${timerEndW3} ))
   echo "Computing time for the rest : ${timerEndRest}"
done

