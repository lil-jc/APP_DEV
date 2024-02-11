from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, TimeField, HiddenField
from wtforms.fields import EmailField, DateField
from wtforms.validators import DataRequired,Length

#jacob part start
class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=8, max=64), validators.DataRequired()])

class RetrieveUserForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=8, max=64), validators.DataRequired()])
#jacob part end


#kenzie part start
class CreateMessageForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    message = TextAreaField('Message', [validators.DataRequired()])
    formspree_endpoint = HiddenField('Formspree Endpoint', [validators.DataRequired()])


class CreateDonationForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    message = TextAreaField('Additonal Remarks', [validators.Optional()])
    service = RadioField('Service', choices=[('Pick Up Service', 'Pick Up Service'), ('Self-Dropoff', 'Self-Dropoff')], validators=[validators.InputRequired()])
    scheduledate = DateField('Schedule Date', format='%Y-%m-%d', validators=[validators.InputRequired()])
    scheduletime = TimeField('Time', format='%H:%M', validators=[validators.InputRequired()])
    quantity = SelectField('Select Quantity of donated furniture:', validators=[validators.InputRequired()], choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3')], default='')
    furnituretype = SelectField('Select Furniture Type of donated furniture:', validators=[validators.InputRequired()], choices=[('', 'Select'), ('Chair', 'Chair'), ('Table', 'Table'), ('Televisions', 'Televisions')], default='')
    fragile = RadioField('Fragile?', choices=[('Y', 'Yes'), ('N', 'No')], validators=[validators.DataRequired()])
    packaged = RadioField('Pre-packaged?', choices=[('Y', 'Yes'), ('N', 'No')], validators=[validators.DataRequired()])
    number = StringField('Phone Number(in the format of 0000 0000)', validators=[DataRequired(message="Phone number is required"),Length(min=9, max=9, message="Please enter a valid 9-digit phone number")])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
#end kenzie part
