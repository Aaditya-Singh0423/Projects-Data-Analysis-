from flask import Flask,render_template,url_for,request
import joblib
model=joblib.load(r"D:\AU\Projects\Bike Price prediction\lr.lb")
app=Flask(__name__)
@ app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=='POST':
        brand_name=request.form['brand_name']
        owner=float(request.form['owner'])
        kms_driven =float(request.form['kms_driven'])
        age=float(request.form['age'])
        power=float(request.form['power'])
        bike_numbers ={'TVS' :1 , 
            'Royal Enfield':2,
            'Triumph' :3, 
            'Yamaha': 4,
            'Honda' : 5,
            'Hero': 6,
            'Bajaj': 7, 
            'Suzuki' : 8, 
            'Benelli':9 , 
            'KTM': 10,
            'Mahindra': 11,
            'Kawasaki':12,
            'Ducati': 13, 
            'Hyosung':14,
            'Harley-Davidson':15, 
            'Jawa': 16, 
            'BMW': 17,
            'Indian':18,
            'Rajdoot':19,
            'LML': 20,
            'Yezdi':21,
            'MV':22,
            'Ideal':23}
        
    brand_name_encode=float(bike_numbers[brand_name])
    lst=[[brand_name_encode,owner,kms_driven,age,power]]
    print(lst)
    pred=float(model.predict(lst)[0])
    #pred=pred[0]
    pred=round(pred,2)
    return render_template('project.html',prediction=pred)
if __name__=='__main__':
    app.run(debug=True)