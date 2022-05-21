#Vivaan and sreeram - takes in date, and colors map based on that 
from typing import Optional

#  import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

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

# RGB Functions
def cmyk_to_rgb(c: int, m: int, y: int, k: int, cmyk_scale: int, rgb_scale: int = 255) -> tuple[int]:
    r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    return int(r), int(g), int(b)

def rgb_to_hex(rgb: tuple[str]) -> str:
    return '#%02x%02x%02x' % rgb

def cmyk_to_hex(c: int, m: int, y: int, k: int) -> str:
    return rgb_to_hex(cmyk_to_rgb(c, m, y, k, 100, 255))

def color_map(MAP: Basemap, day: Optional[int] = None, month: Optional[int] = None, year: Optional[int] = None):
    #format date   
    MAP.readshapefile('st99_d00', name='states', drawbounds=True)
    state_names = [us_state_to_abbrev[shape_dict['NAME']] for shape_dict in MAP.states_info]
    date = ""
    if year is not None:
        date += str(year)
    if month is not None:
        date += "-" + "%02x" % month
        print()
    if day is not None:
        date += "-" + "%02x" % day

    ax = plt.gca()
    
    # Dictionary containing deaths of each states
    deaths = {}
    sum = 0
    count = 0
    print(date)
    most = 0
    with open('all-states-history.csv', 'r') as data:
        data = data.readlines()
        data = data[1:]
        for line in data:
            values = line.split(",")
            if not values[0].strip("\"").startswith(date): 
                continue
            if values[1].strip("\"") not in deaths:
                deaths[values[1].strip("\"")] = 0
            if values[2] != "":
                deaths[values[1].strip("\"")] += int(values[2])
                sum += int(values[2])
                count += 1
            
    # print(deaths)
    average = sum / count
    death_list = list(deaths.values())
    most = max(death_list)
    # max = max(list(deaths.values()))
    print(average, most)
    average = (most + average) / 2
    for index in range(len(MAP.states)):
        death_count = deaths[state_names[index]]
        hex = cmyk_to_hex(0, int(min(death_count / average * 100, 100)), 100, 0)
        poly = Polygon(MAP.states[index], facecolor=hex,edgecolor=hex)
        ax.add_patch(poly)

    plt.show()
    return

