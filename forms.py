

class DonationForm(FlaskForm):
    service = RadioField('Service', choices=[('pickup', 'Pick Up Service'), ('dropoff', 'Self-Dropoff')], validators=[InputRequired()])
    address = StringField('Address')
    drop_off_location = SelectField('Drop-off Location', choices=[('communityCenter', 'AMK Community Center'),
                                                                  ('communityCenter', 'Bedok Community Center'),
                                                                  ('communityCenter', 'Clementi Community Center'),
                                                                  ('communityCenter', 'Punggol Community Center')])
    contact_number = StringField('Contact Information', validators=[InputRequired()])
    schedule_date = DateField('Schedule Date', format='%Y-%m-%d', validators=[InputRequired()])
    schedule_time = TimeField('Schedule Time', validators=[InputRequired()])
    quantity = SelectField('Quantity of donated furniture', choices=[('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    furniture_type = TextAreaField('Furniture Type', render_kw={'rows': 3})
    quantity_dynamic = IntegerField('Quantity', validators=[InputRequired()])
    fragile = BooleanField('My donated furniture is fragile')
    packaged = BooleanField('My donated furniture is packaged')
