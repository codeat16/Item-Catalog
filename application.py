from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, UserID, Category, Item
from flask import session as login_session
import random
import string
from flask import make_response
import json
import time
# google signin
# Need to install google api client on the server to be
# able to use these modules
# pip install --upgrade google-api-python-client
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


CLIENT_ID = "354379757367-a0ru16o24hid3u56h43d8o6nda8cf9o8.apps.googleusercontent.com"

app = Flask(__name__)
app.debug = True
app.secret_key = 'abcde'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 120  # seconds

# set check_same_thread to False to deal with this version of sqlite error:
# ProgrammingError: (sqlite3.ProgrammingError) SQLite objects created in a
# thread can only be used in that same thread.
engine = create_engine(
    'sqlite:///itemcatalog.db',
    connect_args={'check_same_thread': False}
    )
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#
# API
#
@app.route('/category/<int:category_id>/item/JSON')
def categoryItemJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    i = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=i.serialize)


@app.route('/category/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(category=[c.serialize for c in categories])


#
# Category
#
# Show all categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).all()
    if categories:
        category = session.query(Category).first()
    else:
        category = None

    items = []
    if categories:
        category_id = categories[0].id
        items = session.query(Item).filter_by(
            category_id=category_id).all()

    app.logger.info("User {}".format(login_session.get('username')))
    app.logger.info("User variable type {}".format(
                    type(login_session.get('username'))))
    return render_template(
        'categories.html',
        categories=categories,
        category=category,
        items=items,
        username=login_session.get('username'),
        userid=login_session.get('userid')
        )


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'],
            user_id=login_session.get('userid')
            )
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return render_template(
            'editCategory.html', category=editedCategory)


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(
            url_for('showCategories', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)


#
# Item
#
# Show an item
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
def showItem(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()

    app.logger.info("User {}".format(login_session.get('username')))
    app.logger.info("User variable type {}".format(
                    type(login_session.get('username'))))
    return render_template(
        'categories.html',
        categories=categories,
        category=category,
        items=items,
        username=login_session.get('username'),
        userid=login_session.get('userid')
        )


# Create a new item
@app.route(
    '/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form[
                           'description'], category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)

    return render_template('newItem.html', category=category)


# Edit an item
@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']

        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:

        return render_template(
            'editItem.html',
            category_id=category_id,
            item_id=item_id,
            item=editedItem
            )


# Delete an item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# login
@app.route('/login')
@app.route('/logout')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template(
        'login.html',
        STATE=state,
        SIGNEDIN=bool(login_session.get('usersub'))
        )


# google login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # BUG?
    # request.json and request.get_json() appears not working in this flask
    #
    d = json.loads(request.data)
    token = d['idtoken']
    st = d['state']
    app.logger.info('google signin token is {}'.format(token))
    app.logger.info('state is {}'.format(st))
    if st != login_session['state']:
        app.logger.info("Incorrect login state.")
        return make_response("bad state", 400)

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            CLIENT_ID
            )

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in [
                'accounts.google.com',
                'https://accounts.google.com'
                ]:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID and
        # first name from the decoded token.
        login_session['usersub'] = idinfo['sub']
        login_session['username'] = idinfo['given_name']
        app.logger.info("Logged in as Google user: {}, {}".format(
            login_session['usersub'], login_session['username']))
        flash("Logged in as Google user")

        # save the new user in database
        newUser = session.query(UserID).filter_by(
            idstring=login_session['usersub'].decode()).first()

        if newUser:
            login_session['userid'] = newUser.id
            app.logger.info("Old user id {}, idstring {} signed in.".format(
                newUser.id, newUser.idstring))
        else:
            newUser = UserID(idstring=login_session['usersub'])
            login_session['userid'] = newUser.id
            session.add(newUser)
            session.commit()
            app.logger.info("New user id {}, idstring {} saved.".format(
                newUser.id, newUser.idstring))

    except ValueError:
        # Invalid token
        app.logger.info("Invalid token from Google sign in.")

    return make_response("good", 200)


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    # BUG?
    # request.json and request.get_json() appears not working in this flask
    #
    d = json.loads(request.data)
    st = d['state']
    app.logger.info('state is {}'.format(st))
    if st != login_session['state']:
        app.logger.info("Incorrect login state.")
        return make_response("bad state", 400)

    app.logger.info("Signed out of Google user: {}, {}".format(
        login_session['usersub'], login_session['username']))
    flash("Logged out of Google user")
    del login_session['usersub']
    del login_session['username']
    del login_session['userid']

    return make_response("good", 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
