import numpy as np
import re

class city:
    def __init__(self, cityName, x, y):
        self.cityName = cityName
        self.x = x
        self.y = y

def read_tsp(filename):
    """
    Read a file in .tsp format into a pandas DataFrame
    """
    with open(filename) as file:
        cities = []
        flag = False
        for line in file.readlines()[0:-1]:
            if line.startswith('EOF'):
                break
            if line.startswith('NODE_COORD_SECTION'):
                flag = True
            elif flag == True:
                info = re.split('[ ]+', line.strip())
                cities.append(city(info[0], float(info[1]), float(info[2])))
            
        ## check cities
        # for i in range(len(cities)) :
        #     print(cities[i].x, cities[i].y)
    return cities
