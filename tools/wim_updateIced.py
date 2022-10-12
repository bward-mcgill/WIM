#! /usr/bin/env python3

import argparse
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import xarray as xr
import netCDF4 as nc
import os

def writeRstCICE(fileCICE, pathCICE, data, var, defaultExp):
   dsCICE=xr.open_dataset(pathCICE+'/'+fileCICE)
   if (var == "utic"):
       id_var="strwvx"
   elif (var == "vtic"):
       id_var="strwvy"
   elif (var == 'efreq'):
       id_var='efreq'
   else:
       print("Unknown WW3 variable")
#   data=np.ones((data.shape[0], data.shape[1]))*5
#   data1=np.zeros((data.shape[0], data.shape[1]))
   #Only zonal stress.
   if defaultExp == "wimgx3":
       if (id_var == 'strwvx'):
           dsCICE[id_var]=(['lat', 'lon'], data)
       elif (id_var == 'strwvy'):
           dsCICE[id_var]=(['lat', 'lon'], data)
       elif (id_var == 'efreq'):
           dsCICE[id_var]=(['f', 'lat', 'lon'], data)
   elif defaultExp == "wim2p5":
       if (id_var == 'strwvx'):
           dsCICE[id_var]=(['y', 'x'], data)
       elif (id_var == 'strwvy'):
           dsCICE[id_var]=(['y', 'x'], data)
       elif (id_var == 'efreq'):
           dsCICE[id_var]=(['f', 'y', 'x'], data)

   os.system("mv "+pathCICE+'/'+fileCICE+" "+pathCICE+"/temp")
   dsCICE.to_netcdf(pathCICE+'/'+fileCICE)
   print(id_var+" has been added to "+pathCICE+'/'+fileCICE)

def get_geomWW3(path, file, defaultExp):
    '''
    This function reads the ni, nj, tlat, and tlon variables from a netcdf file
    '''
    fid = nc.Dataset("{}/{}".format(path, file), 'r')
    if defaultExp == "wim2p5":
        tlat = fid.variables['y'][:]
        tlon = fid.variables['x'][:]
        ni = fid.dimensions['y'].size #ni is for lat, nj for lon
        nj = fid.dimensions['x'].size
    elif defaultExp == "wimgx3":
        tlat = fid.variables['latitude'][:]
        tlon = fid.variables['longitude'][:]
        ni = fid.dimensions['lon'].size #ni is for lat, nj for lon
        nj = fid.dimensions['lat'].size
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

def read_specWW3(path_a, files_a, var, nj, ni, nf):
    '''
    Read the baseline and test data for sea ice thickness.  The calculate
    the difference for all locations where sea ice thickness is greater
    than 0.01 meters.
    '''
    def fill_data_array(path, files, nj, ni):
        '''Function to fill the data arrays'''
        # Initialize the data array
        data = np.zeros((nf, nj, ni),dtype=np.float32)
        # Read in the data
        fname=files[0]
        nfid = nc.Dataset("{}/{}".format(path, fname), 'r')
        fill_value = nfid.variables[var]._FillValue
        data[:, :, :] = nfid.variables[var][:]
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
    parser.add_argument("defaultExp", help="wim2p5 or wimgx3")
    args = parser.parse_args()

    #Define variables
    case=args.case
    repOutW3=args.repOutW3
    repRstCI=args.repRstCI
    defaultExp=args.defaultExp
    fileOutW3=args.fileOutW3
    fileRstCI=args.fileRstCI
    nlon, nlat, t_lat, t_lon = get_geomWW3(repOutW3, fileOutW3, defaultExp)
#    listVar=['utic', 'vtic', 'efreq']
    listVar=['utic', 'vtic']
    fileOutSpec=fileOutW3[:-3]+"_efreq.nc"
    print("File :"+repOutW3+"/"+fileOutW3+" is read")
    for var in listVar:
       if var == 'efreq':
#          varWW3=read_specWW3(repOutW3, ['ww3.2005-01-01-07200_efreq.nc'], var, nlon, nlat, 20)
           varWW3=read_specWW3(repOutW3, [fileOutSpec], var, nlon, nlat, 20)
       else:
           varWW3=read_stressWW3(repOutW3, [fileOutW3], var, nlon, nlat)
       writeRstCICE(fileRstCI, repRstCI, varWW3, var, defaultExp)
#Call main
if __name__ == "__main__":
    main()
