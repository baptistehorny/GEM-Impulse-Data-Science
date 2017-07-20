import numpy as np
import pandas as pd
import plotly.graph_objs as go
from flask import Flask
from flask import render_template, request
from sklearn.externals import joblib
app = Flask(__name__)

from wtforms import Form, BooleanField, IntegerField, SelectField,FloatField

clf = joblib.load('flask_model.pkl')

class HRForm(Form):
    satisfaction_level = FloatField('Satisfaction level',render_kw={"placeholder": "between 0 and 1"})
    average_montly_hours = IntegerField("Average monthly hours",render_kw={"placeholder": "Mean:201 - Std:50"})
    promotion_last_5years = BooleanField("Promotion in last 5 years")
    number_project = IntegerField("Number of projets",render_kw={"placeholder": "Mean:3.8 - Std:1.2"})
    salary = SelectField(
        "Salary",
        choices=[('LOW', 'LOW'), ('MEDIUM', 'MEDIUM'), ('HIGH', 'HIGH')]
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    form = HRForm(request.form)
    answer = None
    if request.method == "POST" and form.validate():
        salary = [0,'LOW','MEDIUM','HIGH'].index(form.salary.data)
        satisfaction = float(form.satisfaction_level.data)
        number_project = int(form.number_project.data)
        hours = float(form.average_montly_hours.data)
        promotion = int(form.promotion_last_5years.data)
        employee = np.array([satisfaction,hours,promotion,salary,number_project]).reshape(1,-1)
        leaving = clf.predict(employee)
        if leaving[0]:
            answer = "leaving"
        else:
            answer = "staying"

    return render_template("index.html", title='Home', form=form, answer=answer)


if __name__ == '__main__':
    app.run(debug=True)
