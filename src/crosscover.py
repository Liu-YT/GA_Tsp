# ox
def crosscover(population, numOfCity):
    # order crossover
    for i in range(int(POPSIZE / 2)-1):
        # chromosomeFir = random.randint(1, POPSIZE-1)
        # chromosomeSec = random.randint(1, POPSIZE-1)
        chromosomeFir = i * 2
        chromosomeSec = i * 2 + 1
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

        chromosomeFir = i * 2
        chromosomeSec = i * 2 + 1
        if random.random() <= PXOVER:
            index = random.randint(1, numOfCity-2)
            newIndividual_i = []
            newIndividual_j = []
            k = 0
            for j in range(numOfCity):
                if j <= index:
                    newIndividual_i.append(population[chromosomeFir][j])
                else:
                    while k < numOfCity:
                        if population[chromosomeSec][k] not in population[chromosomeFir][0:index+1]:
                            newIndividual_i.append(population[chromosomeSec][k])
                            k += 1
                            break
                        k += 1            
            k = 0            
            for j in range(numOfCity):
                if j > index:
                    newIndividual_j.append(population[chromosomeSec][j])
                else:
                     while k < numOfCity:
                        if population[chromosomeFir][k] not in population[chromosomeSec][index+1:]:
                            newIndividual_j.append(population[chromosomeFir][k])
                            k += 1
                            break
                        k += 1
            population[chromosomeFir] = newIndividual_i[:]
            population[chromosomeSec] = newIndividual_j[:]