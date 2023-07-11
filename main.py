from flask import Flask, request, send_file, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import zipfile
import tinify

tinify.key = "gjbdV6w0lkgJblQ0fdDFMp3C3180chsj"

app = Flask(__name__)
app.secret_key = 'some_secret_key'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')

        # Check if any file is uploaded or not
        if not files or files[0].filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        new_files = []

        for file in files:
            filename = secure_filename(file.filename)
            file.save(filename)

            # Compress the file using TinyPNG
            source = tinify.from_file(filename)
            new_filename = os.path.splitext(
                filename)[0] + "(ReducePng.com)" + os.path.splitext(filename)[1]
            source.to_file(new_filename)

            # Add the compressed file to new_files list
            new_files.append(new_filename)

            # Remove the original file
            os.remove(filename)

        # Create a zip file and add each compressed file to it
        zip_filename = "compressed_files.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in new_files:
                zipf.write(file)

        return render_template('download.html', filename=zip_filename)

    return render_template('upload.html')


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
