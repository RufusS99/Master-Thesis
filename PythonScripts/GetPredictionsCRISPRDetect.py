#folderNumber = "15"
foldernumber = "7"

#toReadPath = "Metagenome_" + folderNumber + "/mg_" + folderNumber + "/out_detect_" + folderNumber + ".txt"
toReadPath = "rw_meta/mg_rw/Part_" + foldernumber + "/out_detect_rw.txt"
#toWritePath = "Metagenome_" + folderNumber + "/detect_Outputlist_" + folderNumber + ".txt" 
toWritePath = "rw_meta/detect_Outputlist_rw.txt"

with open (toReadPath, "r") as f:

    spacerPart = False
    spacerList = []

    for line in f:

        if line.strip() != "":

            line = line.strip()

            if line.split()[0].isdigit(): #identify lines with relevant sequences
                if spacerPart == True:
                    if line.split()[-1].isalpha(): #grab spacer sequence
                        spacerList.append(line.split()[-1])
                else:
                    repeat = line.split()[-1] #grab repeat sequence

                    with open(toWritePath, "a") as o:
                        o.write("Repeat: " + repeat + "\n")
                        for entry in spacerList:
                            o.write("Spacer: " + entry + "\n")
                        o.close()

            if line.startswith("="): #start of relevant sequences
                if spacerPart == False:
                    spacerPart = True
                else:
                    spacerPart = False
    
    f.close()

        
