include wim_launcher.cfg

CI_REP_WRK=${CI_REP_MOD}/work/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
W3_REP_INP=${W3_REP_MOD}/inp/${exp}
W3_REP_WRK=${W3_REP_MOD}/work/${exp}
W3_REP_OUT=${W3_REP_MOD}/out/${exp}

WIM_REP_PP=${WIM_REP}/post-proc
WIM_REP_TOOLS=${WIM_REP}/tools

run: wim_launch post_proc
	@echo "Full run as been launched"

case: ${WIM_REP}/wim_launcher.cfg
	@bash ${WIM_REP_TOOLS}/wim_makeCase.sh ${WIM_REP}

#Different kind of launcher that mimic the NRC operational model (i.e. restart everyday from coupled simulation).
nrc_launch:
	@${WIM_REP_TOOLS}/wim_makeNRClaunch.sh ${WIM_REP}

wim_launch:
	@${WIM_REP}/wim_launcher.sh ${WIM_REP}

README: 
	@${WIM_REP_TOOLS}/wim_makeREADME.sh ${WIM_REP}

post_proc:
	@${WIM_REP_TOOLS}/wim_makePostProc.sh

CONFIG:
	@${WIM_REP_TOOLS}/wim_cpConfig.sh ${WIM_REP}

clean:
	@${WIM_REP_TOOLS}/wim_clean.sh ${WIM_REP}

#Eventuellement, enlever checkbuildCICE et remplacer dans le makefile. Mais le probleme c'est que ca fonctionne pas si executable est pas la et c'est une des choses que j'aimerais verifier. 

#buildCICE: ${exeCICE} ${cice_list_src}
#	@echo '|------------CICE build-------------|'
#	cd ${CI_REP_WRK}
#	csh ${CI_REP_WRK}/cice.build

#buildWW3:

#exeCICE:
#	echo 'No CICE executable build again'
#	cd ${CI_REP_WRK}; csh ${CI_REP_WRK}/cice.build
