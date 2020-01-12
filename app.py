import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env
    
app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get('MONGODB_NAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')
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
    total_time = request.form.get('prep_time') + request.form.get('cooking_time')
    new_recipe = {
        'title': request.form.get('title'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method'),
        'images': request.form.get('images'),
        'prep_time': request.form.get('prep_time'),
        'cooking_time': request.form.get('cooking_time'),
        'total_time': total_time,
        'tags': request.form.get('tags'),
        'likes_count': " "
    }
    mongo.db.recipes.insert_one(new_recipe)
    return redirect(url_for('get_recipes'))


@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    selected_recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template("showrecipe.html", recipes=selected_recipe)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)