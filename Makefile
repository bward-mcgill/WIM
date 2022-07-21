include wim_launcher.cfg

CI_REP_WRK=${CI_REP_MOD}/work/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
W3_REP_INP=${W3_REP_MOD}/inp/${exp}
W3_REP_WRK=${W3_REP_MOD}/work/${exp}
W3_REP_OUT=${W3_REP_MOD}/out/${exp}

WIM_REP=${HOME}/wim

case: ${WIM_REP}/wim_launcher.cfg
	@${WIM_REP_TOOLS}/wim_makeCase.sh

wim_launch: case README
	@${WIM_REP}/wim_launcher.sh

README: 
	@${WIM_REP_TOOLS}/wim_makeREADME.sh ${W3_REP_INP} ${CI_REP_WRK} ${WIM_REP} ${WIM_REP_TOOLS} ${WIM_REP_PP} ${exp} ${year_init} ${month_init} ${day_init} ${sec_init} ${dtCoup} ${ndt} ${bool_coldStart}

clean:
	@${WIM_REP_TOOLS}/wim_clean.sh ${W3_REP_MOD} ${W3_REP_WRK} ${W3_REP_OUT} ${W3_REP_INP} ${CI_REP_WRK} ${CI_REP_OUT} ${WIM_REP_PP}/${exp}

#buildCICE: ${exeCICE} ${cice_list_src}
#	@echo '|------------CICE build-------------|'
#	cd ${CI_REP_WRK}
#	csh ${CI_REP_WRK}/cice.build

#buildWW3:

#exeCICE:
#	echo 'No CICE executable build again'
#	cd ${CI_REP_WRK}; csh ${CI_REP_WRK}/cice.build