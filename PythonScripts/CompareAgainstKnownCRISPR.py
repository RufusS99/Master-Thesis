import os
import json

# input: txt file; max hamming distance
# output: none
def read_outputlist(txt_file, referenceFolder, hammingDistance):

    #checkedFiles = []
    repeatFiles = []
    seq = ""

    foundSequence = ""
    h_d = []

    with open(txt_file) as f:
        for line in f:
            if ":" in line:
                seq = line.split(":")[1].strip()

            if line.startswith("Repeat"):
                # Check in folders and files for repeat sequence
                #pathsToSeq, folderlist = findRepeat(seq, checkedFiles)
                pathsToSeq, folderlist = findRepeat(seq, referenceFolder)
                #checkedFiles.append(pathsToSeq)
                h_d = []

                # Search with Hamming Distance if no exact match was found
                
                #if len(pathsToSeq) == 0:
                #    pathsToSeq, foundSequence, h_d, folderlist = hammingRepeat(seq, referenceFolder, hammingDistance)

                repeatFiles.append(pathsToSeq)
                writeFile("Repeat", seq, pathsToSeq, folderlist, foundSequence, h_d)

            if line.startswith("Spacer"):
                # Check for spacer sequence in returned folders and files where the previous repeat was found
                pathToSpacerSeq = findSpacer(seq, repeatFiles[-1])
                writeFile("Spacer", seq, pathToSpacerSeq, [], "", 0)

    return()

# input: Line that should be found; Paths that don't need to be checked
# output: Path(s) to file in which line was found 
def findRepeat(lineToBeSearched, referenceFolder):

    repeatpaths = []
    folderlist = []

    # iterate through folders
    for folder in os.listdir(referenceFolder):
        folderpath = os.path.join(referenceFolder, folder)

        # iterate through files in the folders
        for item in os.listdir(folderpath):
            filepath = os.path.join(folderpath, item)

            # if the file was not already checked, it is searched for a repeat
            #if filepath not in alreadyChecked:

            with open(filepath, "r") as f:

                # if the repeat is found, the path to the file is added to the returned list
                if lineToBeSearched in f.read():

                    repeatpaths.append(filepath)
                        
                    if folder not in folderlist:
                        folderlist.append(folder)

                        #print("Found ", lineToBeSearched, "in ", folder)

            f.close()

    return(repeatpaths, folderlist)
   
# input: Line that should be found; Paths to files in which line could be found
# output: file that contained spacer; found spacers
def findSpacer(lineToBeSearched, filesToSearch):

    spacerpaths = []
    
    # iterate though files in which the previous repeat was found
    for filepath in filesToSearch:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:

                # if the spacer is found, the path to the file is added to the returned list
                if lineToBeSearched in f.read():
                    spacerpaths.append(filepath)
                    #print("Found ", lineToBeSearched, "in ", filepath)
            
            f.close()

    return(spacerpaths)

# input: Line that should be found; maximum hamming distance
# output: path to file that containes said line
def hammingRepeat(lineToBeSearched, referenceFolder, hammingDistance):

    repeatpaths = []
    folderlist = []
    foundSequence = []
    h_d = []

    # iterate through folders
    for folder in os.listdir(referenceFolder):
        folderpath = os.path.join(referenceFolder, folder)

        # iterate through files in the folders
        for item in os.listdir(folderpath):
            filepath = os.path.join(folderpath, item)

            baseString = ""

            with open(filepath, "r") as f:

                for line in f:

                    if line =="\n":
                        break

                    if not line.startswith(">"):
                        line = line.strip()
                        baseString = baseString + line

            f.close()

            h_d_value, foundSequenceInstance = hammingComparison(lineToBeSearched, baseString, hammingDistance)

            if h_d_value != 0:
                repeatpaths.append(filepath)
                folderlist.append(folder)
                foundSequence.append(foundSequenceInstance)
                h_d.append(h_d_value)

    if len(h_d) == 0:
        h_d.append(0)

    return(repeatpaths, foundSequence, h_d, folderlist)

# input: Line that should be found; Reference line
# output: 
def hammingComparison(lineToBeSearched, referenceLine, hammingDistance):

    h_d = 0
    foundSequence = ""

    for i in range(len(referenceLine)-len(lineToBeSearched)+1):

        if len(lineToBeSearched) != len(referenceLine[i:i+len(lineToBeSearched)]):
            raise ValueError("Undefined")

        else:
            h_d = sum(ch1 != ch2 for ch1, ch2 in zip(lineToBeSearched, referenceLine[i:i+len(lineToBeSearched)]))

        if h_d <= hammingDistance:
            foundSequence = referenceLine[i:i+len(lineToBeSearched)]
            break

    if h_d > hammingDistance:
        h_d = 0 

    return(h_d, foundSequence)

# input: Repeat or Spacer; sequence; list of files with matches
# output: none
def writeFile(type, seq, filepath, folderlist, foundSequence, h_d):
    
    filelist = []

    for entry in filepath:
        filename = os.path.basename(entry)
        filelist.append(filename)

    with open("rw_meta/detect0_Seq_rw_analyzed_hd0.txt", "a") as CRC:
        if len(filelist) != 0:
            CRC.write(type + ": \t" + seq + "\t found in: " + json.dumps(filelist) + " with hamming distance of " + json.dumps(h_d) + "\n")
        else:
            CRC.write(type + ": \t" + seq + "\t not found" + "\n")
    CRC.close()

    # if the current sequence is a repeat, it will also be saved in a special repeat file
    if type == "Repeat":
        with open("rw_meta/detect0_Repeats_rw_analyzed_hd0.txt", "a") as RC:
            
            if len(h_d) == 0:
                RC.write(type + ": \t" + seq + "\t found in: " + json.dumps(folderlist) + "\n")
            elif h_d[0] == 0:
                RC.write(type + ": \t" + seq + "\t not found" + "\n")
            else:
                RC.write(type + ": \t" + seq + "\t found with hamming distance " + str(h_d) + " as " + json.dumps(foundSequence) + "\n")
            
        RC.close()

read_outputlist("rw_meta/detect_Outputlist_rw.txt", "CRISPR_Seq", 0)