from pdfminer.high_level import extract_text
from match import extract_data 
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from datetime import timedelta
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.permanent_session_lifetime = timedelta(minutes=15)


client = MongoClient('mongodb://localhost:27017/')
db = client['BillReader']
collection = db['Bills']

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.jinja_env.globals.update(session=session)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload')
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home')) 

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.users.find_one({'username': username, 'password': password})
        if user:
            session.permanent = False
            session['logged_in'] = True
            session['username'] = username
            session['is_admin'] = user.get('is_admin', False)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = db.users.find_one({'username': username})
        if existing_user:
            return render_template('register.html', error="Username already exists.")

        db.users.insert_one({
            'username': username,
            'password': password,
            'is_admin': False
        })

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    files = request.files.getlist('bill')
    results = []

    if not files or all(f.filename == '' for f in files):
        return render_template('submit_result.html', status="❌ No file selected.", data=None)

    for file in files:
        if not file.filename.endswith('.pdf'):
            results.append({'status': f"❌ {file.filename}: Not a PDF", 'data': None})
            continue

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            text = extract_text(file_path)
            extracted_data = extract_data(text)
            if extracted_data['Name'] and extracted_data['ConsumerId'] and extracted_data['Bill']:
                extracted_data['file_path'] = file.filename
                extracted_data['uploaded_by'] = session.get('username')

                existing_record = collection.find_one({
                    'Name': extracted_data['Name'],
                    'BillNo': extracted_data['BillNo'],
                    'Month': extracted_data['Month'],
                    'Year': extracted_data['Year'],
                    'uploaded_by': extracted_data['uploaded_by']
                })


                if existing_record:
                    status = "Record Already Exists"
                
                else:
                    insert = collection.insert_one(extracted_data)
                    status = "Record Inserted"
                    
                results.append({'status': f"{file.filename}: {status}", 'data': extracted_data})
            else:
                results.append({'status': f"{file.filename}: ❌ No valid bill data found", 'data': None})
        except Exception as e:
            results.append({'status': f"{file.filename}: ❌ Error - {str(e)}", 'data': None})

    return render_template('submit_result.html', status="Batch Upload Summary", results=results)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/view-entries')
def view_entries():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if session.get('is_admin'):
        entries = list(collection.find({}, {
            '_id': 0,
            'Name': 1,
            'Bill': 1,
            'Month': 1,
            'Year': 1,
            'file_path': 1,
            'uploaded_by': 1
        }))
    else:
        entries = list(collection.find(
            {'uploaded_by': session['username']},
            {'_id': 0, 'Name': 1, 'Bill': 1, 'Month': 1, 'Year': 1, 'file_path': 1}
        ))

    return render_template('view.html', entries=entries)


@app.route('/delete/<filename>', methods=['POST'])
def delete_entry(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    query = {'file_path': filename}
    if not session.get('is_admin'):
        query['uploaded_by'] = session['username']

    result = collection.delete_one(query)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    return redirect(url_for('view_entries'))


@app.route('/view-entry/<filename>')
def view_entry(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    entry = collection.find_one({'file_path': filename}, {'_id': 0})

    if not entry:
        return "Entry not found", 404

    return render_template('detail_view.html', entry=entry)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))




if __name__ == "__main__":
    app.run(debug=True)
