import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from os import path
from pymongo import ReturnDocument, IndexModel
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
    """Displays the 4 most recently added recipes in the collection
        The recipes are sorted with the most recently added/updated appearing first"""
    recently_added = mongo.db.recipes.find().limit(4).sort('date_updated', -1)
    """Display the 4 most viewed recipes in the collection
        The recipes are sorted with the most viewed recipes appearing first"""
    most_viewed = mongo.db.recipes.find().limit(4).sort('views_count', -1)
    return render_template('index.html', recently_added=recently_added, most_viewed=most_viewed)


@app.route('/browse_recipes')
def browse_recipes():
    """The browse_recipes route finds all recipes in the recipes collection.
        Pagination has been added to display a maximum of 10 results per page
        Number buttons are displayed for user to navigate between results on different pages"""
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    total_results = mongo.db.recipes.count({})
    max_page = math.ceil((total_results) / per_page)
    page_range = range(1, ((max_page)+1))
    recipes = mongo.db.recipes.find().limit(per_page).skip((page * per_page)-per_page)
    return render_template("recipes.html", recipes=recipes, total=total_results, page=page, 
                            page_range=page_range, max_page=max_page)


@app.route('/create_recipe')
def create_recipe():
    """The create_recipe route allows the user to create a new recipe to add to the collection.
        On submit, the form is posted to the url_for('insert_recipe') which in turn adds the new
        recipe to the recipes collection in the database"""
    return render_template("createrecipe.html", title="Create Recipe", recipes=mongo.db.recipes.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    """On submit of the form, the values from the form are inserted into the relevant fields 
        within the recipes collection in the database"""
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
    """When a recipe is viewed, all of the recipe details are displayed to the user
        The function then increments the views_count field of the selected recipe 
        by 1, increasing the overall views count"""
    selected_recipe=mongo.db.recipes.find_one_and_update({'_id': ObjectId(recipe_id)},
                                                            {'$inc': {'views_count': 1}})
    return render_template("showrecipe.html", recipes=selected_recipe)


@app.route('/find_recipes_by_keywords', methods=['GET', 'POST'])
def find_recipes_by_keywords():
    """If the request method is POST, the value of the search_query variable will be taken 
        from the search_word form field"""
    if request.method == 'POST':
        search_query = request.form.get('search_word')
    """If the request method is GET, the value of the search_query variable will be passed 
        back in to the route on reciperesults.html"""
    if request.method == 'GET':
        search_query = request.args['query']
    """The function creates an index on the title, summary, ingredients and tags fields in the database.
       The find method searches the indexed fields using the search_query variable and scores them. 
       The text score signifies how well the document matched the search term or terms.
       The results are then ordered according to their text score, with the most relevant displayed first"""
    mongo.db.recipes.create_index([('title', 'text'), ('summary', 'text'), ('ingredients', 'text'), 
                                    ('tags', 'text')], name="recipes_index")
    results = mongo.db.recipes.find({"$text": {"$search": search_query}},
                                    {'score': {'$meta': "textScore"}}
                                    ).sort([('score', {'$meta': 'textScore'})])
    """Pagination has been added to the recipe results to show a maximum of 10 results per page
        Numbers buttons are displayed for user to navigate between results on different pages"""
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    total_results = results.count()
    max_page = math.ceil((total_results) / per_page)
    page_range = range(1, ((max_page)+1))
    recipes = results.limit(per_page).skip((page * per_page)-per_page)
    return render_template("reciperesults.html", recipes=recipes, total_results=total_results, 
                            page_range=page_range, page=page, search_query=search_query)


@app.route('/find_recipes_by_total_time', methods=['GET', 'POST'])
def find_recipes_by_total_time():
    """If the request method is POST, the value of the search_query variable will be taken 
        from the search_word form field"""
    if request.method == 'POST':
        search_total_time = request.form.get('search_word')
    """If the request method is GET, the value of the search_query variable will be passed 
        back in to the route on reciperesults.html"""
    if request.method == 'GET':
        search_total_time = request.args['query']
    search_total_time = request.form.get('search_total_time', type=int)
    results = mongo.db.recipes.find({"total_time": {"$lte": search_total_time}}
                                    ).sort('total_time', 1)
    """Pagination has been added to the recipe results to show a maximum of 10 results per page
        Numbers buttons are displayed for user to navigate between results on different pages"""
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    total_results = results.count()
    max_page = math.ceil((total_results) / per_page)
    page_range = range(1, ((max_page)+1))
    recipes = results.limit(per_page).skip((page * per_page)-per_page)
    return render_template("reciperesults.html", recipes=recipes, total_results=total_results, 
                            page_range=page_range, page=page)


@app.route('/my_recipes', methods=['GET'])
def my_recipes():
    """The my_recipes route is only displayed to users who are logged in.
        The find method searches the recipes collection and returns results where the 
        user_email field is equal to the value of the session email. Users logged in 
        will see any recipes that have been added by them"""
    my_recipes=mongo.db.recipes.find({'user_email': session['email']})
    """Pagination has been added to the recipe results to show a maximum of 10 results per page
        Numbers buttons are displayed for user to navigate between results on different pages"""
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    total_results = my_recipes.count()
    max_page = math.ceil((total_results) / per_page)
    page_range = range(1, ((max_page)+1))
    recipes = my_recipes.limit(per_page).skip((page * per_page)-per_page)
    return render_template("myrecipes.html", recipes=recipes, page=page, page_range=page_range)


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """The edit_recipe route takes the user to the selected recipe where they are then 
        able to edit the information contained within the database"""
    selected_recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("editrecipe.html", recipes=selected_recipe)


@app.route('/update_recipe/<recipes_id>', methods=['GET', 'POST'])
def update_recipe(recipes_id):
    """The update_recipe route takes the updated information from the form fields 
    and updates the recipes collection in the database
        The user is then returned to the My Recipes page"""
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
    """The delete_recipe route takes the _id value of the selected recipe and deletes it from the recipes collection in the database
        The user is then returned to the My Recipes page"""
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

    """If form is validated on submit, check if an existing user"""
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