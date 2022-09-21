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

def plotWaveIceRegrid(REP_IN_CICE, fileCI, REP_IN_W3, fileW3, nlon, nlat, lat, lon, repOUT, case, datestr, plot_type, list_var):

    '''This function plots CICE data and creates a .png file.'''

    from mpl_toolkits.basemap import Basemap,shiftgrid
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    orig_map=plt.cm.get_cmap('Spectral')
    reversed_map = orig_map.reversed()
    
    # Suppress Matplotlib deprecation warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    fig, axes = plt.subplots(len(list_var),1,figsize=[14,8*len(list_var)])
    i=0
    for var in list_var:

        #Read the datas
        dataCI=read_data(REP_IN_CICE, [fileCI], var, nlon, nlat)
        data=dataCI
        dataW3=read_data(REP_IN_W3, [fileW3], 'hs', nlon, nlat)
        dataUwind=read_data(REP_IN_W3, [fileW3], 'uwnd', nlon, nlat)
        dataVwind=read_data(REP_IN_W3, [fileW3], 'vwnd', nlon, nlat)

        plt.sca(axes[i])

        #Choose projection
#        m = Basemap(projection='npstere', boundinglat=35,lon_0=270, resolution='l')
#        m = Basemap(projection='spstere', boundinglat=-45,lon_0=270, resolution='l')

        m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
        m.drawcoastlines()

        if plot_type == 'scatter':
            x, y = m(lon,lat)
            sc = m.scatter(x, y, c=data, cmap=reversed_map, lw=0, s=4)
        else:

            # vector_transform require for the longitude to be from -180 to 180 in order,
            # Therefore we have to replace all the data in order.
            lon1 = lon.copy()
            for t in range(len(lon)):
                l=lon[t]
                if l >= 180:
                    lon1[t]=lon1[t]-360. 
            lon = lon1
            
            data1 = data[:,0:int(len(lon)/2)]
            data2 = data[:,60:]
            dataW31 = dataW3[:,0:60]
            dataW32 = dataW3[:,60:]
            dataUwind1 = dataUwind[:,0:60]
            dataUwind2 = dataUwind[:,60:]
            dataVwind1 = dataVwind[:,0:60]
            dataVwind2 = dataVwind[:,60:]

            mask1 = data.mask[:,0:60]
            mask2 = data.mask[:,60:]
            maskwind1 = dataUwind.mask[:,0:60]
            maskwind2 = dataVwind.mask[:,60:]
            maskhs1 = dataW3.mask[:,0:60]
            maskhs2 = dataW3.mask[:,60:]

            lon1 = lon[0:60]
            lon2 = lon[60:]            

            data_new = np.hstack((data2, data1))
            dataUwind_new = np.hstack((dataUwind2, dataUwind1))
            dataVwind_new = np.hstack((dataVwind2, dataVwind1))
            dataW3_new = np.hstack((dataW32, dataW31))

            mask_new=np.hstack((mask2, mask1))
            maskhs_new=np.hstack((maskhs2, maskhs1))
            maskwind_new=np.hstack((maskwind2, maskwind1))

            lon_new = np.hstack((lon2, lon1))

            # Patch the discontinuity data (cyclic longitude).
            # Create new array.
            d = np.zeros((data.shape[0],data.shape[1]+1))
            dW3 = np.zeros((dataW3.shape[0],dataW3.shape[1]+1))
            dUwind = np.zeros((dataUwind.shape[0],dataUwind.shape[1]+1)) 
            dVwind = np.zeros((dataVwind.shape[0],dataVwind.shape[1]+1)) 
            lon_cyc = np.zeros(len(lon_new)+1)
            mask = np.zeros((data.shape[0],data.shape[1]+1))
            maskwind=np.zeros((data.shape[0],data.shape[1]+1))
            maskhs=np.zeros((data.shape[0],data.shape[1]+1))

            #Fill masks.
            mask[:,0:-1] = mask_new[:,:]
            mask[:,-1] = mask_new[:,0]
            maskwind[:,0:-1] = maskwind_new[:,:]
            maskwind[:,-1] = maskwind_new[:,0]
            maskhs[:,0:-1] = maskhs_new[:,:]
            maskhs[:,-1] = maskhs_new[:,0]

            #Fill datas.
            lon_cyc[0:-1] = lon_new[:]; lon_cyc[-1] = -lon_new[0]       
            d[:,0:-1] = data_new[:,:]
            d[:,-1] = data_new[:,0]
            dW3[:,0:-1] = dataW3_new[:,:]
            dW3[:,-1] = dataW3_new[:,0]        
            dUwind[:,0:-1] = dataUwind_new[:,:]
            dUwind[:,-1] = dataUwind_new[:,0]
            dVwind[:,0:-1] = dataVwind_new[:,:]
            dVwind[:,-1] = dataVwind_new[:,0]
        
            #Create masked datas
            d1 = np.ma.masked_array(d,mask=mask)
            d1Uwind=np.ma.masked_array(dUwind,mask=maskwind)
            d1Vwind=np.ma.masked_array(dVwind,mask=maskwind)
            d1hs=np.ma.masked_array(dW3,mask=maskhs)

            #Create the grid (longitude,latitude) and actual position in the projection (x,y)
            lons, lats = np.meshgrid(lon_cyc,lat)
            x, y = m(lons, lats)

            if plot_type == 'contour':
                # Plot ice field
                sc = m.contourf(x, y, d1, 10, cmap=reversed_map)
                # Rotate and interpolate wind for a clean reprensation of vectors in the projection.
                uproj,vproj,xx,yy = m.transform_vector(dUwind,dVwind,lon_cyc,lat,41,41,returnxy=True,masked=True)
                # Plot winds
                Q=axes[i].quiver(xx, yy, uproj, vproj)
                # Plot waves
                cont=axes[i].contour(x,y, dW3, colors='black')

                axes[i].quiverkey(Q, 0.1, 0.1, 20, '20 m/s', labelpos='W')
            else:  # pcolor
                sc = m.pcolor(x, y, d1, cmap=reversed_map)
                uproj,vproj,xx,yy = m.transform_vector(d1Uwind,d1Vwind,lon_cyc,lat,41,41,returnxy=True,masked=True)
                axes[i].barbs(xx, yy, uproj, vproj, length=6, pivot='middle')
                cont=axes[i].contour(x,y, dW3, colors='black')

        m.drawparallels(np.arange(-90.,120.,15.),labels=[1,0,0,0], size=16) # draw parallels
        m.drawmeridians(np.arange(0.,420.,30.),labels=[1,1,1,1], size=16) # draw meridians
        cb=fig.colorbar(sc, ax=axes[i])
        cb.ax.tick_params(labelsize=18)
        axes[i].clabel(cont, fontsize= 12)
        if var == 'ice' or var == 'aice':
            cb.set_label('Ice Concentration', size=20)
        elif var == 'ic1' or var == 'hi':
            cb.set_label('Ice Thickess [m]', size=20)
        elif var == 'ic5' or var == 'fsdrad':
            cb.set_label('Mean Floe Diameter [m]', size=20)
        elif var == 'airtmp':
            cb.set_label('Air temperature', size=20)
        elif var == 'glbrad':
            cb.set_label('Surface downward shortwave', size=20)
        i=i+1

    plt.tight_layout()
    plt.subplots_adjust(top=0.97)
    plt.savefig(repOUT+"/"+case+"_WaveIce_"+datestr, bbbox_to_anchor='tight', dpi=500)
    print("------------"+case+"_WaveIce_"+datestr+" as been plotted---------------------")


def plotWaveIceGx3(REP_IN_CICE, fileCI, REP_IN_W3, fileW3, nlon, nlat, lat, lon, repOUT, case, datestr, plot_type, list_var):

    '''This function plots CICE data and creates a .png file.'''
    from mpl_toolkits.basemap import Basemap
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    orig_map=plt.cm.get_cmap('Spectral')
    reversed_map = orig_map.reversed()

    # Suppress Matplotlib deprecation warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    wnd_var=['uwnd', 'vwnd']
    fig, axes = plt.subplots(len(list_var),1,figsize=[14,8*len(list_var)])
    i=0
    for var in list_var:
       #Read ice field and wave field.
       data=read_data(REP_IN_CICE, [fileCI], var, nlon, nlat)
       
       if fileW3 != "none":
           dataW3=read_data(REP_IN_W3, [fileW3], 'hs', nlon, nlat)

       plt.sca(axes[i])

       #Choose projection
#       m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
#       m = Basemap(projection='spstere', boundinglat=-45,lon_0=270, resolution='l')
#       m = Basemap(width=12000000,height=8000000,resolution='l',projection='stere',lat_0=90,lon_0=270)
#       m = Basemap(projection='ortho',lon_0=270,lat_0=40,resolution='l')
       m = Basemap(projection='npstere', boundinglat=35,lon_0=270, resolution='l')
       m.drawcoastlines()

       if plot_type == 'scatter':
           x, y = m(lon,lat)
           sc = m.scatter(x, y, c=data, cmap=reversed_map, lw=0, s=4)
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

           #Idem with waves
           if fileW3 != "none":
               dW3 = np.zeros((dataW3.shape[0],dataW3.shape[1]+1))
               maskhs=np.zeros((data.shape[0],data.shape[1]+1))
               maskhs[:,0:-1] = dataW3.mask[:,:]
               maskhs[:,-1] = dataW3.mask[:,0]
               dW3[:,0:-1] = dataW3[:,:]
               dW3[:,-1] = dataW3[:,0]
               d1hs=np.ma.masked_array(dW3,mask=maskhs)

           x, y = m(lon_cyc, lat_cyc)

           if plot_type == 'contour':
               #Plot ice fields
               sc = m.contourf(x, y, d1, cmap=reversed_map)
               #Plot contours
               if fileW3 != "none":
                   cont=axes[i].contour(x,y, d1hs, colors='black') #, levels=[0.02, 0.04, 0.06, 0.1, 0.14, 0.2])
                   if(len(cont.allsegs) != 1):
                       axes[i].clabel(cont, fontsize= 12)
               # Rotate and interpolate to have a nice wind field in the projection.
               uproj, vproj, xwind, ywind = create_wind_projection(REP_IN_W3, fileW3, REP_IN_CICE, fileCI, m, wnd_var,nlon,nlat)
               # Plot winds
               Q = m.quiver(xwind, ywind,uproj,vproj,scale=250)
           else:  # pcolor
               sc = m.pcolor(x, y, d1, cmap=reversed_map)
               if fileW3 != "none":
                   cont=axes[i].contour(x,y, d1hs, colors='black') #, levels=[0.02, 0.04, 0.06, 0.1, 0.14, 0.2])
                   if(len(cont.allsegs) != 1):
                       axes[i].clabel(cont, fontsize= 12)
    #               uproj, vproj, xwind, ywind = create_wind_projection(REP_IN_W3, fileW3, REP_IN_CICE, fileCI,  m, wnd_var, nlon, nlat)
    #               axes[i].barbs(xwind, ywind, uproj, vproj, length=4, pivot='middle')

       m.drawparallels(np.arange(-90.,120.,15.),labels=[1,0,0,0], size=16) # draw parallels
       m.drawmeridians(np.arange(0.,420.,30.),labels=[1,1,1,1], size=16) # draw meridians
       cb=fig.colorbar(sc, ax=axes[i])
       cb.ax.tick_params(labelsize=18)

       if var == 'ice' or var == 'aice':
          cb.set_label('Ice Concentration', size=20)
       elif var == 'ic1' or var == 'hi':
          cb.set_label('Ice Thickess [m]', size=20)
       elif var == 'ic5' or var == 'fsdrad':
          cb.set_label('Mean Floe Diameter [m]', size=20)

       i=i+1

    plt.tight_layout()
    plt.subplots_adjust(top=0.97)
    plt.savefig(repOUT+"/"+case+"_WaveIce_"+datestr, bbbox_to_anchor='tight', dpi=500)
    print("------------"+case+"_WaveIce_"+datestr+" as been plotted---------------------")

def create_wind_projection(path_a, file_a, path_g, file_g, basem, wind_var, nlon, nlat):
    '''
    Read wind from WW3 output in the WIM coupled framework. Then rotate it according to the Basemap projection
    Then copy into a new file
    Then interpolate
    '''
    import pandas as pd
    import xarray as xr
    #Read file uwnd and vwnd (pourrait etre remplacer par un readata).
    file_data=path_a+"/"+file_a
    name=file_a[:-3]
    file_wind=path_a+"/"+name+"_wnd.nc"

#    dsData=xr.open_dataset(file_data)
#    dsData=dsData[wind_var]
    for wnd in wind_var:
        if wnd=='uwnd' or wnd=='wndewd':
             uwind=read_data(path_a, [file_a], wnd, nlon, nlat)*1.9434
   #         uwind=np.nan_to_num(dsData[[wnd]][wnd].values.squeeze())*1.9434
        elif wnd=='vwnd' or wnd=='wndnwd':
             vwind=read_data(path_a, [file_a], wnd, nlon, nlat)*1.9434
    #        vwind=np.nan_to_num(dsData[[wnd]][wnd].values.squeeze())*1.9434

    #Creer un nouveau dataset avec juste le vent  dedans.
    df = pd.DataFrame()
    dsWind=df.to_xarray()
    dsWind['uwnd']=(("latitude","longitude"),uwind)
    dsWind['vwnd']=(("latitude","longitude"),vwind)
    dsWind.to_netcdf(file_wind)

    #Copier la grille dans le data set.
    grid_info=path_a+"/griddes.info"
    file_grid=path_g+"/"+file_g
    os.system('/opt/cdo/bin/cdo griddes '+file_grid+">"+grid_info)
    os.system("sed -i '/gridtype  = curvilinear/,$!d' "+grid_info)
    os.system('/opt/cdo/bin/cdo setgrid,'+grid_info+" "+file_wind+" "+file_wind+"_grd>/dev/null 2>&1")
    os.system('rm -f '+file_wind)
    os.system('mv '+file_wind+"_grd "+file_wind)

    #Creer le fichier de directive pour l'interpolation sur une grille equilibre dependamment de la projection.
    lonsout, latsout=basem.makegrid(41,41)
    new_grid_info=path_a+"/remap_griddes.info"
    np.savetxt(path_a+"/lat_remap.dat", latsout[:,1], fmt='%.2f')
    np.savetxt(path_a+"/lon_remap.dat", lonsout[1], fmt='%.2f')
   
    os.system("echo 'gridtype     = lonlat' > "+new_grid_info)
    os.system("echo 'gridsize     = '"+str(latsout.shape[0]*latsout.shape[1])+" >> "+new_grid_info)
    os.system("echo 'xsize     = '"+str(latsout.shape[0])+" >> "+new_grid_info)
    os.system("echo 'ysize     = '"+str(latsout.shape[1])+" >> "+new_grid_info)
    os.system("echo 'xvals     =' >> "+new_grid_info+" && cat "+path_a+"/lon_remap.dat >>"+new_grid_info)
    os.system("echo 'yvals     =' >> "+new_grid_info+" && cat "+path_a+"/lat_remap.dat >>"+new_grid_info)

    #Interpolate
    os.system('/opt/cdo/bin/cdo remapbil,'+new_grid_info+" "+file_wind+" "+file_wind+"_interp>/dev/null 2>&1")
    os.system('rm -f '+file_wind)
    os.system('mv '+file_wind+"_interp"+" "+file_wind)

    dsWind_new=xr.open_dataset(file_wind)
    dsWind_new=dsWind_new[wind_var]
    #Rotate in the projection
    for wnd in wind_var:
        if wnd=='uwnd' or wnd=='wndewd':
             uwind_new=read_data(path_a, [name+"_wnd.nc"], wnd, 41, 41)
#             uwind_new=np.nan_to_num(dsWind_new[[wnd]][wnd].values.squeeze())
        elif wnd=='vwnd' or wnd=='wndnwd':
             vwind_new=read_data(path_a, [name+"_wnd.nc"], wnd, 41, 41)
#             vwind_new=np.nan_to_num(dsWind_new[[wnd]][wnd].values.squeeze())
    lat_new=np.nan_to_num(dsWind_new[['lat']]['lat'].values.squeeze())
    lon_new=np.nan_to_num(dsWind_new[['lon']]['lon'].values.squeeze())
#    lat_new=read_data(path_a, [name+"_wnd.nc"], 'lat', 41, 41)
#    lon_new=read_data(path_a, [name+"_wnd.nc"], 'lon', 41, 41)
    urot,vrot,xx,yy = basem.rotate_vector(uwind_new,vwind_new,lon_new,lat_new,returnxy=True)

    urot_cyc = np.zeros((urot.shape[0],urot.shape[1]+1))
    vrot_cyc = np.zeros((vrot.shape[0],vrot.shape[1]+1))
    xx_cyc = np.zeros((xx.shape[0],xx.shape[1]+1))
    yy_cyc = np.zeros((yy.shape[0],yy.shape[1]+1))
    mask = np.zeros((urot.shape[0],urot.shape[1]+1))

    urot_cyc[:,0:-1] = urot[:,:]; urot_cyc[:,-1] = urot[:,0]
    vrot_cyc[:,0:-1] = vrot[:,:]; vrot_cyc[:,-1] = vrot[:,0]
    xx_cyc[:,0:-1] = xx[:,:]; xx_cyc[:,-1] = xx[:,0]
    yy_cyc[:,0:-1] = yy[:,:]; yy_cyc[:,-1] = yy[:,0]
    mask[:,0:-1] = urot.mask[:,:]; mask[:,-1] = urot.mask[:,0]

    urot_cycM=np.ma.masked_array(urot_cyc,mask=mask)
    vrot_cycM=np.ma.masked_array(vrot_cyc,mask=mask)

    return urot_cycM,vrot_cycM,xx_cyc,yy_cyc

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
        data[:, :] = nfid.variables[var][:]
        nfid.close()
            
        data[data == fill_value] = 0.0

        return data
    
    data_a = fill_data_array(path_a, files_a, nj, ni)
    mask_array_a = np.zeros_like(data_a)

    if var == 'uwnd':
        var='vwnd'
        dataV=fill_data_array(path_a, files_a, nj, ni)
        dataSpeed=np.sqrt(np.square(data_a)+np.square(dataV))
        mask_array_a = np.logical_or(dataSpeed == 0., dataSpeed < 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'vwnd':
        var='uwnd'
        dataU=fill_data_array(path_a, files_a, nj, ni)
        dataSpeed=np.sqrt(np.square(data_a)+np.square(dataU))
        mask_array_a = np.logical_or(dataSpeed == 0., dataSpeed < 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'hs':
        mask_array_a = np.logical_or(data_a == 0., data_a < 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'ice' or var == 'aice':
#         mask_array_a = np.logical_or(\
#                        np.logical_or(\
#                             np.all(np.equal(data_a, 0.), axis=0), np.all(data_a < 0.01, axis=0))
#                        , np.all(data_a < 0.01, axis=0))
        mask_array_a = np.logical_or(data_a == 0., data_a < 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'ic1' or var == 'hi':
        mask_array_a = np.logical_or(data_a == 0., data_a < 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'ic5' or var == 'fsdrad':
        mask_array_a = np.logical_or(data_a == 0., data_a < 0)
        data_a = ma.masked_array(data_a, mask=mask_array_a)
    elif var == 'airtmp':
        data_a=data_a-273.15
#    if var == 'uwnd' or var == 'vwnd':
#        mask_array_a = np.logical_or(\
#                       np.logical_or(\
#                            np.all(np.equal(data_a, 0.), axis=0), np.all(data_a < 1, axis=0))
#                       , np.all(data_a < 1, axis=0))
#        data_a = ma.masked_array(data_a, mask=mask_array_a)
#     data_b = fill_data_array(path_b, files_b, nj, ni)

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


def plotWaveIceIdeal(fileCICE, fileWW3, repW3, repCI, repOUT, exp, datestr, xG, yG, listV):
    import xarray as xr
    warnings.filterwarnings("ignore", category=UserWarning)
    #orig_map=plt.cm.get_cmap('gist_earth')
    orig_map=plt.cm.get_cmap('Spectral')
    reversed_map = orig_map.reversed()

    file_dataW3=repW3+"/"+fileWW3
    file_dataCI=repCI+"/"+fileCICE

    print("File wave : ", file_dataW3)
    print("File ice : ", file_dataCI)
    
    dsW3=xr.open_dataset(file_dataW3)
    hs_2d=np.nan_to_num(dsW3[['hs']]['hs'].values.squeeze())
    dsCI=xr.open_dataset(file_dataCI)
    
    X,Y = np.meshgrid(xG,yG)
    fig, ax = plt.subplots(len(listV),1,figsize=[8,4*len(listV)])
    i=0
    for v in listV:
        if v == 'ic1' or v == 'ice' or v == 'ic5':
            var_2d=np.nan_to_num(dsW3[[v]][v].values.squeeze())
        else:
            var_2d=np.nan_to_num(dsCI[[v]][v].values.squeeze())
#        u_wind=np.nan_to_num(dsW3[['uwnd']]['uwnd'].values.squeeze())
#        v_wind=np.nan_to_num(dsW3[['vwnd']]['vwnd'].values.squeeze())
        ax[i].set_xlim([2.5, 240])
        ax[i].set_ylim([2.5, 240])
        ax[i].tick_params(labelsize=14)
        ax[i].set_xlabel('x [km]', size=16)
        ax[i].set_ylabel('y [km]', size=16)
        cont=ax[i].contour(X,Y, hs_2d, colors='black', levels=[0.01, 0.02, 0.04, 0.06, 0.1, 0.14, 0.2])
        color=ax[i].contourf(X,Y,var_2d, 50, cmap=reversed_map)
        #ax[i].barbs(X[0:100:10,0:100:10], Y[0:100:10,0:100:10], u_wind[0:100:10,0:100:10], v_wind[0:100:10,0:100:10], length=8, pivot='middle')
        ax[i].clabel(cont, fontsize= 12)
        cb=fig.colorbar(color, ax=ax[i])
        cb.ax.tick_params(labelsize=14)
        
        if v == 'ice' or v == 'aice':
            cb.set_label('Ice Concentration', size=16)
        if v == 'ic1' or v == 'hi':
            cb.set_label('Ice Thickess [m]', size=16)
        if v == 'ic5' or v == 'fsdrad':
            cb.set_label('Mean Floe Diameter [m]', size=16)
        i=i+1
        
    plt.tight_layout()
    plt.subplots_adjust(top=0.97)
    fig.savefig(repOUT+"/"+exp+"_WaveIce_"+datestr, bbbox_to_anchor='tight', dpi=500)
    print("------------"+exp+"_WaveIce_"+datestr+" as been plotted---------------------")

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

    if coupledWW3 == "true"  and coupledCICE == "true":
        coupled="true"
    else:
        coupled="false"

    #list_var=['aice_ww', 'hice_ww', 'diam_ww'] #,'ic1','ic5'] #Ice concentration, Ice thickness, Mean floe size diameter

    list_var=['aice', 'hi', 'fsdrad']
    #list_var=['ice', 'ice', 'ice']

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
            datestrStart=str(datetimeStart.year).zfill(4)+"-"+str(datetimeStart.month).zfill(2)+"-"+str(datetimeStart.day).zfill(2)+"-"+str(datetimeStart.hour*3600).zfill(5)
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
#            datetimeStrtCI=datetimeStart+timedelta(seconds=timeStep)
#            datestrStart=str(datetimeStart.year).zfill(4)+"-"+str(datetimeStart.month).zfill(2)+"-"+str(datetimeStart.day).zfill(2)+"-"+str(datetimeStart.hour*3600).zfill(5)
#            datestrStrtCI=str(datetimeStrtCI.year).zfill(4)+"-"+str(datetimeStrtCI.month).zfill(2)+"-"+str(datetimeStrtCI.day).zfill(2)+"-"+str(datetimeStrtCI.hour*3600).zfill(5)
#            file_strt="iceh_01h."+datestrStrtCI+".nc"
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
        elif coupledWW3 == "false":
            print("Uncoupled WW3 simulation")
            print("Time step "+str(i)+":",datetimeW3)
            #If only WW3 simulation : ice always initial ice field.
            datetimeCI=start_day+timedelta(seconds=timeStep)
            datestrW3=str(datetimeW3.year).zfill(4)+str(datetimeW3.month).zfill(2)+str(datetimeW3.day).zfill(2)+"T"+str(datetimeW3.hour).zfill(2)+"Z"
            fileCI="ice_forcing.nc"
            REP_IN_CICE="/aos/home/bward/wim/ww3/model/inp/"+exp #Temporary hardcode
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
            fileW3="none"
            datestrW3=datestrCI
            print("Uncoupled CICE simulation")
            print("Time step "+str(i)+":",datetimeCI)
            print("CICE file : "+fileCI, "WW3 file : "+fileW3)

        if grid == 'wim2p5':
            plotWaveIceIdeal(fileCI, fileW3, REP_IN_W3, REP_IN_CICE, REP_OUT, exp, datestrW3, xgrid, ygrid, list_var)
        elif grid == 'wimgx3':
            # Special case of regrided scenario (might delete).
            if len(t_lat.shape) == 1:
               plotWaveIceRegrid(rep_strt, file_strt, REP_IN_W3, fileW3, nlon, nlat, t_lat, t_lon, REP_OUT, exp, datestrW3, 'pcolor', list_var)
            elif len(t_lat.shape) == 2:
               plotWaveIceGx3(REP_IN_CICE, fileCI, REP_IN_W3, fileW3, nlon, nlat, t_lat, t_lon, REP_OUT, exp, datestrW3, 'pcolor', list_var)
        i=i+1

#Call main
if __name__ == "__main__":
    main()
