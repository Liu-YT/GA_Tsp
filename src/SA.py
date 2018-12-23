from sys import argv, float_info
from io_helper import read_tsp, city
import matplotlib.pyplot as plt
import random
import math

# temperature
T = 100.0

# temperature drop rate
alpha = 0.98 

# distance
distance = []

# search times
SEARCHTIMES = 5000

# calculate path total distance
def evaluate(path):
    dis = 0.0
    for i in range(len(path) - 1):
        dis += distance[path[i]][path[i+1]]
    return dis

def main():
    if len(argv) != 2:
        print("Correct use: python src/SA.py <filename>.tsp")
        return -1

    global T, alpha, SEARCHTIMES


    # get all cities
    cities = read_tsp(argv[1])

    # the num of city
    numOfCity = len(cities)

    SEARCHTIMES = numOfCity * numOfCity

    # Calculate the Euclidean distance between cities
    for i in range(numOfCity):
        toCity = []
        for j in range(len(cities)):
            toCity.append(int(((cities[i].x - cities[j].x)**2 + (cities[i].y - cities[j].y)**2)**0.5 + 0.5))
        distance.append(toCity)

    # init
    path = [i for i in range(numOfCity)]
    random.shuffle(path)

    # add start city in path
    path.append(path[0])
    
    dis = evaluate(path)

    """
    field operation
    two points crossed, the middle is reversed
    """
    while(T > 0.01):
        for i in range(1000):
            first = random.randint(1, len(path)-3)
            second = random.randint(first+1, len(path)-2)
            dE = distance[path[first-1]][path[second]] - distance[path[first-1]][path[first]] \
                + distance[path[second+1]][path[first]] - distance[path[second+1]][path[second]]
            if dE <= 0 or random.random() < math.exp(-dE / T):
                path[first:second+1] = path[second:first-1:-1]
                dis = dis + dE
        T *= alpha

        plt.clf()
        ax = plt.axes()
        ax.set_title('Distance: ' + str(dis))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        for n in range(len(path)-1):
            plt.plot([cities[path[n]].x, cities[path[n + 1]].x], [cities[path[n]].y, cities[path[n+1]].y], '-ro')
        plt.pause(0.001)    

    # output
    print(path)
    print(dis)
    plt.clf()
    ax = plt.axes()
    ax.set_title('Distance: ' + str(dis))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for n in range(len(path)-1):
        plt.plot([cities[path[n]].x, cities[path[n + 1]].x], [cities[path[n]].y, cities[path[n+1]].y], '-ro')
    plt.show() 

if __name__ == "__main__":
    main()