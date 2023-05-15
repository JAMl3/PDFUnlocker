import os
import PyPDF2
from flask import Flask, render_template, request, flash, redirect, send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret!123'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        folder_path = request.form['folder_path']
        unlocked_folder_path = os.path.join(folder_path, 'Unlocked PDFs')

        # Create the Unlocked PDFs folder if it doesn't exist
        os.makedirs(unlocked_folder_path, exist_ok=True)

        # Loop through each file in the folder
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)

            # Check if the file is a PDF
            if os.path.isfile(filepath) and filename.lower().endswith('.pdf'):
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
                output_filepath = os.path.join(unlocked_folder_path, output_filename)
                output_file = open(output_filepath, 'wb')
                pdf_writer.write(output_file)

                # Close the file objects
                pdf_file.close()
                output_file.close()

        flash('PDF files have been unlocked and saved in the "Unlocked PDFs" folder', 'success')
        return redirect('/')
    return render_template('home.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    uploads = os.path.join(app.root_path, 'uploads/Unlocked PDFs')
    return send_from_directory(directory=uploads, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
