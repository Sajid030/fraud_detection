from flask import Flask,request,render_template
import pickle

app=Flask(__name__)
model=pickle.load(open('fraud_prediction.pkl','rb'))

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        # type column
        type=request.form['transaction_type']
        if type == 'Cash Out':
            type_CASH_OUT =1
            type_DEBIT =0 
            type_PAYMENT =0 
            type_TRANSFER =0
        elif type == 'Debit':
            type_CASH_OUT =0
            type_DEBIT =1
            type_PAYMENT =0 
            type_TRANSFER =0
        elif type == 'Payment':
            type_CASH_OUT =0
            type_DEBIT =0 
            type_PAYMENT =1
            type_TRANSFER =0
        elif type == 'Transfer':
            type_CASH_OUT =0
            type_DEBIT =0 
            type_PAYMENT =0 
            type_TRANSFER =1
        else:
            type_CASH_OUT =0
            type_DEBIT =0 
            type_PAYMENT =0 
            type_TRANSFER =0
        # amount column
        amount = float(request.form['amount'])
        # oldbalanceOrg column
        oldbalanceOrg = float(request.form['oldbalanceOrg'])
        # newbalanceOrig column
        newbalanceOrig = oldbalanceOrg - amount
        # oldbalanceDest column
        oldbalanceDest = float(request.form['oldbalanceDest'])
        # newbalanceDest column
        newbalanceDest = oldbalanceDest + amount
    
        # Prediction
        prediction = model.predict([[amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, type_CASH_OUT, type_DEBIT, type_PAYMENT, type_TRANSFER]])
        return render_template('result.html', prediction=prediction)

if __name__=="__main__":
    app.run(debug=True)