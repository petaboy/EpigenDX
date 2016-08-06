#Adapted from https://gist.github.com/keithshep/7776579#file-querybiomartexample-py


def gene_summary_pull(ensembl_gene_id):
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

    with open('gene_summary.html','w') as towrite:
        towrite.write(req.content)
        towrite.close()
    for line in req.iter_lines():
        print line


def transcript_summary_pull(ensembl_gene_id):
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

    with open('transcript_list.html','w') as towrite:
        towrite.write(req.content)
        towrite.close()

    for line in req.iter_lines():
         print line
if __name__ == "__main__":
    import requests
    gene_summary_pull(raw_input("Ensembl gene ID"))
    transcript_summary_pull(raw_input("Ensembl gene ID"))