from string import digits

# input: crt file
# output: list containing lists of repeats and spacers
def readCrtRaw(crtFile):

    #crisprSeq = ""
    tempList = []
    listOfAllSequences = []
    genome = set("A"+"C"+"G"+"T")

    with open(crtFile, "r") as crt:

        for line in crt:

            if line[0].isdigit(): #only lines that start with a number contain spacer and repeat se sequences
                line = line.translate(None, digits) #remove digits
                line = line.translate(None, "[,]")
                line = line.split()

                # remove non-DNA entrys
                temp = []
                for entry in line:
                    if set(entry).issubset(genome):
                        temp.append(entry)

                # remove entrys that contain only the repeat or a lone spacer
                if len(temp) > 1:
                    tempList.append(temp)

            elif line.startswith("CRISPR") and len(tempList) != 0:

                newList = [tempList[0]]
                for list in range(1, len(tempList)):
                    temp = [seq for seq in tempList[list] if seq != tempList[0][0]]
                    newList.append(temp)

                tempList = newList #for continous naming

                listOfAllSequences.append(tempList)

                tempList = []

        crt.close()

    return(listOfAllSequences)

#input: list containing lists of repeats and spacers
#ouput: -
def writeCrtOutputFile(listOfAllSequences, outputpath):

    with open(outputpath, "a") as op:

        for tempList in listOfAllSequences:

            for list in tempList:

                if len(list) > 1:

                    for seq in list:

                        if seq == list[0]:
                            op.write("Repeat:\t" + seq + "\n")

                        else:
                            op.write("Spacer:\t" + seq + "\n")
                    
                else:
                    op.write("Spacer:\t" + list[0] + "\n")
                
                

        op.close()
    
    return()

list = readCrtRaw("rw_meta/CRT/a_7.out")
writeCrtOutputFile(list, "rw_meta/CRT_small_Outputlist_rw.txt")