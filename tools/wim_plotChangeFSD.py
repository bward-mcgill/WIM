#! /usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
from wim_dateTime import createListDateTime
from datetime import datetime, timedelta
#import matplotlib.animation as animation
#from PIL import Image
#import glob
#import xarray as xr
import argparse
import subprocess
import warnings
import netCDF4 as nc
import numpy.ma as ma
import os

def plotChangeFSD(REP_IN_CICE, fileCI, nlon, nlat, lat, lon, repOUT, case, datestr,plot_type, list_var):

    '''This function plots CICE data and creates a .png file.'''
    from mpl_toolkits.basemap import Basemap
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    # Suppress Matplotlib deprecation warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    fig, axes = plt.subplots(len(list_var),1,figsize=[14,8*len(list_var)])
    i=0
    for var in list_var:
       #Read ice field and wave field.
       data=read_data(REP_IN_CICE, [fileCI], var, nlon, nlat)       
       plt.sca(axes[i])

       #Choose projection
#       m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
#       m = Basemap(projection='spstere', boundinglat=-45,lon_0=270, resolution='l')
#       m = Basemap(width=12000000,height=8000000,resolution='l',projection='stere',lat_0=90,lon_0=270)
#       m = Basemap(projection='ortho',lon_0=270,lat_0=40,resolution='l')
       m = Basemap(projection='npstere', boundinglat=35,lon_0=270, resolution='l')
       m.drawcoastlines()
       if var == 'dafsd_newi' or var == 'dafsd_latg' or var == 'dafsd_weld':
          orig_map=plt.cm.get_cmap('YlGnBu')
       elif var == 'dafsd_latm' or var == 'dafsd_wave':
          orig_map=plt.cm.get_cmap('YlOrRd')
          orig_map=orig_map.reversed()

       if plot_type == 'scatter':
           x, y = m(lon,lat)
           sc = m.scatter(x, y, c=data, cmap=orig_map, lw=0, s=4)
       else:
           # Longitude need to be between -180 and 180 for plotting
           lon1 = lon.copy()
           for lt in range(lon.shape[0]):
               for lg in range(lon.shape[1]):
                   pt=lon[lt,lg]
                   if pt >= 180:
                       lon1[lt,lg]=lon1[lt,lg]-360. 
           lon = lon1

           #No need for reordering the datas, just create empty arrays.
           d = np.zeros((data.shape[0],data.shape[1]+1))
           lon_cyc = np.zeros((lon.shape[0],lon.shape[1]+1))
           mask = np.zeros((data.shape[0],data.shape[1]+1))
           lat_cyc = np.zeros((lat.shape[0],lat.shape[1]+1))       
           #Simply fill the arrays
           mask[:,0:-1] = data.mask[:,:]
           mask[:,-1] = data.mask[:,0]
           lon_cyc[:,0:-1] = lon[:,:]; lon_cyc[:,-1] = lon[:,0]
           lat_cyc[:,0:-1] = lat[:,:]; lat_cyc[:,-1] = lat[:,0]
           d[:,0:-1] = data[:,:]
           d[:,-1] = data[:,0]
           # Apply mask to ice field
           d1 = np.ma.masked_array(d,mask=mask)

           x, y = m(lon_cyc, lat_cyc)

           if plot_type == 'contour':
               #Plot ice fields
               sc = m.contourf(x, y, d1, cmap=orig_map)
               #Plot contours
           else:  # pcolor
               sc = m.pcolor(x, y, d1, cmap=orig_map)

       m.drawparallels(np.arange(-90.,120.,15.),labels=[1,0,0,0], size=16) # draw parallels
       m.drawmeridians(np.arange(0.,420.,30.),labels=[1,1,1,1], size=16) # draw meridians
       cb=fig.colorbar(sc, ax=axes[i])
       cb.ax.tick_params(labelsize=18)

       if var == 'dafsd_newi':
          cb.set_label('New Ice [m/days]', size=20)
       elif var == 'dafsd_latg':
          cb.set_label('Lat. Growth [m/days]', size=20)
       elif var == 'dafsd_latm':
          cb.set_label('Lat. Melt. [m/days]', size=20)
       elif var == 'dafsd_weld':
          cb.set_label('Welding [m/days]', size=20)
       elif var == 'dafsd_wave':
          cb.set_label('Wave Frac. [m/days]', size=20)

       i=i+1

    plt.tight_layout()
    plt.subplots_adjust(top=0.97)
    plt.savefig(repOUT+"/"+case+"_ChangeFSD_"+datestr, bbbox_to_anchor='tight', dpi=500)
    print("------------"+case+"_ChangeFSD_"+datestr+" as been plotted---------------------")

def read_data(path_a, files_a, var, nj, ni):
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
        data[:, :] = np.sum(np.squeeze(nfid.variables[var][:]),0)
        nfid.close()
            
        data[data == fill_value] = 0.0

        return data
    
    data_a = fill_data_array(path_a, files_a, nj, ni)
    mask_array_a = np.zeros_like(data_a)

    if var == 'dafsd_newi':
        mask_array_a = np.logical_or(data_a == 0., data_a < 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'dafsd_latg':
        mask_array_a = np.logical_or(data_a == 0., data_a < 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'dafsd_latm':
        mask_array_a = np.logical_or(data_a == 0., data_a > 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'dafsd_weld':
        mask_array_a = np.logical_or(data_a == 0., data_a < 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'dafsd_wave':
        mask_array_a = np.logical_or(data_a == 0., data_a > 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)

    return data_a

def get_geomCICE(path, file):
    '''
    This function reads the ni, nj, tlat, and tlon variables from a netcdf file
    '''
    fid = nc.Dataset("{}/{}".format(path, file), 'r')
    tlat = fid.variables['TLAT'][:]
    tlon = fid.variables['TLON'][:]
    ni = fid.dimensions['ni'].size
    nj = fid.dimensions['nj'].size

    return nj, ni, tlat, tlon

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case", help="Name of the case (e.g. case01).")
    parser.add_argument("nts", help="Number of plot.", type=int)
    parser.add_argument("dt", help="Time step of CICE.", type=int)
    parser.add_argument("start_y", help="Year of the first plot.", type=int)
    parser.add_argument("start_m", help="Month of the first plot.", type=int)
    parser.add_argument("start_d", help="Day of the first plot.", type=int)
    parser.add_argument("start_s", help="Seconds of the first plot", type=int)
    parser.add_argument("rep_inW3", help="Path for WW3 output.")
    parser.add_argument("rep_inCI", help="Path for CICE output.")
    parser.add_argument("rep_out", help="Path to store plot.")
    parser.add_argument("grid", help="Specify grid (default wim2p5)")
    parser.add_argument("outfreq", help="Specify output frequency (default same as dt)", type=int)
    parser.add_argument("outfreqU", help="Specify output frequency unit")
    parser.add_argument("coupledWW3", help="Specify if the run is coupled or not (WW3)")
    parser.add_argument("coupledCICE", help="Specify if the run is coupled or not (CICE)")
    parser.add_argument("--iceIc", help="Specify the name of a netCDF file that contains the initial condition of the ice (will only work for uncoupled simulation).")
    parser.add_argument("--repIceIc", help="Specify the path of netCDF file that contains the initial condition of the ice (will only work for uncoupled simulation).")
    args = parser.parse_args()

    #Define variables
    grid=args.grid
    outfreq=args.outfreq
    outfreqU=args.outfreqU
    timeStep=args.dt
    coupledWW3=args.coupledWW3
    coupledCICE=args.coupledCICE
    nb_ts=args.nts
    list_varFSD=['dafsd_newi', 'dafsd_latg', 'dafsd_latm', 'dafsd_weld', 'dafsd_wave']
    
    if coupledWW3 == "true"  and coupledCICE == "true":
        coupled="true"
    else:
        coupled="false"

    #list_var=['aice_ww', 'hice_ww', 'diam_ww'] #,'ic1','ic5'] #Ice concentration, Ice thickness, Mean floe size diameter

    start_y=args.start_y
    start_d=args.start_d
    start_m=args.start_m
    start_s=args.start_s    
    start_day=datetime(start_y, start_m, start_d)+timedelta(seconds=start_s)
    list_ts=createListDateTime(start_day, outfreq, outfreqU, nb_ts)
    REP_IN_W3=args.rep_inW3
    REP_IN_CICE=args.rep_inCI
    REP_OUT=args.rep_out
    exp=args.case

    if grid == 'wim2p5':
        grdRes=2.5
        grdMax=247.5
        grdMin=-2.5
        xgrid=np.arange(grdMin, grdMax, grdRes)
        ygrid=np.arange(grdMin, grdMax, grdRes)
    elif grid == 'wimgx3':
        datetimeStart=start_day
        if coupled == "true":
            file_strt="ww3."+datestrStart+".nc"
            rep_strt=REP_IN_W3
            nlon, nlat, t_lat, t_lon = get_geomWW3(rep_strt, file_strt)
        elif coupledWW3 == "false":
            datestrStart=str(datetimeStart.year).zfill(4)+str(datetimeStart.month).zfill(2)+str(datetimeStart.day).zfill(2)+"T"+str(datetimeStart.hour).zfill(2)+"Z"
            if (args.iceIc is None or args.repIceIc is None):
                file_strt="ww3."+datestrStart+".nc"
                rep_strt=REP_IN_W3
            else:
                file_strt=args.iceIc
                rep_strt=args.repIceIce
            nlon, nlat, t_lat, t_lon = get_geomWW3(rep_strt, file_strt)
        elif coupledCICE == "false":
            #Take any file in the CICE out directory. 
            rep_strt=REP_IN_CICE
            cmd_list="ls "+rep_strt+"/"+"| tail -n 1"
            file_strt = str(subprocess.check_output(cmd_list, shell=True).rstrip())[2:-1]
            nlon, nlat, t_lat, t_lon=get_geomCICE(rep_strt, file_strt)

    i=1
    #Plot at each timestep
    for ts in list_ts:
        datetimeW3=ts
        if coupled == "true":
            # Keep it like this for now.
            print("Coupled")
            print("Time step "+str(i)+":",datetimeW3)
            datetimeCI=ts+timedelta(seconds=timeStep)
            datestrW3=str(datetimeW3.year).zfill(4)+"-"+str(datetimeW3.month).zfill(2)+"-"+str(datetimeW3.day).zfill(2)+"-"+str(datetimeW3.hour*3600).zfill(5)
            datestrCI=str(datetimeCI.year).zfill(4)+"-"+str(datetimeCI.month).zfill(2)+"-"+str(datetimeCI.day).zfill(2)+"-"+str(datetimeCI.hour*3600).zfill(5)
            fileCI="iceh_01h."+datestrCI+".nc"
            fileW3="ww3."+datestrW3+".nc"
            print("CICE file : "+fileCI, "WW3 file : "+fileW3)
        elif coupledCICE == "false":
            #If not coupled : no wave field
            if outfreqU == 's':
                datetimeCI=ts+timedelta(seconds=timeStep)
                datestrCI=str(datetimeCI.year).zfill(4)+"-"+str(datetimeCI.month).zfill(2)+"-"+str(datetimeCI.day).zfill(2)+"-"+str(datetimeCI.hour*3600).zfill(5)
                fileCI="iceh_01h."+datestrCI+".nc"
            elif outfreqU == 'h':
                datetimeCI=ts+timedelta(seconds=timeStep)
                datestrCI=str(datetimeCI.year).zfill(4)+"-"+str(datetimeCI.month).zfill(2)+"-"+str(datetimeCI.day).zfill(2)+"-"+str(datetimeCI.hour*3600).zfill(5)
                fileCI="iceh_01h."+datestrCI+".nc"
            elif outfreqU == 'd':
                datetimeCI=ts
                datestrCI=str(datetimeCI.year).zfill(4)+"-"+str(datetimeCI.month).zfill(2)+"-"+str(datetimeCI.day).zfill(2)
                fileCI="iceh."+datestrCI+".nc"
            elif outfreqU == 'm':
                datetimeCI=ts
                datestrCI=str(datetimeCI.year).zfill(4)+"-"+str(datetimeCI.month).zfill(2)
                fileCI="iceh."+datestrCI+".nc"
            elif outfreqU == 'y':
                datetimeCI=ts
                datestrCI=str(datetimeCI.year).zfill(4)
                fileCI="iceh."+datestrCI+".nc"
            print("Uncoupled CICE simulation")
            print("Time step "+str(i)+":",datetimeCI)
            print("CICE file : "+fileCI)

            plotChangeFSD(REP_IN_CICE, fileCI, nlon, nlat, t_lat, t_lon, REP_OUT, exp, datestrCI, 'pcolor', list_varFSD)
        i=i+1

#Call main
if __name__ == "__main__":
    main()
