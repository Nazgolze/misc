#!/usr/bin/env python

#   Gimp-Python - allows the writing of Gimp plugins in Python.
#   Copyright (C) 1997  James Henstridge <james@daa.com.au>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import math
from gimpfu import *
def python_center_layer(image, layer):
    x = (image.width - layer.width) / 2
    y = (image.height - layer.height) / 2
    layer.set_offsets(x, y)


register(
    "python_fu_center_layer",
    "Center a layer on the image",
    "Center a layer on the image",
    "Manish Singh",
    "Manish Singh",
    "2004",
    "<Image>/Python-Fu/Center Layer",
    "",
    [],
    [],
    python_center_layer)

main()
