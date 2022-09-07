import logging
import numpy as np
import xarray as xr

import monetio
from monetio.sat.hdfio import hdf_open, hdf_close, hdf_list, hdf_read


def read_gridded_eos(filename, var_dict):

    ds_dict = dict()

    logging.info('read_mod08_m3:' + filename)
    f = hdf_open(filename)
    datasets, indices = hdf_list(f)

    lon = hdf_read(f, 'XDim')
    lat = np.flip(hdf_read(f, 'YDim'))
    lon_da = xr.DataArray(lon,
        attrs={'longname': 'longitude', 'units': 'deg East'})
    lat_da = xr.DataArray(lat,
        attrs={'longname': 'latitude', 'units': 'deg North'})

    for var in var_dict:
        logging.info('read_mod08_m3:' + var)
        data = np.array(hdf_read(f, var), dtype=float)
        data = np.flip(data, axis=0)
        data[data==var_dict[var]['fillvalue']] = np.nan
        data *= var_dict[var]['scale']
        var_da = xr.DataArray(
            data, coords=[lat_da, lon_da],
            dims=['lat', 'lon'],
            attrs={'units': var_dict[var]['units']})
        ds_dict[var] = var_da

    hdf_close(f)

    ds = xr.Dataset(ds_dict)
    ds.to_netcdf(filename.replace('.hdf', '.nc'))

    return ds

