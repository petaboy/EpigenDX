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
   import summary

   UID = summary.ncbi_UIDfinder(str(request.form['gene']),'Human')
   ncbi_summary =  summary.ncbi_summary(UID)
   ensembl_ID = summary.ensembl_ID(UID)
   ensembl_gene_summary = summary.ensembl_gene_summary(ensembl_ID)
   ensembl_transcript_table = summary.ensembl_transcript_table(ensembl_ID)

   return render_template('submit.html',ncbi_summary=ncbi_summary,ensembl_gene_summary=ensembl_gene_summary,ensembl_transcript_table=ensembl_transcript_table)

@app.route('/transcript', methods=['POST'])
   import transcript

   return render_template()

# Run the app :)
if __name__ == '__main__':
   app.run()
