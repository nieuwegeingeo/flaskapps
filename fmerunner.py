from flask import Flask, send_from_directory
from flask import request, render_template
import subprocess

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')

# from: http://stackoverflow.com/questions/23977475/running-a-shell-command-from-a-flask-app

#@app.route("/")
def hello():
    #cmd = ["c:\osgeo4w\oraclespatialwakeup.bat", "-vv"]
	#"C:\Program Files\FME\fme.exe" C:\temp\OphalenGegevensWebpagina_v1.fmw --COORDS "134151.8183 447006.2135 137810.4403 449482.8191" --VBO_GEB_FUNCTIE "woonfunctie" --OUTPUT_FORMAT "csv" --OUTPUT_DATA ""Adres en Oppervlakte en Gebruiksfunctie""
    #cmd = ["C:\Program Files\FME\fme.exe", "C:\temp\OphalenGegevensWebpagina_v1.fmw", --COORDS "134151.8183 447006.2135 137810.4403 449482.8191" --VBO_GEB_FUNCTIE "woonfunctie" --OUTPUT_FORMAT "csv" --OUTPUT_DATA ""Adres en Oppervlakte en Gebruiksfunctie""]
	
    #cmd = ["C:\Program Files\FME\fme.exe", "D:\zuidt\flask\OphalenGegevensWebpagina_v1.fmw"]
    #cmd = ["fme"]
	
	## LET OP LET OP: ofwel // gebruiken in de windows paden, ofwel \ gebruiken
	## Anders problemen met bijvoorbeeld /f wat dan wordt vertaald als een formfeed-character https://docs.python.org/2.0/ref/strings.html
    cmd = ["C:/Program Files/FME/fme.exe", "D:/zuidt/flask/OphalenGegevensWebpagina_v1.fmw", "--COORDS", "134111 447000 137000 449000",  "--VBO_GEB_FUNCTIE", "woonfunctie", "--OUTPUT_FORMAT", "csv", "--OUTPUT_DATA", "Adres en Oppervlakte en Gebruiksfunctie" ]
    cmd = ["C:\\Program Files\\FME\\fme.exe", "D:\\zuidt\\flask\\OphalenGegevensWebpagina_v1.fmw", "--COORDS", "134111 447000 137000 449000",  "--VBO_GEB_FUNCTIE", "woonfunctie", "--OUTPUT_FORMAT", "csv", "--OUTPUT_DATA", "Adres en Oppervlakte en Gebruiksfunctie" ]	
    # print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
    out,err = p.communicate()
	
    return render_template('runapptest.html', out=out)
    #return out
    
    
@app.route('/', methods=['GET', 'POST'])
    
def test():

    coords = "134111 447000 137000 449000"
    vbo_geb_functie = "woonfunctie"
    output_format = "pdf"
    output_data = "Adres en Oppervlakte en Gebruiksfunctie"

    if request.method == 'POST':
        #cmd = ["C:\\Program Files\\FME\\fme.exe", "D:\\zuidt\\flask\\OphalenGegevensWebpagina_v1.fmw", "--COORDS", "134111 447000 137000 449000",  "--VBO_GEB_FUNCTIE", "woonfunctie", "--OUTPUT_FORMAT", "csv", "--OUTPUT_DATA", "Adres en Oppervlakte en Gebruiksfunctie" ]
        
        
        # get values from form
        coords = request.form['coords']
        vbo_geb_functie = request.form['vbo_geb_functie']
        output_format = request.form['output_format']
        output_data = request.form['output_data']

      	## LET OP LET OP: ofwel // gebruiken in de windows paden, ofwel \ gebruiken
        ## Anders problemen met bijvoorbeeld /f wat dan wordt vertaald als een formfeed-character https://docs.python.org/2.0/ref/strings.html
        cmd = ["C:\\Program Files\\FME\\fme.exe", "D:\\zuidt\\flask\\OphalenGegevensWebpagina_v1.fmw", "--COORDS", coords,  "--VBO_GEB_FUNCTIE", vbo_geb_functie, "--OUTPUT_FORMAT", output_format, "--OUTPUT_DATA", output_data ]	
        print cmd
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        out,err = p.communicate()
        return render_template('test_resultaat.html', coords=coords, vbo_geb_functie=vbo_geb_functie, output_format=output_format, output_data=output_data )
    else:
        # GET: create form
        return render_template( 'test_invoer.html', coords=coords, vbo_geb_functie=vbo_geb_functie, output_format=output_format, output_data=output_data )
	
if __name__ == "__main__" :
    app.run()