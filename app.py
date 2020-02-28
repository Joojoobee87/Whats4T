import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from os import path
from pymongo import ReturnDocument, IndexModel, ASCENDING, DESCENDING
from forms import RegistrationForm, LoginForm
import datetime
import math
if path.exists("env.py"):
    import env
    
app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get('MONGODB_NAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.secret_key = '1ee8825fe32fcc5a03559086d4218a1a'
bcrypt = Bcrypt()

mongo = PyMongo(app)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    """Home page"""
    """Displays the 4 most recently added recipes in the collection"""
    recently_added = mongo.db.recipes.find().limit(4).sort('date_updated', -1)
    """Display the 4 most liked recipes in the collection"""
    most_viewed = mongo.db.recipes.find().limit(4).sort('views_count', -1)
    return render_template('index.html', recently_added=recently_added, most_viewed=most_viewed)


@app.route('/get_recipes')
def get_recipes():
    page = request.args.get('page', default=1, type=int)
    per_page = 5
    total_results = mongo.db.recipes.count_documents({})
    max_page = math.ceil((total_results) / per_page)
    page_range = range(1, ((max_page)+1))
    recipes = mongo.db.recipes.find().limit(per_page).skip((page * per_page)-per_page)
    return render_template("recipes.html", 
                           recipes=recipes, total=total_results, page=page, page_range=page_range, max_page=max_page)


@app.route('/create_recipe')
def create_recipe():
    return render_template("createrecipe.html", 
                            title="Create Recipe",
                            recipes=mongo.db.recipes.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    new_recipe = {
        'user_email': session['email'],
        'title': request.form.get('title'),
        'summary': request.form.get('summary'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method'),
        'image': request.form.get('image'),
        'prep_time': request.form.get('prep_time', type=int),
        'cooking_time': request.form.get('cooking_time', type=int),
        'total_time': request.form.get('total_time', type=int),
        'tags': request.form.get('tags'),
        'views_count': 0,
        'date_updated': datetime.datetime.utcnow()
    }
    mongo.db.recipes.insert_one(new_recipe)
    return redirect(url_for('get_recipes'))


@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    selected_recipe=mongo.db.recipes.find_one_and_update({'_id': ObjectId(recipe_id)},
                                                            {'$inc': {'views_count': 1}})
    return render_template("showrecipe.html", recipes=selected_recipe)


@app.route('/find_recipes', methods=['GET', 'POST'])
def find_recipes():
    search_query = request.form.get('search_word')
    if request.form.get('total_time') == "":
        total_time = 0
    else:
        total_time = request.form.get('total_time', type=int)
    mongo.db.recipes.drop_index('recipes_index')
    mongo.db.recipes.create_index([('title', 'text'), ('summary', 'text'), ('ingredients', 'text'), ('tags', 'text')], name="recipes_index")
    results = mongo.db.recipes.find({"$text": {"$search": search_query}},
                                    {'score': {'$meta': "textScore"}}
                                    ).sort([('score', {'$meta': 'textScore'})])
    return render_template("reciperesults.html", recipes=recipes, total_time=total_time)


@app.route('/my_recipes', methods=['GET'])
#Need to add a validation class here to confirm if a user is logged in
def my_recipes():
    #Need to add the key:value into the find() method for user_id
    #if 'email' in session:
    #    user_id = session['_id']
    my_recipes=mongo.db.recipes.find()
    return render_template("myrecipes.html", recipes=my_recipes)


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    selected_recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("editrecipe.html", recipes=selected_recipe)


@app.route('/update_recipe/<recipes_id>', methods=['GET', 'POST'])
def update_recipe(recipes_id):
    mongo.db.recipes.update_one({
        '_id': ObjectId(recipes_id),
        }, {
            '$set': {
                'title': request.form.get('title'),
                'summary': request.form.get('summary'),
                'ingredients': request.form.get('ingredients'),
                'method': request.form.get('method'),
                'image': request.form.get('image'),
                'prep_time': request.form.get('prep_time', type=int),
                'cooking_time': request.form.get('cooking_time', type=int),
                'total_time': request.form.get('total_time', type=int),
                'tags': request.form.get('tags'),
                'date_updated': datetime.datetime.utcnow()
            }
        })
    return redirect(url_for('my_recipes'))


@app.route('/delete_recipe/<recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    selected_recipe=mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
    recipes=mongo.db.recipes.find()
    return render_template("myrecipes.html", recipes=recipes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        existing = mongo.db.users.find_one({'email': request.form.get('email')})
        
        if existing:
            """Encrypt password of user"""
            """If an existing user email is present, check match on passwords"""
            encrypted_pass = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            if bcrypt.check_password_hash(existing.get('password'), request.form.get('password')):
                session['email'] = request.form['email']
                session['logged_in'] = True
                flash(f'Welcome back!', 'success')
                return redirect(url_for('home'))
            else: 
                flash(f'Sorry, this password is incorrect. Please retype', 'danger')
                return redirect(url_for('login'))
            
        if existing is None:
            """If not an existing user, redirect user to registration page"""
            flash(f'Sorry this email address does not exist. Please register to create an account', 'danger')
            return redirect(url_for('register'))

    return render_template('login.html', title='Log In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    """If form is validate on submit, check if an existing user"""
    if form.validate_on_submit():
        existing = mongo.db.users.find_one({'email': request.form.get('email')})
        """If not an existing user, create a new user in the database"""
        if existing is None:
            """Encrypt password of user"""
            encrypted_pass = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            new_user = {
                'username': request.form.get('username'),
                'email': request.form.get('email'),
                'password': encrypted_pass,
            }
            mongo.db.users.insert_one(new_user)
            session['email'] = request.form['email']
            session['logged_in'] = True
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        """If existing user, redirect to login page to enter existing details"""
        flash(f'Email address already in use. Please login to your account.', 'danger')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    """logs out user and clears session"""
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)