from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    IntegerField,
    SubmitField
)
from wtforms.validators import DataRequired

# Hardcoded choices to avoid reading the large CSV file
RESTAURANT_CATEGORY_CHOICES = [
    "Fast Food", "Other", "American", "Italian", "Japanese", "Chinese", "Mexican", "Indian"
]

PERMIT_STATUS_CHOICES = [
    "Active", "Expired"
]

VIOLATION_CATEGORY_CHOICES = [
    "Unknown",
    "Vermin and Sanitation",
    "Facility and Equipment",
    "Administrative and Documentation",
    "Food Temperature and Protection",
    "Miscellaneous"
]

class InputForm(FlaskForm):
    restaurant_category = SelectField(
        label="Restaurant Category",
        choices=RESTAURANT_CATEGORY_CHOICES,
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
        choices=PERMIT_STATUS_CHOICES,
        validators=[DataRequired()]

    )
    violation_category = SelectField(
        label ='Violation Type',
        choices=VIOLATION_CATEGORY_CHOICES,
        validators=[DataRequired()]
        
    )
    submit = SubmitField("Predict")