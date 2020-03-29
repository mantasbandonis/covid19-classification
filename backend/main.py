from PIL import Image
import base64
import io
import re
import numpy as np
import cv2
import tensorflow as tf

print(tf.__version__)
model = tf.keras.models.load_model('modelV3.h5')


def predict(image_np):
    #image = cv2.imread("img.png")
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    imageReshape = image[None, :]
    # print(imageReshape.shape)

    score = model.predict(imageReshape)[:, 3]
    return score[0]


def handler(request):
    # https://cloud.google.com/functions/docs/writing/http#functions_http_cors-python
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json()
    base64_encoded_image = request_json['image']
    # base64_encoded_image = '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'
    base64_decoded = base64.b64decode(base64_encoded_image)
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)
    # print(image_np)

    probability = predict(image_np)

    print(probability)
    prob_str = str(probability)  # " ".join(str(x) for x in image_np.shape)
    return (prob_str, 200, headers)


# handler({})
