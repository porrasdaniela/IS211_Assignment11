from flask import Flask, render_template, request, redirect, url_for
import pickle
import os

app = Flask(__name__)

SAVE_FILE = 'to_do_list.pkl'

# Global list to hold To-Do items
to_do_list = []

def save_to_file():
    with open(SAVE_FILE, 'wb') as file:
        pickle.dump(to_do_list, file)

def load_from_file():
    global to_do_list
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'rb') as file:
            to_do_list = pickle.load(file)

# Load To-Do list on startup
load_from_file()

@app.route('/')
def home():
    return render_template('index.html', to_do_list=to_do_list)

# New controller to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')

    # Validate the data
    if not task or not email or priority not in ['Low', 'Medium', 'High']:
        return redirect(url_for('home'))

    # Adding the new item to the to_do_list
    to_do_list.append({'task': task, 'email': email, 'priority': priority})
    return redirect(url_for('home'))

# New controller to clear the list
@app.route('/clear', methods=['POST'])
def clear_list():
    global to_do_list
    to_do_list = [] # Clear the list
    return redirect(url_for('home'))

@app.route('/save', methods=['POST'])
def save_list():
    save_to_file()
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_item():
    task_to_delete = request.form.get('task')
    global to_do_list
    to_do_list = [item for item in to_do_list if item['task'] != task_to_delete]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

