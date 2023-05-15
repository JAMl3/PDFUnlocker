import os
import PyPDF2
from flask import Flask, render_template, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename
from flask import send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret!123'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        unlocked_files = []

        # Loop through each uploaded file
        for uploaded_file in request.files.getlist('pdf_files'):
            if uploaded_file.filename == '':
                continue

            # Save the uploaded file to a secure location
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.root_path, 'uploads', filename)
            uploaded_file.save(filepath)

            # Check if the file is a PDF
            if filename.lower().endswith('.pdf'):
                # Open the password-protected PDF file
                pdf_file = open(filepath, 'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)

                # Create a new PDF writer object
                pdf_writer = PyPDF2.PdfFileWriter()

                # Loop through each page of the PDF file
                for page_num in range(pdf_reader.numPages):
                    # Extract the page and add it to the new PDF writer
                    page_obj = pdf_reader.getPage(page_num)
                    pdf_writer.addPage(page_obj)

                # Save the new PDF file without any password or permission restrictions
                output_filename = os.path.splitext(filename)[0] + '_Unlocked.pdf'
                output_filepath = os.path.join(app.root_path, 'uploads', output_filename)
                output_file = open(output_filepath, 'wb')
                pdf_writer.write(output_file)

                # Close the file objects
                pdf_file.close()
                output_file.close()

                unlocked_files.append(output_filename)

        flash('PDF files have been unlocked.', 'success')
        return render_template('home.html', unlocked_files=unlocked_files)

    return render_template('home.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    uploads = os.path.join(app.root_path, 'uploads')
    return send_file(os.path.join(uploads, filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
