## Some tricks to help make pretty maps in Python!

def Graticule(Resolution = 1, Spacing = 30):
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import LineString
    
    lon_grid = np.arange(-180, 181, Spacing)
    lat_grid = np.arange(-90, 91, Resolution)
    
    Type = []
    Value = []
    Lines = []
    for lon in lon_grid:
        X = []
        Y = []
        Type.append("Meridian")
        Value.append(lon)
        for lat in lat_grid:
            X.append(lon)
            Y.append(lat)
        Lines.append(LineString([x for x in zip(X, Y)]))
        
        
    lon_grid = np.arange(-180, 181, Resolution)
    lat_grid = np.arange(-90, 91, Spacing)
    for lat in lat_grid:
        X = []
        Y = []
        Type.append("Paralell")
        Value.append(lat)
        for lon in lon_grid:
            X.append(lon)
            Y.append(lat)
        Lines.append(LineString([x for x in zip(X, Y)]))
    Grat = gpd.GeoDataFrame(data = {'Type':Type,'Value':Value},geometry=Lines,crs='WGS84')  
    
    return(Grat)

def scalebar(ax,distance=100,label='100 m',scale=5e-2,pos='lower left',Frame=True):
    from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
    ax.add_artist(AnchoredSizeBar(ax.transData,
                           distance, label, pos, 
                           pad=0.3,
                           frameon=Frame,
                           size_vertical=distance*scale,
                          ))

class arrow_Box:
    from matplotlib.patches import BoxStyle
    from matplotlib.path import Path

    """A simple box."""

    def __init__(self, pad=0.3):
        """
        The arguments must be floats and have default values.

        Parameters
        ---------- 
        pad : float
            amount of padding
        """
        self.pad = pad
        super().__init__()

    def __call__(self, x0, y0, width, height, mutation_size):
        """
        Given the location and size of the box, return the path of the box
        around it.

        Rotation is automatically taken care of.

        Parameters
        ----------
        x0, y0, width, height : float
            Box location and size.
        mutation_size : float
            Reference scale for the mutation, typically the text font size.
        """
        # padding
        pad = mutation_size * self.pad
        # width and height with padding added
        width = width + 2.*pad
        height = height + 2.*pad
        # boundary of the padded box
        x0, y0 = x0 - pad, y0 - pad
        x1, y1 = x0 + width, y0 + height
        # return the new path
        return Path([(x0, y0),
                     (x1, y0), 
                     (x1, y1),
                     ((x0+x1)/2.,y1+pad*1.5), 
                     (x0, y1),
                     (x0, y0),
                     (x0, y0)],
                    closed=True)


def North_Arrow(ax,fontsize=12,x=0.05,y=0.1):

    BoxStyle._style_list["northarrow"] = arrow_Box  # Register the custom style.

    ax.text(x, y, "N", size=fontsize, va="center", ha="center", rotation=0,transform=ax.transAxes,
            bbox=dict(boxstyle="northarrow,pad=0.13", fc='white',ec='k',lw=1))
    del BoxStyle._style_list["northarrow"]  # Unregister it.


class LegendTitle(object):
    def __init__(self, text_props=None):
        self.text_props = text_props or {}
        super(LegendTitle, self).__init__()

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        title = mtext.Text(x0, y0, orig_handle,  **self.text_props)
        handlebox.add_artist(title)
        return title