from typing import Optional

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
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
def cmyk_to_rgb(
    c: int, 
    m: int, 
    y: int, 
    k: int, 
    cmyk_scale: int, 
    rgb_scale: int = 255
) -> tuple[int, int, int]:
    r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    return int(r), int(g), int(b)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % rgb


def cmyk_to_hex(c: int, m: int, y: int, k: int) -> str:
    return rgb_to_hex(cmyk_to_rgb(c, m, y, k, 100, 255))


def color_map(
    MAP: Basemap,
    to_plot: str,
    day: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
) -> None:
    index = -1
    if to_plot == "deaths":
        index = 2
    elif to_plot == "hospitalized":
        index = 6
    else:
        index = 19

    MAP.readshapefile("st99_d00", name="states", drawbounds=True)
    state_names = [us_state_to_abbrev[shape_dict["NAME"]] for shape_dict in MAP.states_info]

    date = ""
    if year is not None:
        date += str(year)
    if month is not None and month != 0:
        date += "-" + "%02x" % month
    if day is not None and day != 0:
        date += "-" + "%02x" % day

    ax = plt.gca()

    # Dictionary containing the number of deaths, hospitalizations, or cases in each state
    deaths = {}
    _sum = 0
    count = 0
    most = 0

    # index:    0       1       2          6             19
    # format: "date","state","death","hospitalized", "positive"
    with open("all-states-history.csv", "r") as data:
        data = data.readlines()
        data = data[1:]
        for line in data:
            values = line.split(",")
            state = values[1].strip('"')
            if not values[0].strip('"').startswith(date):
                continue
            if state not in deaths:
                deaths[state] = 0
            if values[index]:
                deaths[state] += int(values[index])
                _sum += int(values[index])
                count += 1

    average = _sum / count
    death_list = tuple(deaths.values())
    most = max(death_list)

    average = (most + average) / 2
    for index in range(len(MAP.states)):
        death_count = deaths[state_names[index]] # bc of missing data in CSV file
        hex = cmyk_to_hex(0, int(min(death_count / average * 100, 100)), 100, 0)
        poly = Polygon(MAP.states[index], facecolor=hex, edgecolor=hex)
        ax.add_patch(poly)

    plt.title(to_plot)

    plt.show()
    return
