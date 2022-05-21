import matplotlib
import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap(llcrnrlon=-130, llcrnrlat=25, urcrnrlon=-65.,urcrnrlat=52., lat_0 = 40., lon_0 = -80)
 
# background color
map.drawmapboundary(fill_color='#A6CAE0', color="black")

# country color
map.fillcontinents(color='#e6b800',lake_color='#A6CAE0')
map.drawcountries(color='grey', linewidth=1)

# Show states
map.drawstates(color='lightgrey', linewidth=1)

plt.show()