import xml.etree.ElementTree as ET

#read xml file and return spacers
#input : xml file name
#output : array of spacers and repeats in xml file
def read_xml(xml_file):
        tree = ET.parse(xml_file)
        crispr = tree.getroot()
        print(crispr.tag,crispr.attrib)
        repeats = []
        spacers = []
        outputlist = []
        for group in crispr:
            seq = group.attrib['drseq']
            if seq not in repeats:
                repeats.append(seq)
                outputlist.append("Repeat: \t" + seq)
                for data in group:
                    if data.find("spacers"):
                        for spacer in data.find("spacers"):
                            if spacer.attrib['seq']:
                                spacers.append(spacer.attrib['seq'])
                                outputlist.append("Spacer: \t" + spacer.attrib['seq'])

        return spacers, repeats, outputlist

spacers_from_xml, repeats_from_xml, outputlist = read_xml("rw_meta/CRASS_20_50_rw/crass.crispr")

with open("rw_meta/CRASS_20_50_rw/CRASS_Repeats_15.txt", "a") as r:
    for entryIndex in range(0, len(repeats_from_xml)):
        r.write(">query_" + str(entryIndex) + "\n" + repeats_from_xml[entryIndex] + "\n")
    r.close()

with open("rw_meta/CRASS_20_50_rw/CRASS_Outputlist_15.txt", "a") as ol:
    for entry in outputlist:
        ol.write(entry + "\n")
    ol.close()