import os
import logging
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def plot_lon_lat(plotdir, plotfile, plottitle,
    field_min, field_max, nlevel,
    lon, lat, field, symmetric=False):

    logging.info(plotfile)

    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')

    # ax = plt.axes(projection=ccrs.Robinson())
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-140, -100, 30, 50])

    lon_mesh, lat_mesh = np.meshgrid(lon, lat)

    levels = np.linspace(field_min, field_max,
        nlevel, endpoint=True)
    logging.info(levels)

    extend_option = 'both' if symmetric else 'max' 
    # cmap_option = plt.cm.gist_rainbow if symmetric else plt.cm.gist_ncar
    cmap_option = plt.cm.gist_ncar

    cp = ax.contourf(lon_mesh, lat_mesh, field, levels,
        cmap=cmap_option, extend=extend_option,
        transform=ccrs.PlateCarree())

    ax.gridlines()
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(states_provinces)

    plt.title(plottitle)
    cbar = plt.colorbar(cp,
        orientation='horizontal', pad=0.01)

    plt.savefig(os.path.join(plotdir, plotfile) + '.png',
        bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(plotdir, plotfile) + '.pdf',
        bbox_inches='tight')
    plt.clf()

