from flask import Flask, render_template, request, jsonify
import re
from extractor import Extractor
from checker import Checker
from typing import Union,List
import os

app = Flask(__name__)
ext = Extractor()

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        if 'input_file' in request.files:
            file = request.files['inputFile']
            if file and file.filename.endswith('.txt'):
                file_content = file.read().decode('utf-8').splitlines()
                extracted_data_list = [ext.extract(line) for line in file_content if line.strip()]
        elif 'inputString' in request.form:
            input_strings = request.form['inputString'].splitlines()
            extracted_data_list = [ext.extract(line) for line in input_strings if line.strip()]

        input_string = request.form['inputString']
        extracted_data = ext.extract(input_string)

        # if len(extracted_data)>1:
        #     response = []
        #     for data in extracted_data:
        
        #         extracted_json = {
        #     "name" : data['name'],
        #     "address" : data['address'],
        #     "lineone" : data['lineone'],
        #     "linetwo" : data['linetwo'],
        #     "cityid" : data['cityid'],
        #     "cityname" : data['cityname'],
        #     "citysubdivisionname" : data['citysubdivisionname'],
        #     "countryid" : data['countryid'],
        #     "countryname" : data['countryname'],
        #     "countrysubdivisionid" : data['countrysubdivisionid'],
        #     "country_model_prob" : data['country_model_prob'] 
        #     }
        #         response.append[extracted_json]
        #     return render_template('multidata_extract',extracted_data_list =response)
        
        extracted_data = extracted_data[0]
        extracted_json = {
            "name" : extracted_data['name'],
            "address" : extracted_data['address'],
            "lineone" : extracted_data['lineone'],
            "linetwo" : extracted_data['linetwo'],
            "cityid" : extracted_data['cityid'],
            "cityname" : extracted_data['cityname'],
            "citysubdivisionname" : extracted_data['citysubdivisionname'],
            "countryid" : extracted_data['countryid'],
            "countryname" : extracted_data['countryname'],
            "countrysubdivisionid" : extracted_data['countrysubdivisionid'],
            "country_model_prob" : extracted_data['country_model_prob'] 
            }
        

        return render_template('extract.html', extracted_data=extracted_json)
    return render_template('extract.html', extracted_data=None)

@app.route('/api/extract', methods=['POST'])
def api_extract():
    data = request.get_json()
    input_string = data.get('inputString', '')
    extracted_data = ext.extract(input_string)
    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True,port=8000)
