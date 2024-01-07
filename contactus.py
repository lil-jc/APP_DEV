from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email

contact_us = Blueprint('contact_us', __name__)

# Form for unsigned-in users
class UnsignedForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Submit')

# Form for signed-in users
class SignedForm(FlaskForm):
    message_signed = TextAreaField('Message', validators=[InputRequired()])
    submit_signed = SubmitField('Submit')

