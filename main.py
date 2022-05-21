import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from color_map import color_map
from menu import Menu, MenuItem

MAP: Basemap = Basemap(llcrnrlon=-130, llcrnrlat=25, urcrnrlon=-65.,urcrnrlat=52., lat_0 = 40., lon_0 = -80)

color_map(MAP, "hospitalized", None, 2, 2021)

