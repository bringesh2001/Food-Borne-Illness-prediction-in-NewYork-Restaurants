from flask import Flask,url_for,render_template
from forms import InputForm
import pandas as pd

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    form = InputForm()
    if form.validate_on_submit():
        x_new = pd.DataFrame(dict(
            restaurant_category=[form.restaurant_category.data],
            avg_days_bw_inspection=[form.avg_days_bw_inspection.data],
            source=[form.source.data],
            total_critical_violations=[form.total_critical_violations.data],
            total_crit_not_corrected=[form.total_crit_not_corrected.data],
            total_noncritical_violations=[form.total_noncritical_violations.data],
            permit_status=[form.permit_status.data],
            violation_type=[form.violation_type.data],
            
        ))
        prediction = model.predict(x_new)[0]
        message = f"The restaurant falls into {prediction:,.0f} category."
    else:
        message = "Please provide valid input details!"
    return render_template("predict.html", title="Predict", form=form, output=message)
if __name__ == '__main__':
    app.run(debug=True)