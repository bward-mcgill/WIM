#! /usr/bin/env python3

#import pandas as pd
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
#import matplotlib.colors as mcolors
#import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib.animation as animation
from PIL import Image
import glob
import xarray as xr
import argparse

def cleanGrdFiles_ww3(nparray_var2d, nparray_rst, def_v, convFac_ww3):
    listBadRow=[]
    listBadCol=[]
    for col_i in range(len(nparray_var2d[0])):
        col=nparray_var2d[:,col_i]
        if (np.count_nonzero(col == def_v) == len(col)):
            listBadCol.append(col_i)
    for row_i in range(len(nparray_var2d[:,0])):
        row=nparray_var2d[row_i]
        if (np.count_nonzero(row == def_v) == len(row)):
            listBadRow.append(row_i)
            
    nparray_var2d[listBadRow]=nparray_rst[listBadRow]/convFac_ww3
    nparray_var2d[:,listBadCol]=nparray_rst[:,listBadCol]/convFac_ww3
    
    return nparray_var2d

def plot_waveIce(dateCICE, dateWW3, repW3, repCI, xG, yG, listV):
    
    #orig_map=plt.cm.get_cmap('gist_earth')
    orig_map=plt.cm.get_cmap('Spectral')
    reversed_map = orig_map.reversed()
    datestrCI=str(dateCICE.year).zfill(4)+"-"+str(dateCICE.month).zfill(2)+"-"+str(dateCICE.day).zfill(2)+"-"+str(dateCICE.hour*3600).zfill(5)
    datestrW3=str(dateWW3.year).zfill(4)+"-"+str(dateWW3.month).zfill(2)+"-"+str(dateWW3.day).zfill(2)+"-"+str(dateWW3.hour*3600).zfill(5)
    
    file_dataW3=repW3+"/ww3."+datestrW3+".nc"
    file_dataCI=repCI+"/iceh_01h."+datestrCI+".nc"
        
    print("File wave : ", file_dataW3)
    print("File ice : ", file_dataCI)
    
    dsW3=xr.open_dataset(file_dataW3)
    hs_2d=np.nan_to_num(dsW3[['hs']]['hs'].values.squeeze())
    dsCI=xr.open_dataset(file_dataCI)
    
    
    #cbar_min=0
    #cbar_max=300
    #cbarlabels = np.linspace(np.floor(cbar_min), np.ceil(cbar_max), num=5, endpoint=True)
    
    #Read wave field
#     hs_2d=np.genfromtxt(file_hs, dtype=None, skip_header=1)
#     hs_rst=np.zeros((len(xG), len(yG)))
#     hs_2d=cleanGrdFiles_ww3(hs_2d, hs_rst, defV, convF)
    
    X,Y = np.meshgrid(xG,yG)
    fig, ax = plt.subplots(len(listV),1,figsize=[8,4*len(listV)])
    i=0
    for v in listV:
        var_2d=np.nan_to_num(dsCI[[v]][v].values.squeeze())  
        ax[i].set_xlim([2.5, 240])
        ax[i].set_ylim([2.5, 240])
        ax[i].tick_params(labelsize=14)
#         ax[i].set_yticks(np.arange(0.5, 3, 0.5))
        ax[i].set_xlabel('x [km]', size=16)
        ax[i].set_ylabel('y [km]', size=16)
        cont=ax[i].contour(X,Y, hs_2d, colors='black', levels=[0.01, 0.02, 0.04, 0.06, 0.1, 0.14, 0.2])
        color=ax[i].contourf(X,Y,var_2d, 50, cmap=reversed_map)
        ax[i].clabel(cont, fontsize= 12)
        cb=fig.colorbar(color, ax=ax[i])
        cb.ax.tick_params(labelsize=14)
        
        if i == 0:
            cb.set_label('Ice Concentration', size=16)
    
        if i == 1:
            cb.set_label('Ice Thickess [m]', size=16)
        if i == 2:
            cb.set_label('Mean Floe Diameter [m]', size=16)
        i=i+1
        
    plt.tight_layout()
    plt.subplots_adjust(top=0.97)
    fig.savefig("/aos/home/bward/wim/post-proc/case12"+"/plotWaveIce_"+datestrW3, bbbox_to_anchor='tight', dpi=500)
    print("------------plotWaveIce_"+datestrW3+" as been plotted---------------------")
    

def animate(rep_img, exp_name, start, end):
    # Create the frames
    frames = []
    list_imgs = glob.glob(rep_img+'/*.png')
    list.sort(list_imgs)
    for i in list_imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
 
    # Save into a GIF file that loops forever
    frames[0].save(rep_img+'/'+start+"_"+end+"_"+exp_name+'.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=3000, loop=0)
    
def createListDateTime(init_dateTime, ts, nts):
   list_ts=[]
   start_day=init_dateTime
   start_sec=init_dateTime.second
   for i in range(nts):
      new_day=start_day+timedelta(seconds=start_sec+i*ts)
#      list_ts.append(str(new_day.year).zfill(4)+str(new_day.month).zfill(2)+str(new_day.day).zfill(2)+str(new_day.hour*3600).zfill(5))
      list_ts.append(new_day)
   return list_ts


def printDataModel(date, repI, model, index):
    datestr=str(date.year).zfill(4)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)+"-"+str(date.hour*3600).zfill(5)
    
    if model == "CICE":
        listV=['aice', 'hi', 'fsdrad']
        file_data=repI+"/iceh_01h."+datestr+".nc"
        print("CICE")
    elif model == "WW3":
        listV=['ice', 'ic1', 'ic5']
        file_data=repI+"/ww3."+datestr+".nc"
        print("WW3")
        
    ds=xr.open_dataset(file_data)
    
    for v in listV:
        var_2d=np.nan_to_num(ds[[v]][v].values.squeeze()) 
        print(var_2d)

def main():

    parser = argparse.ArgumentParser()
    #parser.add_argument("case", help="Enter the name of the case (e.g. case01).")
    parser.add_argument("nts", help="Enter the number of plot.", type=int)
    parser.add_argument("dt", help="Time step of the model.", type=int)
    parser.add_argument("start_y", help="Enter the year for the first plot.", type=int)
    parser.add_argument("start_m", help="Enter the month for the first plot.", type=int)
    parser.add_argument("start_d", help="Enter the day for the first plot.", type=int)
    parser.add_argument("start_s", help="Enter the second for the first plot", type=int)
    parser.add_argument("rep_inW3", help="Enter the path for WW3 output.")
    parser.add_argument("rep_inCI", help="Enter the path for CICE output.")
    parser.add_argument("rep_out", help="Enter the path to store plot.")
    parser.add_argument("-g", "--grid", help="Specify grid (default wim2p5)")
    parser.add_argument("-f", "--outfreq", help="Specify output frequency (default same as dt)", type=int)
    args = parser.parse_args()

    #Define variables
    #exp=args.case
    grid=args.grid
    outfreq=args.outfreq
    timeStep=args.dt
    nb_ts=args.nts

    if not grid:
       grid='wim2p5'
    if not outfreq:
       outfreq=timeStep
    #list_var=['aice_ww', 'hice_ww', 'diam_ww'] #,'ic1','ic5'] #Ice concentration, Ice thickness, Mean floe size diameter
    list_var=['aice', 'hi', 'fsdrad']

    start_y=args.start_y
    start_d=args.start_d
    start_m=args.start_m
    start_s=args.start_s    
    start_day=datetime(start_y, start_m, start_d)+timedelta(seconds=start_s)

    list_ts=createListDateTime(start_day, outfreq, nb_ts)

    REP_IN_W3=args.rep_inW3
    REP_IN_CICE=args.rep_inCI
    REP_OUT=args.rep_out

    if grid == 'wim2p5':
       grdRes=2.5
       grdMax=247.5
       grdMin=-2.5
    
    xgrid=np.arange(grdMin, grdMax, grdRes)
    ygrid=np.arange(grdMin, grdMax, grdRes)
    i=1            
#    #Plot at each timestep
    for ts in list_ts:
        datetimeW3=ts
        datetimeCI=ts+timedelta(seconds=timeStep)
        print("Time step "+str(i)+":",datetimeW3)
#        #printDataModel(dateCI, REP_IN_CICE, 'CICE', i)
        plot_waveIce(datetimeCI, datetimeW3, REP_IN_W3, REP_IN_CICE, xgrid, ygrid, list_var) #xgrid, ygrid, defValue, txt2ww3)
        i=i+1
#        #printDataModel(date, REP_IN, 'WW3')
#        #fig, ax = plt.subplots(3,1,figsize=[8,12])
#        #ani=animation.FuncAnimation(fig, plot_waveIce, list_ts)
#    #Animate
#    #animate(REP_PP, exp, list_ts[0], list_ts[len(list_ts)-1])

#Call main
if __name__ == "__main__":
    main()
