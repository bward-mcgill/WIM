#! /bin/bash

#Source config file
WIM_REP=${1}
. ${WIM_REP}/wim_launcher.cfg
source ${HOME}/miniconda3/bin/activate wim
conda info

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

export WWATCH3_NETCDF=NC4
export NETCDF_CONFIG="/usr/bin/nc-config"
#REP_CDO="/opt/cdo/bin/"

#----------------------Set up WW3 environment -------------------# 
#Verify if exp exist.
if [ ! -d ${W3_REP_INP} ]; then
   echo "--------------------WW3 create new case----------------------"
   echo "Enter a reference case for WW3:"
   read -r refCaseWW3
   if [ ! -d ${W3_REP_MOD}/inp/${refCaseWW3} ]; then
      echo "Reference case doesn't exist, use the default one."
      ${WIM_REP_TOOLS}/wim_cpCaseww3.sh "default${default_exp}" "${exp}"
   else
      echo "Creating new case from ${refCaseWW3}"
      ${WIM_REP_TOOLS}/wim_cpCaseww3.sh "${refCaseWW3}" "${exp}"
   fi
fi

switch_file=`cat ${W3_REP_INP}/switch_${exp}`
switch_old=`cat ${W3_REP_BIN}/switch`

if [[ "$switch_file" == *"$WWATCH3_NETCDF"* ]]; then
   echo "Switch file contains ${WWATCH3_NETCDF}. NETCDF fortran librairies (compiled with GNU) are required to run ww3_prnc and ww3_ounf."
else
   echo "Switch file doesn't contain ${WWATCH3_NETCDF}. Use ww3_prep and ww3_outf."
   exit 1
fi

# If switch changed, need to redo setup and recompile.
if [ "${switch_file}" != "${switch_old}" ]; then
   echo '|------------Set up WW3-------------|'
   rm -f ${W3_REP_BIN}/switch_${exp}
   ln -s ${W3_REP_INP}/switch_${exp} ${W3_REP_BIN}/switch_${exp}
   bash ${W3_REP_BIN}/w3_setup ${W3_REP_MOD} -c Gnu -s ${exp}

   echo '|------------Compile WW3-------------|'
   bash ${WIM_REP_TOOLS}/wim_buildww3.sh ${W3_REP_MOD} ${exp} ${w3listProg}
fi

# Look if source code have changed.
bash ${WIM_REP_TOOLS}/wim_checkBuildWW3.sh ${W3_REP_MOD} ${WIM_REP_TOOLS} ${W3_REP_WRK} ${exp} ${w3listProg}

###----------------------Set up CICE environment-------------------#

##If case doesn't exist, we create it. 
if [ ! -e ${CI_REP_WRK} ]; then
   echo '|------------CICE create new case-------------|'

   cd ${CI_REP_MOD}

   if [ ${default_exp} == "wimgx3" ]; then
      grid="gx3"
   elif [ ${default_exp} == "wim2p5" ]; then
      grid="gbox80"
   fi

   csh ./cice.setup -m conda -e linux -c ${CI_REP_WRK} -g ${grid} -s ${default_exp}

   if [ ! -e ${CI_REP_WRK} ]; then
      echo "There was a problem with CICE setup"
      exit 1
   fi

   echo '|------------Compile CICE-------------|'
   cd ${CI_REP_WRK}
   echo "Enter a reference case for CICE:"
   read -r refCaseCICE
   if [ ! -e ${CI_REP_MOD}/work/${refCaseCICE}/ice_in ]; then
      echo "Reference case doesn't exist, use the default namelist"
   else 
      echo "Creating new case from ${refCaseCICE} namelist."
      cat ${CI_REP_MOD}/work/${refCaseCICE}/ice_in > ice_in
   fi

   csh ${CI_REP_WRK}/cice.build
fi

bash ${WIM_REP_TOOLS}/wim_checkBuildCICE.sh ${CI_REP_MOD} ${WIM_REP_TOOLS} ${CI_REP_WRK} ${CI_REP_OUT}

