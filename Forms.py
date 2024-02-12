from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, TimeField, HiddenField, FileField, SubmitField
from wtforms.fields import EmailField, DateField
from wtforms.validators import DataRequired,Length, Email

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


#eujon part start
class CreateProductForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Price', [validators.Length(min=1, max=150), validators.DataRequired()])
    colour = SelectField('Colour', [validators.DataRequired()], choices=[('', 'Select'), ('Green', 'Green'), ('Blue', 'Blue'), ('Red', 'Red'), ('Brown', 'Brown'), ('Gray', 'Gray'), ('Black', 'Black'), ('Beige', 'Beige')], default='')
    description = TextAreaField('Product Description', [validators.DataRequired()])
    image = FileField('Image')


class PaymentForm(Form):
    name = StringField('Name', validators=[DataRequired(message="Name is required")])
    address = StringField('Address', validators=[DataRequired(message="Address is required")])
    email = StringField('Email', validators=[DataRequired(message="Email is required"), Email(message="Invalid email address")])
    phone = StringField('Phone Number(in the format of 0000 0000)', validators=[DataRequired(message="Phone number is required"), Length(min=9, max=9, message="Please enter a valid 9-digit phone number")])
    card_number = StringField('Card Number(in the format of 0000 0000 0000 0000)', validators=[DataRequired(message="Card number is required"), Length(min=19, max=19, message="Please enter a valid 16-digit card number")])
    card_expiry = StringField('Expiration Date(in the format of 00/00)', validators=[DataRequired(message="Expiration date is required"), Length(min=5, max=5, message="Please enter a valid expiration date in the format MM/YY")])
    cvv = StringField('CVV(in the format of 000)', validators=[DataRequired(message="CVV is required"), Length(min=3, max=3, message="Please enter a valid 3-digit CVV")])
    submit = SubmitField('Submit Payment')   
#end eujon part