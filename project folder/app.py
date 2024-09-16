from flask import Flask, request, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    # Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Process the student data
    students = process_student_data(file_path)

    # Generate the Excel file with results
    result_file_path = os.path.join('downloads', 'student_audit_report.xlsx')
    students.to_excel(result_file_path, index=False)

    # Provide the file for download
    return send_file(result_file_path, as_attachment=True)

def process_student_data(file_path):
    df = pd.read_excel(file_path)

    # Example logic: Add a column for "Eligibility" based on attendance > 75%
    if 'Attendance' in df.columns:
        df['Eligible'] = df['Attendance'] > 75
    else:
        return 'Attendance column not found', 400

    return df

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    app.run(debug=True)
