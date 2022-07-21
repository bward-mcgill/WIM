#! /bin/bash
W3_REP_MOD=${1}
W3_REP_WRK=${2}
W3_REP_OUT=${3}
W3_REP_INP=${4}
CI_REP_WRK=${5}
CI_REP_OUT=${6}
WIM_REP_PP=${7}

#Full clean WW3
rm -rf ${W3_REP_MOD}/exe/* ${W3_REP_MOD}/obj/* ${W3_REP_MOD}/tmp/* ${W3_REP_MOD}/mod/*
rm -rf ${W3_REP_WRK} ${W3_REP_OUT} ${W3_REP_INP}
#Full clean CICE
rm -rf ${CI_REP_WRK} ${CI_REP_OUT}
#Clean post-proc
rm -rf ${WIM_REP_PP}

echo "Case cleaned, you can recompile again"
