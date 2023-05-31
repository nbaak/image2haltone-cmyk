from flask import Flask, render_template, request, redirect
import io
import base64
from halftone import transform_image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/transform', methods=['POST'])
def transform():
    if 'image' not in request.files:
        return redirect('/')

    image = request.files['image']
    image_bytes = io.BytesIO(image.read())

    transformed_image = transform_image(image_bytes)
    transformed_image_encoded = base64.b64encode(transformed_image.getvalue()).decode('utf-8')

    return render_template('result.html', transformed_image=transformed_image_encoded)


if __name__ == '__main__':
    app.run()
