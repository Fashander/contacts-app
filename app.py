import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.ferretdb
contacts_collection = db.contacts

@app.route('/')
def index():
    contacts = contacts_collection.find()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    try:
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        contacts_collection.insert_one({'name': name, 'phone': phone, 'email': email})
    except Exception as e:
        message = f"An error occurred: {e}"
        print(message)
    return redirect(url_for('index'))

@app.route('/delete/<contact_id>', methods=['POST'])
def delete_contact(contact_id):
    try:
        contacts_collection.delete_one({'_id': ObjectId(contact_id)})
    except Exception as e:
        message = f"An error occurred while deleting the contact: {e}"

    return redirect(url_for('index'))

@app.route('/update/<contact_id>', methods=['GET', 'POST'])
def update_contact(contact_id):
    contact = contacts_collection.find_one({'_id': ObjectId(contact_id)})

    if request.method == 'POST':
        try:
            updated_data = {
                'name': request.form.get('name'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email')
            }
            contacts_collection.update_one({'_id': ObjectId(contact_id)}, {'$set': updated_data})
        except Exception as e:
            message = f"An error occurred while updating the contact: {e}"
        return redirect(url_for('index'))

    return render_template('update.html', contact=contact)

if __name__ == '__main__':
    app.run(debug=True)
