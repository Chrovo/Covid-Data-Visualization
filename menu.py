#Momo and Abhiram - Make menu
from __future__ import annotations

from typing import Any, Callable, TYPE_CHECKING

import matplotlib.artist as artist
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.transforms import IdentityTransform

if TYPE_CHECKING:
    from matplotlib.figure import Figure

# select what you want to filter by - deaths, hospitalizations, or cases
# select the day, month, year

# fontsize, label color, background color, alpha = 1.0

class MenuItem(artist.Artist):
    padx = 5
    pady = 5

    def __init__(self, fig: Figure, label_str: str, on_select: Callable[..., Any]) -> None:
        super().__init__()

        self.set_figure(fig)
        self.label_str = label_str

        self.props = (14, 'black', 'white', 1.0)
        self.hoverprops = (14, 'black', 'white', 1.0)

        self.on_select = on_select

        self.label = fig.text(0, 0, label_str, transform=IdentityTransform(), size=self.props[0])
        self.text_bbox = self.label.get_window_extent(
            fig.canvas.get_renderer()
        )

        self.rect = patches.Rectangle((0, 0), 1, 1)  # Will be updated later.

        self.set_hover_props(False)

        fig.canvas.mpl_connect('button_release_event', self.check_select)

    def check_select(self, event):
        over, _ = self.rect.contains(event)
        if not over:
            return
        if self.on_select is not None:
            self.on_select(self)

    def set_extent(self, x, y, w, h, depth):
        self.rect.set(x=x, y=y, width=w, height=h)
        self.label.set(position=(x + self.padx, y + depth + self.pady/2))
        self.hover = False

    def draw(self, renderer):
        self.rect.draw(renderer)
        self.label.draw(renderer)

    def set_hover_props(self, b):
        props = self.hoverprops if b else self.props
        self.label.set(color=props[1])
        self.rect.set(facecolor=props[2], alpha=props[3])

    def set_hover(self, event):
        b, _ = self.rect.contains(event)
        changed = (b != self.hover)
        if changed:
            self.set_hover_props(b)
        self.hover = b
        return changed


class Menu:
    def __init__(self, fig: Figure, menuitems) -> None:
        self.figure = fig

        self.menuitems = menuitems

        maxw = max(item.text_bbox.width for item in menuitems)
        maxh = max(item.text_bbox.height for item in menuitems)
        depth = max(-item.text_bbox.y0 for item in menuitems)

        x0 = 100
        y0 = 400

        width = maxw + 2*MenuItem.padx
        height = maxh + MenuItem.pady

        for item in menuitems:
            left = x0
            bottom = y0 - maxh - MenuItem.pady

            item.set_extent(left, bottom, width, height, depth)

            fig.artists.append(item)
            y0 -= maxh + MenuItem.pady

        fig.canvas.mpl_connect('motion_notify_event', self.on_move)

    def on_move(self, event):
        if any(item.set_hover(event) for item in self.menuitems):
            self.figure.canvas.draw()
