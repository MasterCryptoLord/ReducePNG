from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import tinify

# replace 'YOUR_API_KEY' with your actual TinyPNG API key
tinify.key = "gjbdV6w0lkgJblQ0fdDFMp3C3180chsj"

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(filename)

        # compress the file using TinyPNG
        source = tinify.from_file(filename)
        source.to_file("optimized.png")

        # remove the original file
        os.remove(filename)

        return {'message': 'File uploaded and compressed successfully'}

    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/download', methods=['GET'])
def download_file():
    try:
        return send_file('optimized.png', as_attachment=True)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
