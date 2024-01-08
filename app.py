import shelve
from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, DateField
from User import User
from Forms import CreateUserForm
from Products import Product

#donationform
from datetime import datetime
from wtforms import Form
from donation import DonationForm

#contactus:
from contactus import ContactUsForm

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/product')
def product():
    return render_template('product_page.html')


@app.route('/contactus')
def contact():
    return render_template('contactus.html')


@app.route('/donation', methods=['GET', 'POST'])
def donation():
    form = DonationForm(request.form)

    if request.method == 'POST' and form.validate():
        service = form.service.data
        address = form.address.data
        drop_off_location = form.drop_off_location.data
        contact_number = form.contact_number.data
        schedule_date = form.schedule_date.data
        schedule_time = form.schedule_time.data
        quantity = form.quantity.data
        fragile = form.fragile.data
        packaged = form.packaged.data
    return render_template('donation.html', form=form)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup = CreateUserForm(request.form) #CreateUserForm is from Forms.py
    if request.method == 'POST' and signup.validate():

        users_dict = {}
        db = shelve.open('user', 'c')

        try:
            users_dict = db['Users']
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        user = User(
            signup.first_name.data,
            signup.last_name.data,
            signup.email.data,
            signup.password.data
        )

        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('index'))
    return render_template('signup.html', form=signup)#form is new variable passed to signup.html 


@app.route('/login')
def login():
     login = CreateUserForm(request.form)#CreateUserForm is from Forms.py
     return render_template('login.html', form=login)#form is new variable passed to login.html

@app.route('/thank-you')
def thank_you():
    return "Thank you for contacting us!"

@app.route('/bean_bag')
def bean_bag():
    return render_template('beanbag.html')

@app.route('/checkout.html')
def check_out():
    return render_template('checkout.html')


@app.route('/beanbag', methods=['GET', 'POST'])
def beanbag():
    products = Product()
    cart_items = []

    if request.method == 'POST' or request.method == 'GET':
        stock = products.get_bean_bag()
        print ("123")
        print (stock)

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        cart_quantity = int(request.form.get('cart_quantity', 0))
        
        print(f"Received: Product ID - {product_id}, Quantity - {cart_quantity}")

        if product_id == 'beanbag':
            item_exists = any(item['product_id'] == 'beanbag' for item in cart_items)

            if item_exists:
                for item in cart_items:
                    if item['product_id'] == 'beanbag':
                        item['quantity'] += cart_quantity
            else:
                cart_item = {'product_id': 'beanbag', 'quantity': cart_quantity}
                cart_items.append(cart_item)
                
            print(f"Updated Cart: {cart_items}")

    return render_template('beanbag.html', products=stock, cart_items=cart_items)


if __name__ == '__main__':
    app.run(debug=True)

