#! /bin/bash

WIM_REP="${HOME}/wim"
WIM_REP_PP="${WIM_REP}/post-proc/"
WIM_REP_TOOLS="${WIM_REP}/tools/"
W3_REP_MOD="${WIM_REP}/ww3/model"
CI_REP_MOD="${WIM_REP}/cice"

machine=`hostname`

couplingVar="aice hi fsdrad"
listVarOutCICE="dafsd_latg dafsd_latm dafsd_newi dafsd_wave dafsd_weld strairx strairy uvel vvel strwvx strwvy"
list_year='2018'
list_month="01 02 03"
#list_month='03'
list_case='case11'

echo ${machine}

ndtAvg=1
dtAvg_u='d'
dtAvg=1

dtAvg_U='m'
day=1
sec=0

if [ ${machine} == "tookoolito.meteo.mcgill.ca" ]; then
    for expN in ${list_case}; do 
        if [ ! -d "${WIM_REP_PP}/${expN}/avg" ]; then
            mkdir -p "${WIM_REP_PP}/${expN}/avg"
        fi
        W3_REP_OUT=${W3_REP_MOD}/out/${expN}
        CI_REP_OUT=${CI_REP_MOD}/out/${expN}/history/
        W3_REP=${W3_REP_MOD}/out/${expN}/
        CI_REP=${CI_REP_MOD}/out/${expN}/
        for year in ${list_year}; do
            for month in ${list_month}; do
#                 scp -pr ${CI_REP_OUT}/iceh_01h.${year}-${month}-*.nc bward@bjerknes:${CI_REP}
                if [ ${month} -eq '01' ] || [ ${month} -eq '03' ] || [ ${month} -eq '05' ] || [ ${month} -eq '07' ] || [ ${month} -eq '08' ] || [ ${month} -eq '10' ] || [ ${month} -eq '12' ]; then
                    list_day=`seq 1 31`
                elif [ ${month} -eq '04' ] || [ ${month} -eq '06' ] || [ ${month} -eq '09' ] || [ ${month} -eq '11' ]; then
                    list_day=list_day=`seq 1 30`
                elif [ ${month} -eq '02' ]; then
                    list_day=list_day=`seq 1 28`
                fi
                echo ${expN}
                # Create the monthly average
                ${WIM_REP_TOOLS}/wim_monthlyAvg.py ${expN} ${year} ${month} ${day} ${sec} ${ndtAvg} ${dtAvg} ${dtAvg_U} ${W3_REP_OUT} "${CI_REP_OUT}" "${WIM_REP_PP}/${expN}/avg" ${couplingVar} ${listVarOutCICE}
                scp -pr ${WIM_REP_PP}/${expN}/avg/iceh_avg.${year}-${month}.nc bward@bjerknes:~/wim/cice/out/${expN}/history/

#Daily
#                for day in ${list_day}; do
#                   #Create the daily average
#                   ${WIM_REP_TOOLS}/wim_dailyAvg.py ${exp} ${year} ${month} ${day} ${sec} ${ndtAvg} ${dtAvg} ${dtAvg_u} ${W3_REP_OUT} "${CI_REP_OUT}" "${WIM_REP_PP}/${exp}/avg" ${couplingVar} ${listVarOutCICE}
#		   pad_day=`printf "%02d\n" $day`
#                done
#                # Transfert to Bjerknes, then remove daily avg (keep only a copy on Bjerknes)
#                scp -pr ${WIM_REP_PP}/${expN}/avg/iceh_avg.${year}-${month}*.nc bward@bjerknes:~/wim/cice/out/${exp}/history/
##                rm -rf ${WIM_REP_PP}/${exp}/avg/*
            done
        done
    done
else 
    echo "You are on ${machine}, no need to transfert datas"
fi
