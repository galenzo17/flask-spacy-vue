
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
import urllib.request
import os

from flask_cors import CORS
#import speech_recognition as sr
import dateparser
from spaccy import spacyTopFive
import json
from spacydisplay import makeGraphs

app=Flask(__name__,
        static_folder='../front_end/frontend/dist/static',
        template_folder='../front_end/frontend/dist'
            )
cors=CORS(app,resources={r"/api/*":{"origins":"*"}})
UPLOAD_FOLDER = 'C:\\Users\\Agustin\\Documents\\repos\\flask-vue\\somedir'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/api/v1.0/mensaje')
def mensaje():
    return jsonify("hola")

@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def render_vue(path):
    return render_template('index.html')

@app.route("/api/v1.0/prediction", methods=["GET","POST"])
def prediction():
    if request.method == "GET":
        return render_template("index.html")
    else:
        #file = request['text']
        #print(request.form['text'])
        #actual=file.save(os.path.join(app.config["UPLOAD_FOLDER"], "filename.wav"))
        textToTopfive=spacyTopFive(request.form['text'])
        testtodisplay=makeGraphs(request.form['text'])
        response={"textToFive":textToTopfive,"testtodisplaydep":testtodisplay["result_dep"],"testtodisplayent":testtodisplay["resultent"]}
        return response
        # r = sr.Recognizer()
        # harvard = sr.AudioFile(os.path.join(app.config["UPLOAD_FOLDER"], "filename.wav"))
        # with harvard as source:
        #     audio = r.record(source)
        # subt = r.recognize_google(audio)
        fecha=dateparser.parse('Martes 21 de Octubre de 2014') 
          
        return json.dumps(textToTopfive)
        audiovar = request.form.get('file')
        #file=form.file.data
        #if audiovar:
        # print(subt)
        return 'hola'


if __name__ == '__main__':
    app.run(debug=True)