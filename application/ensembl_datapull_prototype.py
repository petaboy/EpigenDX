#Adapted from https://gist.github.com/keithshep/7776579#file-querybiomartexample-py


def gene_summary_pull(ensembl_id):
    query_in_string= \
        '''http://ensembl.org/biomart/martservice?query=''' \
        '''<?xml version="1.0" encoding="UTF-8"?>'''\
        '''<!DOCTYPE Query>'''\
        '''<Query  virtualSchemaName = "default" formatter = "HTML" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >'''\
        '''<Dataset name = "hsapiens_gene_ensembl" interface = "default" >'''\
        '''<Filter name = "transcript_gencode_basic" excluded = "0"/>'''\
        '''<Filter name = "ensembl_gene_id" value = "ENSG00000105963"/>'''\
        '''<Attribute name = "external_gene_name" />'''\
        '''<Attribute name = "ensembl_gene_id" />'''\
        '''<Attribute name = "description" />'''\
        '''<Attribute name = "chromosome_name" />'''\
        '''<Attribute name = "start_position" />'''\
        '''<Attribute name = "end_position" />'''\
        '''<Attribute name = "transcript_count" />'''\
        '''</Dataset>'''\
        '''</Query>'''

    req = requests.get(query_in_string, stream=True)

    with open('new_file.html','w') as towrite:
        towrite.write(req.content)
        towrite.close()
    for line in req.iter_lines():
        print line


def transcript_summary_pull(ensembl_id):
    #Work on converting hsapiens.. and ensemblid into string input

    query_in_string = \
        '''http://ensembl.org/biomart/martservice?query=''' \
        '''<?xml version="1.0" encoding="UTF-8"?>''' \
        '''<!DOCTYPE Query>'''\
        '''<Query  virtualSchemaName = "default" formatter = "HTML" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >''' \
        '''<Dataset name = "hsapiens_gene_ensembl" interface = "default" >'''\
        '''<Filter name = "ensembl_gene_id" value = "%s"/>'''%(ensembl_id)\
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

    #print query_in_string
    req = requests.get(query_in_string, stream=True)

    for line in req.iter_lines():
         print line
if __name__ == "__main__":
    import requests
    #gene_summary_pull()
    transcript_summary_pull(raw_input("Ensembl ID"))