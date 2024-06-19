import base64
import json
import os
from flask import request, render_template, redirect, url_for, Flask
import requests
from werkzeug.utils import secure_filename
import sqlite3
from config import NAMES, IMAGE_PREFIX, VIDEO_PREFIX, HOST, IMAGES_TYPES, \
    VIDEO_TYPES, SOURCE_IMG_FILENAME, RESULT_IMG_FILENAME
from Animal import Animal


app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/index', methods=['POST', 'GET'])
def _index():
    return render_template('index.html', title="Главная", visibility='nothing', animals=[])


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect(url_for('_index'), code=302)


@app.route('/database', methods=['POST', 'GET'])
def database():
    _animals = [x for x in range(80)]
    return render_template('database.html', title='База данных', animals=get_animals(_animals))


@app.route('/info', methods=['POST', 'GET'])
def info():
    return render_template('info.html', title='Справка')


@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    if file.filename.endswith(IMAGES_TYPES):
        return redirect(url_for('detect_image', image=filepath), code=307)
    elif file.filename.endswith(VIDEO_TYPES):
        return redirect(url_for('detect_video', video=filepath), code=307)


@app.route('/detect/image', methods=['POST'])
def detect_image():
    image = request.args.get('image')
    with open(image, 'rb') as img_file:
        img = img_file.read()
    response = requests.post(HOST + "/image-animal-detection", data=img,
                             headers={'content-type': 'image/jpeg'})
    json_data = json.loads(response.text)
    animals = get_animals(json_data['classes'])
    return render_template('index.html', title='Определение', image_result=IMAGE_PREFIX + json_data['media'],
                           visibility='img', animals=animals)


@app.route('/detect/video', methods=['POST'])
def detect_video():
    video = request.args.get('video')
    with open(video, 'rb') as video_file:
        vid = video_file.read()
    response = requests.post(HOST + "/video-animal-detection", data=vid,
                             headers={'content-type': 'video/mp4'})
    json_data = json.loads(response.text)
    animals = get_animals(json_data['classes'])
    return render_template('index.html', title='Определение', video_result=VIDEO_PREFIX + json_data['media'],
                           visibility='video', animals=animals)


def get_animals(animals):
    con = sqlite3.connect('animals.db')
    cur = con.cursor()
    data = []
    for animal in animals:
        data.append(get_animal(cur, animal))
    cur.close()
    con.close()
    return data


def get_animal(cursor, animal):
    data = cursor.execute('SELECT name, img, info FROM animals WHERE uid = {}'.format(animal))
    for row in data:
        return Animal(row[0], row[1], row[2])


if __name__ == "__main__":
    app.run(port=5001)
