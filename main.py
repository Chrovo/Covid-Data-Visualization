import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

MAP: Basemap = Basemap(llcrnrlon=-130, llcrnrlat=25, urcrnrlon=-65.,urcrnrlat=52., lat_0 = 40., lon_0 = -80)

# load the shapefile, use the name 'states'
MAP.readshapefile('st99_d00', name='states', drawbounds=True)

# collect the state names from the shapefile attributes so we can
# look up the shape obect for a state by it's name
state_names = [shape_dict['NAME'] for shape_dict in MAP.states_info]

ax = plt.gca() # get current axes instance

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}


state_names = [us_state_to_abbrev[name] for name in state_names]
print(state_names)

# RGB Functions
def cmyk_to_rgb(c, m, y, k, cmyk_scale, rgb_scale=255):
    r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    return int(r), int(g), int(b)

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def cmyk_to_hex(c,m,y,k):
    return rgb_to_hex(cmyk_to_rgb(c,m,y,k,100, 255))

# Dictionary containing deaths of each states
deaths = {}
max = 0

with open('all-states-history.csv', 'r') as data:
    data = data.readlines()
    data = data[1:]
    for line in data:
        values = line.split(",")
        #print(values)
        if values[0] != '\"2021-03-07\"': 
            break
        deaths[values[1].strip("\"")] = int(values[2])
        if int(values[2]) > max:
            max = int(values[2])
        
print(deaths)
# a = ''
# #FF2D00 -> #CF2500 -> #A71E00 -> #841700

for index in range(len(MAP.states)):
    death_count = deaths[state_names[index]]
    hex = cmyk_to_hex(0, int(min(death_count / 17500.000 * 100, 100)), 100, 0)
    poly = Polygon(MAP.states[index], facecolor=hex,edgecolor=hex)
    ax.add_patch(poly)

plt.show()

# # background color
# MAP.drawmapboundary(fill_color='#A6CAE0', color="black")

# # country color
# MAP.fillcontinents(color='#e6b800',lake_color='#A6CAE0')
# MAP.drawcountries(color='grey', linewidth=1)

# # Show states
# MAP.drawstates(color='lightgrey', linewidth=1)

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


# MAP.scatter(x, y, color='red', latlon=True)


# plt.show()