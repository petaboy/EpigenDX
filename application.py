# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for

# Initialize the Flask application
app = Flask(__name__)



# Define a route for the default URL, which loads the form
@app.route('/')
def index():
   return render_template('index.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case

@app.route('/submit', methods=['POST'])
def submit():
   #Data Pull - NCBI
   def ncbi_UID(Gene, Species):    #Input Gene,Spcies, returns GeneID,NCBI Summary and EnsemblID
       from Bio import Entrez  #NCBI Data Interface)
       import xml.etree.ElementTree as ET

       Entrez.email = "nsaldanha@outlook.com"
       input_concat = "%s[Gene] %s[Orgn]" %(Gene,Species)
       search_results = Entrez.esearch("gene" ,input_concat )  #Outputs search results in XML
       xml_tree = ET.parse(search_results)
       root = xml_tree.getroot()
       #record = Entrez.read(search_results)    #Parses and converts XML to python dictionary

       return root[3][0].text  #Selects first UID in the IDList

   def ncbi_summary(UID):     #Input UID, returns NCBI summary
       # from Bio import Entrez  #NCBI Data Interface)
       # summary = Entrez.efetch(db="gene" ,id=UID ,retmode="xml")
       import requests

       query_in_string = '''https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id=%s&retmode=text&rettype=abstract'''
       url = query_in_string % (UID)
       summary = requests.get(url, stream=True)
       return summary.content[4:] #Starts the string read at 4th letter, removes extraneous words.


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

   UID = ncbi_UID(str(request.form['gene']),'Human')
   ncbi_summary =  ncbi_summary(UID)
   ensembl_ID = ensembl_ID(UID)
   ensembl_gene_summary = ensembl_gene_summary(ensembl_ID)
   ensembl_transcript_table = ensembl_transcript_table(ensembl_ID)

   return render_template('submit.html',ncbi_summary=ncbi_summary,ensembl_gene_summary=ensembl_gene_summary,ensembl_transcript_table=ensembl_transcript_table)



# Run the app :)
if __name__ == '__main__':
   app.run()
