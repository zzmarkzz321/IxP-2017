#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, flash, session, redirect, url_for
import json
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    if session["loggedin"] != True:
        session["loggedin"] = False
    return render_template('pages/placeholder.home.html', loggedin=session["loggedin"])


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/profile')
def profile():
    # Need to present the useres data here
    return render_template('pages/profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = form.name.data
        password = form.password.data

        user_doc = get_logged_user(user, password)
        # Failed login, re render the login and flash error
        if user_doc[1] != 200:
            flash('Invalid Credentials')

        # Successful login, redirect to front page
        else:
            session['loggedin'] = True
            session['username'] = user_doc[0]['username']
            session['firstname'] = user_doc[0]['firstname']
            session['lastname'] = user_doc[0]['lastname']
            session['routes'] = user_doc[0]['routes']

            return redirect(url_for('home'))

    return render_template('forms/login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/create-location', methods=['POST', 'GET'])
def createLocation():
    form = LocationForm(request.form)
    if request.method == 'POST':
        # if we have successfully created the location, redirect to the users profile
        return redirect(url_for('profile'))

    return render_template('forms/location.html', form=form)

@app.route('/list-of-locations')
def listoflocations():
    return render_template('layouts/list-of-locations.html')


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
