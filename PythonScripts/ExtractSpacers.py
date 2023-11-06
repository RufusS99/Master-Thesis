def ExtractSpacers(filepath):

    algorithm = filepath.split("/")[1]
    algorithm = algorithm.split("_")[0]  

    foldernumber = filepath.split("/")[0]
    foldernumber = foldernumber.split("_")[1]

    newfilename = filepath.split("/")[0] + "/" + algorithm + "_small_Spacers_" + foldernumber + "_analyzed_hd0.txt"
    
    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("Spacer"):
                with open(newfilename, "a") as nf:
                    nf.write(line)
                    nf.close()
        f.close()

ExtractSpacers("rw_meta/CRT_small_Seq_rw_analyzed_hd0.txt")