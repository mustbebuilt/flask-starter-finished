import os
import json
from flask import render_template, current_app
from . import main

@main.route('/')
def index():
    return render_template('index.html', name='World')
@main.route('/about')
def about():
    return render_template('about.html')
@main.route('/food')
def food():
    foods = ["Apple", "Banana", "Orange"]
    return render_template('food.html', foods=foods)
@main.route('/dictionary')
def dictionary():
    staffDict = {
        'name': 'Alice', 'position': 'Manager'
        }
    return render_template('dictionary.html', staffDict=staffDict)
@main.route('/dictionary-nested')
def dictionary_nested():
    staffDict = {
        "staff1": {
            'name': 'Alice',
            'position': 'Manager',
            'department': 'Sales'
        },
        "staff2": {
            'name': 'Bob',
            'position': 'Developer',
            'department': 'IT'
        },
        "staff3": {
            'name': 'Charlie',
            'position': 'Designer',
            'department': 'Marketing'
        }
    }
    return render_template('dictionary_nested.html', staffDict=staffDict)
@main.route('/staffdata')
def staffdata():
    json_path = os.path.join(current_app.static_folder, 'data/staff.json')
    with open(json_path) as f:
        staff_data = json.load(f)
    return render_template('from_json.html', staffData=staff_data)

    