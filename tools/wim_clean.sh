#! /bin/bash
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

WIM_REP_PP=${WIM_REP}/post-proc/${exp}
WIM_REP_TOOLS=${WIM_REP}/tools

#Full clean WW3
#ls ${W3_REP_MOD}/exe/* ${W3_REP_MOD}/obj/* ${W3_REP_MOD}/tmp/* ${W3_REP_MOD}/mod/*
#ls ${W3_REP_WRK} ${W3_REP_OUT} ${W3_REP_INP}
rm -rf ${W3_REP_MOD}/exe/* ${W3_REP_MOD}/obj/* ${W3_REP_MOD}/tmp/* ${W3_REP_MOD}/mod/*
rm -rf ${W3_REP_WRK} ${W3_REP_OUT} ${W3_REP_INP}
#Full clean CICE
#ls ${CI_REP_WRK} ${CI_REP_OUT}
rm -rf ${CI_REP_WRK} ${CI_REP_OUT}
#Clean post-proc
#ls ${WIM_REP_PP}
rm -rf ${WIM_REP_PP}

echo "Case cleaned, you can recompile again"
