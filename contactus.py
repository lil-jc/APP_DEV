from wtforms import Form, StringField, TextAreaField, validators
from wtforms.fields import html5 as h5fields


class ContactUsForm(Form):
    # Define your form fields here
    uName = StringField('Name', validators=[validators.InputRequired(), validators.Length(min=1, max=150), validators.DataRequired()])
    Ucontactnumber = h5fields.IntegerField('Phone', validators=[validators.InputRequired()], widget=h5widgets.NumberInput(min-6000000000, max-10000000000))
    uMessage =TextAreaField('Message', validators=[validators.InputRequired(), validators.length(max=300)]
    
    #uMessage = StringField('Name', validators=[validators.InputRequired(), validators.length(max=300)], widget=TextArea())

    # Add more fields as needed
# {{form.uMessage.label}}
