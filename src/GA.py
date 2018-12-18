from sys import argv, float_info
from io_helper import read_tsp, city
import matplotlib.pyplot as plt
import re
import random
import math

filename = "../assets/ch130.tsp"

# population size

POPSIZE = 100
# max number of generations
MAXGENS = 1000

# probability of crosscover
PXOVER = 0.7

# probability of mutation
PMUTATION = 0.1

# 存储结点的距离 
distance = []

# Initial population
def initPopulation(cities, numOfCity):
    population = []
    for i in range(POPSIZE):
        individual = []
        j = 0
        while j < numOfCity:
            index = random.randint(0, numOfCity-1)
            if index not in individual:
                individual.append(index)
                j = j + 1
        population.append(individual)    
    return population

# calculate indibidual fitness
def evaluate(individual):
    fitness = 0.0
    for i in range(len(individual) - 1):
        fitness += distance[individual[i]][individual[i+1]]
    # back to starting point
    fitness += distance[individual[len(individual)-1]][individual[0]]
    return fitness

# selection operation
def select(population, numOfCity):
    newPopulation = []
    best = float_info.max
    bestId = 0
    fitness = []
    sumOfFitness = 0.0

    # evalute
    for i in range(len(population)):
        fit = evaluate(population[i])
        fitness.append(1 / fit)
        sumOfFitness += 1 / fit
        if (best > fit) :
            best = fit
            bestId = i

    # choosing the best individual to directly inherit to the next generation
    newPopulation.append(population[bestId])

    # cumulative probability
    cumPro = []
    for i in range(POPSIZE):
        if i == 0:
            cumPro.append(fitness[i] / sumOfFitness)
        else:
            cumPro.append(fitness[i] / sumOfFitness + cumPro[i-1])       
    
    # roulette selection of offspring
    for i in range(POPSIZE-1):
        pro = random.random()
        for j in range(POPSIZE):
            if cumPro[j] >= pro:
                newPopulation.append(population[j])
                break
    return newPopulation

# crossover operation
def crosscover(population, numOfCity):
    # order crossover
    for _ in range(POPSIZE):
        chromosomeFir = random.randint(1, POPSIZE-1)
        chromosomeSec = random.randint(1, POPSIZE-1)
        if chromosomeFir == chromosomeSec:
            continue
        if random.random() <= PXOVER:
            start = random.randint(0, numOfCity - 2)
            end = random.randint(start + 1, numOfCity - 1)
            newIndividual_i = []
            newIndividual_j = []
            j, k = 0, 0
            for j in range(numOfCity):
                if j >= start and j < end:
                    newIndividual_i.append(population[chromosomeFir][j])
                    j = end
                else:
                    while k < numOfCity:
                        if population[chromosomeSec][k] not in population[chromosomeFir][start:end]:
                            newIndividual_i.append(population[chromosomeSec][k])
                            k += 1
                            break
                        k += 1
            j, k = 0, 0            
            for j in range(numOfCity):
                if population[chromosomeSec][j] in population[chromosomeFir][start:end]:
                    newIndividual_j.append(population[chromosomeSec][j])
                else:
                    if k == start:
                        k = end
                    newIndividual_j.append(population[chromosomeFir][k])
                    k += 1
            population[chromosomeFir] = newIndividual_i[:]
            population[chromosomeSec] = newIndividual_j[:]
    return population

# mutation operation
def mutate(population, numOfCity):
    for i in range(POPSIZE):
        if random.random() <= PMUTATION:
            geneFir = random.randint(0,numOfCity-1)
            geneSec = random.randint(0, numOfCity-1)
            if geneFir != geneSec:
                temp = population[i][geneFir]
                population[i][geneFir] = population[i][geneSec]
                population[i][geneSec] = temp
    return population

# local search
def localSearch(population, numOfCity):
    for i in range(POPSIZE):
        best = population[i][:]
        for _ in range(100):
            first = random.randint(1, numOfCity - 2)
            second = random.randint(first + 1, numOfCity - 1)
            if first != second:
                population[i][first:second+1] = population[i][second:first-1:-1]
                if evaluate(best) > evaluate(population[i]):
                    best = population[i][:]
        population[i] = best[:]
    return population

def main():
    # if len(argv) != 2:
    #     print("Correct use: python src/GA.py <filename>.tsp")
    #     return -1
    cities = read_tsp(filename)

    # the num of city
    numOfCity = len(cities)

    # Calculate the Euclidean distance between cities
    for i in range(len(cities)):
        node = []
        for j in range(len(cities)):
            node.append(int(((cities[i].x - cities[j].x)**2 + (cities[i].y - cities[j].y)**2)**0.5 + 0.5))
        distance.append(node)

    population = initPopulation(cities, numOfCity)
    curGen = 0 
    while curGen < MAXGENS:
        population = select(population, numOfCity)
        population = crosscover(population, numOfCity)
        # population = mutate(population, numOfCity)
        population = localSearch(population, numOfCity)
        curGen += 1

    # find best
    best = float_info.max
    bestId = 0
    for i in range(POPSIZE):
        fit = evaluate(population[i])
        if (best > fit) :
            best = fit
            bestId = i
    print(population[bestId])
    print(best)
    plt.clf()
    ax = plt.axes()
    ax.set_title('130 city problem (Churritz)')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for n in range(numOfCity - 1):
        plt.plot([cities[n].x, cities[n+1].x], [cities[n].y, cities[n + 1].y], '-ro')
    plt.show()

if __name__ == "__main__":
    main()