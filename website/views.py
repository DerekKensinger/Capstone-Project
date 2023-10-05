# Import necessary modules and packages
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# Create a Blueprint named 'views'
views = Blueprint('views', __name__)

# Route for the home page (GET and POST methods)
@views.route('/', methods=['GET', 'POST'])
@login_required  # Requires the user to be logged in to access this route
def home():
    if request.method == 'POST':
        note = request.form.get('note')  # Get the note from the HTML form

        if len(note) < 1:
            flash('Note is too short!', category='error')  # Display an error message for a short note
        else:
            new_note = Note(data=note, user_id=current_user.id)  # Create a new 'Note' object
            db.session.add(new_note)  # Add the note to the database
            db.session.commit()  # Commit the changes
            flash('Note added!', category='success')  # Display a success message

    return render_template("home.html", user=current_user)  # Render the home page template

# Route for deleting a note (POST method)
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # Parse the JSON data sent from the INDEX.js file
    noteId = note['noteId']  # Extract the note ID from the JSON data
    note = Note.query.get(noteId)  # Retrieve the note from the database based on the ID

    if note:
        if note.user_id == current_user.id:  # Check if the note belongs to the current user
            db.session.delete(note)  # Delete the note from the database
            db.session.commit()  # Commit the changes

    return jsonify({})  # Return an empty JSON response


# Route and data to render table of optimized lineups

headings = ("Constructor", "Captain", "Driver #1", "Driver #2", "Driver #3", "Driver #4", "Total Fantasy Points")

data = (
    ("Scuderia Alpha Tauri", "Daniel Ricciardo", "Max Verstappen", "George Russell", "Zhou Guanyu", "Lance Stroll", "119.7"),
    ("Scuderia Alpha Tauri", "Daniel Ricciardo", "Max Verstappen", "Charles Lelcrec", "Zhou Guanyu", "Fernando Alonso", "118.9"),
    ("CNSTR_Red_Bull_Racing", "CPT_Kevin_Magnussen","D_Charles_Leclerc", "D_Guanyu_Zhou","D_Liam_Lawson","D_Max_Verstappen", "115.9"),
)
        
@views.route('/table')
@login_required
def table():
    return render_template("table.html", headings = headings, data = data)

