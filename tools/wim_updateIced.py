#! /usr/bin/env python3

import argparse
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import xarray as xr
import netCDF4 as nc
import os

#def readVarWW3(fileWW3, pathWW3, var):
#
#    dsWW3=xr.open_dataset(pathWW3+'/'+fileWW3)
#    var2d=np.nan_to_num(dsWW3[[var]][var].values.squeeze())
#    return var2d

def writeRstCICE(fileCICE, pathCICE, data, var):
   dsCICE=xr.open_dataset(pathCICE+'/'+fileCICE)
   if (var == "utic"):
       id_var="strwvx"
   elif (var == "vtic"):
       id_var="strwvy"
   else:
       print("Unknown WW3 variable")
   data=np.ones((data.shape[0], data.shape[1]))*5
   data1=np.zeros((data.shape[0], data.shape[1]))
   #Only zonal stress.
   if (id_var == 'strwvx'):
       dsCICE[id_var]=(['nj', 'ni'], data)
   elif (id_var == 'strwvy'):
       dsCICE[id_var]=(['nj', 'ni'], data1)

   os.system("mv "+pathCICE+'/'+fileCICE+" "+pathCICE+"/temp")
   dsCICE.to_netcdf(pathCICE+'/'+fileCICE)
   print(id_var+" has been added to "+pathCICE+'/'+fileCICE)

def get_geomWW3(path, file):
    '''
    This function reads the ni, nj, tlat, and tlon variables from a netcdf file
    '''
    fid = nc.Dataset("{}/{}".format(path, file), 'r')
    tlat = fid.variables['latitude'][:]
    tlon = fid.variables['longitude'][:]
    ni = fid.dimensions['longitude'].size #ni is for lat, nj for lon
    nj = fid.dimensions['latitude'].size

    return nj, ni, tlat, tlon

def read_stressWW3(path_a, files_a, var, nj, ni):
    '''
    Read the baseline and test data for sea ice thickness.  The calculate
    the difference for all locations where sea ice thickness is greater
    than 0.01 meters.
    '''
    def fill_data_array(path, files, nj, ni):
        '''Function to fill the data arrays'''
        # Initialize the data array
        data = np.zeros((nj, ni),dtype=np.float32)
        # Read in the data
        fname=files[0]
        nfid = nc.Dataset("{}/{}".format(path, fname), 'r')
        fill_value = nfid.variables[var]._FillValue
        data[:, :] = nfid.variables[var][:]
        nfid.close()
        data[data == fill_value] = 0.0

        return data
    
    data_a = fill_data_array(path_a, files_a, nj, ni)

    return data_a

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
    nlon, nlat, t_lat, t_lon = get_geomWW3(repOutW3, fileOutW3)
    listVar=['utic', 'vtic']
    for var in listVar:
       varWW3=read_stressWW3(repOutW3, [fileOutW3], var, nlon, nlat)
       print(varWW3)
       writeRstCICE(fileRstCI, repRstCI, varWW3, var)

#Call main
if __name__ == "__main__":
    main()
