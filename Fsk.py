from flask import Flask,request,url_for,redirect,jsonify,render_template
from flask_restful import Resource,Api
from Clas import AUTh
import os
import pandas as pd 

app=Flask(__name__)
api=Api(app)
app.secret_key = '5791628bb0b13ce0c676dfde280ba245' 
username='Harsha'
password='12345'

@app.route('/upload',methods=['post','get'])
def upload():
    results=None
    if request.method=='POST':
        file = request.files['data']
        upload_folder = os.path.join(app.root_path, 'FlaskApi')
        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, file.filename))
        df=pd.read_csv(os.path.join(upload_folder, file.filename))
        missing_values = df.isnull().sum().sum()
        null_values = df.isnull().sum().sum()
        for each in df.columns:
            if type(df[each][0]) is not str:
                print('numdatatype')
            else:
                valid_values = df[df[each].str.match(r'^[a-zA-Z]{3}\d{3}$').fillna(False)].shape[0]
        duplicates = df.duplicated().sum()
        results = {
            'missing_values': missing_values,
            'null_values': null_values,
            'valid_values': valid_values,
            'duplicates': duplicates
        }
    print(results)
    for key,value in results.items():
        results[key]=str(value)
    print(results)
    return jsonify(results)
@app.route('/auth',methods=['post'])
def auth():
    uusername=request.form.get('username')
    pp=request.form.get('password')
    if uusername==username and pp==password:
        print('done')
        return render_template('upload.html')
    return redirect(url_for('home'))
@app.route('/')
def home():
    return render_template('front.html')
app.run(debug=True)