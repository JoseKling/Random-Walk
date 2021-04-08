#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 10:22:05 2021

@author: kling
"""

#%% Packages

import numpy as np
from numpy.linalg import norm
import random
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

#%% Classes

class Drunk:
   ''' 
   This class is used only as a superclass. It only initializes a name and
   prints its name.
   Each subclass has its own 'move' method and possibly its own parameters.
   ''' 
   def __init__(self, name):
       self.name = name
    
   def __str__(self):
       return(str(self.name))

class FourDirectionsDrunk(Drunk):
    '''
    This drunk moves 1 step in any of the 4 cardinal directions with equal
    probability.
    '''
  
    def __init__(self, name = '4 Directions'):
        super().__init__(name)
        
    def move(self):
        step = random.choice([[1,0], [0,1], [-1,0], [0,-1]]) 
        return(np.array(step))
    
class FourDNorthBiasedDrunk(Drunk):
    '''
    This drunk has an equal probability of moving 1 step east, 1 step west,
    1.1 step north or 0.9 step south. 
    '''
    def __init__(self, name = '4D North Biased'):
        super().__init__(name)
        
    def move(self):
        step = random.choice([[1.1,0], [0,1], [-0.9,0], [0,-1]]) 
        return(np.array(step))
    
class AnyDirectionDrunk(Drunk):
    '''
    This drunk takes a step to any direction with equal probability.
    '''
    def __init__(self, name = 'Any Direction'):
        super().__init__(name)
        
    def move(self):
        # length = random.random()
        length = 1
        angle = random.random()
        step = [np.sin(2*np.pi*angle), np.cos(2*np.pi*angle)]
        return(np.array(step)*length)
    
class AnyDirectionLengthDrunk(Drunk):
    '''
    This drunk takes an any sized step (0 to 1) to any direction with equal probability.
    '''
    def __init__(self, name = 'Any Direction and length'):
        super().__init__(name)
        
    def move(self):
        length = random.random()
        angle = random.random()
        step = [np.sin(2*np.pi*angle), np.cos(2*np.pi*angle)]
        return(np.array(step)*length)
        
class Map:
    '''
    Intended as a superclass. It asks for a name, has a method for adding a
    drunk to the map, stores information about the drunks in the map, has a 
    '__str__' that displays the average distance each kind of drunk has
    traveled and 2 methods for plotting. One of them plots only the positions
    of each drunk, the other plots their positions and also the path they
    traveled.
    Subclasses may have other parameters and specifies how the drunks move.
    '''
    def __init__(self, name):
        self.name = name
        self.drunks = {}
        
    def add_drunk(self, drunk):
        self.drunks[drunk] = [self.start_point, [self.start_point], drunk.name]
        
    def __str__(self):
        message = ''
        values = list(self.drunks.values())
        distances = [norm(self.start_point-value[0]) 
                     for value in values]
        names = [value[2] for value in values]
        set_names = set(names)
        message = message + 'Name of the map: ' + self.name + '.\n'
        message = message + 'Names of the drunks in the map: '
        for name in set_names:
            message = message + name + ', '
        message = message[:-2] + '.\n'
        for name in set_names:
            avg = np.mean(np.array([distances[i] 
                                    for i in range(len(distances)) 
                                    if name==names[i]]))
            message = (message + 'Average distance of ' + 
                       name + ': ' + str(avg) + '.\n')
        avg = np.mean(np.array(distances))
        message = (message + 'Average distance from starting point: ' 
                   + str(avg) + '.')
        return(message)   
    
    def plot_positions(self, area=None):
        '''
        Parameter 'area' may be: None, 'All', int/float, length 2
        array/list/tuple or length 4 array/list/tuple.
        - None: Plots the area containing the whole paths of every drunk.
        - 'All': For maps with limited size. Plots the whole map.
        - int/float: Plots the area with this x and y axes length centered at 
        the starting point.
        - Length 2 array/list/tuple [x,y]: x is the length of the x axis and
        y is the length of the y axis. Centered at the starting point.
        - Length 4 array/list/tuple [x0,x1,y0,y1]: Plot the area of the rectangle
        defined by the corners (x0,y0) and (x1,y1).
        '''
        palette = ['r','b','g','y','purple','orange','gray','black']        
        values = list(self.drunks.values())
        xpositions = [value[0][1] for value in values]
        ypositions = [value[0][0] for value in values]
        xpositions.append(self.start_point[1])
        ypositions.append(self.start_point[0])
        colors = [value[2] for value in values]
        colors.append('Start')
        xpositions = xpositions[::-1]
        ypositions = ypositions[::-1]
        colors = colors[::-1]
        palette = palette[:len(set(colors))]
        figure = sns.scatterplot(x = xpositions, y = ypositions, 
                                 s=12, hue = colors, palette=palette)
        plt.axis('scaled')
        if area:
            if area=='All': 
                try: 
                    size = self.map_size
                    ax.set_xlim(0,size[0])
                    ax.set_ylim(0,size[1])
                except NameError:
                    print("Can't plot all of the map. Disregarding area parameter.")
            else:
                try:
                    if isinstance(area, int) or isinstance(area, float):
                        length = area/2
                        area = np.array([self.start_point[1]-length, 
                                         self.start_point[1]+length,
                                         self.start_point[0]-length, 
                                         self.start_point[0]+length])
                        ax.set_xlim(area[:2])
                        ax.set_ylim(area[2:])
                    elif len(area)==2:
                        length = np.array(area)/2
                        area = np.array([self.start_point[1]-length[0], 
                                         self.start_point[1]+length[0],
                                         self.start_point[0]-length[1], 
                                         self.start_point[0]+length[1]])
                        ax.set_xlim(area[:2])
                        ax.set_ylim(area[2:])
                    elif len(area)==4:
                        area = np.array(area)
                        ax.set_xlim(area[:2])
                        ax.set_ylim(area[2:])
                except:
                    print("Invalid 'area' parameter. Disregarding.")
        ax.legend(bbox_to_anchor=(1, 1), loc='upper left')
        return(figure)
        
    def plot_paths(self, jumps=False, area=None):
        '''
        Some maps may containg jumps, which may may not be plotted. If jumps
        is 'False', then they will not be plotted, but is a little slower.
        Parameter 'area' may be: None, 'All', int/float, length 2
        array/list/tuple or length 4 array/list/tuple.
        - None: Plots the area containing the whole paths of every drunk.
        - 'All': For maps with limited size. Plots the whole map.
        - int/float: Plots the area with this x and y axes length centered at 
        the starting point.
        - Length 2 array/list/tuple [x,y]: x is the length of the x axis and
        y is the length of the y axis. Centered at the starting point.
        - Length 4 array/list/tuple [x0,x1,y0,y1]: Plot the area of the rectangle
        defined by the corners (x0,y0) and (x1,y1).
        '''
        palette = ['r','b','g','y','purple','orange','gray','black']
        alpha = 0.3
        values = list(self.drunks.values())
        types = [value[2] for value in values]
        xpositions = [value[0][1] for value in values]
        ypositions = [value[0][0] for value in values]
        xpositions.append(self.start_point[0])
        ypositions.append(self.start_point[1])
        types.append('start')
        xpositions = xpositions[::-1]
        ypositions = ypositions[::-1]
        types = types[::-1]
        types_set = []
        for item in types:
            if item not in types_set:
                types_set.append(item)
        palette = palette[:len(types_set)]
        fig, ax = plt.subplots()
        if jumps:
            for drunk in self.drunks:
                vertices = list(self.drunks[drunk][1])
                x = np.array([vertex[1] for vertex in vertices])
                y = np.array([vertex[0] for vertex in vertices])
                jumps = np.array([vertex[2] for vertex in vertices])
                color = palette[types_set.index(self.drunks[drunk][2])]
                lines = [[(x[i],y[i]),(x[i+1],y[i+1])] 
                         for i in range(len(x)-1) if not jumps[i+1]]
                lc = LineCollection(lines, colors=color, 
                                    alpha=alpha, zorder=1)
                ax.add_collection(lc)
        else:
            for drunk in self.drunks:
                vertices = np.array(self.drunks[drunk][1])
                x = vertices[:,1]
                y = vertices[:,0]
                color = palette[types_set.index(self.drunks[drunk][2])]
                line = plt.Line2D(x, y, c=color, alpha=alpha, zorder=1)
                ax.add_line(line)
        sns.scatterplot(y=ypositions, x=xpositions, s=25, edgecolor='black',
                        hue=types, ax=ax, zorder=2, palette=palette)
        ax.axis('scaled')
        if area:
            if area=='All': 
                try: 
                    size = self.map_size
                    ax.set_xlim(0,size[0])
                    ax.set_ylim(0,size[1])
                except NameError:
                    print("Can't plot all of the map. Disregarding area parameter.")
            else:
                try:
                    if isinstance(area, int) or isinstance(area, float):
                        length = area/2
                        area = np.array([self.start_point[1]-length, 
                                         self.start_point[1]+length,
                                         self.start_point[0]-length, 
                                         self.start_point[0]+length])
                        ax.set_xlim(area[:2])
                        ax.set_ylim(area[2:])
                    elif len(area)==2:
                        length = np.array(area)/2
                        area = np.array([self.start_point[1]-length[0], 
                                         self.start_point[1]+length[0],
                                         self.start_point[0]-length[1], 
                                         self.start_point[0]+length[1]])
                        ax.set_xlim(area[:2])
                        ax.set_ylim(area[2:])
                    elif len(area)==4:
                        area = np.array(area)
                        ax.set_xlim(area[:2])
                        ax.set_ylim(area[2:])
                except:
                    print("Invalid 'area' parameter. Disregarding.")
        ax.legend(bbox_to_anchor=(1, 1), loc='upper left')
        return(ax)
    
class Plane(Map):        

    def __init__(self, name = 'Plane'):
        super().__init__(name)
        self.start_point = np.array([0,0])
        
    def move_drunk(self, drunk):
        try:
            step = drunk.move()
        except:
            raise Exception('This drunk cannot move.')
        position = self.drunks[drunk][0]+step
        self.drunks[drunk][0] = position
        self.drunks[drunk][1].append(position)
        
class Torus(Map):
    
    def __init__(self, map_size, name = 'Torus'):
        super().__init__(name)
        if isinstance(map_size, int) or isinstance(map_size, float):
            map_size = np.array([int(map_size), int(map_size)])
        self.start_point = np.array([int(map_size[1]/2), int(map_size[0]/2)])
        self.map_size = np.array(map_size)
        
    def add_drunk(self, drunk):
        super().add_drunk(drunk)
        self.drunks[drunk][1] = [[self.start_point[0], 
                                  self.start_point[1],
                                  False]]
        
    def move_drunk(self, drunk):
        try:
            step = drunk.move()
        except:
            raise Exception('This drunk cannot move.')
        position = self.drunks[drunk][0]+step
        if (position[0] >= self.map_size[0] or position[1] >= self.map_size[1] 
            or position[0] < 0 or position[1] < 0):
            jump = True
        else:
            jump = False
        position = position%self.map_size
        self.drunks[drunk][0] = position
        position = list(position)
        position.append(jump)
        self.drunks[drunk][1].append(position)
        
class Portals(Map):
    
    def __init__(self, entrances, exits, name = 'Portals'):
        if len(entrances) != len(exits):
            raise Exception('There must be same number of entrances and exits.')
        super().__init__(name)
        self.start_point = np.array([0,0])
        self.entrances = np.array(entrances)
        self.exits = np.array(exits)
        
    def add_drunk(self, drunk):
        super().add_drunk(drunk)
        self.drunks[drunk][1] = [[self.start_point[0],self.start_point[1],
                                  False]]        

    def move_drunk(self, drunk):
        try:
            step = drunk.move()
        except:
            raise Exception('This drunk cannot move.')
        position = self.drunks[drunk][0]+step
        previous = np.array(self.drunks[drunk][1][-1][:-1])
        jump = False
        for i, entrance in enumerate(self.entrances):
            if (norm(position-previous) == norm(entrance-previous) + 
                                           norm(entrance-position)):
                jump = True
                position = self.exits[i] + position - entrance
        self.drunks[drunk][0] = position
        position = list(position)
        position.append(jump)
        self.drunks[drunk][1].append(position)

#%% Test

if __name__ == '__main__':
   
    print('This is the drunk walk simulator. You can choose any number of' + 
          ' different drunks to be added to any of the maps and choose how' +
          ' many steps they will take.')
    print('For now we have the following drunks: four directions, four' +
          ' directions with a north bias, any direction and any direction' +
          ' and length.')
    print('We also have the following maps: plane, torus and portals.')
    field = int(input('What map do you choose? 0-Plane, 1-Torus, 2-Portals. '))
    fd = int(input('Choose how many of each type of drunk will be in the map.\n'
                   + 'How many four directions drunk? '))
    nb = int(input('How many four directions north biased drunk? '))
    ad = int(input('How many any direction drunk? '))
    dl = int(input('How many any direction and length drunk? '))
    number_steps = int(input('How many steps will they take? '))
    plot= int(input('What would you like to plot?\n' +
                    '0-Positions, 1-Paths '))
    
    n_drunks = {'FourDirectionsDrunk':fd, 
                 'FourDNorthBiasedDrunk':nb, 
                 'AnyDirectionDrunk':ad,
                 'AnyDirectionLengthDrunk':dl}
     
    maps = ['Plane', 'Torus', 'Portals']
   
    if field == 1:
        map_size = input('What is the maps size? ') #Fazer
        field = Torus(map_size)
    elif field == 2:
        portals = input('Location of the portals: ') #Fazer
        field = Portals(portals)
    else:
        field = Plane()
        jumps = False
    for drunk_name in n_drunks:
        for _ in range(n_drunks[drunk_name]):
            drunk = eval(str(drunk_name)+'()')
            field.add_drunk(drunk)
            for _ in range(number_steps):
                field.move_drunk(drunk)
    
    if plot == 0:
        ax = field.plot_positions()
        plt.show()
    else:
        ax = field.plot_paths()
        plt.show()