from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from tkinter import *

from color_map import color_map

MAP: Basemap = Basemap(llcrnrlon=-130, llcrnrlat=25, urcrnrlon=-65,urcrnrlat=52, lat_0 = 40, lon_0 = -80)

root: Tk = Tk()
root.geometry('400x300')
root.config(bg='#00ffbb')

current_choice = 'cases'
current_day = 0
current_month = 0
current_year = 2020

def on_select_option(choice: str) -> None:
    global current_choice
    current_choice = choice

def on_select_days(choice: int) -> None:
    global current_day
    current_day = choice

def on_select_year(choice: int) -> None:
    global current_year
    current_year = choice

def on_select_month(choice: int) -> None:
    global current_month
    current_month = choice

def on_click() -> None:
    color_map(MAP, current_choice, int(current_day), int(current_month), int(current_year))

OPTIONS = ('cases', 'deaths', 'hospitalized')

variable = StringVar()
variable.set(OPTIONS[0])

option_dropdown = OptionMenu(root, variable, *OPTIONS, command=on_select_option)
option_dropdown.pack(expand=True)
option_dropdown.config(font = 'Georgia')

DAYS = tuple(range(32))
variable = IntVar()

day_dropdown = OptionMenu(root, variable, *DAYS, command=on_select_days)
day_dropdown.pack(expand=True)

MONTHS = tuple(range(13))
variable = IntVar()

month_dropdown = OptionMenu(root, variable, *MONTHS, command=on_select_month)
month_dropdown.pack(expand=True)

YEARS = (2020, 2021)
variable = IntVar()
variable.set(YEARS[0])

year_dropdown = OptionMenu(root, variable, *YEARS, command=on_select_year)
year_dropdown.pack(expand=True)
  
b = Button(root, text = "View Map", command=on_click)  
b.pack()
  
root.mainloop()