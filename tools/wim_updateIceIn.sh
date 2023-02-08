#! /bin/bash

#Pourrais faire ca en python envrai.

# Read arguments
year_init_new=${1}
month_init_new=${2}
day_init_new=${3}
sec_init_new=${4}
ice_ic_new=${5}
wave_spec_file_new=${6}
wave_spec_type_new=${7}
tr_fsd_new=${8}
ndtCICE_new=${9}
ndtCICEUnit_new=${10}
freqCICE_new=${11}
CI_REP_WRK=${12}

# Last arguments : Unknown size (i.e. list of the variables that we want to output)

i=1
list_var=""
for args in $@
do
    if (($i < 13)); then
	((i=i+1))
        continue
    else
        list_var=${list_var}" "${args}
        ((i=i+1))
    fi
done

echo "|------------Update CICE namelist ${CI_REP_WRK}/ice_in-------------|"

# Update time of the run, atm. forcing, ic, wave forcing.
sed -i "/ year_init /c\    year_init       = ${year_init_new}" ${CI_REP_WRK}/ice_in
echo "year_init has been updated to $year_init_new"

sed -i "/month_init /c\    month_init       = ${month_init_new}" ${CI_REP_WRK}/ice_in
echo "month_init has been updated to $month_init_new"

sed -i "/day_init /c\    day_init       = ${day_init_new}" ${CI_REP_WRK}/ice_in
echo "day_init has been updated to $day_init_new"

sed -i "/sec_init /c\    sec_init       = ${sec_init_new}" ${CI_REP_WRK}/ice_in
echo "sec_init has been updated to $sec_init_new"

sed -i "/fyear_init /c\    fyear_init       = ${year_init_new}" ${CI_REP_WRK}/ice_in
echo "fyear_init has been updated to $year_init_new"

sed -i "/ice_ic /c\    ice_ic         = \'${ice_ic_new}\'" ${CI_REP_WRK}/ice_in
echo "ice_ic has been updated to ${ice_ic_new}"

sed -i "/wave_spec_file /c\    wave_spec_file  = \'${wave_spec_file_new}\'" ${CI_REP_WRK}/ice_in
sed -i "/wave_spec_type /c\    wave_spec_type  = \'${wave_spec_type_new}\'" ${CI_REP_WRK}/ice_in
sed -i "/tr_fsd /c\    tr_fsd  = .${tr_fsd_new}." ${CI_REP_WRK}/ice_in

echo "wave_spec_file has been updated to $wave_spec_file_new"
echo "wave_spec_type has been updated to $wave_spec_type_new"
echo "tr_fsd has been updated to $tr_fsd_new"

# Update output variables, frequency
sed -i "/npt /c\    npt         = ${ndtCICE_new}" ${CI_REP_WRK}/ice_in
echo "npt has been updated to ${ndtCICE_new}"

sed -i "/npt_unit /c\    npt_unit        = \'${ndtCICEUnit_new}\'" ${CI_REP_WRK}/ice_in
echo "npt_unit has been updated to \'${ndtCICEUnit_new}\'"

sed -i "/dumpfreq /c\    dumpfreq         = \'${freqCICE_new}\'" ${CI_REP_WRK}/ice_in
echo "Dumpfreq has been updated to \'${freqCICE_new}\'"

sed -i "/histfreq /c\    histfreq         = \'${freqCICE_new}\', \'x\',\'x\',\'x\',\'x\'" ${CI_REP_WRK}/ice_in
echo "Histfreq has been updated to \'${freqCICE_new}\', \'x\',\'x\',\'x\',\'x\'"


for var in ${list_var}; 
do
    sed -i "/f_${var} /c\    f_${var}         = \'${freqCICE_new}\'" ${CI_REP_WRK}/ice_in
    echo "f_${var} has been updated to \'${freqCICE_new}\'" 
done

# sed -i "/f_aice /c\    f_aice         = \'${freqCICE_new}\'" ${CI_REP_WRK}/ice_in
# sed -i "/f_hi /c\    f_hi         = \'${freqCICE_new}\'" ${CI_REP_WRK}/ice_in
# sed -i "/f_fsdrad /c\    f_fsdrad         = \'${freqCICE_new}\'" ${CI_REP_WRK}/ice_in
# echo "f_aice, f_hi and f_fsdrad has been updated to \'${freqCICE_new}\'"
