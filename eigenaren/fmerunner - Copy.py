from flask import Flask, send_from_directory
from flask import request, render_template
import subprocess

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')

# from: http://stackoverflow.com/questions/23977475/running-a-shell-command-from-a-flask-app  
    
@app.route('/', methods=['GET', 'POST'])
    
def handle_request():

    wijk = []
    #email = "r.duivenvoorde@nieuwegein.nl"
    email = "m.kselik@nieuwegein.nl" 
       
    if request.method == 'POST':
    
        # "C:\Program Files\FME\fme.exe" D:\zuidt\flask\OphalenGegevensWebpagina_v1.fmw --EMAIL "r.duivenvoorde@nieuwegein.nl" --COORDS "POLYGON((135213.12 450199.68,135045.12 449984.64,135327.36 449883.84,135508.8 450152.64,135213.12 450199.68))" --VBO_GEB_FUNCTIE "woonfunctie" --OUTPUT_FORMAT "pdf" --OUTPUT_DATA "Adres en Oppervlakte en Gebruiksfunctie"

        # get values from form        
        #wijk = request.form['wijk1']
        wijk.append(request.form['wijkenSelect'])
        #wijk.append(request.form['wijk2'])
        email = request.form['email']        
        
        if "@nieuwegein.nl" not in email:
            return render_template('test_fout.html')
            
      	## LET OP LET OP: ofwel // gebruiken in de windows paden, ofwel \ gebruiken
        ## Anders problemen met bijvoorbeeld /f wat dan wordt vertaald als een formfeed-character https://docs.python.org/2.0/ref/strings.html
        
        #cmd = ["C:\\Program Files\\FME\\fme.exe", "D:\\zuidt\\flask\\OphalenGegevensWebpagina_v1.fmw", "--COORDS", coords,  "--VBO_GEB_FUNCTIE", vbo_geb_functie, "--OUTPUT_FORMAT", output_format, "--OUTPUT_DATA", output_data, "--EMAIL", email ]	
        cmd = ["C:\\Program Files\\FME\\fme.exe", "C:\\programs\\flask\\eigenaren\\eigenaren_binnen_wijk_export.fmw", "--SELECT_WIJK", wijkenSelect, "--EMAIL", email ]	
        print cmd
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        out,err = p.communicate()
        print out
        print err
        return render_template('test_resultaat.html', wijk=wijk, email=email)
     
    else:
        # GET: create form
        return render_template( 'test_invoer.html', wijk=wijk, email=email)
	
if __name__ == "__main__" :
    app.run()