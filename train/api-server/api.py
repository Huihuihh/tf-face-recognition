from time import time

from PIL import Image
from flask import Flask, request, jsonify, make_response

# assuming that script is run from `server` dir
import sys, os
sys.path.append(os.path.realpath('..'))

from tensorface import detection
from tensorface.recognition import recognize, learn_from_examples

# For test examples acquisition
SAVE_DETECT_FILES = False
SAVE_TRAIN_FILES = False

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# for CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')  # Put any other methods you need here
    return response


@app.route('/detect', methods=['POST'])
def detect():
    try:
        image_stream = request.files.get('image')  # get the image
        if not image_stream:
            return make_response('Please provide \'image\' for train.\n', 400)
        image = Image.open(image_stream)

        # Set an image confidence threshold value to limit returned data
        threshold = request.form.get('threshold')
        if threshold is None:
            threshold = 0.5
        else:
            threshold = float(threshold)

        faces = recognize(detection.get_faces(image, threshold))

        j = [f.data() for f in faces]
        # print("Result:", j)

        # save files
        if SAVE_DETECT_FILES and len(faces):
            id = time()
            with open('test_{}.json'.format(id), 'w') as f:
                f.write(j)

            image.save('test_{}.png'.format(id))
            for i, f in enumerate(faces):
                f.img.save('face_{}_{}.png'.format(id, i))

        return make_response(jsonify(j), 200)

    except Exception as e:
        import traceback
        traceback.print_exc()


@app.route('/train', methods=['POST'])
def train():
    try:
        # image with sprites
        image_stream = request.files.get('image')  # get the image
        if not image_stream:
            return make_response('Please provide \'image\' for train.\n', 400)
        image_sprite = Image.open(image_stream)

        # forms data
        name = request.form.get('name')
        if not name:
            return make_response('Please provide \'name\' for train.\n', 400)

        num = request.form.get('num')
        if not num:
            return make_response('Please provide \'num\' for train.\n', 400)
        num = int(num)

        size = request.form.get('size')
        if not size:
            return make_response('Please provide \'size\' for train.\n', 400)
        size = int(size)

        # save for debug purposes
        if SAVE_TRAIN_FILES:
            image_sprite.save('train_{}_{}_{}.png'.format(name, size, num))

        info = learn_from_examples(name, image_sprite, num, size)
        return make_response(jsonify([{'name': n, 'train_examples': s} for n, s in info.items()]), 200)

    except Exception as e:
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
