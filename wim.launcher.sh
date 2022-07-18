
#! /bin/bash
# --------------------------------------------------------------------------- #
# wim.launcher.sh : Set up, compile, and launch CICE and WW3 sequentially     #
#                   and exchange variables in the coupled WIM framework       #
#                                                                             #
# use  : ./wim.launcher.sh                                                    #
#                                                                             #
#                                                      Benjamin Ward          #
#                                                      June 2022              #
#                                                      McGill University      #
# --------------------------------------------------------------------------- #

#Source config file
. wim.launcher.cfg

#Constants
W3_REP_BIN=${W3_REP_MOD}/bin
W3_REP_INP=${W3_REP_MOD}/inp/${exp}
W3_REP_WIM=${W3_REP_MOD}/wim
W3_REP_WRK=${W3_REP_MOD}/work/${exp}
W3_REP_OUT=${W3_REP_MOD}/out/${exp}

CI_REP_WRK=${CI_REP_MOD}/work/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
CI_REP_RST=${CI_REP_OUT}/restart
CI_REP_WIM=${CI_REP_MOD}/wim

export WWATCH3_NETCDF=NC4
export NETCDF_CONFIG="/usr/bin/nc-config"
REP_CDO="/opt/cdo/bin/"

#----------------------Set up WW3 environment -------------------# 
#Verify if exp exist.
if [ ! -d ${W3_REP_INP} ]; then
   ${W3_REP_WIM}/wim.cpCase.sh "default${default_exp}" "${exp}"
fi

switch_file=`cat ${W3_REP_INP}/switch_${exp}`
switch_default=`cat ${W3_REP_BIN}/switch_default${default_exp}`

if [[ "$switch_file" == *"$WWATCH3_NETCDF"* ]]; then
   echo "Switch file contains ${WWATCH3_NETCDF}."
else
   echo "Switch file doesn't contain ${WWATCH3_NETCDF}. NETCDF fortran librairies (compiled with GNU) are required to run ww3_prnc and ww3_ounf."
   exit 1
fi

#rm -rf ${W3_REP_OUT} ${W3_REP_INP}/ice_forcing*

# Ajouter une conditions qui regarde si les executables sont la.
# If switch changed, need to redo setup and recompile.
#Regarder aussi si le case est la 
if [ "${switch_file}" != "${switch_default}" ]; then

   echo '|------------Set up WW3-------------|'
   rm -f ${W3_REP_BIN}/switch_${exp}
   ln -s ${W3_REP_INP}/switch_${exp} ${W3_REP_BIN}/switch_${exp}
   bash ${W3_REP_BIN}/w3_setup ${W3_REP_MOD} -c Gnu -s ${exp}

   echo '|------------Compile WW3-------------|'
   bash ${W3_REP_WIM}/wim.buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
fi


#If source code changed, need to recompile.
w3_list_src=`ls ${W3_REP_MOD}/ftn/*.ftn`
rm -f ${W3_REP_WIM}/test_list_MD5.txt

for file in $w3_list_src
do
   md5sum $file >> ${W3_REP_WIM}/test_list_MD5.txt 
done

if [ ! -e ${W3_REP_WIM}/list_MD5.txt ]; then
   echo '|------------WW3 first build-------------|'
   bash ${W3_REP_WIM}/wim.buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
   for file in $w3_list_src
   do
      md5sum $file >> ${W3_REP_WIM}/list_MD5.txt 
   done
elif ! $(cmp -s "${W3_REP_WIM}/list_MD5.txt" "${W3_REP_WIM}/test_list_MD5.txt"); then
   echo '|------------WW3 source code has changed, build again.-------------|'
   bash ${W3_REP_WIM}/wim.buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
   cat ${W3_REP_WIM}/test_list_MD5.txt > ${W3_REP_WIM}/list_MD5.txt
elif [ ! -d ${W3_REP_WRK} ]; then
   echo '|------------Work directory dont exist, build again.-------------|'
   bash ${W3_REP_WIM}/wim.buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
   cat ${W3_REP_WIM}/test_list_MD5.txt > ${W3_REP_WIM}/list_MD5.txt
elif [ ! "$(ls -A ${W3_REP_MOD}/exe)" ] || [ ! "$(ls -A ${W3_REP_MOD}/mod)" ] || [ ! "$(ls -A ${W3_REP_MOD}/obj)" ]; then
   echo '|------------WW3 Executable missing, build again.-------------|'
   bash ${W3_REP_WIM}/wim.buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
   cat ${W3_REP_WIM}/test_list_MD5.txt > ${W3_REP_WIM}/list_MD5.txt
fi

####----------------------Set up CICE environment -------------------#

rm -rf ${CI_REP_MOD}/caselist*

##If case doesn't exist, we create it. 
if [ ! -e ${CI_REP_WRK} ]; then
   echo '|------------Set up CICE-------------|'

   cd ${CI_REP_MOD}
   csh ./cice.setup -m conda -e linux -c ${CI_REP_WRK} -s ${default_exp} -g gbox80 #-s buildincremental

   echo '|------------Compile CICE-------------|'
   if [ ! -e ${CI_REP_WRK} ]; then
      echo "There was a problem with CICE setup"
      exit 1
   fi

   cd ${CI_REP_WRK}

   csh ${CI_REP_WRK}/cice.build
fi

#If case exist, but source code has changed, need to recompile.
ci_list_src=`find ${CI_REP_MOD}/cicecore/ -name "*.F90"` 
ip_list_src=`find ${CI_REP_MOD}/icepack/columnphysics/ -name "*.F90"`
ci_list_src="${ci_list_src} ${ip_list_src}"

rm -f ${CI_REP_WIM}/test_list_MD5.txt

for file in $ci_list_src
do
   md5sum $file >> ${CI_REP_WIM}/test_list_MD5.txt 
done

if [ ! -e ${CI_REP_WIM}/list_MD5.txt ]; then
   echo '|------------CICE first build-------------|'
   cd ${CI_REP_WRK}
   csh ${CI_REP_WRK}/cice.build
   for file in $ci_list_src
   do
      md5sum $file >> ${CI_REP_WIM}/list_MD5.txt 
   done
elif ! $(cmp -s "${CI_REP_WIM}/list_MD5.txt" "${CI_REP_WIM}/test_list_MD5.txt"); then
   echo '|------------CICE source code has changed build again.-------------|'
   cd ${CI_REP_WRK}
   csh ${CI_REP_WRK}/cice.build
   cat ${CI_REP_WIM}/test_list_MD5.txt > ${CI_REP_WIM}/list_MD5.txt
elif [ ! -e ${CI_REP_OUT}/cice ] ; then
   echo '|------------CICE Executable missing, build again !-------------|'
   cd ${CI_REP_WRK}
   csh ${CI_REP_WRK}/cice.build
fi


##Initialise namelist
i=0

###----------------------Run the WIM-------------------#
list_ts=`python3 -c "import wimCouplerCice as couplerCice; couplerCice.createListTs(${year_init}, ${month_init}, ${day_init}, ${sec_init}, ${dt}, ${ndt})"`

for timeStep in ${list_ts}
do
   cd ${CI_REP_WRK}

   yyyy=`echo ${timeStep} | cut -c -4`
   mm=`echo ${timeStep} | cut -c 5-6` 
   dd=`echo ${timeStep} | cut -c 7-8`
   ts=`echo ${timeStep} | cut -c 9-`
   yyyy_int=$(echo $yyyy | sed 's/^0*//')
   mm_int=$(echo $mm | sed 's/^0*//')
   dd_int=$(echo $dd | sed 's/^0*//')
   if [ $ts -eq "00000" ]; then
      ts_int=0
   else
      ts_int=$(echo $ts | sed 's/^0*//')
   fi
   ((tsp1_int=ts_int+dt))
   dateTs=`python3 -c "import wimCouplerCice as couplerCice; couplerCice.createTimeCice(${yyyy_int}, ${mm_int}, ${dd_int}, ${ts_int})"`
   dateTsp1=`python3 -c "import wimCouplerCice as couplerCice; couplerCice.createTimeCice(${yyyy_int}, ${mm_int}, ${dd_int}, ${tsp1_int})"`
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
        bash ${CI_REP_WIM}/wim.updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${CI_REP_WRK}
        ./cice.submit
      elif [ $i -eq 1 ]; then
        #Now we start simulation for real !
	ice_ic='internal'
        wave_spec_file=${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
        wave_spec_type="random"
        bash ${CI_REP_WIM}/wim.updateIceIn.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${CI_REP_WRK}
        ./cice.submit
      else
        ice_ic=${CI_REP_RST}/iced.${dateTs}.nc
        wave_spec_file=${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
        wave_spec_type="random"
        bash ${CI_REP_WIM}/wim.updateIceIn.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${ice_ic} ${wave_spec_file} ${wave_spec_type} ${CI_REP_WRK}
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
        bash ${W3_REP_WIM}/wim.updateInpWW3.sh ${year_init} ${month_init} ${day_init} ${sec_init} ${dt} ${exp} ${W3_REP_INP}
        rm -rf ${W3_REP_INP}/ice_forcing.nc
        ln -s ${CI_REP_OUT}/history/iceh_ic.${dateTsp1}.nc ${W3_REP_INP}/ice_forcing.nc
        bash ${W3_REP_WIM}/wim.runww3.sh ${W3_REP_MOD} ${exp} ${dateTs} ${w3listProg}
        ${REP_CDO}/cdo chname,ef,efreq "${W3_REP_WRK}/ww3.${dateTs_w3}_ef.nc" "${W3_REP_WRK}/ww3.${dateTs}_efreq.nc"
        mv ${W3_REP_WRK}/ww3.${dateTs}_efreq.nc ${W3_REP_OUT}/ww3.${dateTs}_efreq.nc
        mv ${W3_REP_WRK}/ww3.${dateTs_w3}.nc ${W3_REP_OUT}/ww3.${dateTs}.nc
        echo "Output are ${W3_REP_OUT}/ww3.${dateTs}_efreq.nc ${W3_REP_OUT}/ww3.${dateTs}.nc"
      else
        w3listProg="ww3_prnc ww3_shel ww3_ounf"
        bash ${W3_REP_WIM}/wim.updateInpWW3.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${dt} ${exp} ${W3_REP_INP}
        rm -rf ${W3_REP_INP}/ice_forcing-${dateTs}.nc
        mv ${W3_REP_INP}/ice_forcing.nc ${W3_REP_INP}/ice_forcing-${dateTs}.nc
        ln -s ${CI_REP_OUT}/history/iceh_01h.${dateTsp1}.nc ${W3_REP_INP}/ice_forcing.nc
        bash ${W3_REP_WIM}/wim.runww3.sh ${W3_REP_MOD} ${exp} ${date4name} ${ts} ${w3listProg}
        ${REP_CDO}/cdo chname,ef,efreq "${W3_REP_WRK}/ww3.${dateTsp1_w3}_ef.nc" "${W3_REP_WRK}/ww3.${dateTsp1}_efreq.nc"
        mv ${W3_REP_WRK}/ww3.${dateTsp1}_efreq.nc ${W3_REP_OUT}/ww3.${dateTsp1}_efreq.nc
        mv ${W3_REP_WRK}/ww3.${dateTsp1_w3}.nc ${W3_REP_OUT}/ww3.${dateTsp1}.nc
        echo "Output are ${W3_REP_OUT}/ww3.${dateTsp1}_efreq.nc ${W3_REP_OUT}/ww3.${dateTsp1}.nc"
      fi
   else
      #Make some verification here (if file is there).
      #bash ${W3_REP_WIM}/wim.updateInpWW3.sh ${yyyy_int} ${mm_int} ${dd_int} ${ts_int} ${dt} ${exp} ${W3_REP_INP}
      echo "Hot start (not implemented yet)"
   fi
#   python3 -c "import wimCouplerWW3 as couplerWW3; couplerWW3.exchangeVarWW3Cice('${nextTs}', '${W3_REP_OUT}' ,'${CI_REP_OUT}', '${date4name}')"
   ((i=i+1))
done

#Post-processing

if [ ! -d "${WIM_REP_PP}/${exp}" ]; then
   mkdir -p "${WIM_REP_PP}/${exp}"
fi

