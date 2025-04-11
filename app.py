from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage
khoya_items = []
paaya_items = []

# Base class
class Vastu:
    def __init__(self, name, description, contact, image_filename=None):
        self.name = name
        self.description = description
        self.contact = contact
        self.image_filename = image_filename

class KhoyaItem(Vastu):
    def __init__(self, name, description, contact, image_filename=None):
        super().__init__(name, description, contact, image_filename)

class PaayaItem(Vastu):
    def __init__(self, name, description, contact, image_filename=None):
        super().__init__(name, description, contact, image_filename)

@app.route('/')
def home():
    return render_template('index.html', khoya_items=khoya_items, paaya_items=paaya_items)

@app.route('/report_khoya', methods=['POST'])
def report_khoya():
    try:
        name = request.form['name']
        description = request.form['description']
        contact = request.form['contact']
        image = request.files.get('image')
        filename = None
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        item = KhoyaItem(name, description, contact, filename)
        khoya_items.append(item)
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error while reporting khoya item: {e}"

@app.route('/report_paaya', methods=['POST'])
def report_paaya():
    try:
        name = request.form['name']
        description = request.form['description']
        contact = request.form['contact']
        image = request.files.get('image')
        filename = None
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        item = PaayaItem(name, description, contact, filename)
        paaya_items.append(item)
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error while reporting paaya item: {e}"

if __name__ == '__main__':
    print("\n✨ Khoya-Paaya Vibhag app is running!")
    print("Visit: http://127.0.0.1:5000\n")
    app.run(debug=True)
    
