#! /bin/bash

#Pourrais faire ca en python envrai.

year_init_new=${1}
month_init_new=${2}
day_init_new=${3}
sec_init_new=${4}
ice_ic_new=${5}
wave_spec_file_new=${6}
wave_spec_type_new=${7}
CI_REP_WRK=${8}

echo "|------------Update CICE namelist ${CI_REP_WRK}/ice_in-------------|"

sed -i "/ year_init /c\    year_init       = ${year_init_new}" ${CI_REP_WRK}/ice_in
echo "year_init as been updated to $year_init_new"

sed -i "/month_init /c\    month_init       = ${month_init_new}" ${CI_REP_WRK}/ice_in
echo "month_init as been updated to $month_init_new"

sed -i "/day_init /c\    day_init       = ${day_init_new}" ${CI_REP_WRK}/ice_in
echo "day_init as been updated to $day_init_new"

sed -i "/sec_init /c\    sec_init       = ${sec_init_new}" ${CI_REP_WRK}/ice_in
echo "sec_init as been updated to $sec_init_new"

sed -i "/fyear_init /c\    fyear_init       = ${year_init_new}" ${CI_REP_WRK}/ice_in
echo "fyear_init as been updated to $year_init_new"

sed -i "/ice_ic /c\    ice_ic         = \'${ice_ic_new}\'" ${CI_REP_WRK}/ice_in
echo "ice_ic as been updated to ${ice_ic_new}"

sed -i "/wave_spec_file /c\    wave_spec_file  = \'${wave_spec_file_new}\'" ${CI_REP_WRK}/ice_in
sed -i "/wave_spec_type /c\    wave_spec_type  = \'${wave_spec_type_new}\'" ${CI_REP_WRK}/ice_in

echo "wave_spec_file as been updated to $wave_spec_file_new"
echo "wave_spec_type as been updated to $wave_spec_type_new"


