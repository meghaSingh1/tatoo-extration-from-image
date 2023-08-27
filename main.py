import os
import io
import base64
import cv2
import numpy

from flask import Flask, request, jsonify, render_template, redirect, send_file
from werkzeug.utils import secure_filename
from io import BytesIO

from PIL import Image
app = Flask(__name__)


allowed_exts = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}

def check_allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts


@app.route("/",methods=['GET', 'POST'])
def index():
    print(request.method)
    print(request.files)
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and check_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            filestr = request.files['file'].read()
            #convert string data to numpy array
            file_bytes = numpy.fromstring(filestr, numpy.uint8)
            # convert numpy array to image
            img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
            cv2.imwrite("./inputimage.jpeg", img)
            os.system('backgroundremover -i "inputimage.jpeg" -m "u2netp" -o "tatoo.png"')
            #os.remove("./inputimage.jpeg")
            
            img = cv2.imread(os.path.join("tatoo.png"))
            # img = Image.fromarray(img.astype("uint8"))
            rawBytes = io.BytesIO()
            # img.save(rawBytes, "JPEG")
            # rawBytes.seek(0)
            encoded_string = base64.b64encode(rawBytes.read()).decode("utf-8")
            with open("tatoo.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            return render_template('index.html', img_data=encoded_string), 200
    else:
        return render_template('index.html', img_data=""), 200

# main driver function
if __name__ == '__main__':
	app.run(host="127.0.0.1", port="8080")
