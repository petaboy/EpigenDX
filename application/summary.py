#ID Finder NCBI and Ensembl
def ncbi_UIDfinder(Gene,Species):    #Input Gene,Spcies, returns GeneID,NCBI Summary and EnsemblID
    from Bio import Entrez  #NCBI Data Interface)

    Entrez.email = "nsaldanha@outlook.com"
    input_concat = "%s[Gene] %s[Orgn]" %(Gene,Species)
    search_results = Entrez.esearch("gene" ,input_concat )  #Outputs search results in XML
    record = Entrez.read(search_results)    #Parses and converts XML to python dictionary
    return record["IdList"][0]   #Selects first UID in the IDList

#Data Pull - NCBI
def ncbi_UID(Gene, Species):    #Input Gene,Spcies, returns GeneID,NCBI Summary and EnsemblID
    from Bio import Entrez  #NCBI Data Interface)

    Entrez.email = "nsaldanha@outlook.com"
    input_concat = "%s[Gene] %s[Orgn]" %(Gene,Species)
    search_results = Entrez.esearch("gene" ,input_concat )  #Outputs search results in XML
    record = Entrez.read(search_results)    #Parses and converts XML to python dictionary
    return record["IdList"][0]   #Selects first UID in the IDList

def ncbi_summary(UID):     #Input UID, returns NCBI summary
    from Bio import Entrez  #NCBI Data Interface)
    summary = Entrez.efetch(db="gene" ,id=UID ,retmode="txt")
    return summary.read()[4:] #Starts the string read at 4th letter, removes extraneous words.



def ensembl_ID(UID):  #Input UID, returns Ensembl ID
    from Bio import Entrez  #NCBI Data Interface)
    import xml.etree.ElementTree as ET

    xml_dump = Entrez.efetch(db="gene", id=UID, retmode="xml")
    xml_tree = ET.parse(xml_dump)
    root = xml_tree.getroot()
    return root[0][3][0][3][1][1][0][0].text

#Data Pull ENSEMBL
#Adapted from https://gist.github.com/keithshep/7776579#file-querybiomartexample-py

def ensembl_gene_summary(ensembl_gene_id):
    from BeautifulSoup import BeautifulSoup
    import requests

    query_in_string= \
        '''http://ensembl.org/biomart/martservice?query=''' \
        '''<?xml version="1.0" encoding="UTF-8"?>'''\
        '''<!DOCTYPE Query>'''\
        '''<Query  virtualSchemaName = "default" formatter = "HTML" header = "1" uniqueRows = "0"'''\
        ''' count = "" datasetConfigVersion = "0.6" ><Dataset name = "hsapiens_gene_ensembl" interface = "default" >'''\
        '''<Filter name = "transcript_gencode_basic" excluded = "0"/>'''\
        '''<Filter name = "ensembl_gene_id" value = "%s"/>'''\
        '''<Attribute name = "external_gene_name" />'''\
        '''<Attribute name = "ensembl_gene_id" />'''\
        '''<Attribute name = "description" />'''\
        '''<Attribute name = "chromosome_name" />'''\
        '''<Attribute name = "start_position" />'''\
        '''<Attribute name = "end_position" />'''\
        '''<Attribute name = "transcript_count" />'''\
        '''</Dataset>'''\
        '''</Query>'''
    url = query_in_string % (ensembl_gene_id)
    req = requests.get(url, stream=True)
    soup = BeautifulSoup(req.text)
    table = soup.table
    return table



    # with open('gene_summary.html','w') as towrite:
    #     towrite.write(req.content)
    #     towrite.close()
    # for line in req.iter_lines():
    #     print line

def ensembl_transcript_table(ensembl_gene_id):
    from BeautifulSoup import BeautifulSoup
    import requests

    #Work on converting hsapiens.. and ensemblid into string input
    query_in_string = \
        '''http://ensembl.org/biomart/martservice?query=''' \
        '''<?xml version="1.0" encoding="UTF-8"?>''' \
        '''<!DOCTYPE Query>'''\
        '''<Query  virtualSchemaName = "default" formatter = "HTML" header = "1" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >''' \
        '''<Dataset name = "hsapiens_gene_ensembl" interface = "default" >'''\
        '''<Filter name = "ensembl_gene_id" value = "%s"/>'''\
        '''<Filter name = "transcript_gencode_basic" excluded = "0"/>'''\
        '''<Attribute name = "external_transcript_name" />'''\
        '''<Attribute name = "ensembl_transcript_id" />'''\
        '''<Attribute name = "transcript_length" />'''\
        '''<Attribute name = "transcript_biotype" />'''\
        '''<Attribute name = "refseq_mrna" />'''\
        '''<Attribute name = "refseq_peptide" />'''\
        '''<Attribute name = "transcript_gencode_basic" />'''\
        '''<Attribute name = "transcript_tsl" />'''\
        '''<Attribute name = "transcript_appris" />'''\
        '''</Dataset>'''\
        '''</Query>'''

    url = query_in_string % (ensembl_gene_id)
    req = requests.get(url, stream=True)
    soup = BeautifulSoup(req.text)
    table = soup.table
    return table


if __name__ == "__main__":
    UID = ncbi_UID(raw_input('gene'), raw_input('species'))
    ncbi_summary =  ncbi_summary(UID)
    print ncbi_summary
    ensembl_ID = ensembl_ID(UID)
    ensembl_gene_summary = ensembl_gene_summary(ensembl_ID)
    ensembl_transcript_table = ensembl_transcript_table(ensembl_ID)

