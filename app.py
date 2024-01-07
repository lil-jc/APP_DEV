import shelve
from flask import Flask, render_template, request
from contactus import contact_us, UnsignedForm, SignedForm 
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, DateField

app = Flask(__name__)
app.config['SECRET_KEY'] ='thecodex'

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/product')
def product():
    return render_template('product_page.html')

@app.route('/donation', methods=['GET', 'POST'])
def donation():
    return render_template('donation.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # Process the form data here (e.g., send an email)
        # For simplicity, let's just print the data for now
        print("Name:", form.name.data)
        print("Email:", form.email.data)
        print("Message:", form.message.data)

        return redirect(url_for('thank_you'))

    return render_template('contact.html', form=form)


@app.route('/thank-you')
def thank_you():
    return "Thank you for contacting us!"


@contact_us.route('/contact', methods=['GET', 'POST'])
def contact():
    unsigned_form = UnsignedForm()
    signed_form = SignedForm()

    if request.method == 'POST':
        if unsigned_form.validate_on_submit() and not signed_form.validate_on_submit():
            # Process unsigned-in user form submission
            name = unsigned_form.name.data
            email = unsigned_form.email.data
            message = unsigned_form.message.data
            # Handle the form data as needed
            return f"Unsigned-in user form submitted: Name - {name}, Email - {email}, Message - {message}"
        elif signed_form.validate_on_submit() and not unsigned_form.validate_on_submit():
            # Process signed-in user form submission
            message_signed = signed_form.message_signed.data
            # Handle the form data as needed
            return f"Signed-in user form submitted: Message - {message_signed}"

    return render_template('contact_us.html', unsigned_form=unsigned_form, signed_form=signed_form)


if __name__ == '__main__':
    app.run(debug=True)

