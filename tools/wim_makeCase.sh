#! /bin/bash

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
#REP_CDO="/opt/cdo/bin/"

#----------------------Set up WW3 environment -------------------# 
#Verify if exp exist.
if [ ! -d ${W3_REP_INP} ]; then
   echo "--------------------WW3 create new case----------------------"
   ${WIM_REP_TOOLS}/wim_cpCaseww3.sh "default${default_exp}" "${exp}"
fi

switch_file=`cat ${W3_REP_INP}/switch_${exp}`
switch_default=`cat ${W3_REP_BIN}/switch_default${default_exp}`

if [[ "$switch_file" == *"$WWATCH3_NETCDF"* ]]; then
   echo "Switch file contains ${WWATCH3_NETCDF}. NETCDF fortran librairies (compiled with GNU) are required to run ww3_prnc and ww3_ounf."
else
   echo "Switch file doesn't contain ${WWATCH3_NETCDF}. Use ww3_prep and ww3_outf."
   exit 1
fi

rm -rf ${W3_REP_INP}/ice_forcing*

# If switch changed, need to redo setup and recompile.
if [ "${switch_file}" != "${switch_default}" ]; then

   echo '|------------Set up WW3-------------|'
   rm -f ${W3_REP_BIN}/switch_${exp}
   ln -s ${W3_REP_INP}/switch_${exp} ${W3_REP_BIN}/switch_${exp}
   bash ${W3_REP_BIN}/w3_setup ${W3_REP_MOD} -c Gnu -s ${exp}

   echo '|------------Compile WW3-------------|'
   bash ${WIM_REP_TOOLS}/wim_buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
fi

bash ${WIM_REP_TOOLS}/wim_checkBuildWW3.sh ${W3_REP_MOD} ${WIM_REP_TOOLS} ${W3_REP_WRK} ${exp} ${w3listProg}

####----------------------Set up CICE environment -------------------#

rm -rf ${CI_REP_MOD}/caselist*
rm -rf ${CI_REP_OUT}/cice.runlog*

##If case doesn't exist, we create it. 
if [ ! -e ${CI_REP_WRK} ]; then
   echo '|------------CICE create new case-------------|'

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

bash ${WIM_REP_TOOLS}/wim_checkBuildCICE.sh ${CI_REP_MOD} ${WIM_REP_TOOLS} ${CI_REP_WRK} ${CI_REP_OUT}

#rm -f ${WIM_REP_TOOLS}/MD4Readme.txt
#w3_list_src=`ls ${W3_REP_INP}/*.inp`
#ci_list_src=`ls ${CI_REP_WRK}/ice_in`
#list_src="${w3_list_src} ${ci_list_src}"
#for file in $list_src
#do
#   md5sum $file >> ${WIM_REP_TOOLS}/MD4Readme.txt 
#done

