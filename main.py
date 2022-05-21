import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from color_map import color_map
from menu import Menu, MenuItem

MAP: Basemap = Basemap(llcrnrlon=-130, llcrnrlat=25, urcrnrlon=-65.,urcrnrlat=52., lat_0 = 40., lon_0 = -80)

#color_map(MAP, None, 2, 2021)

    
# create button
# creating functionality to select the date
def date() -> ...:
    ...


fig = plt.figure()
fig.subplots_adjust(left=0.3)

menuitems = []
for label in ('cases', 'hospitalized', 'deaths'):
    def on_select(item):
        print(f'you selected {item.label_str}')
    item = MenuItem(fig, label, on_select=on_select)
    menuitems.append(item)

menu = Menu(fig, menuitems)
plt.show()
