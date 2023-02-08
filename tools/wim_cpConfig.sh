#! /bin/bash
WIM_REP=${1}

echo "Write the name of the case:"

read -r caseName

if [ ! -e  ${WIM_REP}/config/config_${caseName} ]; then
    echo "Enter a reference case: "
    read -r refCase
    if [ ! -e  ${WIM_REP}/config/config_${refCase} ]; then 
        echo "Reference case don't exist"
	exit 1
    else 
       cat ${WIM_REP}/config/config_${refCase} > ${WIM_REP}/config/config_${caseName}
       sed -i "/exp=c/c\exp=${caseName}" ${WIM_REP}/config/config_${caseName}
       ln -sf ${WIM_REP}/config/config_${caseName} ${WIM_REP}/wim_launcher.cfg
    fi
else
   ln -sf ${WIM_REP}/config/config_${caseName} ${WIM_REP}/wim_launcher.cfg
   echo "Creating symbolic link with config_${caseName}"
#   exit 1
fi

