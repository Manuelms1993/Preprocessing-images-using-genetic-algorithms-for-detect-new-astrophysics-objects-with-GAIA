import numpy as np
import GaussianCreator
import astropy.io.fits
import matplotlib.pyplot as plt

def run(x, y, realImagePath,maxIter,individuals,stopIter):

    def getRegion():
        boxSize = GaussianCreator.size / 2
        realStar = np.zeros([boxSize*2, boxSize*2])
        boxXL = boxSize if x > boxSize else x
        boxXR = boxSize if x < 1024 - boxSize else 1024 - x
        boxYL = boxSize if y > boxSize else y
        boxYR = boxSize if y < 1024 - boxSize else 1024 - y
        hdulist = astropy.io.fits.open(realImagePath)
        databaseOriginal = hdulist[0].data
        region = databaseOriginal[int(x)-int(boxXL):int(x)+int(boxXR),int(y)-int(boxYL):int(y)+int(boxYR)]
        realStar[boxSize-int(boxXL):int(boxXR)+boxSize,boxSize-int(boxYL):boxSize+int(boxYR)] = region
        sky = np.median(realStar)
        for i in range(realStar.shape[0]):
            for j in range(realStar.shape[0]):
                if realStar[i, j] < sky: realStar[i, j] = sky
        return realStar

    def fitnessFunction(population):

        for i in range(population.shape[0]):
            star = GaussianCreator.createGaussian(population[i, 0], population[i, 1], population[i, 2],
                                                  population[i,3], population[i,4], population[i,5], population[i, 6])
            population[i,7] = np.sum(((realStarLessFlux + star) ** 2))

        pop = population[population[:, 7].argsort()]
        return pop

    def createPopulation(individuals,maxFlux):
        popu = np.zeros([individuals,8])

        for i in range(popu.shape[0]):
            for j in range(popu.shape[1]):

                if j==0: popu[i,j] = maxFlux
                if j==1: popu[i,j] = np.random.randint(1,90)
                if j == 2 or j == 3: popu[i, j] = np.random.randint(-9, 9)
                if j==4:
                    if np.random.randint(1,3) == 1:
                        popu[i, j] = 1
                        popu[i, j+1] = np.random.randint(1,3)
                    else:
                        popu[i, j] = np.random.randint(1,3)
                        popu[i, j+1] = 1
                if j==6: popu[i,j] = -0.00008

        return popu

    def selection(population):
        size = population.shape[0] / 2
        selected = np.zeros([size, 8])
        selected[0,:] = population[0,:]
        selected[1,:] = population[1,:]

        for i in range(2, size):
            n1 = np.random.randint(2, population.shape[0])
            n2 = np.random.randint(2, population.shape[0])
            selected[i, :] = population[n1, :] if population[n1, 7] < population[n2, 7] else population[n2, :]

        return selected

    def crossover(population, bestIndividuals):
        pop = np.zeros(population.shape)
        pop[0, :] = bestIndividuals[0, :]
        pop[1, :] = bestIndividuals[1, :]

        for i in range(2, population.shape[0]):
            n1 = np.random.randint(2, bestIndividuals.shape[0])
            n2 = np.random.randint(2, bestIndividuals.shape[0])
            g1 = bestIndividuals[n1,0] if np.random.randint(0, 11) < 5 else bestIndividuals[n2,0]
            g2 = bestIndividuals[n1,1] if np.random.randint(0, 11) < 5 else bestIndividuals[n2,1]
            g3 = bestIndividuals[n1,2] if np.random.randint(0, 11) < 5 else bestIndividuals[n2,2]
            g4 = bestIndividuals[n1,3] if np.random.randint(0, 11) < 5 else bestIndividuals[n2,3]
            g5 = bestIndividuals[n1,4] if np.random.randint(0, 11) < 5 else bestIndividuals[n2,4]
            g6 = bestIndividuals[n1,5] if np.random.randint(0, 11) < 5 else bestIndividuals[n2,5]
            g7 = bestIndividuals[n1,6] if np.random.randint(0, 11) < 5 else bestIndividuals[n2,6]
            pop[i, :] = [g1, g2, g3, g4, g5, g6, g7, 0]
        return pop

    def mutate(population, percentage):

        for i in range(2,population.shape[0]):
            if np.random.rand() < percentage:

                n = np.random.randint(1,7)
                if n==0: population[i,n] += np.random.randint(-1000, 1000)
                if n==1:
                    population[i,n] += np.random.uniform(-1,1)
                    if population[i,n] < 3: population[i,n]= 3
                    elif population[i, n] > 90: population[i, n] = 90

                if n==2 or n==3:
                    population[i,n] += np.random.uniform(-1,1)
                    if population[i,n] < -8: population[i,n]= -8
                    elif population[i, n] > 8: population[i, n] = 8
                if n==4 or n==5:
                    if population[i,4] == 1:
                        population[i, 5] += np.random.uniform(-0.1,0.1)
                        if population[i, 5] < 1: population[i, n] = 1
                        elif population[i, 5] > 2: population[i, n] = 2
                    else:
                        population[i, 4] += np.random.uniform(-0.1, 0.1)
                        if population[i, 4] < 1: population[i, n] = 1
                        elif population[i, 4] > 2: population[i, n] = 2

                if n==6: population[i, n] += np.random.uniform(-0.00008,-0.00007) if np.random.randint(1,3) == 1 else np.random.uniform(0.00008,0.00007)

        return population

    mutationPercentage = 0.1

    realStar = getRegion()
    (values, counts) = np.unique(np.squeeze(realStar), return_counts=True)
    skyFlux = values[np.argmax(counts)]
    realStarLessFlux = realStar - skyFlux
    maxFlux = np.max(realStarLessFlux)

    iter = 0
    population = createPopulation(individuals,maxFlux)
    population = fitnessFunction(population)
    bestIndividuals = np.zeros(maxIter)
    populationMeans = np.zeros(maxIter)
    bestFitness = population[0,7]
    stopTrain = 0

    while iter < maxIter:
        bestIndividuals[iter] = population[0,7]
        populationMeans[iter] = np.mean(population[:,7])

        selected = selection(population)
        population = crossover(population,selected)
        population = mutate(population,mutationPercentage)
        population = fitnessFunction(population)

        if bestFitness==population[0,7]: stopTrain += 1
        else: stopTrain = 0; bestFitness = population[0,7]

        if stopTrain > stopIter: break
        else: iter += 1

    # fig = plt.figure()
    # a = fig.add_subplot(1, 2, 1)
    # imgplot = plt.imshow(realStar,cmap='Greys')
    # a = fig.add_subplot(1, 2, 2)
    # imgplot = plt.imshow(GaussianCreator.createGaussian(population[0,0],population[0,1],population[0,2],
    #                                   population[0,3],population[0,4],population[0,5], population[0, 6]),cmap='Greys')
    #
    # plt.show()

    return population[0,:]




