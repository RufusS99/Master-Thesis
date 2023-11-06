import re

foundTotal = 0

countFoundRepeats_hd_0 = 0
countFoundIndividualRepeats_hd_0 = 0
foundRepeats_hd_0 = []
foundRepeats_hd_2 = 0

foundMultiples = 0
listOfMultiples = [] # list of str
listOfNumberOfMultiples = [] # list of int

notfound = 0

with open ("rw_meta/detect0_Spacers_meta_analyzed_hd0.txt", "r") as f:

    for line in f:
        foundTotal = foundTotal + 1 #count total amount of "repeats" found

        repeat = line.split()
        print("Checking Repeat: ", repeat[1])
        newSeq = True

        # count the number of unique repeats
        for entry in listOfMultiples:                
            # if sequences are the same, no new seqence is appenden and only the counter is upped by one
            if repeat[1] == entry.split()[1]:
                newSeq = False
                index = listOfMultiples.index(entry)
                listOfNumberOfMultiples[index] = listOfNumberOfMultiples[index] + 1
                foundMultiples = foundMultiples + 1
                break
            elif repeat[1] in entry.split()[1] or entry.split()[1] in repeat[1]:
                # if entry has hd 0, don't replace
                newSeq = False
                print(repeat[1], entry.split()[1])
                # if new sequence is longer than current (new one must contain the old), replace
                if (len(repeat[1]) > len(entry.split()[1])) and repeat != "hamming distance":
                    index = listOfMultiples.index(entry)
                    listOfMultiples[index] = line

                foundMultiples = foundMultiples + 1
                break
        
        # append new sequence only if the flag remains true. Otherwise the flag is set to False and the for loop is terminated
        if newSeq == True:    
            listOfMultiples.append(line)
            listOfNumberOfMultiples.append(1)

        if re.search("not found", line):
            notfound = notfound + 1
        # List all perfect matches
        elif re.search("found in:", line):
            
            newPerfectMatch = True
            countFoundRepeats_hd_0 = countFoundRepeats_hd_0 + 1

            for entry in foundRepeats_hd_0:
                if repeat[1] == entry.split()[1]:
                    newPerfectMatch = False
                    break
                elif repeat[1] in entry.split()[1] or entry.split()[1] in repeat[1]:
                    newPerfectMatch = False
                    if len(repeat[1]) > len(entry.split()[1]):
                        index = foundRepeats_hd_0.index(entry)
                        foundRepeats_hd_0[index] = line
                    break

            if newPerfectMatch == True:
                foundRepeats_hd_0.append(line)
                countFoundIndividualRepeats_hd_0 = countFoundIndividualRepeats_hd_0 + 1

        elif re.search("found with hamming distance", line):
            foundRepeats_hd_2 = foundRepeats_hd_2 + 1
    
    f.close()


with open("rw_meta/detect0_Spacer_Final_hd0.txt", "w") as ca:

    ca.write("Total amount of repeats found: " + str(foundTotal) + "\n")
    ca.write("Total amount of perfect matched repeats: " + str(countFoundRepeats_hd_0) + "\n")
    ca.write("Out of those, " + str(countFoundIndividualRepeats_hd_0) + " individual repeats were found. \n")
    ca.write("Total amount of repeat found with a hamming distance of 1 or 2: " + str(foundRepeats_hd_2) + "\n")
    ca.write("Total amount of found multiples: " + str(foundMultiples) + "\n")
    ca.write("\n")

    ca.write("Exactly matched sequences \n")
    for entry in foundRepeats_hd_0:
        ca.write(entry)
    
    ca.write("\n")

    for entry in listOfMultiples:
        ca.write(entry[:-1] + "\t was found " + str(listOfNumberOfMultiples[listOfMultiples.index(entry)]) + " times \n")

    ca.close()