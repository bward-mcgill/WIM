#! /bin/bash

REP_WRK="/storage/bward/cice-dirs/cases"
exp="case8"

#conda activate cice
### Step 0 : Set up CICE environment -------------------------------------------#

rm -rf caselist*
rm -rf work/${exp} out/${exp}
echo ' '
echo '+-------------------------------+'
echo '|          Set up CICE           |'
echo '+-------------------------------+'
echo ' '

./cice.setup -m conda -e linux -c ${REP_WRK}/${exp} -s wim2p5 -g gbox80

### Step 1 : Compile CICE ---------------------------------------------------#

echo ' '
echo '+-------------------------------+'
echo '|          Compile CICE           |'
echo '+-------------------------------+'
echo ' '

#Move to work directory
if [ ! -d ${REP_WRK}/${exp} ]; then
   mkdir -p ${REP_WRK}/${exp}
fi

cd ${REP_WRK}/${exp}

./cice.build

### Step 2 : Run CICE ---------------------------------------------------#

echo ' '
echo '+-------------------------------+'
echo '|          Run CICE           |'
echo '+-------------------------------+'
echo ' '

./cice.submit


#conda deactivate

