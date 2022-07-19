import pandas as pd
import numpy as np
import xarray as xr
import sys

path_cice=str(sys.argv[1])
path_ww3=str(sys.argv[2])
exp=str(sys.argv[3])

file_nc=path_cice+'/'+exp+'/history/iceh_06h.2005-01-01-21600.nc'
rep_out=path_ww3+'/'+exp
list_var=['aice', 'hi']

for var in list_var:
    if var == 'aice':
        nww3='ice'
    else:
        nww3='ic1'
    
    file_out=rep_out+'/'+nww3+'_'+exp+'.txt'
    ds=xr.open_dataset(file_nc)
    var_2d = np.nan_to_num(ds[var].values.reshape((100,100)))
    np.savetxt(file_out, var_2d)
