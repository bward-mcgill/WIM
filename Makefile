include wim_launcher.cfg

ci_list_src=`find ${CI_REP_MOD}/cicecore/ -name "*.F90"`
ip_list_src=`find ${CI_REP_MOD}/icepack/columnphysics/ -name "*.F90"`
cice_list_src=${ci_list_src} ${ip_list_src}

CI_REP_WRK=${CI_REP_MOD}/work/${exp}
CI_REP_OUT=${CI_REP_MOD}/out/${exp}
exeCICE=${CI_REP_OUT}/cice

WIM_REP=${HOME}/wim

case: ${WIM_REP}/wim_launcher.cfg
	@${WIM_REP_TOOLS}/wim_makeCase.sh

wim_launch: case README
	@${WIM_REP}/wim_launcher.sh

README: 
	@${WIM_REP_TOOLS}/wim_makeREADME.sh

clean:
	@${WIM_REP_TOOLS}/wim_clean.sh

#buildCICE: ${exeCICE} ${cice_list_src}
	@echo '|------------CICE build-------------|'
#	cd ${CI_REP_WRK}
#	csh ${CI_REP_WRK}/cice.build

#buildWW3:

#exeCICE:
#	echo 'No CICE executable build again'
#	cd ${CI_REP_WRK}; csh ${CI_REP_WRK}/cice.build
