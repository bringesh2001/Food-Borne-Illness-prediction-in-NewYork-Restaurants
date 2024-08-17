import pandas as pd
import psycopg2
from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    IntegerField,
    SubmitField
)
from wtforms.validators import DataRequired

# getting the data
hostname = 'localhost'
database = 'nyfd'
user_name = 'postgres'
pwd = 'raksha' 
port_id= 5432
conn=None
cur=None

conn = psycopg2.connect(
    host=hostname,
    database=database,
    user=user_name,
    password=pwd
)

cur = conn.cursor()
cur.execute('SELECT * FROM public."vi"')
data = cur.fetchall() 

cur.close()
conn.close()

data = pd.DataFrame(data)

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
        validators=[DataRequired()]
    )
    total_crit_not_corrected = IntegerField(
        label="Number of crtical violations not corrected ",
        validators=[DataRequired()]
    )
    total_noncritical_violations = IntegerField(
        label="Number of Non-crtical violations ",
        validators=[DataRequired()]
    )
    permit_status = SelectField(
        label = 'Permit status',
        choices=data.permit_status.unique().tolist(),
        validators=[DataRequired()]

    )
    violation_type = SelectField(
        label ='Violation Type',
        choices = data.violation_category.unique().tolist(),
        validators=[DataRequired()]
        
    )
    submit = SubmitField("Predict")