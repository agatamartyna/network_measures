from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class NeighboursForm(FlaskForm):
    word = StringField("word", validators=[DataRequired()])


class CoefficientForm(FlaskForm):
    word_co = StringField("word_co", validators=[DataRequired()])
