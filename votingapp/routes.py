from flask import render_template, url_for, flash, redirect, request
import pymongo
from pymongo import MongoClient
from votingapp import app, cluster
from votingapp.forms import RegistrationForm, LoginForm
from votingapp.models import User
from flask_login import login_user, current_user, logout_user, login_required
from LoginRadius import LoginRadius as LR
import uuid
import cgi

LR.API_KEY = "e91795bb-fa16-40b6-b9bd-1d8f120333de"
LR.API_SECRET = "e19e43cc-7ebe-42a1-999d-f3a271d12bd8"

LR.API_REQUEST_SIGNING = True

login_radius = LR()



@app.route("/")
@app.route("/home")
def home():
    access_token = request.args.get("token")
    print(access_token)
    fields = 'email'
    print("this is done")
    try:    
        profile = login_radius.authentication.get_profile_by_access_token(access_token, fields)
        email = profile['Email'][0]['Value']
        print("ab email print hoga\n")
        print(email)
        Database = cluster["Vote_App"]
        usrDb = Database["User"]
        user = usrDb.find_one({"email": email})
        print(user)
        if user is None:
            print("\nhere\n")
            add_user = {"email": email, "hasVoted": False, "_id": uuid.uuid4().hex}
            usrDb.insert_one(add_user)
        user = usrDb.find_one({"email": email})
        print(user)
        print("\nyaha tak aya\n")
        my_user = User(user["email"], user["hasVoted"], user["_id"])
        login_user(my_user)
    except Exception as e:
        print(e)
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    return redirect("https://dev-1234qwerty.hub.loginradius.com/auth.aspx?action=register&return_url=http://localhost:5000/")

@app.route("/login", methods=['GET', 'POST'])
def login():
    return redirect("https://dev-1234qwerty.hub.loginradius.com/auth.aspx?action=login&return_url=http://localhost:5000/")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("https://dev-1234qwerty.hub.loginradius.com/auth.aspx?action=logout&return_url=http://localhost:5000/")

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':

        # Check if user has selected any candiate
        if 'candidate' in request.form:
            # Check if user has already submitted the vote
            Database = cluster["Vote_App"]
            usrDb = Database["User"]
            usr = usrDb.find_one({"email": current_user.email})
            hasAlreadyVoted = usr["hasVoted"]
            if hasAlreadyVoted:
                flash("You already voted for the best candidate", 'danger')
                return redirect(url_for('home'))
            else:
                candidate_name = request.form['candidate']

                # Increasing the vote by 1
                votesDb = Database["Votes"]
                update_1 = votesDb.update_one({"candidates":candidate_name}, {"$inc":{"votes":1}})
                
                # Setting true that user has submitted the vote
                update_2 = usrDb.update_one({"email":current_user.email}, {"$set":{"hasVoted":True}})
                
                # db.session.commit()

                flash("Thank you for the vote", 'success')
                return redirect(url_for('home'))
        else:
            flash('Please select a candidate to vote', 'danger')
            return redirect(url_for('dashboard'))
    else:
        # Fetching the candidates name in case of GET request
        Database = cluster["Vote_App"]
        votesDb = Database["Votes"]
        candidate_list = list(votesDb.find({}))
        print(candidate_list)
        return render_template('dashboard.html', candidate_list=candidate_list)