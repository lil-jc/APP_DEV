import shelve
import openai

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from User import User
from Forms import CreateUserForm, RetrieveUserForm, CreateMessageForm, CreateDonationForm #add missing field to Forms.py 
from Donation import Donation #make Donation.py
from werkzeug.utils import secure_filename
from Forms import CreateProductForm, PaymentForm
import shelve
from Product import Product
from Order import Order
import os
from flask_wtf.file import file_allowed, FileAllowed

#this is jacobs part
#under this section has no errors
#section starts here
#----------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = 'my_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'


#home page
@app.route('/')
def index():
    base_template = 'base_dashboard.html' if current_user.is_authenticated else 'base.html'
    return render_template('index.html', base_template=base_template)

#user loader
@login_manager.user_loader
def load_user(user_id):
    users_dict = {}
    db = shelve.open('user', 'r')
    users_dict = db.get('Users', {})
    db.close()
    
    return users_dict.get(int(user_id))

#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    login_form = RetrieveUserForm(request.form)

    if request.method == 'POST' and login_form.validate():
        email = login_form.email.data
        password = login_form.password.data

        users_dict = {}
        db = shelve.open('user', 'r')
        users_dict = db['Users']
        db.close()

        for key in users_dict:
            user = users_dict[key]
            if user.check_credentials(email,password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('login.html', form=login_form)

# logout (login required)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


#create user page(login required)
@app.route('/signup', methods=['GET', 'POST'])
@login_required
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

        return redirect(url_for('retrieve_users'))
    return render_template('signup.html', form=signup)#form is new variable passed to signup.html 


#dash board (login required)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index_dashboard.html')


# retrieve user (login required)
@app.route('/retrieveUsers')
@login_required
def retrieve_users():
    users_dict = {}
    db = shelve.open('user', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)



# delete user (login required)
@app.route('/deleteUser/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    users_dict = {}
    db = shelve.open('user', 'w')
    users_dict = db['Users']
    users_dict.pop(id)
    db['Users'] = users_dict
    db.close()
    return redirect(url_for('retrieve_users'))


#update user (login required)
@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user', 'w')
        users_dict = db['Users']
        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_email(update_user_form.email.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()
        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.email.data = user.get_email()
        update_user_form.password.data = user.get_password()
        return render_template('updateUser.html', form=update_user_form)
    
# Initialize the OpenAI API key
openai.api_key = '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'

# Chatbot route
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    base_template = 'base_dashboard.html' if current_user.is_authenticated else 'base.html'
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        # Call the OpenAI API to generate a response using the chat/completions endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            max_tokens=150
        )

        chatbot_response = response['choices'][0]['message']['content'].strip()

        return render_template('chatbot.html', user_input=user_input, chatbot_response=chatbot_response, base_template=base_template)

    return render_template('chatbot.html', base_template=base_template)
#----------------------------------------------------------------------------------------------------
#section for Jacob part ends here




#this is Kenzie's part
#under this section has no errors
#section starts here
#----------------------------------------------------------------------------------------------------
@app.route('/contactUs', methods=['GET', 'POST'])
def create_Message():
    base_template = 'base_dashboard.html' if current_user.is_authenticated else 'base.html'
    create_message_form = CreateMessageForm(request.form)
    create_message_form.formspree_endpoint.data = "https://formspree.io/f/xoqgjbnd"
    return render_template('contactus.html', form=create_message_form, base_template=base_template)



#DONATION SECTION



@app.route('/donation', methods=['GET', 'POST'])
def create_donation():
    base_template = 'base_dashboard.html' if current_user.is_authenticated else 'base.html'
    create_donation_form = CreateDonationForm(request.form)
    if request.method == 'POST' and create_donation_form.validate():
        donations_dict = {}


        with shelve.open('donations.db', 'c') as db:
            donations = Donation(
                create_donation_form.name.data,
                create_donation_form.email.data,
                create_donation_form.message.data,
                create_donation_form.service.data,
                create_donation_form.scheduledate.data,
                create_donation_form.scheduletime.data,
                create_donation_form.furnituretype.data,
                create_donation_form.quantity.data,
                create_donation_form.fragile.data,
                create_donation_form.packaged.data,
                create_donation_form.address.data,
                create_donation_form.number.data,
            )

            try:
                donations_dict = db['Donations']
            except Exception as e:
                print(f"Error in retrieving Donations from donations.db: {e}")

            donations_dict[donations.get_user_id()] = donations
            db['Donations'] = donations_dict



        return redirect(url_for('retrieve_donations'))
    return render_template('donationform.html', form=create_donation_form, base_template=base_template)

@app.route('/retrieve_donations')
@login_required
def retrieve_donations():
    base_template = 'base_dashboard.html' if current_user.is_authenticated else 'base.html'
    donations_dict = {}
    with shelve.open('donations.db', 'r') as db:
        try:
            donations_dict = db['Donations']
        except shelve.ShelveError:
            print("Error in retrieving Donations from donations.db.")

    donations_list = list(donations_dict.values())
    return render_template('retrieveDonation.html', count=len(donations_list), donations_list=donations_list, base_template=base_template)


@app.route('/updateDonation/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_donation(id):
    base_template = 'base_dashboard.html' if current_user.is_authenticated else 'base.html'
    update_donation_form = CreateDonationForm(request.form)
    if request.method == 'POST' and update_donation_form.validate():
        donations_dict = {}
        db = shelve.open('donations.db', 'w')
        donations_dict = db['Donations']

        donations = donations_dict.get(id)
        donations.set_name(update_donation_form.name.data)
        donations.set_email(update_donation_form.email.data)
        donations.set_message(update_donation_form.message.data)
        donations.set_service(update_donation_form.service.data)
        donations.set_scheduledate(update_donation_form.scheduledate.data)
        donations.set_scheduletime(update_donation_form.scheduletime.data)
        donations.set_furnituretype(update_donation_form.furnituretype.data)
        donations.set_quantity(update_donation_form.quantity.data)
        donations.set_fragile(update_donation_form.fragile.data)
        donations.set_packaged(update_donation_form.packaged.data)
        donations.set_address(update_donation_form.address.data)
        donations.set_number(update_donation_form.number.data)

        db['Donations'] = donations_dict
        db.close()

        return redirect(url_for('retrieve_donations'))
    else:
        donations_dict = {}
        db = shelve.open('donations.db', 'r')
        donations_dict = db['Donations']
        db.close()

        donations = donations_dict.get(id)
        update_donation_form.name.data = donations.get_name()
        update_donation_form.email.data = donations.get_email()
        update_donation_form.message.data = donations.get_message()
        update_donation_form.service.data = donations.get_service()
        update_donation_form.scheduledate.data = donations.get_scheduledate()
        update_donation_form.scheduletime.data = donations.get_scheduletime()
        update_donation_form.furnituretype.data = donations.get_furnituretype()
        update_donation_form.quantity.data = donations.get_quantity()
        update_donation_form.fragile.data = donations.get_fragile()
        update_donation_form.packaged.data = donations.get_packaged()
        update_donation_form.address.data = donations.get_address()
        update_donation_form.number.data = donations.get_number()

        return render_template('updateDonation.html', form=update_donation_form, base_template=base_template)


@app.route('/deleteDonation/<int:id>', methods=['POST'])
@login_required
def delete_donation(id):
    donations_dict = {}
    db = shelve.open('donations.db', 'w')
    donations_dict = db['Donations']

    if id in donations_dict:
        donations_dict.pop(id)

        # Reset user IDs after deletion
        new_user_id = 0
        for key in donations_dict:
            new_user_id = max(new_user_id, key)

        Donation.user_id = new_user_id

    db['Donations'] = donations_dict
    db.close()

    return redirect(url_for('retrieve_donations'))

#----------------------------------------------------------------------------------------------------
#section for Kenzie part ends here


#this is jacobs part
#under this section has no errors
#section starts here
#----------------------------------------------------------------------------------------------------
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')

# Set allowed file types
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'c')

        try:
            products_dict = db['Products']
        except KeyError:
            print("Error in retrieving Products from products.db.")


        product = Product(
            create_product_form.name.data,
            create_product_form.price.data,
            create_product_form.colour.data,
            create_product_form.description.data,
            create_product_form.image.data)

        products_dict[product.get_product_id()] = product
        db['Products'] = products_dict

        count = get_product_count()
        db[Product.count_id_key] = count
        db.close()

        return redirect(url_for('retrieve_products'))
    return render_template('createProduct.html', form=create_product_form)



@app.route('/retrieveProduct')
def retrieve_products():
    products_dict = get_products_dict()
    product_count = get_product_count()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('retrieveProducts.html', count=product_count, products_list=products_list)

@app.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)

    if request.method == 'POST' and update_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'w')
        products_dict = db['Products']

        product = products_dict.get(id)
        if product:
            product.set_name(update_product_form.name.data)
            product.set_price(update_product_form.price.data)
            product.set_colour(update_product_form.colour.data)
            product.set_description(update_product_form.description.data)

            # Check if 'image' is present in the form and update accordingly
            if update_product_form.image.data:
                # Validate the file extension
                if not FileAllowed(update_product_form.image.data, ['jpg', 'png']):
                    flash('Invalid file type. Please use jpg or png.')
                    db.close()
                    return redirect(url_for('update_product', id=id))

                # Save the new image file
                image_filename = secure_filename(update_product_form.image.data.filename)
                update_product_form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                product.set_image(image_filename)

            db['Products'] = products_dict
            db.close()

            return redirect(url_for('retrieve_products'))

    # Rest of the code for handling GET request and rendering the form
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    product = products_dict.get(id)
    if product:
        update_product_form.name.data = product.get_name()
        update_product_form.price.data = product.get_price()
        update_product_form.colour.data = product.get_colour()
        update_product_form.description.data = product.get_description()
        update_product_form.image.data = product.get_image()

        return render_template('updateProduct.html', form=update_product_form)
@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('product.db', 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('retrieve_products'))

@app.route('/shopnow')
def shop_now():
    tf = True
    products_dict = {}
    try: 
        db = shelve.open('product.db', 'r')
    except Exception as e:
            print(f"An unexpected error occurred: {e}")
            tf = False


    try:
        products_dict = db['Products']
    except:
        print("Error in retrieving Products from product.db.")

    if tf:
        db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('shopnow.html', count=len(products_list), products_list=products_list)

@app.route('/add_to_cart/<int:id>', methods=['POST'])
def add_to_cart(id):
    quantity = int(request.form['quantity'])

    products_dict = {}
    db = shelve.open('product.db', 'c')  # Open the database in read-write mode
    products_dict = db['Products']

    product = products_dict.get(id)

    if product:
        # Initialize the cart in the database if it doesn't exist
        db.setdefault('cart', {})

        # Add the product to the cart in the database with the chosen quantity
        cart = db['cart']
        cart[id] = cart.get(id, 0) + quantity
        db['cart'] = cart

        db.close()

        return redirect(url_for('shop_now'))

    return "Product not found"

@app.route('/get_cart_quantity')
def get_cart_quantity_endpoint():
    return jsonify(get_cart_quantity())
def get_cart_quantity():
    db = shelve.open('product.db', 'r')
    cart = db.get('cart', {})
    db.close()

    total_quantity = sum(cart.values())
    return {'quantity': total_quantity}

def get_cart_items():
    db = shelve.open('product.db', 'r')
    cart_items = db.get('cart', {})
    db.close()
    return cart_items

def get_products_dict():
    db = shelve.open('product.db', 'c')
    products_dict = db.get('Products', {})
    db.close()
    return products_dict


def get_product_count():
    db = shelve.open('product.db', 'r')
    count = db.get(Product.count_id_key, 0)
    db.close()
    return count
# Inside __init__.py

# ...

def calculate_total_fee(cart_items, products_dict):
    total_fee = 0

    for product_id, quantity in cart_items.items():
        product = products_dict.get(product_id)
        if product:
            # Remove the dollar sign from the price and convert to float
            price = float(product.get_price().replace('$', ''))
            total_fee += price * quantity

    return total_fee

# ...

# ...

@app.route('/checkout')
def checkout():
    # Get cart items and products dictionary using the functions
    cart_items = get_cart_items()
    products_dict = get_products_dict()

    # Assuming you have a function to get the product information by ID
    def get_product_info(product_id):
        product = products_dict.get(product_id)
        if product:
            return {
                'name': product.get_name(),
                'price': product.get_price(),
                'image': product.get_image(),
                'color': product.get_colour(),  # Corrected the attribute name
            }
        return {}

    # Get product information for each item in the cart
    cart_details = []
    for product_id, quantity in cart_items.items():
        product_info = get_product_info(product_id)
        if product_info:
            cart_details.append({
                'id': product_id,
                'quantity': quantity,
                **product_info,
            })

    total_fee = calculate_total_fee(cart_items, products_dict)
    return render_template('checkout.html', cart_details=cart_details, total_fee=total_fee)

@app.route('/update_cart_item/<int:id>', methods=['POST'])
def update_cart_item(id):
    cart_items = get_cart_items()

    # Get the requested quantity to remove
    quantity_to_remove = int(request.form['quantity'])

    # Remove the product from the cart with the specified quantity
    if id in cart_items and quantity_to_remove > 0:
        if quantity_to_remove >= cart_items[id]:
            # If the requested quantity is greater or equal to the current quantity, remove the product
            cart_items.pop(id)
        else:
            # Otherwise, update the quantity
            cart_items[id] -= quantity_to_remove

        # Update the cart in the database
        db = shelve.open('product.db', 'w')
        db['cart'] = cart_items
        db.close()

    return redirect(url_for('checkout'))


# ... (previous code)

# ... (previous code)

# ... (previous code)


# ... (remaining code)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    payment_form = PaymentForm(request.form)
    if request.method == 'POST' and payment_form.validate():
        order_dict = {}
        db = shelve.open('order.db', 'c')

        try:
            order_dict = db['Order']
        except KeyError:
            print("Error in retrieving Orders from order.db.")

        order = Order(
            payment_form.name.data,
            payment_form.address.data,
            payment_form.email.data,
            payment_form.phone.data,
            payment_form.card_number.data,
            payment_form.card_expiry.data,
            payment_form.cvv.data
        )

        order_dict[order.get_order_id()] = order
        db['Order'] = order_dict

        db.close()

        db = shelve.open('product.db', 'w')
        db['cart'] = {}
        db.close()

        return redirect(url_for('confirmation'))
    return render_template('payment.html', form=payment_form)


@app.route('/retrieveOrder', methods=['GET', 'POST'])
def retrieve_orders():
   order_dict = {}
   db = shelve.open('order.db', 'r')
   order_dict = db['Order']
   db.close()

   order_list = []
   for key in order_dict:
       order = order_dict[key]
       order_list.append(order)

   return render_template('retrieveOrder.html', count=len(order_list), order_list=order_list)


#delete order
@app.route("/deleteOrder/<int:id>", methods=['POST'])
def delete_order(id):
    order_dict = {}
    db = shelve.open('order.db', 'w')
    users_dict = db['Order']
    users_dict.pop(id)
    db['Order'] = users_dict
    db.close()
    return redirect(url_for('retrieve_orders'))

@app.route('/confirmation')
def confirmation():
    # Include any necessary order details here
    return render_template('confirmation.html')




# Inside __init__.py

# ... (previous code)
#----------------------------------------------------------------------------------------------------
#section for Kenzie part ends here


if __name__ == '__main__':
    db = shelve.open('product.db', 'c')
    db['cart'] = {}
    db.close()
    app.run(debug=True)

