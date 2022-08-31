include wim_launcher.cfg

CI_REP_WRK=${CI_REP_MOD}/work/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
W3_REP_INP=${W3_REP_MOD}/inp/${exp}
W3_REP_WRK=${W3_REP_MOD}/work/${exp}
W3_REP_OUT=${W3_REP_MOD}/out/${exp}

WIM_REP_PP=${WIM_REP}/post-proc
WIM_REP_TOOLS=${WIM_REP}/tools

run: case wim_launch README post_proc
	@echo "Full run as been launched"

case: ${WIM_REP}/wim_launcher.cfg
	@${WIM_REP_TOOLS}/wim_makeCase.sh

wim_launch:
	@${WIM_REP}/wim_launcher.sh

README: 
	@${WIM_REP_TOOLS}/wim_makeREADME.sh ${W3_REP_WRK} ${CI_REP_WRK} ${WIM_REP} ${WIM_REP_TOOLS} ${WIM_REP_PP} ${exp} ${year_init} ${month_init} ${day_init} ${sec_init} ${dtCoup} ${ndt} ${bool_coldStart}

post_proc: README
	@${WIM_REP_TOOLS}/wim_makePostProc.sh

clean:
	@${WIM_REP_TOOLS}/wim_clean.sh ${W3_REP_MOD} ${W3_REP_WRK} ${W3_REP_OUT} ${W3_REP_INP} ${CI_REP_WRK} ${CI_REP_OUT} ${WIM_REP_PP}/${exp}

#Eventuellement, enlever checkbuildCICE et remplacer dans le makefile. Mais le probleme c'est que ca fonctionne pas si executable est pas la et c'est une des choses que j'aimerais verifier. 

#buildCICE: ${exeCICE} ${cice_list_src}
#	@echo '|------------CICE build-------------|'
#	cd ${CI_REP_WRK}
#	csh ${CI_REP_WRK}/cice.build

#buildWW3:

#exeCICE:
#	echo 'No CICE executable build again'
#	cd ${CI_REP_WRK}; csh ${CI_REP_WRK}/cice.build
