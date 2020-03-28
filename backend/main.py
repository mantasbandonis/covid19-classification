from PIL import Image
import base64
import io
import re
import numpy as np

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
    base64_decoded = base64.b64decode(base64_encoded_image)
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)
    print(image_np)

    probability = ''
    if np.random.rand() < 0.5:
        probability = -1
    else:
        probability = np.random.rand()

    prob_str = str(probability) # " ".join(str(x) for x in image_np.shape)
    return (prob_str, 200, headers)