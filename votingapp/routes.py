from flask import render_template, url_for, flash, redirect, request
from votingapp import app, db, bcrypt
from votingapp.forms import RegistrationForm, LoginForm
from votingapp.models import User, Votes
from flask_login import login_user, current_user, logout_user, login_required
from LoginRadius import LoginRadius as LR
import cgi

LR.API_KEY = "e91795bb-fa16-40b6-b9bd-1d8f120333de"
LR.API_SECRET = "e19e43cc-7ebe-42a1-999d-f3a271d12bd8"

LR.API_REQUEST_SIGNING = True

login_radius = LR()


# @app.before_first_request
# def setup():
#     # Drop tables if exists
#     db.drop_all()

#     # Creating tables
#     db.create_all()

#     #Inserting rows in candidatevotes table
#     db.session.add(Votes(candidate_name='Candidate A'))
#     db.session.add(Votes(candidate_name='Candidate B'))
#     db.session.add(Votes(candidate_name='Candidate C'))
#     db.session.add(Votes(candidate_name='Candidate D'))
    
#     # Commit
#     db.session.commit()


@app.route("/")
@app.route("/home")
def home():
    access_token = request.args.get("token")
    fields = 'email'
    try:
        profile = login_radius.authentication.get_profile_by_access_token(access_token, fields)
        email_id = profile['Email'][0]['Value']
        user = User(email = email_id)
        if User.query.filter_by(email=email_id).first() is None:
            db.session.add(user)
            db.session.commit()
        else:
            user = User.query.filter_by(email=email_id).first()
        login_user(user)
    except Exception as e:
        print(e)
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now login', 'success')
        return redirect(url_for('login'))
    return redirect("https://dev-1234qwerty.hub.loginradius.com/auth.aspx?action=register&return_url=http://localhost:5000/")
    #return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return redirect("https://dev-1234qwerty.hub.loginradius.com/auth.aspx?action=login&return_url=http://localhost:5000/")
    #return render_template('login.html', title = 'Login', form = form)

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
            hasAlreadyVoted = User.query.filter_by(email = current_user.email).first().hasVoted
            if hasAlreadyVoted:
                flash("You already voted for the best candidate", 'danger')
                return redirect(url_for('home'))
            else:
                candidate_name = request.form['candidate']

                # Increasing the vote by 1
                voted_candidate = Votes.query.filter_by(candidate_name=candidate_name).first()
                voted_candidate.votes = voted_candidate.votes + 1
                
                # Setting true that user has submitted the vote
                user_voted = User.query.filter_by(email= current_user.email).first()
                user_voted.hasVoted = True
                
                db.session.commit()

                flash("Thank you for the vote", 'success')
                return redirect(url_for('home'))
        else:
            flash('Please select a candidate to vote', 'danger')
            return redirect(url_for('dashboard'))
    else:
        # Fetching the candidates name in case of GET request
        candidate_list = Votes.query.all()
        return render_template('dashboard.html', candidate_list=candidate_list)