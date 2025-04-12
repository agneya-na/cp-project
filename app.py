from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage
lost_items = []
found_items = []

# Base class
class Vastu:
    def __init__(self, name, description, contact, image_filename=None):
        self.name = name
        self.description = description
        self.contact = contact
        self.image_filename = image_filename

class LostItem(Vastu):
    def __init__(self, name, description, contact, image_filename=None):
        super().__init__(name, description, contact, image_filename)

class FoundItem(Vastu):
    def __init__(self, name, description, contact, image_filename=None):
        super().__init__(name, description, contact, image_filename)

@app.route('/')
def home():
    return render_template('index.html', lost_items=lost_items, found_items=found_items)

@app.route('/report_lost', methods=['POST'])
def report_lost():
    try:
        name = request.form['name']
        description = request.form['description']
        contact = request.form['contact']
        image = request.files.get('image')
        filename = None
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        item = LostItem(name, description, contact, filename)
        lost_items.append(item)
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error while reporting lost item: {e}"

@app.route('/report_found', methods=['POST'])
def report_found():
    try:
        name = request.form['name']
        description = request.form['description']
        contact = request.form['contact']
        image = request.files.get('image')
        filename = None
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        item = FoundItem(name, description, contact, filename)
        found_items.append(item)
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error while reporting found item: {e}"

if __name__ == '__main__':
    print("\n✨ Welcome to VastuVault! ✨")
    print("Visit: http://0.0.0.0:$PORT\n")

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
