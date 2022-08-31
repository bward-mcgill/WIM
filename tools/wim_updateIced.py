#! /usr/bin/env python3

import argparse
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import xarray as xr
import os

def readVarWW3(fileWW3, pathWW3, var):
    dsWW3=xr.open_dataset(pathWW3+'/'+fileWW3)
    var2d=np.nan_to_num(dsWW3[[var]][var].values.squeeze())
    return var2d

def writeRstCICE(fileCICE, pathCICE, data, var):
   dsCICE=xr.open_dataset(pathCICE+'/'+fileCICE)
   if (var == "utic"):
       id_var="strwvx"
   elif (var == "vtic"):
       id_var="strwvy"
   else:
       print("Unknown WW3 variable")
   dsCICE[id_var]=(['nj', 'ni'], data)
   os.system("mv "+pathCICE+'/'+fileCICE+" "+pathCICE+"/temp")
   dsCICE.to_netcdf(pathCICE+'/'+fileCICE)
   print(id_var+" has been added to "+pathCICE+'/'+fileCICE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case", help="Name of the case (e.g. case01).")
    parser.add_argument("repOutW3", help="Path for WW3 output file.")
    parser.add_argument("fileOutW3", help="Name of WW3 output file.")
    parser.add_argument("repRstCI", help="Path for CICE restart file.")
    parser.add_argument("fileRstCI", help="Path for CICE restart file.")
    args = parser.parse_args()

    #Define variables
    case=args.case
    repOutW3=args.repOutW3
    repRstCI=args.repRstCI
    fileOutW3=args.fileOutW3
    fileRstCI=args.fileRstCI
    listVar=['utic', 'vtic']
    for var in listVar:
       varWW3=readVarWW3(fileOutW3, repOutW3, var)
       writeRstCICE(fileRstCI, repRstCI, varWW3, var)

#Call main
if __name__ == "__main__":
    main()

