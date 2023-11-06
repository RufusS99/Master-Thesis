import os
import json 

def ReadRelevantFiles(relevantFolder):
    
    filepaths = []
    
    for file in os.listdir(relevantFolder):
        if "Final_hd0" in file:
            filepath = os.path.join(relevantFolder, file)
            filepaths.append(filepath)

    return(filepaths)

def CompareFiles(relevantFolder, usedAlgorithms):
    
    filepaths = ReadRelevantFiles(relevantFolder)
    #print(filepaths)
    seqlist = []

    for file in filepaths:

        # determine algorithm
        filename = os.path.basename(file)
        filename = filename.split("_")[0]

        # read files
        with open(file, "r") as f:
            for i in range(7):
                next(f)
            
            for line in f:
                if ":" and "was found" in line: #grab all sequences (found and not found)
                    seq = line.split(":")[1].strip()
                    seq = seq.split(" ")[0].strip()
                    print(seq)

                    tempFlagNewSeq = True

                    for entry in seqlist:
                        if seq in entry.split()[1]:
                            #print(entry.split()[1])
                            index = seqlist.index(entry)
                            addition = line.split("\t")[3] #new
                            addition = int(addition.split()[2])
                            oldAmount = int(entry.split("times")[-2][-2])
                            seqlist[index] = seqlist[index].split("-")[0] + " and was found " + str(oldAmount + addition) + " times via " + filename + " - " + seqlist[index].split("-")[1][:-1] + " and " + filename + "\n" #changed
                            tempFlagNewSeq = False
                            break

                    if tempFlagNewSeq:
                        entry = line[:-1] + " via " + filename + " - detected via " + filename + "\n" #changed
                        seqlist.append(entry)

            f.close()

    WriteFile(seqlist, relevantFolder, usedAlgorithms)

    return()

def WriteFile(seqList, relevantFolder, usedAlgorithms):

    foundAmount = [0, 0, 0] # [CRASS, CRT, mCAAT]

    for entry in seqList:
        for alg in usedAlgorithms:
            if alg in entry:
                index = usedAlgorithms.index(alg)
                foundAmount[index] = foundAmount[index] + 1

    
    count = relevantFolder.split("/")[0]
    count = count.split("_")[1]
    foldername = relevantFolder + "/File_Comparison_" + count + "_2.txt"

    with open(foldername, "w") as f:
        
        for entry in foundAmount:
            index = foundAmount.index(entry)
            f.write("Algorithm " + usedAlgorithms[index] + " found " + str(entry) + " CRISPRs\n")
        
        for entry in seqList:
            f.write(entry)
        f.close()

CompareFiles("rw_meta", ["CRASS", "CRT", "detect0"])