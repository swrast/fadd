#!/usr/bin/env python3

from Xlib import X
from Xlib.display import Display

disp = Display()
root = disp.screen().root

# get active window dimensions
atom = disp.intern_atom("_NET_ACTIVE_WINDOW")

class Pos():
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

pos = Pos(0, 0)

res = root.get_full_property(atom, X.AnyPropertyType)
if res.value[0] == 0:
    data = root.query_pointer()._data
    pos.x = data["root_x"]
    pos.y = data["root_y"]
else:
    window = disp.create_resource_object("window", res.value[0])
    geom = window.get_geometry()
    pos = geom.root.translate_coords(window.id, 0, 0)

# get active screen dimensions

x = y = w = h = 0

for z in root.xrandr_get_monitors().monitors:
    if z.x < pos.x and z.x + z.width_in_pixels + 1 > pos.x and \
        z.y < pos.y and z.y + z.height_in_pixels + 1 > pos.y:
        x, y, w, h = z.x, z.y, z.width_in_pixels, z.height_in_pixels

print(f"{w}x{h}+{x}+{y}")
