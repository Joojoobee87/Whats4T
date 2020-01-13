import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
from pymongo import ReturnDocument
import datetime
if path.exists("env.py"):
    import env
    
app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get('MONGODB_NAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')
@app.route('/home')
def home():
    """Home page"""
    """Displays the 4 most recently added recipes in the collection"""
    recently_added = mongo.db.recipes.find().limit(4).sort([('date_updated', -1)])
    """Display the 4 most liked recipes in the collection"""
    most_likes = mongo.db.recipes.find().limit(4).sort([('likes_count', -1)])
    return render_template('index.html', recently_added=recently_added, most_likes=most_likes)


@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", 
                           recipes=mongo.db.recipes.find())


@app.route('/create_recipe')
def create_recipe():
    return render_template("createrecipe.html", 
                            title="Create Recipe",
                            recipes=mongo.db.recipes.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    new_recipe = {
        'title': request.form.get('title'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method'),
        'image': request.form.get('image'),
        'prep_time': request.form.get('prep_time'),
        'cooking_time': request.form.get('cooking_time'),
        'total_time': request.form.get('total_time'),
        'tags': request.form.get('tags'),
        'likes_count': 0,
        'date_updated': datetime.datetime.utcnow()
    }
    mongo.db.recipes.insert_one(new_recipe)
    return redirect(url_for('get_recipes'))


@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    selected_recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("showrecipe.html", recipes=selected_recipe)



@app.route('/find_recipes', methods=['GET', 'POST'])
def find_recipes():
    #search_word = request.form.get('search_word')
    recipes=mongo.db.recipes.find()
    selected=mongo.db.recipes.find({'title': 'Chinese Chicken Stir Fry'})
    return render_template("reciperesults.html", recipes=selected)


@app.route('/my_recipes', methods=['GET'])
#Need to add a validation class here to confirm if a user is logged in
def my_recipes():
    #Need to add the key:value into the find() method for user_id
    my_recipes=mongo.db.recipes.find({'user_id': 'testuser'})
    return render_template("myrecipes.html", recipes=my_recipes)


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    selected_recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("editrecipe.html", recipes=selected_recipe)


@app.route('/delete_recipe/<recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    selected_recipe=mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
    recipes=mongo.db.recipes.find()
    return render_template("myrecipes.html", recipes=recipes)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)