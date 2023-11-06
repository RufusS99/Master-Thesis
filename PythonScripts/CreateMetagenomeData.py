import os
import random

# count files
def CountFiles():
    
    genomesTotal = 0
    allFilePaths = []
    allFileNames = []

    for file in os.listdir("Genomes"):
        genomesTotal = genomesTotal + 1
        filepath = os.path.join("Genomes", file)
        allFilePaths.append(filepath)
        allFileNames.append(file)

    return(genomesTotal, allFilePaths, allFileNames)

#select genome
def SelectGenome(allFilePaths, allFileNames, usedGenomes):

    temp = random.randint(0, (len(allFilePaths)-1))
    useGenomePath = allFilePaths[temp]

    if useGenomePath in usedGenomes:
        useGenomePath, genomeName = SelectGenome(allFilePaths, allFileNames, usedGenomes)

    else: 
        usedGenomes.append(useGenomePath)
        genomeName = allFileNames[temp]

    return(useGenomePath, genomeName)

# create new folder
def CreateNewFolder(count):

    foldername = "Metagenome_" + str(count)

    if os.path.isdir(foldername):
        count = count + 1
        foldername = CreateNewFolder(count)

    return(foldername)

def Main():
    
    usedGenomes = []
    totalCoverage = 0
    coverageList = []
    
    genomesTotal, allFilePaths, allFileNames = CountFiles()

    foldername = CreateNewFolder(1)
    os.mkdir(foldername)

    newFastaPath = foldername + "/multi.fasta"
    newCoveragePath = foldername + "/Coverage.txt"
    newAbundancePath = foldername + "/Abundance.txt"

    # select amount for metagenome
    selectedGenomes = random.randint(15, genomesTotal)
    for genome in range(0, selectedGenomes):
        useGenomePath, genomeName = SelectGenome(allFilePaths, allFileNames, usedGenomes)

        with open(useGenomePath, "r") as f:
            temp = f.read()

            with open(newFastaPath, "a") as nFP:
                nFP.write(temp + "\n")
            nFP.close()

            with open(newCoveragePath, "a") as nCP:
                genomeName = genomeName[:-6]
                coverage = random.randint(5, 100)
                totalCoverage += coverage
                coverageList.append(coverage)
                nCP.write(genomeName + "\t" + str(coverage) + "\n")
            nCP.close()
        f.close()

    with open(newCoveragePath, "r") as nCP:
        temp = 0
        for line in nCP:
            name = line.split()[0]
            with open(newAbundancePath, "a") as nAP:
                abundance = 0.0
                abundance = float(coverageList[temp]) / float(totalCoverage)

                nAP.write(name + "\t" + str(abundance) + "\n")
            nAP.close()
            temp += 1
    nCP.close()

    return()

Main()