
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
. ${HOME}/wim/wim_launcher.cfg

#Constants
W3_REP_BIN=${W3_REP_MOD}/bin
W3_REP_INP=${W3_REP_MOD}/inp/${exp}
W3_REP_WRK=${W3_REP_MOD}/work/${exp}
W3_REP_OUT=${W3_REP_MOD}/out/${exp}

CI_REP_WRK=${CI_REP_MOD}/work/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
CI_REP_RST=${CI_REP_OUT}/restart

export WWATCH3_NETCDF=NC4
export NETCDF_CONFIG="/usr/bin/nc-config"
REP_CDO="/opt/cdo/bin/"

i=0
###----------------------Run the WIM-------------------#
listDateTs=`${WIM_REP_TOOLS}/wim_dateTime.py printListTs ${year_init} ${month_init} ${day_init} ${sec_init} ${dtCoup} ${ndt}`

for dateTimeStep in ${listDateTs}
do
   cd ${CI_REP_WRK}

   yyyy=`echo ${dateTimeStep} | cut -c -4`
   mm=`echo ${dateTimeStep} | cut -c 5-6` 
   dd=`echo ${dateTimeStep} | cut -c 7-8`
   ts=`echo ${dateTimeStep} | cut -c 9-`
   yyyy_int=$(echo $yyyy | sed 's/^0*//')
   mm_int=$(echo $mm | sed 's/^0*//')
   dd_int=$(echo $dd | sed 's/^0*//')
   if [ $ts -eq "00000" ]; then
      ts_int=0
   else
      ts_int=$(echo $ts | sed 's/^0*//')
   fi
   ((tsp1_int=ts_int+dt))
   dateTs=`${WIM_REP_TOOLS}/wim_dateTime.py printTs ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} 'CICE'`
   dateTsp1=`${WIM_REP_TOOLS}/wim_dateTime.py printTs ${yyyy_int} ${mm_int} ${dd_int} ${tsp1_int} 'CICE'`
   dateTsp1_w3=`echo "${dateTs//-}" | cut -c -8`
   dateTs_w3=`echo "${dateTsp1//-}" | cut -c -8`

   echo "Timestep $i : $dateTs"

   echo '|------------Run CICE-------------|'

   if ${bool_coldStart}; then
      if [ $i -eq 0 ]; then
        #Timestep 0 only job is to create a wave field !
      	echo "Cold start !"
        ice_ic='internal'
        wave_spec_file='unknown_wave_spec_file'
        wave_spec_type="none"
        bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${CI_REP_WRK}
        ./cice.submit
      elif [ $i -eq 1 ]; then
        #Now we start simulation for real !
	ice_ic='internal'
        wave_spec_file=${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
        wave_spec_type="random"
        bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${CI_REP_WRK}
        ./cice.submit
      else
        ice_ic=${CI_REP_RST}/iced.${dateTs}.nc
        wave_spec_file=${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
        wave_spec_type="random"
        bash ${WIM_REP_TOOLS}/wim_updateIceIn.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${CI_REP_WRK}
       ./cice.submit
       ${REP_CDO}/cdo aexpr,"fsdrad=fsdrad*2"  ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc_2xfsdrad 
       cp ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc_2xfsdrad ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc
      fi
   else
      #Make some verification here.
      echo "Hot Start (not implemented yet)."
      echo "ice_ic is required".
      echo "wave_spec_file is required".
   fi

   echo '|------------Run WW3-------------|'

   if ${bool_coldStart}; then
      if [ $i -eq 0 ]; then
        bash ${WIM_REP_TOOLS}/wim_updateInpWW3.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${dt} ${exp} ${W3_REP_INP} ${WIM_REP_TOOLS}
        rm -rf ${W3_REP_INP}/ice_forcing.nc
        ln -s ${CI_REP_OUT}/history/iceh_ic.${dateTsp1}.nc ${W3_REP_INP}/ice_forcing.nc
        bash ${WIM_REP_TOOLS}/wim_runww3.sh ${W3_REP_MOD} ${exp} ${dateTs} ${w3listProg}
        ${REP_CDO}/cdo chname,ef,efreq "${W3_REP_WRK}/ww3.${dateTs_w3}_ef.nc" "${W3_REP_WRK}/ww3.${dateTs}_efreq.nc"
        mv ${W3_REP_WRK}/ww3.${dateTs}_efreq.nc ${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
        mv ${W3_REP_WRK}/ww3.${dateTs_w3}.nc ${W3_REP_OUT}/ww3.${dateTs}.nc
        echo "Output are ${W3_REP_OUT}/ww3.${dateTs}_efreq.nc ${W3_REP_OUT}/ww3.${dateTs}.nc"
      else
        w3listProg="ww3_prnc ww3_shel ww3_ounf"
        bash ${WIM_REP_TOOLS}/wim_updateInpWW3.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${dt} ${exp} ${W3_REP_INP} ${WIM_REP_TOOLS}
        rm -rf ${W3_REP_INP}/ice_forcing-${dateTs}.nc
        mv ${W3_REP_INP}/ice_forcing.nc ${W3_REP_INP}/ice_forcing-${dateTs}.nc
        ln -s ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc ${W3_REP_INP}/ice_forcing.nc
        bash ${WIM_REP_TOOLS}/wim_runww3.sh ${W3_REP_MOD} ${exp} ${date4name} ${ts} ${w3listProg}
        ${REP_CDO}/cdo chname,ef,efreq "${W3_REP_WRK}/ww3.${dateTsp1_w3}_ef.nc" "${W3_REP_WRK}/ww3.${dateTsp1}_efreq.nc"
        mv ${W3_REP_WRK}/ww3.${dateTsp1}_efreq.nc ${W3_REP_OUT}/ww3.${dateTsp1}_efreq.nc
        mv ${W3_REP_WRK}/ww3.${dateTsp1_w3}.nc ${W3_REP_OUT}/ww3.${dateTsp1}.nc
        echo "Output are ${W3_REP_OUT}/ww3.${dateTsp1}_efreq.nc ${W3_REP_OUT}/ww3.${dateTsp1}.nc"
      fi
   else
      #Make some verification here (if file is there).
      #bash ${WIM_REP_TOOLS}/wim_updateInpWW3.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${dt} ${exp} ${W3_REP_INP}
      echo "Hot start (not implemented yet)"
   fi
#   python3 -c "import wimCouplerWW3 as couplerWW3; couplerWW3.exchangeVarWW3Cice('${nextTs}', '${W3_REP_OUT}' ,'${CI_REP_OUT}', '${date4name}')"
   ((i=i+1))
done

#w3_list_src=`ls ${W3_REP_INP}/*.inp`
#ci_list_src=`ls ${CI_REP_WRK}/ice_in`
#list_src="${w3_list_src} ${ci_list_src}"

#for file in $list_src
#do
#   md5sum $file > ${WIM_REP_TOOLS}/listMD4Readme.txt 
#done

#Post-processing
if ${bool_PP}; then
   echo '|------------Post-Processing-------------|'

   ${WIM_REP_PP}/plotWaveIce.py ${ndt} ${dt} ${year_init} ${month_init} ${day_init} ${sec_init} ${W3_REP_OUT} ${CI_REP_OUT}/history ${WIM_REP_PP}/${exp} -g ${default_exp} -f ${dt}
fi
