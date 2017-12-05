from flask import Flask, send_from_directory
from flask import request, render_template
import subprocess

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')

# from: http://stackoverflow.com/questions/23977475/running-a-shell-command-from-a-flask-app  
    
@app.route('/', methods=['GET', 'POST'])
 
 
def handle_request():

    #email = "r.duivenvoorde@nieuwegein.nl"
    email = "m.kselik@nieuwegein.nl" 
    coords = []
    wijk = ''
    
    if request.method == 'POST':
    
        # "C:\Program Files\FME\fme.exe" D:\zuidt\flask\OphalenGegevensWebpagina_v1.fmw --EMAIL "r.duivenvoorde@nieuwegein.nl" --COORDS "POLYGON((135213.12 450199.68,135045.12 449984.64,135327.36 449883.84,135508.8 450152.64,135213.12 450199.68))" --VBO_GEB_FUNCTIE "woonfunctie" --OUTPUT_FORMAT "pdf" --OUTPUT_DATA "Adres en Oppervlakte en Gebruiksfunctie"

        # create the input string FME wants as input: "Batau Noord, Het Klooster, Fokkesteeg"
        # NOTE: the 'wijkenSelect' is a html FORM with a group of (multi) select boxes
        # so you need to use 'getlist' on the form, which returns an array/list
        wijk_array = request.form.getlist('wijkenSelect')
        wijk =  ','.join(wijk_array) # quickest way to create a csv from a list/array

        #print wijk
        #print(request.form['coords'])
        email = request.form['email']        
        coords = request.form['coords']        
        if not request.form.getlist('wijkenSelect'):
            if not coords:
                print("wijken en coords zijn leeg")
                return render_template('geen_wijk_geen_coords.html')
        if "@nieuwegein.nl" not in email:
            return render_template('mail_fout.html')
            
      	## LET OP LET OP: ofwel // gebruiken in de windows paden, ofwel \ gebruiken
        ## Anders problemen met bijvoorbeeld /f wat dan wordt vertaald als een formfeed-character https://docs.python.org/2.0/ref/strings.html
        
        #cmd = ["C:\\Program Files\\FME\\fme.exe", "D:\\zuidt\\flask\\OphalenGegevensWebpagina_v1.fmw", "--COORDS", coords,  "--VBO_GEB_FUNCTIE", vbo_geb_functie, "--OUTPUT_FORMAT", output_format, "--OUTPUT_DATA", output_data, "--EMAIL", email ]	
        cmd = ["C:\\Program Files\\FME\\fme.exe", "C:\\programs\\flask\\adressen\\verblijfsobjecten_binnen_wijk_export.fmw", "--WIJKEN_SELECT", wijk, "--EMAIL", email, "--COORDS", coords ]
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        out,err = p.communicate()
        print out
        print err
        if not coords:
            return render_template('wijk_resultaat.html', wijk=wijk, email=email)
        else:
            return render_template('coords_resultaat.html', coords=coords, email=email)    
     
    else:
        # GET: create form
        return render_template( 'adressen_invoer.html', wijk=wijk, coords=coords, email=email)
        
# @app.route('/postmethod', methods = ['POST'])
# def get_post_javascript_data():
    # jsdata = request.form['javascript_data']
    # return json.loads(jsdata)[0]
    
if __name__ == "__main__" :
    app.run()