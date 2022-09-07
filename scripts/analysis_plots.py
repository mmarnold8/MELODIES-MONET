import os
import logging
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def plot_lon_lat(plotfile, plotname,
    plot_params, field,
    symmetric=False, swap_lon=False):

    logging.info(plotfile)

    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')

    ax = plt.axes(projection=ccrs.PlateCarree())

    lon_values = field.lon.values
    lat_values = field.lat.values

    levels = np.linspace(
        plot_params['range_min'], plot_params['range_max'],
        plot_params['nlevel'], endpoint=True)

    if field.ndim == 3: 
        field_values = np.clip(field.values[0,:,:], levels[0], levels[-1])
    else:
        field_values = np.clip(field.values[:,:], levels[0], levels[-1])

    if swap_lon:
        nlon = len(lon_values)
        lon_swap = lon_values
        lon_values[0:nlon//2] = lon_swap[nlon//2:nlon]
        lon_values[nlon//2:nlon] = lon_swap[0:nlon//2]
        field_swap = field_values
        field_values[:,0:nlon//2] = field_swap[:,nlon//2:nlon]
        field_values[:,nlon//2:nlon] = field_swap[:,0:nlon//2]

    lon_mesh, lat_mesh \
        = np.meshgrid(lon_values, lat_values)

    extend_option = 'both' if symmetric else 'max' 
    # cmap_option = plt.cm.gist_rainbow if symmetric else plt.cm.gist_ncar
    cmap_option = plt.cm.gist_ncar

    cp = ax.contourf(lon_mesh, lat_mesh, field_values,
        levels, cmap=cmap_option, extend=extend_option,
        transform=ccrs.PlateCarree())

    # ax.gridlines()
    ax.coastlines()
    # ax.add_feature(cfeature.BORDERS)
    # ax.add_feature(states_provinces)

    plt.title(plotname)
    cbar = plt.colorbar(cp, orientation='horizontal', pad=0.05)

    plt.savefig(os.path.join(plot_params['outdir'], plotfile) + '.png',
        bbox_inches='tight', dpi=1000)
    plt.savefig(os.path.join(plot_params['outdir'], plotfile) + '.pdf',
        bbox_inches='tight')
    plt.clf()

