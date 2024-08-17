from flask import Flask, url_for, render_template
from forms import InputForm
import pandas as pd
import joblib
import numpy as np
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

# Use the DATABASE_URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://nyc_perd_user:wXmfSj1xeta1LlE6ygXzsoOOgSy50dKn@dpg-cr00pho8fa8c73ct29pg-a.oregon-postgres.render.com/nyc_perd"
db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_category = db.Column(db.String(100), nullable=False)
    avg_days_bw_inspection = db.Column(db.Float, nullable=False)
    total_critical_violations = db.Column(db.Integer, nullable=False)
    total_crit_not_corrected = db.Column(db.Integer, nullable=False)
    total_noncritical_violations = db.Column(db.Integer, nullable=False)
    permit_status = db.Column(db.String(100), nullable=False)
    violation_category = db.Column(db.String(100), nullable=False)
    prediction = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Restaurant('{self.restaurant_category}', '{self.prediction}')"

model = joblib.load("Notebooks/xgboostmdl.joblib")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    form = InputForm()
    message = ""
    if form.validate_on_submit():
        try:
            x_new = pd.DataFrame(dict(
                restaurant_category=[form.restaurant_category.data],
                avg_days_bw_inspection=[form.avg_days_bw_inspection.data],
                total_critical_violations=[form.total_critical_violations.data],
                total_crit_not_corrected=[form.total_crit_not_corrected.data],
                total_noncritical_violations=[form.total_noncritical_violations.data],
                permit_status=[form.permit_status.data],
                violation_category=[form.violation_category.data],
            ))
            prediction = model.predict(x_new)[0]
            if prediction == 0:
                cat = 'Not Critical Violation'
                message = f"The restaurant falls into {cat} category. You can eat your food there."
            else:
                cat = 'Critical Violation'
                message = f"The restaurant falls into {cat} category. It is advised to avoid that restaurant."
            
        except Exception as e:
            message = str(e)
    else:
        message = "Please provide valid input details!"
    return render_template("predict.html", title="Predict", form=form, output=message)

if __name__ == '__main__':
    app.run(debug=True)