#! /usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
from wim_dateTime import createListDateTime
from datetime import datetime, timedelta
import netCDF4 as nc
import argparse
import subprocess
import warnings
#import netCDF4 as nc
import numpy.ma as ma
import os
import pandas as pd
import xarray as xr

def avgHourlyFile(list_ts, list_var, nhour, REP_IN_CI, REP_IN_W3):
    dfInit=pd.DataFrame()
    dsSum=dfInit.to_xarray()
    dsAvg=dfInit.to_xarray()
    compteur=0
    for ts in list_ts:
        
        #Open each of the hourly files
        datetimeW3=ts
        datetimeCI=ts+timedelta(seconds=3600)
        datestrW3=str(datetimeW3.year).zfill(4)+"-"+str(datetimeW3.month).zfill(2)+"-"+str(datetimeW3.day).zfill(2)+"-"+str(datetimeW3.hour*3600).zfill(5)
        datestrCI=str(datetimeCI.year).zfill(4)+"-"+str(datetimeCI.month).zfill(2)+"-"+str(datetimeCI.day).zfill(2)+"-"+str(datetimeCI.hour*3600).zfill(5)
        nameCI="iceh_01h."+datestrCI+".nc"
        nameW3="ww3."+datestrW3+".nc"
        nameW3ef="ww3."+datestrW3+"_efreq.nc"
        fileCI=REP_IN_CI+"/"+nameCI
        fileW3=REP_IN_W3+"/"+nameW3
        fileW3ef=REP_IN_W3+"/"+nameW3ef

        temp_ds=xr.open_dataset(fileCI)
        temp_dsW3=xr.open_dataset(fileW3)
        temp_dsW3ef=xr.open_dataset(fileW3ef)

        # For a CICE variable.
        for var in list_var:
            if compteur == 0:
                dsSum[var]=temp_ds[var]
            else:
                dsSum[[var]][var].values=dsSum[[var]][var].values+temp_ds[[var]][var]
            
        # For a WW3 variable.
        #Initialize variable
        if compteur == 0:
            dsSum['hs']=temp_ds['aice']
            dsSum[['hs']]['hs'].values=temp_dsW3[['hs']]['hs']
            dsSum['lm']=temp_ds['aice']
            dsSum[['lm']]['lm'].values=temp_dsW3[['lm']]['lm']
            dsSum['uatm']=temp_ds['aice']
            dsSum[['uatm']]['uatm'].values=temp_dsW3[['uwnd']]['uwnd']
            dsSum['vatm']=temp_ds['aice']
            dsSum[['vatm']]['vatm'].values=temp_dsW3[['vwnd']]['vwnd']
            dsSum['efreq']=temp_dsW3ef['efreq']
            dsSum[['efreq']]['efreq'].values=temp_dsW3ef[['efreq']]['efreq']
        #Sum each timestep
        else:
            dsSum[['hs']]['hs'].values=dsSum[['hs']]['hs'].values+temp_dsW3[['hs']]['hs']
            dsSum[['lm']]['lm'].values=dsSum[['lm']]['lm'].values+temp_dsW3[['lm']]['lm']
            dsSum[['uatm']]['uatm'].values=dsSum[['uatm']]['uatm'].values+temp_dsW3[['uwnd']]['uwnd']
            dsSum[['vatm']]['vatm'].values=dsSum[['vatm']]['vatm'].values+temp_dsW3[['vwnd']]['vwnd']
            dsSum[['efreq']]['efreq'].values=dsSum[['efreq']]['efreq'].values+temp_dsW3ef[['efreq']]['efreq']
        compteur=compteur+1

    # Average all
    for var in list_var:
        dsAvg=dsSum/nhour
    
    return dsAvg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case", help="Name of the case (e.g. case01).")
    parser.add_argument("start_y", help="Starting year.", type=int)
    parser.add_argument("start_m", help="Starting month.", type=int)
    parser.add_argument("start_d", help="Starting day.", type=int)
    parser.add_argument("start_s", help="Starting second.", type=int)
    parser.add_argument("nbAvg", help="Number of averaging period.", type=int)
    parser.add_argument("avgFreq", help="Avg. frequency.", type=int)
    parser.add_argument("avgFreqU", help="Avg. frequency units.")
    parser.add_argument("rep_inW3", help="Path for WW3 output.")
    parser.add_argument("rep_inCI", help="Path for CICE output.")
    parser.add_argument("rep_out", help="Path to store plot.")

#    args = parser.parse_args()
    args, list_var = parser.parse_known_args()

    #Define variables
    avgFreq=args.avgFreq
    avgFreqU=args.avgFreqU
    nbAvg=args.nbAvg+1

#    list_var=['aice', 'hi', 'fsdrad'] #, 'strwvx', 'strwvy', 'strairx', 'strairy', 'dafsd_wave', 'dafsd_weld', 'dafsd_latg', 'dafsd_latm', 'dafsd_newi'] #, 'uatm', 'vatm']

    start_y=args.start_y
    start_d=args.start_d
    start_m=args.start_m
    start_s=args.start_s
    start_day=datetime(start_y, start_m, start_d)+timedelta(seconds=start_s)
    list_avg=createListDateTime(start_day, avgFreq, avgFreqU, nbAvg)
    exp=args.case
    REP_IN_W3=args.rep_inW3
    REP_IN_CI=args.rep_inCI
    REP_OUT=args.rep_out

    for nAvg in range(nbAvg-1):
        delta_t=(list_avg[nAvg+1]-list_avg[nAvg]).total_seconds()
        nhour=int(divmod(delta_t, 3600)[0])
        freqCoup=1
        freqCoupU='h'

        list_ts=createListDateTime(list_avg[nAvg], freqCoup, freqCoupU, nhour)
        strTimeAvg=str(list_avg[nAvg].year).zfill(4)+'-'+str(list_avg[nAvg].month).zfill(2)

        if not (os.path.isfile(REP_OUT+"/"+"iceh_avg."+strTimeAvg+".nc")):
            print("Averaging all files between : ",list_avg[nAvg], " and ", list_avg[nAvg+1])
            dsAvg=avgHourlyFile(list_ts, list_var, nhour, REP_IN_CI, REP_IN_W3)
            print("Saving :", REP_OUT+"iceh_avg."+strTimeAvg+".nc") 
            dsAvg.to_netcdf(REP_OUT+"/"+"iceh_avg."+strTimeAvg+".nc")
        else:
            print(REP_OUT+"/"+"iceh_avg."+strTimeAvg+".nc"+" already exists !")     

#Call main
if __name__ == "__main__":
    main()