import os
import json
from flask import jsonify, redirect, request, render_template, current_app, url_for
from . import main
from config import db_config
import mysql.connector

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
@main.route('/json_filtered', methods=['GET'])
def json_filtered():
    json_path = os.path.join(current_app.static_folder, 'data/staff.json')
    with open(json_path) as f:
        staff_data = json.load(f)

    # Get department from query string (form)
    department_filter = request.args.get('department')

    # Apply filter if form submitted
    if department_filter:
        filtered_data = [s for s in staff_data if s['department'].lower() == department_filter.lower()]
    else:
        filtered_data = staff_data

    return render_template('json_filtered.html', staffData=filtered_data, selected=department_filter)
@main.route('/json_dropdown', methods=['GET'])
def json_dropdown():
    json_path = os.path.join(current_app.static_folder, 'data/staff.json')
    with open(json_path) as f:
        staff_data = json.load(f)

    # Extract unique department names for the dropdown
    departments = sorted({s['department'] for s in staff_data})

    # Get selected department from query string
    selected_department = request.args.get('department')

    # Filter if a department is selected
    if selected_department:
        filtered_data = [
            s for s in staff_data if s['department'].lower() == selected_department.lower()
        ]
    else:
        filtered_data = staff_data

    return render_template(
        'json_dropdown.html',
        staffData=filtered_data,
        departments=departments,
        selected=selected_department
    )
@main.route('/db_data')
def db_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM staff")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('db_data.html', data=data)
@main.route('/staff/<int:staff_id>')
def staff_details(staff_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM staff WHERE id = %s", (staff_id,))
    staff = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if staff:
        return render_template('staff_details.html', staff=staff)
    else:
        return "Staff member not found", 404
    
# This route handles the sign-up form. It displays the form on GET requests and processes the form on POST requests.    
@main.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # Make sure to hash this in production!

        try:
            # Connect to the database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert the user into the signup table
            insert_query = """
                INSERT INTO signup (username, email, password)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (username, email, password))
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            # Optionally render an error page
            return "An error occurred while signing up."

        finally:
            cursor.close()
            conn.close()

        # Redirect to the success page
        return redirect(url_for('main.sign_up_success'))

    return render_template('sign_up.html')

@main.route('/sign_up_success')
def sign_up_success():
    return render_template('sign_up_success.html')

@main.route('/api/staff')
def get_staff_json():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM staff")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@main.route('/api/staff/<int:staff_id>')
def get_staff_by_id_json(staff_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM staff WHERE id = %s", (staff_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(row)

