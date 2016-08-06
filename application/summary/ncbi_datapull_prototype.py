def ncbi_UIDfinder(Gene,Species):    #Input Gene,Spcies, returns GeneID,NCBI Summary and EnsemblID
    Entrez.email = "nsaldanha@outlook.com"
    input_concat = "%s[Gene] %s[Orgn]" %(Gene,Species)
    search_results = Entrez.esearch("gene" ,input_concat )  #Outputs search results in XML
    record = Entrez.read(search_results)    #Parses and converts XML to python dictionary
    return record["IdList"][0]   #Selects first UID in the IDList

def fetch_summary(UID):     #Input UID, returns NCBI summary
     input_str = str(UID)
     summary = Entrez.efetch(db="gene" ,id=UID ,retmode="txt")
     return summary.read()[4:]  # [4:] Starts the string read at 4th letter, removes extraneous words.

def fetch_Ensembl_ID(UID):  #Input UID, returns Ensembl ID
    xml_dump = Entrez.efetch(db="gene", id=UID, retmode="xml")
    xml_tree = ET.parse(xml_dump)
    root = xml_tree.getroot()
    return root[0][3][0][3][1][1][0][0].text



if __name__ == '__main__':
    UID_input = ncbi_UIDfinder(raw_input("Gene"),raw_input("Species"))
    import xml.etree.ElementTree as ET
    from Bio import Entrez  #NCBI Data Interface
    print fetch_summary(UID_input)
    print fetch_Ensembl_ID(UID_input)