from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Dummy patient data
patients = [
    {"id": 1, "name": "John Doe", "age": 30, "condition": "Diabetes"},
    {"id": 2, "name": "Jane Smith", "age": 25, "condition": "Asthma"}
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/patients')
def get_patients():
    return jsonify(patients)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
