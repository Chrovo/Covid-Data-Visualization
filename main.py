import matplotlib
import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

map = Basemap(llcrnrlon=-130, llcrnrlat=25, urcrnrlon=-65.,urcrnrlat=52., lat_0 = 40., lon_0 = -80)

# load the shapefile, use the name 'states'
map.readshapefile('st99_d00', name='states', drawbounds=True)

# collect the state names from the shapefile attributes so we can
# look up the shape obect for a state by it's name
state_names = []
for shape_dict in map.states_info:
    print(shape_dict)
    state_names.append(shape_dict['NAME'])

ax = plt.gca() # get current axes instance


# get Texas and draw the filled polygon

for index in range(0, len(map.states)):
    
    if state_names[index] == "New Jersey":
        poly = Polygon(map.states[index], facecolor='red',edgecolor='red')
        ax.add_patch(poly)

plt.show()

# # background color
# map.drawmapboundary(fill_color='#A6CAE0', color="black")

# # country color
# map.fillcontinents(color='#e6b800',lake_color='#A6CAE0')
# map.drawcountries(color='grey', linewidth=1)

# # Show states
# map.drawstates(color='lightgrey', linewidth=1)

# x = []
# y = []
# with open('statelatlong.csv', mode='r') as csv_file:
#     csv_file = csv_file.readlines()
#     csv_file = csv_file[1:]
#     for line in csv_file:
#         values = line.split(",")
#         if values[0] == "AK" or values[0] == "HI":
#             continue
#         x.append(float(values[2]))
#         y.append(float(values[1]))


# map.scatter(x, y, color='red', latlon=True)


# plt.show()