import shelve
import openai

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from User import User
from Forms import CreateUserForm, RetrieveUserForm, CreateMessageForm, CreateDonationForm #add missing field to Forms.py 
from Donation import Donation #make Donation.py

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
    create_message_form = CreateMessageForm(request.form)
    create_message_form.formspree_endpoint.data = "https://formspree.io/f/xoqgjbnd"
    return render_template('contactus.html', form=create_message_form)



#DONATION SECTION



@app.route('/donation', methods=['GET', 'POST'])
def create_donation():
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
    return render_template('donationform.html', form=create_donation_form)

@app.route('/retrieve_donations')
def retrieve_donations():
    donations_dict = {}
    with shelve.open('donations.db', 'r') as db:
        try:
            donations_dict = db['Donations']
        except shelve.ShelveError:
            print("Error in retrieving Donations from donations.db.")

    donations_list = list(donations_dict.values())
    return render_template('retrieveDonation.html', count=len(donations_list), donations_list=donations_list)


@app.route('/updateDonation/<int:id>/', methods=['GET', 'POST'])
def update_donation(id):
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








        return render_template('updateDonation.html', form=update_donation_form)


@app.route('/deleteDonation/<int:id>', methods=['POST'])
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
#section for Jacob part ends here

if __name__ == '__main__':
    app.run(debug=True)

