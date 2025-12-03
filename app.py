from flask import Flask, url_for, render_template
from forms import InputForm
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

# Hack to fix AttributeError: Can't get attribute '_RemainderColsList'
import sklearn.compose._column_transformer
class _RemainderColsList(list):
    pass
sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList

model = joblib.load("Notebooks/xgboostmdl.joblib")

# Hack to fix AttributeError: 'OneHotEncoder' object has no attribute 'sparse'
def patch_one_hot_encoder(estimator):
    if hasattr(estimator, 'steps'):  # Pipeline
        for name, step in estimator.steps:
            patch_one_hot_encoder(step)
    elif hasattr(estimator, 'transformers_'):  # ColumnTransformer
        for item in estimator.transformers_:
            if len(item) == 3:
                name, transformer, columns = item
                patch_one_hot_encoder(transformer)
    elif 'OneHotEncoder' in str(type(estimator)):
        if not hasattr(estimator, 'sparse'):
            if hasattr(estimator, 'sparse_output'):
                estimator.sparse = estimator.sparse_output
            else:
                estimator.sparse = False
            print(f"Patched OneHotEncoder with sparse={estimator.sparse}")

try:
    patch_one_hot_encoder(model)
except Exception as e:
    print(f"Failed to patch OneHotEncoder: {e}")
from flask import Flask, url_for, render_template
from forms import InputForm
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

# Hack to fix AttributeError: Can't get attribute '_RemainderColsList'
import sklearn.compose._column_transformer
class _RemainderColsList(list):
    pass
sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList

model = joblib.load("Notebooks/xgboostmdl.joblib")

# Hack to fix AttributeError: 'OneHotEncoder' object has no attribute 'sparse'
def patch_one_hot_encoder(estimator):
    if hasattr(estimator, 'steps'):  # Pipeline
        for name, step in estimator.steps:
            patch_one_hot_encoder(step)
    elif hasattr(estimator, 'transformers_'):  # ColumnTransformer
        for item in estimator.transformers_:
            if len(item) == 3:
                name, transformer, columns = item
                patch_one_hot_encoder(transformer)
    elif 'OneHotEncoder' in str(type(estimator)):
        if not hasattr(estimator, 'sparse'):
            if hasattr(estimator, 'sparse_output'):
                estimator.sparse = estimator.sparse_output
            else:
                estimator.sparse = False
            print(f"Patched OneHotEncoder with sparse={estimator.sparse}")

try:
    patch_one_hot_encoder(model)
except Exception as e:
    print(f"Failed to patch OneHotEncoder: {e}")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    form = InputForm()
    message = ""
    is_safe = None
    
    if form.validate_on_submit():
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
        is_safe = (prediction == 0)
        cat = 'Not Critical Violation' if is_safe else 'Critical Violation'
        message = f"The restaurant falls into {cat} category. {'You can eat your food there.' if is_safe else 'It is advised to avoid that restaurant.'}"
    elif form.errors:
        message = "Please provide valid input details!"
        
    return render_template("predict.html", title="Predict", form=form, output=message, is_safe=is_safe)


if __name__ == '__main__':
    app.run(debug=True)