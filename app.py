import shelve
import openai

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from User import User
from Forms import CreateUserForm, RetrieveUserForm

app = Flask(__name__)
app.secret_key = 'my_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'


#home page
@app.route('/')
def index():
    return render_template("index.html")

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

# ... (your existing routes)

# Chatbot route
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
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

        return render_template('chatbot.html', user_input=user_input, chatbot_response=chatbot_response)

    return render_template('chatbot.html')



if __name__ == '__main__':
    app.run(debug=True)

