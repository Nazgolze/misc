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
import random 
import string
import time

def make(x, y, width, height):
    return [[(x+1+width)%width, (y+1+height)%height], [(x+1+width)%width, (y+height)%height], [(x+1+width)%width, (y-1+height)%height], [(x-1+width)%width, (y+1+height)%height], [(x-1+width)%width, (y+height)%height], [(x-1+width)%width, (y-1+height)%height], [(x+width)%width, (y-1+height)%height], [(x+width)%width, (y+1+height)%height]]

def gol2(timg, tdrawable):
    t = timg
    td = tdrawable
    f = t.filename
    for i in xrange(0, 100, 1):
        gol(t, td)
        td = t.layers[0]

def gol(timg, tdrawable):
    bgcolor = 255 
    def gol_basic():
        begin = time.time() 
        width = tdrawable.width
        height = tdrawable.height
        l = timg.active_layer
        l.add_alpha()
        pr = l.get_pixel_rgn(0, 0, width, height)
        
        #list_of_cells = {}
        cell_list = []
        livelist = []
        deathlist = []
        color_change_list = []
        gimp.progress_init()
        percent = 0
        counter = 0
        test = 0
        for i in xrange(0, width, 1):
            for j in xrange(0, height, 1):
                #next line will create a list with color and list of neighbors
                #list_of_cells[(i, j)] = [pr[i, j], make(i, j, width, height)]
                for z in make(i,j,width,height):
                    if pr[z[0],z[1]] != (chr(bgcolor) + chr(bgcolor) + chr(bgcolor) + chr(255)):
                        test = test + 1
                if pr[i,j] != (chr(bgcolor) + chr(bgcolor) + chr(bgcolor) + chr(255)) or test > 0:
                    cell_list.append([[i,j], make(i, j, width, height), pr[i,j]])
                    test = 0
                counter = counter + 1
                percent = counter / (1.0*width*height*4)
                gimp.progress_update(percent)
        counter = 0
        for i in cell_list:
            temp = 0
            counter = counter + 1.0
            percent = .25 + (counter / (len(cell_list)*4.0))
            gimp.progress_update(percent)
            l_color = []
            for j in i[1]:	    
                if pr[j[0],j[1]] != (chr(bgcolor) + chr(bgcolor) + chr(bgcolor) + chr(255)):	        
                    temp = temp + 1
            if pr[i[0][0],i[0][1]] == (chr(bgcolor) + chr(bgcolor) + chr(bgcolor) + chr(255)) and (temp == 2 or temp == 3):
                livelist.append(i)
                counterx = 0
                r = 0
                g = 0
                b = 0
                for x in i[1]:
                    if pr[x[0],x[1]] != (chr(bgcolor) + chr(bgcolor) + chr(bgcolor) + chr(255)):
                        rtemp = ord(pr[x[0],x[1]][0])
                        gtemp = ord(pr[x[0],x[1]][1])
                        btemp = ord(pr[x[0],x[1]][2])
                        r = r + rtemp
                        g = g + gtemp
                        b = b + btemp
                        counterx = counterx + 1
                r = (r / counterx) 
                g = (g / counterx) 
                b = (b / counterx)
                color_change_list.append([i[0], (chr(r) + chr(g) + chr(b) + chr(255))])
            elif pr[i[0][0],i[0][1]] != (chr(bgcolor) + chr(bgcolor) + chr(bgcolor) + chr(255)) and temp >=1 and temp <= 5:
                #i[2] = chr(255) + chr(255) + chr(255) + chr(255)
                livelist.append(i)
            else:
                deathlist.append(i[0])
        counter = 0
        for i in deathlist:
            counter = counter + 1
            percent = .50 + (counter / (len(deathlist)*4.0))
            gimp.progress_update(percent)
            pr[i[0],i[1]] = (chr(bgcolor) + chr(bgcolor) + chr(bgcolor) + chr(255))
        counter = 0
        for i in livelist:
            counter = counter + 1
            percent = .75 + (counter / (len(livelist)*4.0))
            gimp.progress_update(percent)
            #pr[i[0][0],i[0][1]] = (chr(255) + chr(255) + chr(255) + chr(255))
            #pr[i[0][0],i[0][1]] = (chr(i[2][0]) + chr(i[2][1]) + chr(i[2][2]) + chr(255))
            pr[i[0][0],i[0][1]] = i[2]
        for i in color_change_list:
            pr[i[0][0],i[0][1]] = i[1]
        gimp.progress_update(100)
        l.flush() 
        timg.flatten()
        end = time.time()
        print (end - begin)
    gol_basic()

def randomstuff(timg, tdrawable):
    width = tdrawable.width
    height = tdrawable.height
    l = timg.active_layer
    l.add_alpha()
    pr = l.get_pixel_rgn(0, 0, width, height)
    for i in xrange(0, width, 1):
        for j in xrange(0, height, 1):
    	    pr[i,j] = chr(int(random.random()*255)) + chr(int(random.random()*255)) + chr(int(random.random()*255)) + chr(255) 
    l.flush() 
    timg.flatten()
    
register(
        "GameofLife",
        "I hope this works",
        "Please let this work",
        "Juan Gonzalez",
        "Juan Gonzalez",
        "2006",
        "<Image>/Filters/Map/_Game of Life",
        "RGB*, GRAY*",
        [],
        [],
        gol)
register(
        "GameofLife2",
        "I hope this works",
        "Please let this work",
        "Juan Gonzalez",
        "Juan Gonzalez",
        "2006",
        "<Image>/Filters/Map/Game of Life x10",
        "RGB*, GRAY*",
        [],
        [],
        gol2)
register(
        "random",
        "I hope this works",
        "Please let this work",
        "Juan Gonzalez",
        "Juan Gonzalez",
        "2006",
        "<Image>/Python-Fu/Alchemy/Random",
        "RGB*, GRAY*",
        [],
        [],
        randomstuff)
main()
