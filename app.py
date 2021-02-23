from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import Feedback, connect_db, db, User
from forms import FeedbackForm, RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "feedfeedfeedback"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

def page_not_found(e):
    """define custom 404 page"""
    return render_template('404.html'), 404

app.register_error_handler(404, page_not_found)

@app.route('/')
def home_page():
    """Show homepage"""
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/users/<username>')
def show_user_info(username):
    """Show uer info and any feedback submitted"""
    if "user_id" not in session:
        flash("Please login to view user feedback!", "danger")
        return redirect('/')
    user = User.query.filter(User.username==username).first()
    if user:
        return render_template('user_detail.html', user=user)
    else:
        return render_template('404.html'), 404

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Show add feedback form or process added feedback"""

    if "user_id" not in session:
        flash("Please login to add feedback!", "danger")
        return redirect('/')
    
    user = User.query.filter(User.username==username).first()
    if not user:
        return render_template('404.html'), 404

    if user.id != session['user_id']:
        return render_template('401.html'), 401

    form = FeedbackForm()
    if form.validate_on_submit():
        new_feedback = Feedback(title=form.title.data, content=form.content.data, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def update_feedback(id):
    """Show or process form to update feedback"""

    if "user_id" not in session:
        flash("Please login to add feedback!", "danger")
        return redirect('/')
    
    feedback = Feedback.query.get_or_404(id)
    user = feedback.user
    if user.id != session['user_id']:
        return render_template('401.html'), 401

    form=FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        form.populate_obj(feedback)
        db.session.commit()
        return redirect(f'/users/{user.username}')
    
    return render_template('edit_feedback.html', form=form)

@app.route('/feedback/<int:id>/delete')
def delete_feedback(id):
    """Delete item of feedback if the creator of that item is the logged-in user"""

    if "user_id" not in session:
        flash("You must be logged in to delete feedback.", "danger")
        return redirect('/')

    feedback = Feedback.query.get_or_404(id)
    user = feedback.user
    if user.id != session['user_id']:
        return render_template('401.html'), 401

    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted.', 'info')
    return redirect(f'/users/{user.username}')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """Show or process registration form if no logged in user"""

    if 'user_id' in session:
        return redirect('/')

    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User.register(form)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError as e:
            if 'users_username_key' in e.orig.args[0]:
                form.username.errors.append('Username taken. Please pick another')
            if 'users_email_key' in e.orig.args[0]:
                form.email.errors.append('Email used by another account. Please use a different one.')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Show or process login form if no logged in user"""

    if 'user_id' in session:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():

        user = User.authenticate(form)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    """logs out the user"""

    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')

@app.route('/users/<username>/delete')
def delete_user(username):
    """Deletes user"""

    if "user_id" not in session:
        flash("You must be logged in to delete your account.", "danger")
        return redirect('/')

    user = User.query.filter(User.username==username).first()
    if not user:
        return render_template('404.html'), 404

    if user.id != session['user_id']:
        return render_template('401.html'), 401

    db.session.delete(user)
    db.session.commit()
    flash("Account deleted", "info")
    session.pop('user_id')
    return redirect('/')