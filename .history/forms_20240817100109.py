import pandas as pd
import psycopg2
from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    IntegerField,
    SubmitField
)
from wtforms.validators import DataRequired

data = pd.read_csv("Notebooks\data.csv")

class InputForm(FlaskForm):
    restaurant_category = SelectField(
        label="Restaurant Category",
        choices = data.iloc[:, 0].unique().tolist(),
        validators=[DataRequired()]
    )
    
    avg_days_bw_inspection = IntegerField(
        label="Average days b/w inspection of the restaurant",
        validators=[DataRequired()]
    )
    total_critical_violations = IntegerField(
        label="Number of crtical violations ",
    )
    total_crit_not_corrected = IntegerField(
        label="Number of crtical violations not corrected ",
    )
    total_noncritical_violations = IntegerField(
        label="Number of Non-crtical violations ",
    )
    permit_status = SelectField(
        label = 'Permit status',
        choices=data.iloc[:,-3].unique().tolist(),
        validators=[DataRequired()]

    )
    violation_category = SelectField(
        label ='Violation Type',
        choices = data.iloc[:,-1].unique().tolist(),
        validators=[DataRequired()]
        
    )
    submit = SubmitField("Predict")