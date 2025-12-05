from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)

# Data storage (in memory for this example, would use database in production)
data = {
    "streams": [],
    "semesters": [],
    "majors": ["Core"],  # Core is default and can't be removed
    "minors": [],
    "subjects": {},  # {major_name: [subjects]}
    "teachers": {},  # {subject_name: [teachers]}
    "connections": []  # [(major, minor), ...]
}

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/add_stream', methods=['POST'])
def add_stream():
    stream_name = request.form.get('stream_name')
    if stream_name and stream_name not in data["streams"]:
        data["streams"].append(stream_name)
    return jsonify(success=True)

@app.route('/add_semester', methods=['POST'])
def add_semester():
    semester_name = request.form.get('semester_name')
    if semester_name and semester_name not in data["semesters"]:
        data["semesters"].append(semester_name)
    return jsonify(success=True)

@app.route('/add_major', methods=['POST'])
def add_major():
    major_name = request.form.get('major_name')
    if major_name and major_name not in data["majors"]:
        data["majors"].append(major_name)
    return jsonify(success=True)

@app.route('/add_minor', methods=['POST'])
def add_minor():
    minor_name = request.form.get('minor_name')
    if minor_name and minor_name not in data["minors"]:
        data["minors"].append(minor_name)
    return jsonify(success=True)

@app.route('/add_subject', methods=['POST'])
def add_subject():
    major = request.form.get('major')
    subject_name = request.form.get('subject_name')
    
    if major and subject_name:
        if major not in data["subjects"]:
            data["subjects"][major] = []
        if subject_name not in data["subjects"][major]:
            data["subjects"][major].append(subject_name)
    return jsonify(success=True)

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    subject = request.form.get('subject')
    teacher_name = request.form.get('teacher_name')
    
    if subject and teacher_name:
        if subject not in data["teachers"]:
            data["teachers"][subject] = []
        if teacher_name not in data["teachers"][subject]:
            data["teachers"][subject].append(teacher_name)
    return jsonify(success=True)

@app.route('/add_connection', methods=['POST'])
def add_connection():
    major = request.form.get('major')
    minor = request.form.get('minor')
    
    if major and minor:
        connection = (major, minor)
        if connection not in data["connections"]:
            data["connections"].append(connection)
    return jsonify(success=True)

@app.route('/get_data')
def get_data():
    return jsonify(data)

@app.route('/save_data', methods=['POST'])
def save_data():
    filename = request.form.get('filename', 'academic_data.json')
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    return jsonify(success=True, message=f"Data saved to {filename}")

@app.route('/load_data', methods=['POST'])
def load_data():
    filename = request.form.get('filename', 'academic_data.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            loaded_data = json.load(f)
        global data
        data = loaded_data
        return jsonify(success=True, message=f"Data loaded from {filename}")
    else:
        return jsonify(success=False, message=f"File {filename} does not exist")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)