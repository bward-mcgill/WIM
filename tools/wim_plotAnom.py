#! /usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
from wim_dateTime import createListDateTime
from datetime import datetime, timedelta
import pandas as pd
import xarray as xr
import argparse
import subprocess
import warnings
import netCDF4 as nc
import numpy.ma as ma
import os
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib as mpl
import cmoocean as cmo
from matplotlib import cm
# import cmocean
# import cmocean.cm as cmo


def defineCBAnom(variable, var):

    #cmap=cmo.balance()
    cmap=plt.cm.RdBu
    v_lim = max([abs(variable.max()),abs(variable.min())])
    # print(variable.max())
    if var == 'aice':
        #cmap=cmo.crop(cmap,vmax=0.012,vmin=-0.012,pivot=0, N=13, dmax=0.012)
        bounds = [-0.12,-0.1,-0.08,-0.06,-0.04,-0.02, 0.02,0.04,0.06, 0.08,0.1,0.12]
        bounds = [x*0.2 for x in bounds]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    elif var == 'hi':
        #cmap=cmo.crop(cmap,vmax=variable.max(),vmin=variable.min(),pivot=0)
        bounds = [-0.12,-0.1,-0.08,-0.06,-0.04,-0.02, 0.02,0.04,0.06, 0.08,0.1,0.12]
        bounds = [x*0.5 for x in bounds]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    elif var == 'fsdrad':
        bounds = [-600,-500,-400,-300,-200,-100,-50,50,100,200,300,400,500,600]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    elif var == 'hs':
        bounds = [-600,-500,-400,-300,-200,-100,-50,50,100,200,300,400,500,600]
        bounds = [x*0.0001 for x in bounds]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    else :
        cmap=cmo.crop(cmap,vmax=variable.max(),vmin=variable.min(),pivot=0)
    #v_lim = max([abs(variable.max()),abs(variable.min())])

# if var == 'aice':
# elif var == 'hi':
# elif var == 'fsdrad':
# elif var == 'dafsd_newi' or var == 'dafsd_latg' or var == 'dafsd_latm' or var == 'dafsd_weld' or var == 'dafsd_wave':
# elif var == 'hs' or var == 'lm':
# elif var == 'strwv' or var == 'strair':
# elif var == 'sst'

    return cmap, norm


def defineCB(variable, var):

    path_colormap="/aos/home/bward/wim/post-proc/cmo_colormap/"

    if var == 'aice':
        cmap=cmo.ice()
        bounds = [0, 0.05, 0.10, 0.15, 0.20, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.995, 0.996,0.997, 0.998, 0.999, 1]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'hi':
        # cmap=cmo.matter().reversed()
        cmap=plt.cm.Spectral.reversed()
        bounds = [0, 0.2, 0.4, 0.6, 0.8, 1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.6, 4]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'fsdrad':
        # cmap2=cmo.curl()
        # cmap=cmo.curl_pink().reversed()
        # test=cmap.colors
        # test2=cmap2.colors
        # test3=np.concatenate((test2,test))
        # cmap=ListedColormap(test3)
        cmap=cmo.matter()
        bounds = [0, 10, 30, 60, 100, 180, 280, 424, 600, 860, 1160, 1500, 2000]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'dafsd_newi' or var == 'dafsd_latg' or var == 'dafsd_weld' :
        cmap=plt.cm.YlGnBu
        bounds = [0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        bounds = [x*10**-6 for x in bounds]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'dafsd_wave':
        cmap=plt.cm.YlOrRd
        bounds = [0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        bounds = [x*10**-6 for x in bounds]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'dafsd_latm':
        cmap=plt.cm.YlOrRd.reversed()
        bounds = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.15, -0.1, -0.05, 0]
        bounds = [x*10**-6 for x in bounds]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'hs':
        cmap=cmo.amp().reversed()
        bounds = levels=[0.01, 0.05, 0.1, 0.2, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'strair' :
        cmap=cmo.speed()
        bounds = [0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        bounds = [2*x*10**-1 for x in bounds]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'strwv':
        cmap=cmo.speed()
        bounds = [0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        bounds = [2*x*10**-2 for x in bounds]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'strnorm':
        cmap=cmo.speed()
        bounds=[0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    elif var == 'lm':
        cmap=cmo.curl().reversed()
        bounds = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
    else:
        cmap=plt.cm.Blues
    
    return cmap,norm


def plotOneVar(dataCol, dataCont, dataVec, lat, lon, repOUT, case, case2, datestr, plot_type, m, var):

    '''This function plots CICE data and creates a .png file.'''

    cmap, norm=defineCBAnom(dataCol, var)
    # orig_map=plt.cm.get_cmap('Spectral')
    # reversed_map = orig_map.reversed()

    # Suppress Matplotlib deprecation warnings
    warnings.filterwarnings("ignore", category=UserWarning)

    fig, axes = plt.subplots(1,1,figsize=[14,8])

    plt.sca(axes)

    #Choose projection
    m.drawcoastlines()
    m.fillcontinents()

    # Longitude need to be between -180 and 180 for plotting
    lon1 = lon.copy()
    for lt in range(lon.shape[0]):
        for lg in range(lon.shape[1]):
            pt=lon[lt,lg]
            if pt >= 180:
                lon1[lt,lg]=lon1[lt,lg]-360. 
    lon = lon1

    #No need for reordering the datas, just create empty arrays.
    d = np.zeros((dataCol.shape[0],dataCol.shape[1]+1))
    lon_cyc = np.zeros((lon.shape[0],lon.shape[1]+1))
    mask = np.zeros((dataCol.shape[0],dataCol.shape[1]+1))
    lat_cyc = np.zeros((lat.shape[0],lat.shape[1]+1))
    #Simply fill the arrays
    mask[:,0:-1] = dataCol.mask[:,:]
    mask[:,-1] = dataCol.mask[:,0]
    lon_cyc[:,0:-1] = lon[:,:]; lon_cyc[:,-1] = lon[:,0]
    lat_cyc[:,0:-1] = lat[:,:]; lat_cyc[:,-1] = lat[:,0]
    d[:,0:-1] = dataCol[:,:]
    d[:,-1] = dataCol[:,0]
    # Apply mask to ice field
    d1 = np.ma.masked_array(d,mask=mask)

    #Idem with contour
    if dataCont.size != 0:
        dCont = np.zeros((dataCont.shape[0],dataCont.shape[1]+1))
        maskCont=np.zeros((dataCont.shape[0],dataCont.shape[1]+1))
        maskCont[:,0:-1] = dataCont.mask[:,:]
        maskCont[:,-1] = dataCont.mask[:,0]
        dCont[:,0:-1] = dataCont[:,:]
        dCont[:,-1] = dataCont[:,0]
        d1Cont=np.ma.masked_array(dCont,mask=maskCont)
    
    # if dataVec[0].size != 0 and dataVec[1].size != 0:
    #     dataVecX=dataVec[0]
    #     dataVecY=dataVec[1]
    #     dVecX = np.zeros((dataVecX.shape[0],dataVecX.shape[1]+1))
    #     dVecY = np.zeros((dataVecY.shape[0],dataVecY.shape[1]+1))
    #     maskVec=np.zeros((dataVecX.shape[0],dataVecX.shape[1]+1))
    #     maskVec[:,0:-1] = dataVecX.mask[:,:]
    #     maskVec[:,-1] = dataVecX.mask[:,0]
    #     dVecX[:,0:-1] = dataVecX[:,:]
    #     dVecX[:,-1] = dataVecX[:,0]
    #     d1VecX=np.ma.masked_array(dVecX,mask=maskVec)
    #     dVecY[:,0:-1] = dataVecY[:,:]
    #     dVecY[:,-1] = dataVecY[:,0]
    #     d1VecY=np.ma.masked_array(dVecY,mask=maskVec)


    x, y = m(lon_cyc, lat_cyc)

    if plot_type == 'contour':
        #Plot ice fields
        sc = m.contourf(x, y, d1, cmap=reversed_map)
        #Plot contour
        if dataCont.size != 0:
            cont=axes.contour(x,y, d1Cont, colors='black', levels=[0.15])
            if(len(cont.allsegs) != 1):
                axes.clabel(cont, fontsize= 12)
        #         axes.clabel(cont, fontsize= 12)
        # # Rotate and interpolate to have a nice wind field in the projection.
        # uproj, vproj, xwind, ywind = create_wind_projection(REP_IN_W3, fileW3, REP_IN_CICE, fileCI, m, wnd_var,nlon,nlat)
        # # Plot winds
        # Q = m.quiver(xwind, ywind,uproj,vproj,scale=250)
    else:  # pcolor
        sc = m.pcolor(x, y, d1, cmap=cmap, norm=norm)
#Temporary?
        if dataCont.size != 0:
            cont=axes.contour(x,y, d1Cont, colors='k', levels=[0.15, 0.8])
            if(len(cont.allsegs) != 1):
                axes.clabel(cont, fontsize= 12)

        if dataVec[0].size != 0:
            xwind=dataVec[2]
            ywind=dataVec[3]
            uproj=dataVec[0]
            vproj=dataVec[1]
            norm=np.sqrt(uproj**2+vproj**2)
            mask=np.logical_or(norm<0, norm==0)
            uprojM=ma.masked_array(uproj, mask=mask)
            vprojM=ma.masked_array(vproj, mask=mask)
            scaleFac=np.amax(uproj+vproj)
            axes.quiver(xwind, ywind, uprojM, vprojM) #, scale = 800/25*scaleFac,  pivot='middle')
#            axes.barbs(x,y,d1VecX, d1VecY, length=4, pivot='middle')

    m.drawparallels(np.arange(-90.,120.,15.),labels=[1,0,0,0], size=16) # draw parallels
    m.drawmeridians(np.arange(0.,420.,30.),labels=[1,1,0,1], size=16) # draw meridians
    cb=fig.colorbar(sc, ax=axes)
    cb.ax.tick_params(labelsize=18)

    if var == 'ice' or var == 'aice':
        cb.set_label('Ice Concentration', size=20)
    elif var == 'ic1' or var == 'hi':
        cb.set_label('Ice Thickess [m]', size=20)
    elif var == 'ic5' or var == 'fsdrad':
        cb.set_label('Mean Floe Diameter [m]', size=20)
    elif var == 'dafsd_newi':
        cb.set_label('Change in FSD(12) : new ice [1/s]', size=20)
    elif var == 'dafsd_weld':
        cb.set_label('Change in FSD(12) : weld. [1/s]', size=20)
    elif var == 'dafsd_latg':
        cb.set_label('Change in FSD(1) : lat. g. [1/s]', size=20)
    elif var == 'dafsd_latm':
        cb.set_label('Change in FSD(1) : lat. m. [1/s]', size=20)
    elif var == 'dafsd_wave':
        cb.set_label('Change in FSD(1) : wave [1/s]', size=20)
    elif var == 'strair':
        cb.set_label('Wind Stress [N/m2]', size=20)
    elif var == 'strwv':
        cb.set_label('Wave Radiation Stress [N/m2]', size=20)
    elif var == 'strnorm':
        cb.set_label('Normalized Stress [1]', size=20)
    elif var == 'hs':
        cb.set_label('Significant Wave Height [m]', size=20)
    elif var == 'lm':
        cb.set_label('Average Wavelenght', size=20)

    axes.set_title(datestr, fontsize=20)
    plt.tight_layout()
    plt.subplots_adjust(top=0.97)
#    plt.savefig(repOUT+"/"+case+"_WaveIce_"+datestr, bbbox_to_anchor='tight', dpi=500)
    plt.savefig(repOUT+"/anom_"+case+"-"+case2+"_"+datestr+"_"+var+".png",dpi='figure',format='png',metadata=None, bbbox_inches='tight')
    print("------------"+"anom_"+case+"-"+case2+"_"+datestr+"_"+var+" as been plotted---------------------")


def create_wind_projection(dataX, dataY, path_g, file_g, path_out, basem, nlon, nlat):
    '''
    Read wind from WW3 output in the WIM coupled framework. Then rotate it according to the Basemap projection
    Then copy into a new file
    Then interpolate
    '''
    #Read file uwnd and vwnd (pourrait etre remplacer par un readata).
    file_data=path_g+"/"+file_g
    name=file_g[:-3]
    file_wind=path_out+"/"+name+"_vec.nc"

   #Creer un nouveau dataset avec juste le vent  dedans.
    df = pd.DataFrame()
    dsWind=df.to_xarray()
    dsWind['vecX']=(("latitude","longitude"),dataX)
    dsWind['vecY']=(("latitude","longitude"),dataY)
    dsWind.to_netcdf(file_wind)

    # Copier la grille dans le data set.
    grid_info=path_out+"/griddes.info"
    file_grid=path_g+"/"+file_g
    os.system('/opt/cdo/bin/cdo griddes '+file_grid+">"+grid_info)
    os.system("sed -i '/gridtype  = curvilinear/,$!d' "+grid_info)
    os.system('/opt/cdo/bin/cdo setgrid,'+grid_info+" "+file_wind+" "+file_wind+"_grd>/dev/null 2>&1")
    os.system('rm -f '+file_wind)
    os.system('mv '+file_wind+"_grd "+file_wind)

    # Creer le fichier de directive pour l'interpolation sur une grille equilibre dependamment de la projection.
    lonsout, latsout=basem.makegrid(31,31)
    new_grid_info=path_out+"/remap_griddes.info"
    np.savetxt(path_out+"/lat_remap.dat", latsout, fmt='%.2f')
    np.savetxt(path_out+"/lon_remap.dat", lonsout, fmt='%.2f')

   
    os.system("echo 'gridtype     = curvilinear' > "+new_grid_info)
    os.system("echo 'gridsize     = '"+str(latsout.shape[0]*latsout.shape[1])+" >> "+new_grid_info)
    os.system("echo 'xsize     = '"+str(latsout.shape[0])+" >> "+new_grid_info)
    os.system("echo 'ysize     = '"+str(latsout.shape[1])+" >> "+new_grid_info)
    os.system("echo 'xvals     =' >> "+new_grid_info+" && cat "+path_out+"/lon_remap.dat >>"+new_grid_info)
    os.system("echo 'yvals     =' >> "+new_grid_info+" && cat "+path_out+"/lat_remap.dat >>"+new_grid_info)

    #Interpolate
    os.system('/opt/cdo/bin/cdo remapbil,'+new_grid_info+" "+file_wind+" "+file_wind+"_interp>/dev/null 2>&1")
    os.system('rm -f '+file_wind)
    os.system('mv '+file_wind+"_interp"+" "+file_wind)

    dsWind_new=xr.open_dataset(file_wind)
    #Rotate in the projection
    uwind_new=np.squeeze(np.nan_to_num(dsWind_new['vecX'].values))
    vwind_new=np.squeeze(np.nan_to_num(dsWind_new['vecY'].values))

    lon_new=np.nan_to_num(dsWind_new[['lon']]['lon'].values.squeeze())
    lat_new=np.nan_to_num(dsWind_new[['lat']]['lat'].values.squeeze())
# #    lat_new=read_data(path_a, [name+"_wnd.nc"], 'lat', 41, 41)
# #    lon_new=read_data(path_a, [name+"_wnd.nc"], 'lon', 41, 41)
    urot,vrot,xx,yy = basem.rotate_vector(uwind_new,vwind_new,lon_new,lat_new,returnxy=True)

    urot_cyc = np.zeros((urot.shape[0],urot.shape[1]+1))
    vrot_cyc = np.zeros((vrot.shape[0],vrot.shape[1]+1))
    xx_cyc = np.zeros((xx.shape[0],xx.shape[1]+1))
    yy_cyc = np.zeros((yy.shape[0],yy.shape[1]+1))
    # mask = np.zeros((urot.shape[0],urot.shape[1]+1))

    urot_cyc[:,0:-1] = urot[:,:]; urot_cyc[:,-1] = urot[:,0]
    vrot_cyc[:,0:-1] = vrot[:,:]; vrot_cyc[:,-1] = vrot[:,0]
    xx_cyc[:,0:-1] = xx[:,:]; xx_cyc[:,-1] = xx[:,0]
    yy_cyc[:,0:-1] = yy[:,:]; yy_cyc[:,-1] = yy[:,0]
    # mask[:,0:-1] = urot.mask[:,:]; mask[:,-1] = urot.mask[:,0]

    # urot_cycM=np.ma.masked_array(urot_cyc,mask=mask)
    # vrot_cycM=np.ma.masked_array(vrot_cyc,mask=mask)

    return urot_cyc,vrot_cyc,xx_cyc,yy_cyc

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
    ni = fid.dimensions['lon'].size #ni is for lat, nj for lon
    nj = fid.dimensions['lat'].size

    return nj, ni, tlat, tlon

def readDataCICEWW3(REP_IN, file, lat, var):
    if file != "none":
        ds=xr.open_dataset(REP_IN+'/'+file)
        data=np.squeeze(np.nan_to_num(ds[var].values))
        mask=np.logical_or(lat<0, data==0)
        data=ma.masked_array(data, mask=mask)
    else:
        data=np.array([])
    return data

def readVectorCICEWW3(REP_IN, file, lat, varVec):
    if file != "none":
        ds=xr.open_dataset(REP_IN+'/'+file)
        dataX=np.squeeze(np.nan_to_num(ds[varVec[0]].values))
        dataY=np.squeeze(np.nan_to_num(ds[varVec[1]].values))
        norm=np.sqrt(dataX**2+dataY**2)
        mask=np.logical_or(norm<0, norm==0)
        dataX=ma.masked_array(dataX, mask=mask)
        dataY=ma.masked_array(dataY, mask=mask)
    else:
        dataX=np.array([])
        dataY=np.array([])
    return dataX, dataY

def readFsdVarCICE(REP_IN, file, lat, varFSD, nfsd_avg):
    if file != "none":
        ds=xr.open_dataset(REP_IN+'/'+file)
        data=np.squeeze(np.nan_to_num(ds[varFSD].values))
        # data=np.squeeze(np.average(data[nfsd_avgS:nfsd_avgE,:,:], axis=0))
        data=np.squeeze(data[nfsd_avg,:,:])
        mask=np.logical_or(lat<0, data==0)
        data=ma.masked_array(data, mask=mask)
    else:
        data=np.array([])
    return data

def readDataNonStdCICE(REP_IN, file, lat, var):
    if file != "none":
        ds=xr.open_dataset(REP_IN+'/'+file)
        # data=np.squeeze(np.average(data[nfsd_avgS:nfsd_avgE,:,:], axis=0))
        if var == "strair":
            dataX=np.squeeze(np.nan_to_num(ds['strairx'].values))
            dataY=np.squeeze(np.nan_to_num(ds['strairy'].values))
            data=np.sqrt(dataX**2+dataY**2)
        if var == "strwv":
            dataX=np.squeeze(np.nan_to_num(ds['strwvx'].values))
            dataY=np.squeeze(np.nan_to_num(ds['strwvy'].values))
            data=np.sqrt(dataX**2+dataY**2)
        if var == "strnorm":
            dataX=np.squeeze(np.nan_to_num(ds['strwvx'].values))
            dataY=np.squeeze(np.nan_to_num(ds['strwvy'].values))
            strwv=np.sqrt(dataX**2+dataY**2)
            dataX=np.squeeze(np.nan_to_num(ds['strairx'].values))
            dataY=np.squeeze(np.nan_to_num(ds['strairy'].values))
            strair=np.sqrt(dataX**2+dataY**2)
            mask_array=np.logical_or(lat<0, strair==0)
            strair=ma.masked_array(strair, mask=mask_array)
            strwv=ma.masked_array(strwv, mask=mask_array)
            data=strwv/(strair+strwv)

        mask=np.logical_or(lat<0, data==0)
        data=ma.masked_array(data, mask=mask)
    else:
        data=np.array([])
    return data


def findFilesCICEWW3(ts, pp_prod, coupled, coupledWW3, coupledCICE, timeStep, outfreqU, list_avg,i):
    datetimeW3=ts
    if pp_prod == "hourly":
        if coupled == "true":
            print("Coupled")
            datetimeCI=ts+timedelta(seconds=timeStep)
            datestrW3=str(datetimeW3.year).zfill(4)+"-"+str(datetimeW3.month).zfill(2)+"-"+str(datetimeW3.day).zfill(2)+"-"+str(datetimeW3.hour*3600).zfill(5)
            datestrCI=str(datetimeCI.year).zfill(4)+"-"+str(datetimeCI.month).zfill(2)+"-"+str(datetimeCI.day).zfill(2)+"-"+str(datetimeCI.hour*3600).zfill(5)
            fileCI="iceh_01h."+datestrCI+".nc"
            fileW3="ww3."+datestrW3+".nc"

        elif coupledWW3 == "false":
            print("Uncoupled WW3 simulation")
            #If only WW3 simulation : ice always initial ice field.
            datetimeCI=start_day+timedelta(seconds=timeStep)
            datestrW3=str(datetimeW3.year).zfill(4)+str(datetimeW3.month).zfill(2)+str(datetimeW3.day).zfill(2)+"T"+str(datetimeW3.hour).zfill(2)+"Z"
            fileCI="ice_forcing.nc"
            REP_IN_CICE="/aos/home/bward/wim/ww3/model/inp/"+exp #Temporary hardcode
            fileW3="ww3."+datestrW3+".nc"
        elif coupledCICE == "false":
            print("Uncoupled CICE simulation")
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
    elif pp_prod == 'avg':
        print("Plotting averaged values between : ",list_avg[i-1], " and ", list_avg[i])
        strTimeIni=str(list_avg[i-1].year).zfill(4)+str(list_avg[i-1].month).zfill(2)+str(list_avg[i-1].day).zfill(2)+str(list_avg[i-1].hour*3600).zfill(5)
        strTimeEnd=str(list_avg[i].year).zfill(4)+str(list_avg[i].month).zfill(2)+str(list_avg[i].day).zfill(2)+str(list_avg[i].hour*3600).zfill(5)
        fileCI="iceh_avg."+strTimeIni+"-"+strTimeEnd+".nc"
        fileW3="iceh_avg."+strTimeIni+"-"+strTimeEnd+".nc"
        datestrW3=strTimeIni+"-"+strTimeEnd
    else:
        print("Unknown post-processing option.")
        fileCI="none"
        fileW3="none"

    return fileCI,fileW3,datestrW3

# def plotWaveIceIdeal(fileCICE, fileWW3, repW3, repCI, repOUT, exp, datestr, xG, yG, listV):
#     import xarray as xr
#     warnings.filterwarnings("ignore", category=UserWarning)
#     #orig_map=plt.cm.get_cmap('gist_earth')
#     orig_map=plt.cm.get_cmap('Spectral')
#     reversed_map = orig_map.reversed()

#     file_dataW3=repW3+"/"+fileWW3
#     file_dataCI=repCI+"/"+fileCICE

#     print("File wave : ", file_dataW3)
#     print("File ice : ", file_dataCI)

#     if fileWW3 != 'none':
#         dsW3=xr.open_dataset(file_dataW3)
#         hs_2d=np.nan_to_num(dsW3[['hs']]['hs'].values.squeeze())

#     dsCI=xr.open_dataset(file_dataCI)
#     X,Y = np.meshgrid(xG,yG)
#     fig, ax = plt.subplots(len(listV),1,figsize=[8,4*len(listV)])
#     i=0
#     for v in listV:
#         if v == 'ic1' or v == 'ice' or v == 'ic5':
#             var_2d=np.nan_to_num(dsW3[[v]][v].values.squeeze())
#         else:
#             var_2d=np.nan_to_num(dsCI[[v]][v].values.squeeze())
#         u_wind=np.nan_to_num(dsCI[['uatm']]['uatm'].values.squeeze())
#         v_wind=np.nan_to_num(dsCI[['vatm']]['vatm'].values.squeeze())
# #        ax[i].set_xlim([2.5, 240])
# #        ax[i].set_ylim([2.5, 240])

#         ax[i].tick_params(labelsize=14)
#         ax[i].set_xlabel('x [km]', size=16)
#         ax[i].set_ylabel('y [km]', size=16)

#         if fileWW3 != 'none':
#             cont=ax[i].contour(X,Y, hs_2d, colors='black') #, levels=[0.02, 0.1, 0.2, 0.4, 0.8, 1, 1.4, 2, 3]) #, levels=[0.01, 0.02, 0.04, 0.06, 0.1, 0.14, 0.2])
#             ax[i].clabel(cont, fontsize= 12)

#         color=ax[i].contourf(X,Y,var_2d, 50, cmap=reversed_map)
#         ax[i].quiver(X[0:100:10,0:100:10], Y[0:100:10,0:100:10], u_wind[0:100:10,0:100:10], v_wind[0:100:10,0:100:10], scale=100) #, length=8, pivot='middle')
#         cb=fig.colorbar(color, ax=ax[i])
#         cb.ax.tick_params(labelsize=14)
        
#         if v == 'ice' or v == 'aice':
#             cb.set_label('Ice Concentration', size=16)
#         if v == 'ic1' or v == 'hi':
#             cb.set_label('Ice Thickess [m]', size=16)
#         if v == 'ic5' or v == 'fsdrad':
#             cb.set_label('Mean Floe Diameter [m]', size=16)
#         i=i+1
        
#     plt.tight_layout()
#     plt.subplots_adjust(top=0.97)
# #    fig.savefig(repOUT+"/"+exp+"_WaveIce_"+datestr, bbbox_to_anchor='tight', dpi=500)
#     plt.savefig(repOUT+"/"+exp+"_WaveIce_"+datestr,dpi='figure',format='png',metadata=None, bbbox_inches='tight')
#     print("------------"+exp+"_WaveIce_"+datestr+" as been plotted---------------------")

def main():

    #Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("pp_prod", help="Post-processing product (e.g. hourly or avg)")
    parser.add_argument("case", help="Name of the case (e.g. case01).")
    parser.add_argument("caseAnom", help="Name of the case to compute anomalies (e.g. case01).")
    parser.add_argument("nts", help="Number of plot.", type=int)
    parser.add_argument("dt", help="Time step of CICE.", type=int)
    parser.add_argument("start_y", help="Year of the first plot.", type=int)
    parser.add_argument("start_m", help="Month of the first plot.", type=int)
    parser.add_argument("start_d", help="Day of the first plot.", type=int)
    parser.add_argument("start_s", help="Seconds of the first plot", type=int)
    parser.add_argument("rep_inW3", help="Path for WW3 output.")
    parser.add_argument("rep_inCI", help="Path for CICE output.")
    parser.add_argument("rep_anomCI", help="Path for WW3 output to compute anomalies.")
    parser.add_argument("rep_anomW3", help="Path for CICE output to compute anomalies.")
    parser.add_argument("rep_out", help="Path to store plot.")
    parser.add_argument("grid", help="Specify grid (default wim2p5)")
    parser.add_argument("outfreq", help="Specify output frequency (default same as dt)", type=int)
    parser.add_argument("outfreqU", help="Specify output frequency unit")
    parser.add_argument("coupledWW3", help="Specify if the run is coupled or not (WW3)")
    parser.add_argument("coupledCICE", help="Specify if the run is coupled or not (CICE)")
    parser.add_argument("addCont", help="Boolean : true to add a contour on top on the pcolor")
    parser.add_argument("contVar", help="Specify if the variable of the contour")
    parser.add_argument("addVec", help="Boolean : true to add vector to the plot on top of the pcolor")
    parser.add_argument("vecVarX", help="Specify the x variable of the vector")
    parser.add_argument("vecVarY", help="Specify the y variable of the vector")
    parser.add_argument("region", help="Specify region (labrador or panarc)")

    parser.add_argument("--iceIc", help="Specify the name of a netCDF file that contains the initial condition of the ice (will only work for uncoupled simulation).")
    parser.add_argument("--repIceIc", help="Specify the path of netCDF file that contains the initial condition of the ice (will only work for uncoupled simulation).")
    args, list_var = parser.parse_known_args()

    #Assign arguments to variables
    pp_prod=args.pp_prod
    grid=args.grid
    outfreq=args.outfreq
    outfreqU=args.outfreqU
    timeStep=args.dt
    coupledWW3=args.coupledWW3
    coupledCICE=args.coupledCICE
    nb_ts=args.nts
    start_y=args.start_y
    start_d=args.start_d
    start_m=args.start_m
    start_s=args.start_s    
    start_day=datetime(start_y, start_m, start_d)+timedelta(seconds=start_s)
    REP_IN_W3=args.rep_inW3
    REP_IN_CICE=args.rep_inCI
    REP_IN_W3_a=args.rep_anomCI
    REP_IN_CICE_a=args.rep_anomCI
    REP_OUT=args.rep_out
    exp=args.case
    exp_a=args.caseAnom
    add_contour=args.addCont
    contourVar=args.contVar
    add_vector=args.addVec
    vectorVar=[args.vecVarX, args.vecVarY]
    region=args.region
    #Define stuff
    if coupledWW3 == "true"  and coupledCICE == "true":
        coupled="true"
    else:
        coupled="false"

    if add_contour == "true":
        add_contour=True
    else:
        add_contour=False
    if add_vector == "true":
        add_vector=True
    else:
        add_vector=False

    if pp_prod == "avg":
        list_avg=createListDateTime(start_day, outfreq, outfreqU, nb_ts+1)
    else:
        list_avg=[]

    list_ts=createListDateTime(start_day, outfreq, outfreqU, nb_ts)
    list_varWW3=['hs', 'lm']
    list_varCICE=['aice', 'hi', 'fsdrad']
    list_varNonStdCICE=['strair', 'strwv', 'strnorm']
    list_varFSDCICE=['dafsd_latg', 'dafsd_latm', 'dafsd_newi', 'dafsd_wave', 'dafsd_weld']
    list_varVecCICE=['strairx', 'strairy', 'uvel', 'vvel', 'strwvx', 'strwvy', 'uatm', 'vatm']
    list_varVecWW3=[]

    if grid == 'wim2p5':
        #Hardcoded... could be the same as the other.
#        grdRes=2.5
#        grdMax=247.5
#        grdMin=-2.5
        grdRes=25
        grdMax=2475
        grdMin=-25
#        grdRes=50
#        grdMax=4950
#        grdMin=-50
        xgrid=np.arange(grdMin, grdMax, grdRes)
        ygrid=np.arange(grdMin, grdMax, grdRes)
        m = Basemap(projection='npstere', boundinglat=45,lon_0=270, resolution='l')
    elif grid == 'wimgx3' or grid == 'wimgx1' or grid == 'wimtx1':
        if region == 'panarc':
            m = Basemap(projection='npstere', boundinglat=35,lon_0=270, resolution='l')
        elif region == 'labrador':
            m = Basemap(width=1850000,height=2500000, resolution='l',projection='stere',\
            lat_ts=50,lat_0=60,lon_0=-55.)

        datetimeStart=start_day
        if coupled == "true":
            # datestrStart=str(datetimeStart.year).zfill(4)+"-"+str(datetimeStart.month).zfill(2)+"-"+str(datetimeStart.day).zfill(2)+"-"+str(datetimeStart.hour*3600).zfill(5)
            # file_strt="ww3."+datestrStart+".nc"
            # rep_strt=REP_IN_W3
            # nlon, nlat, t_lat, t_lon = get_geomWW3(rep_strt, file_strt)
            rep_strt=REP_IN_CICE
            cmd_list="ls "+rep_strt+"/"+"| tail -n 1"
            file_strt = str(subprocess.check_output(cmd_list, shell=True).rstrip())[2:-1]
            nlon, nlat, t_lat, t_lon=get_geomCICE(rep_strt, file_strt)
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
    #Plot hourly, or averaged datas, or ?. 
    for ts in list_ts:
        print("Time step "+str(i)+":",ts)
        fileCI,fileW3,date4str=findFilesCICEWW3(ts, pp_prod, coupled, coupledWW3, coupledCICE, timeStep, outfreqU, list_avg,i)
        fileCI_a,fileW3_a,date4str=findFilesCICEWW3(ts, pp_prod, coupled, coupledWW3, coupledCICE, timeStep, outfreqU, list_avg,i)
        print("CICE file : "+REP_IN_CICE+"/"+fileCI, "WW3 file : "+REP_IN_W3+"/"+fileW3)
        for var in list_var:

        #Read variable for color
            if var in list_varCICE:
                data_1=readDataCICEWW3(REP_IN_CICE, fileCI, t_lat, var)
                data_2=readDataCICEWW3(REP_IN_CICE_a, fileCI_a, t_lat, var)
            elif var in list_varWW3:
                data_1=readDataCICEWW3(REP_IN_W3, fileW3, t_lat, var)
                data_2=readDataCICEWW3(REP_IN_W3_a, fileW3_a, t_lat, var)
            elif var in list_varNonStdCICE:
                data_1=readDataNonStdCICE(REP_IN_W3, fileW3, t_lat, var)
                data_2=readDataCICEWW3(REP_IN_W3_a, fileW3_a, t_lat, var)
            elif var in list_varFSDCICE:
                if var == "dafsd_latm" or var == "dafsd_wave" or var == "dafsd_latg":
                    data_1=readFsdVarCICE(REP_IN_W3, fileW3, t_lat, var, 0)
                    data_2=readFsdVarCICE(REP_IN_W3_a, fileW3_a, t_lat, var, 0)
                elif var == "dafsd_weld" or var == "dafsd_newi" :
                    data_1=readFsdVarCICE(REP_IN_W3, fileW3, t_lat, var, 11)
                    data_2=readFsdVarCICE(REP_IN_W3_a, fileW3_a, t_lat, var, 0)
            else:
                print("Unknown var")
                return
            #Compute anom
            data = data_1-data_2
            #Read variable for contour
            if add_contour:
                if contourVar in list_varCICE:
                    dataCont=readDataCICEWW3(REP_IN_CICE, fileCI, t_lat, contourVar)
                elif contourVar in list_varWW3:
                    dataCont=readDataCICEWW3(REP_IN_W3, fileW3, t_lat, contourVar)
            else:
                dataCont=np.array([])
            
            #Read variable for vector
            REP_INTERP=REP_OUT+"/interp"
            if add_vector:
                if (vectorVar[0] in list_varVecCICE) and (vectorVar[1] in list_varVecCICE) :
                    dataVecX,dataVecY=readVectorCICEWW3(REP_IN_CICE, fileCI, t_lat, vectorVar)
                    uproj, vproj, xwind, ywind=create_wind_projection(dataVecX, dataVecY, REP_IN_CICE, fileCI, REP_INTERP, m, nlon, nlat)
                    dataVecX1,dataVecY1=readVectorCICEWW3(REP_IN_CICE_a, fileCI_a, t_lat, vectorVar)
                    uproj1, vproj1, xwind1, ywind1=create_wind_projection(dataVecX1, dataVecY1, REP_IN_CICE_a, fileCI_a, REP_INTERP, m, nlon, nlat)
                    uprojA = uproj-uproj1
                    vprojA = vproj-vproj1
                elif (vectorVar[0] in list_varVecWW3) and (vectorVar[1] in list_varVecWW3):
                    dataVecX,dataVecY=readVectorCICEWW3(REP_IN_W3, fileW3, t_lat, vectorVar)
                    uproj, vproj, xwind, ywind=create_wind_projection(dataVecX, dataVecY, REP_IN_W3, fileW3, REP_INTERP, m, nlon, nlat)
                    dataVecX1,dataVecY1=readVectorCICEWW3(REP_IN_W3_a, fileW3_a, t_lat, vectorVar)
                    uproj1, vproj1, xwind1, ywind1=create_wind_projection(dataVecX1, dataVecY1, REP_IN_W3_a, fileW3, REP_INTERP, m, nlon, nlat)
                    uprojA = uproj-uproj1
                    vprojA = vproj-vproj1
            else:
                uprojA=np.array([])
                vprojA=np.array([])
                xwind=np.array([])
                ywind=np.array([])

            dataVec=[uprojA, vprojA, xwind, ywind]

            if grid == 'wim2p5':
                plotWaveIceIdeal(data, dataCont, dataVec, REP_OUT, exp, datestrW3, xgrid, ygrid, list_var)
            if grid == 'wimgx3' or grid == 'wimgx1' or grid == 'wimtx1':
                plotOneVar(data, dataCont, dataVec, t_lat, t_lon, REP_OUT, exp, exp_a, date4str, 'pcolor', m, var)
        #         if len(list_var) == 1:
        #            plotOneVar(REP_IN_CICE, fileCI, REP_IN_W3, fileW3, nlon, nlat, t_lat, t_lon, REP_OUT, exp, datestrW3, 'pcolor', list_var)
        #         else:
        #            plotWaveIceArctic(REP_IN_CICE, fileCI, REP_IN_W3, fileW3, nlon, nlat, t_lat, t_lon, REP_OUT, exp, datestrW3, 'pcolor', list_var)
        i=i+1

#Call main
if __name__ == "__main__":
    main()


# def read_data(path_a, files_a, var, nj, ni):
#     '''
#     Read the baseline and test data for sea ice thickness.  The calculate
#     the difference for all locations where sea ice thickness is greater
#     than 0.01 meters.
#     '''

#     def fill_data_array(path, files, nj, ni):
#         '''Function to fill the data arrays'''
#         # Initialize the data array
#         data = np.zeros((nj, ni),dtype=np.float32)
#         # Read in the data
#         fname=files[0]
#         nfid = nc.Dataset("{}/{}".format(path, fname), 'r')
#         fill_value = nfid.variables[var]._FillValue
#         data[:, :] = nfid.variables[var][:]
#         nfid.close()
            
#         data[data == fill_value] = 0.0

#         return data
    
#     data_a = fill_data_array(path_a, files_a, nj, ni)
#     mask_array_a = np.zeros_like(data_a)

#     if var == 'uwnd':
#         var='vwnd'
#         dataV=fill_data_array(path_a, files_a, nj, ni)
#         dataSpeed=np.sqrt(np.square(data_a)+np.square(dataV))
#         mask_array_a = np.logical_or(dataSpeed == 0., dataSpeed < 0)
#         data_a = ma.masked_array(data_a, mask=mask_array_a)
#     elif var == 'vwnd':
#         var='uwnd'
#         dataU=fill_data_array(path_a, files_a, nj, ni)
#         dataSpeed=np.sqrt(np.square(data_a)+np.square(dataU))
#         mask_array_a = np.logical_or(dataSpeed == 0., dataSpeed < 0)
#         data_a = ma.masked_array(data_a, mask=mask_array_a)
#     elif var == 'hs':
#         mask_array_a = np.logical_or(data_a == 0., data_a < 0)
#         data_a = ma.masked_array(data_a, mask=mask_array_a)
#     elif var == 'ice' or var == 'aice':
# #         mask_array_a = np.logical_or(\
# #                        np.logical_or(\
# #                             np.all(np.equal(data_a, 0.), axis=0), np.all(data_a < 0.01, axis=0))
# #                        , np.all(data_a < 0.01, axis=0))
#         mask_array_a = np.logical_or(data_a == 0., data_a < 0)
#         data_a = ma.masked_array(data_a, mask=mask_array_a)
#     elif var == 'ic1' or var == 'hi':
#         mask_array_a = np.logical_or(data_a == 0., data_a < 0)
#         data_a = ma.masked_array(data_a, mask=mask_array_a)
#     elif var == 'ic5' or var == 'fsdrad':
#         mask_array_a = np.logical_or(data_a == 0., data_a < 0)
#         data_a = ma.masked_array(data_a, mask=mask_array_a)
#     elif var == 'airtmp':
#         data_a=data_a-273.15
# #    if var == 'uwnd' or var == 'vwnd':
# #        mask_array_a = np.logical_or(\
# #                       np.logical_or(\
# #                            np.all(np.equal(data_a, 0.), axis=0), np.all(data_a < 1, axis=0))
# #                       , np.all(data_a < 1, axis=0))
# #        data_a = ma.masked_array(data_a, mask=mask_array_a)
# #     data_b = fill_data_array(path_b, files_b, nj, ni)

#     return data_a

# def plotWaveIceArctic(REP_IN_CICE, fileCI, REP_IN_W3, fileW3, nlon, nlat, lat, lon, repOUT, case, datestr, plot_type, list_var):

#     '''This function plots CICE data and creates a .png file.'''
#     orig_map=plt.cm.get_cmap('Spectral')
#     reversed_map = orig_map.reversed()

#     # Suppress Matplotlib deprecation warnings
#     warnings.filterwarnings("ignore", category=UserWarning)
#     wnd_var=['uatm', 'vatm']
#     fig, axes = plt.subplots(len(list_var),1,figsize=[14,8*len(list_var)])
#     i=0
#     for var in list_var:
#        #Read ice field and wave field.
#        data=read_data(REP_IN_CICE, [fileCI], var, nlon, nlat)
       
#        if fileW3 != "none":
#            dataW3=read_data(REP_IN_W3, [fileW3], 'hs', nlon, nlat)

#        plt.sca(axes[i])

#        #Choose projection
# #       m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
# #       m = Basemap(projection='spstere', boundinglat=-45,lon_0=270, resolution='l')
# #       m = Basemap(width=12000000,height=8000000,resolution='l',projection='stere',lat_0=90,lon_0=270)
# #       m = Basemap(projection='ortho',lon_0=270,lat_0=40,resolution='l')
#        m = Basemap(projection='npstere', boundinglat=35,lon_0=270, resolution='l')
#        m.drawcoastlines()
#        m.fillcontinents()
#        if plot_type == 'scatter':
#            x, y = m(lon,lat)
#            sc = m.scatter(x, y, c=data, cmap=reversed_map, lw=0, s=4)
#        else:
#            # Longitude need to be between -180 and 180 for plotting
#            lon1 = lon.copy()
#            for lt in range(lon.shape[0]):
#                for lg in range(lon.shape[1]):
#                    pt=lon[lt,lg]
#                    if pt >= 180:
#                        lon1[lt,lg]=lon1[lt,lg]-360. 
#            lon = lon1

#            #No need for reordering the datas, just create empty arrays.
#            d = np.zeros((data.shape[0],data.shape[1]+1))
#            lon_cyc = np.zeros((lon.shape[0],lon.shape[1]+1))
#            mask = np.zeros((data.shape[0],data.shape[1]+1))
#            lat_cyc = np.zeros((lat.shape[0],lat.shape[1]+1))

#            maskNH=np.logical_or(lat==0, lat<0)

#            mask[:,0:-1] = data.mask[:,:]+maskNH[:,:]
#            mask[:,-1] = data.mask[:,0]+maskNH[:,0]
      
#            #Simply fill the arrays
#            lon_cyc[:,0:-1] = lon[:,:]; lon_cyc[:,-1] = lon[:,0]
#            lat_cyc[:,0:-1] = lat[:,:]; lat_cyc[:,-1] = lat[:,0]
#            d[:,0:-1] = data[:,:]
#            d[:,-1] = data[:,0]
#            # Apply mask to ice field
#            d1 = np.ma.masked_array(d,mask=mask)

#            #Idem with waves
#            if fileW3 != "none":
#                dW3 = np.zeros((dataW3.shape[0],dataW3.shape[1]+1))
#                maskhs=np.zeros((data.shape[0],data.shape[1]+1))
#                maskhs[:,0:-1] = dataW3.mask[:,:]
#                maskhs[:,-1] = dataW3.mask[:,0]
#                dW3[:,0:-1] = dataW3[:,:]
#                dW3[:,-1] = dataW3[:,0]
#                d1hs=np.ma.masked_array(dW3,mask=maskhs)

#            x, y = m(lon_cyc, lat_cyc)

#            if plot_type == 'contour':
#                #Plot ice fields
#                sc = m.contourf(x, y, d1, cmap=reversed_map)
#                #Plot contours
#                if fileW3 != "none":
#                    cont=axes[i].contour(x,y, d1hs, colors='black') #, levels=[0.02, 0.04, 0.06, 0.1, 0.14, 0.2])
#                    if(len(cont.allsegs) != 1):
#                        axes[i].clabel(cont, fontsize= 12)
#                # Rotate and interpolate to have a nice wind field in the projection.
#                uproj, vproj, xwind, ywind = create_wind_projection(REP_IN_W3, fileW3, REP_IN_CICE, fileCI, m, wnd_var,nlon,nlat)
#                # Plot winds
#                Q = m.quiver(xwind, ywind,uproj,vproj,scale=250)
#            else:  # pcolor
#                sc = m.pcolor(x, y, d1, cmap=reversed_map)
# #Temporary?
#                if fileW3 != "none":
#                    cont=axes[i].contour(x,y, d1hs, colors='black') #, levels=[0.02, 0.04, 0.06, 0.1, 0.14, 0.2])
#                    if(len(cont.allsegs) != 1):
#                        axes[i].clabel(cont, fontsize= 12)
# #                   uproj, vproj, xwind, ywind = create_wind_projection(REP_IN_W3, fileW3, REP_IN_CICE, fileCI,  m, wnd_var, nlon, nlat)
# #                   axes[i].barbs(xwind, ywind, uproj, vproj, length=4, pivot='middle')

#        m.drawparallels(np.arange(-90.,120.,15.),labels=[1,0,0,0], size=16) # draw parallels
#        m.drawmeridians(np.arange(0.,420.,30.),labels=[1,1,0,1], size=16) # draw meridians
#        cb=fig.colorbar(sc, ax=axes[i])
#        cb.ax.tick_params(labelsize=18)

#        if var == 'ice' or var == 'aice':
#           cb.set_label('Ice Concentration', size=20)
#        elif var == 'ic1' or var == 'hi':
#           cb.set_label('Ice Thickess [m]', size=20)
#        elif var == 'ic5' or var == 'fsdrad':
#           cb.set_label('Mean Floe Diameter [m]', size=20)

#        i=i+1
#     axes[0].set_title(datestr, fontsize=20)
#     plt.tight_layout()
#     plt.subplots_adjust(top=0.97)
# #    plt.savefig(repOUT+"/"+case+"_WaveIce_"+datestr, bbbox_to_anchor='tight', dpi=500)
#     plt.savefig(repOUT+"/"+case+"_WaveIce_"+datestr,dpi='figure',format='png',metadata=None, bbbox_inches='tight')
#     print("------------"+case+"_WaveIce_"+datestr+" as been plotted---------------------")
