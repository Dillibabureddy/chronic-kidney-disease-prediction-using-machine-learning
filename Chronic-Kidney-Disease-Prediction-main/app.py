from flask import Flask, render_template, request, flash, redirect, url_for
import pickle
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session and flash messages

# Load the kidney model once at startup
with open(r'C:\Users\dilli\Downloads\kidney1.pkl', 'rb') as f:
    kidney_model = pickle.load(f)

# Prediction logic for kidney disease
def predict_kidney(values):
    values = np.asarray(values).reshape(1, -1)
    return kidney_model.predict(values)[0]

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/kidney", methods=['GET', 'POST'])
def kidneyPage():
    return render_template('kidney.html')

@app.route("/predict", methods=['POST'])
def predictPage():
    try:
        to_predict_dict = request.form.to_dict()
        to_predict_list = list(map(float, list(to_predict_dict.values())))

        # Check if the input size matches the kidney model
        if len(to_predict_list) == 18:
            pred = predict_kidney(to_predict_list)
            return render_template('predict.html', pred=pred)
        else:
            flash("Invalid input data for kidney prediction.")
            return redirect(url_for('home'))
    except Exception as e:
        flash("Error: Please enter valid data. " + str(e))
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)