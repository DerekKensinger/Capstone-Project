# Import necessary Flask modules and packages
from .optimizer import run_optimizer
from flask import Blueprint, redirect, render_template, request, url_for, send_file
from flask_login import login_required
import pandas as pd
from pulp import *

# Create a Blueprint named 'f1'
f1 = Blueprint('f1', __name__)

# Route for optimizing Formula 1 data (GET and POST methods)
@f1.route('/optimize-f1', methods=['GET', 'POST'])
@login_required  # Requires the user to be logged in to access this route
def optimize_f1():
    if request.method == 'POST':
        # Process the POST request if needed
        print("Post Received")  # Add this line for debugging
        # After processing the POST request, return a response to the client. In this case, redirect them back to the same page.
        return redirect(url_for('f1.optimize-f1'))

    # If it's a GET request or no data has been posted, render the template with data
    optimized_data = generate_optimized_data()  # Fetch or generate your data
    return render_template("f1_optimization.html", data=optimized_data)  # Pass data to the template

# Route for fetching optimized Formula 1 data as a CSV file (GET method)
@f1.route('/f1/optimize-f1-data', methods=['GET'])
@login_required  # Requires the user to be logged in to access this route
def optimize_f1_data():
    # Replace this with your actual data generation logic
    optimized_data = generate_optimized_data()

    # Create a DataFrame from the optimized data
    df = pd.DataFrame(optimized_data)

    # Create a temporary CSV file to store the data
    temp_csv_file = "optimized_lineups.csv"
    df.to_csv(temp_csv_file, index=False)

    # Send the CSV file as a response to the client
    return send_file(
        temp_csv_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name='optimized_lineups.csv'
    )

# Function to generate optimized Formula 1 data 
def generate_optimized_data():
    # Call your optimization logic from DFS_Optimizer.py
    optimized_data = run_optimizer()

    return optimized_data