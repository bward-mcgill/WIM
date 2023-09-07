#! /bin/bash

#Source config file
WIM_REP=${1}
. ${WIM_REP}/wim_launcher.cfg
#source ${HOME}/miniconda3/bin/activate wim
#conda info

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

REP_ICE_IC="/aos/home/bward/storage/cice-dirs/input/CICE_data/ic/restart_exp/ice_ic"
REP_WAVE_SPEC="/aos/home/bward/storage/cice-dirs/input/CICE_data/ic/restart_exp/wave_spec"
REP_WAVE_IC="/aos/home/bward/storage/cice-dirs/input/CICE_data/ic/restart_exp/wave_ic"
list_year="2018"
list_month="3"
list_day=`seq 1 31`

for year in ${list_year}; do
   for month in ${list_month}; do
      for day in ${list_day}; do

         cd ${WIM_REP}
         #Update config file.
         zeroPad_day=`printf "%02d\n" $day`
         zeroPad_month=`printf "%02d\n" $month`
         ln -sf ${REP_ICE_IC}/iced.${year}-${zeroPad_month}-${zeroPad_day}-00000.nc ${CI_REP_RST}/iced.${year}-${zeroPad_month}-${zeroPad_day}-00000.nc
         if ${bool_CoupledCICE}; then
             ln -sf ${REP_WAVE_SPEC}/ww3.${year}-${zeroPad_month}-${zeroPad_day}-00000_efreq.nc ${W3_REP_OUT}/ww3.${year}-${zeroPad_month}-${zeroPad_day}-00000_efreq.nc
             if [ ${day} -eq 1 ]; then
                 ln -sf ${REP_WAVE_IC}/restart_2018-02-28-82800.ww3 ${W3_REP_WRK}/restart_2018-02-28-82800.ww3
             elif [ ${day} -ge 1 ]; then
                 ((prevDay=day-1))
                 zeroPad_prevDay=`printf "%02d\n" $prevDay`
                 ln -sf ${REP_WAVE_IC}/restart_${year}-${zeroPad_month}-${zeroPad_prevDay}-82800.ww3 ${W3_REP_WRK}/restart_${year}-${zeroPad_month}-${zeroPad_prevDay}-82800.ww3
             fi
         fi
         sed -i "/day_init/c\day_init=${day}" config/config_${exp}
         echo "day_init has been updated to ${day}"
         #Standard launch
	 make wim_launch
         rm -rf ${CI_REP_RST}/iced.${year}-${zeroPad_month}-*.nc
      done
   done
done
