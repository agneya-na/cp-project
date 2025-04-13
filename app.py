from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import certifi
import os
from bson import ObjectId

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://vansh:database@resumedb.vziesyw.mongodb.net/?retryWrites=true&w=majority&appName=resumedb", tlsCAFile=certifi.where())
db = client["VastuVault"]
lost_collection = db["lost_items"]
found_collection = db["found_items"]

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    khoya_items = list(lost_collection.find())
    paaya_items = list(found_collection.find())
    return render_template('index.html', khoya_items=khoya_items, paaya_items=paaya_items)

@app.route('/report_khoya', methods=['POST'])
def report_khoya():
    try:
        name = request.form['name']
        description = request.form['description']
        contact = request.form['contact']
        image = request.files.get('image')
        filename = None
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        lost_collection.insert_one({
            "name": name,
            "description": description,
            "contact": contact,
            "image_filename": filename
        })
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error while reporting lost item: {e}"

@app.route('/report_paaya', methods=['POST'])
def report_paaya():
    try:
        name = request.form['name']
        description = request.form['description']
        contact = request.form['contact']
        image = request.files.get('image')
        filename = None
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        found_collection.insert_one({
            "name": name,
            "description": description,
            "contact": contact,
            "image_filename": filename
        })
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error while reporting found item: {e}"

# Route to serve uploaded images
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'uploads'), filename)

# Delete Lost Item
@app.route('/delete_lost/<item_id>', methods=['POST'])
def delete_lost(item_id):
    try:
        # Ensure the item_id is in the correct format (ObjectId)
        lost_collection.delete_one({'_id': ObjectId(item_id)})
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error while deleting lost item: {e}"

# Delete Found Item
@app.route('/delete_found/<item_id>', methods=['POST'])
def delete_found(item_id):
    try:
        # Ensure the item_id is in the correct format (ObjectId)
        found_collection.delete_one({'_id': ObjectId(item_id)})
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error while deleting found item: {e}"

if __name__ == '__main__':
    print("\n✨ Welcome to VastuVault! ✨")
    print("Visit: http://0.0.0.0:$PORT\n")

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
