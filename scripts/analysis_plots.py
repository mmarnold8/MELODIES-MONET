import os
import logging
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def plot_lon_lat(plotfile, plot_params, field, symmetric=False):

    logging.info(plotfile)

    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')

    # ax = plt.axes(projection=ccrs.Robinson())
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-180, -180, -80, 80])

    lon_mesh, lat_mesh \
        = np.meshgrid(field.lon.values, field.lat.values)

    levels = np.linspace(
        plot_params['range_min'], plot_params['range_max'],
        plot_params['nlevel'], endpoint=True)

    extend_option = 'both' if symmetric else 'max' 
    # cmap_option = plt.cm.gist_rainbow if symmetric else plt.cm.gist_ncar
    cmap_option = plt.cm.gist_ncar

    cp = ax.contourf(lon_mesh, lat_mesh, field.values, levels,
        cmap=cmap_option, extend=extend_option,
        transform=ccrs.PlateCarree())

    ax.gridlines()
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(states_provinces)

    plt.title(plot_params['name'])
    cbar = plt.colorbar(cp,
        orientation='horizontal', pad=0.01)

    plt.savefig(os.path.join(plot_params['outdir'], plotfile) + '.png',
        bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(plot_params['outdir'], plotfile) + '.pdf',
        bbox_inches='tight')
    plt.clf()

