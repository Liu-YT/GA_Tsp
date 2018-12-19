from sys import argv, float_info
from io_helper import read_tsp, city
import matplotlib.pyplot as plt
import random
import math

filename = "../assets/ch130.tsp"

# population size
POPSIZE = 50

# max number of generations
MAXGENS = 100

# probability of crosscover
PXOVER = 0.9

# probability of mutation
PMUTATION = 0.15

# distance
distance = []

# Initial population
def initPopulation(cities, numOfCity):
    population = []
    # for _ in range(POPSIZE):
    #     individual = []
    #     nextCity = random.randint(0, numOfCity-1)
    #     individual.append(nextCity)
    #     for j in range(numOfCity-1):
    #         if random.random() <= 0.5:
    #             nextCity = random.randint(0, numOfCity-1)
    #             while nextCity in individual:
    #                 nextCity = random.randint(0, numOfCity-1)
    #             individual.append(nextCity)
    #         else:
    #             mixDis = float_info.max 
    #             bestId = 0
    #             for k in range(numOfCity):
    #                 if (k not in individual) and distance[individual[-1]][k] < mixDis:
    #                     bestId = k
    #                     mixDis = distance[individual[-1]][k]
    #             individual.append(bestId)
    #     population.append(individual[:])

    individual = [i for i in range(numOfCity)]
    for _ in range(int(POPSIZE * 6 / 10)):
        random.shuffle(individual)
        population.append(individual[:])    
    for _ in range(POPSIZE - len(population)):
        start = random.randint(0, numOfCity-1)
        gIndividual = []
        gIndividual.append(start)
        j = 1
        while j < numOfCity:
            mixDis = float_info.max 
            i, bestId = 0, 0
            while i < numOfCity:
                if (i not in gIndividual) and i != gIndividual[-1] and distance[gIndividual[-1]][i] < mixDis:
                    bestId = i
                    mixDis = distance[gIndividual[-1]][i]
                i += 1
            j = j + 1
            gIndividual.append(bestId)
        population.append(gIndividual[:]) 
    random.shuffle(population)
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
    for i in range(POPSIZE):
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
    subPopulation = []
    for i in range(int(POPSIZE / 2)-1):
        if random.random() <= PXOVER:
            chromosomeFir = i * 2
            chromosomeSec = i * 2 + 1
            # chromosomeFir = random.randint(0, POPSIZE-1)
            # chromosomeSec = random.randint(0, POPSIZE-1)
            # while chromosomeFir == chromosomeSec:
            #     chromosomeSec = random.randint(0, POPSIZE-1)
            start = random.randint(0, numOfCity - 2)
            end = random.randint(start + 1, numOfCity - 1)
            newIndividual_i = []
            newIndividual_j = []
            k = 0
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
            k = 0      
            for j in range(numOfCity):
                if population[chromosomeSec][j] in population[chromosomeFir][start:end]:
                    newIndividual_j.append(population[chromosomeSec][j])
                else:
                    if k == start:
                        k = end
                    newIndividual_j.append(population[chromosomeFir][k])
                    k += 1
            subPopulation.append(newIndividual_i[:])
            subPopulation.append(newIndividual_j[:])
    
    # competition
    subPopulation.sort(key = lambda x: evaluate(x))
    subPopulation = mutate(subPopulation, numOfCity)
    subPopulation = localSearch(subPopulation, numOfCity)
    for i in range(len(subPopulation)):
        for j in range(POPSIZE):
            if evaluate(subPopulation[i]) < evaluate(population[j]):
                population[j] = subPopulation[i]
                break

    return population

# mutation operation
def mutate(population, numOfCity):
    for i in range(len(population)):
        if random.random() <= PMUTATION:
            geneFir = random.randint(0,numOfCity-1)
            geneSec = random.randint(0, numOfCity-1)
            while geneFir == geneSec:
                geneSec = random.randint(0, numOfCity-1)
            population[i][geneFir], population[i][geneSec] = population[i][geneSec], population[i][geneFir]
    return population

# local search
def localSearch(population, numOfCity):
    for i in range(len(population)):
        best = population[i][:]
        for _ in range(100):
            first = random.randint(0, numOfCity - 2)
            second = random.randint(first + 1, numOfCity - 1)
            if first != second:
                population[i][first], population[i][second] = population[i][second], population[i][first]
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
        population.sort(key = lambda x: evaluate(x))
        print(curGen, evaluate(population[10]), evaluate(population[0]))
        plt.clf()
        ax = plt.axes()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        for n in range(numOfCity - 1):
            plt.plot([cities[population[10][n]].x, cities[population[10][n + 1]].x], [cities[population[10][n]].y, cities[population[10][n+1]].y], '-ro')
        plt.plot([cities[population[10][-1]].x, cities[population[10][0]].x], [cities[population[10][-1]].y, cities[population[10][0]].y], '-ro')    
        plt.pause(0.001)
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
        plt.plot([cities[population[0][n]].x, cities[population[0][n + 1]].x], [cities[population[0][n]].y, cities[population[0][n+1]].y], '-ro')
    plt.plot([cities[population[0][-1]].x, cities[population[0][0]].x], [cities[population[0][-1]].y, cities[population[0][0]].y], '-ro')
    plt.show()

if __name__ == "__main__":
    main()