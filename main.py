import io
import logging
import os
import sys
import time

import numpy as np
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image, ImageOps

import basnet

logging.basicConfig(level=logging.INFO)

# Initialize the Flask application
app = Flask(__name__)
CORS(app)


# Simple probe.
@app.route('/', methods=['GET'])
def hello():
    return 'Hello from BASNet HTTP Service!'


@app.route('/extract', methods=['POST'])
def extract():
    start = time.time()
    logging.info(" EXTRACT")

    # Convert string of image data to uint8.
    if "data" not in request.files:
        return jsonify({"status": "error", "error": "missing file param `data`"}), 400
    data = request.files["data"].read()
    if len(data) == 0:
        return jsonify({"status:": "error", "error": "empty image"}), 400

    # Save debug locally.
    with open("original_image.jpg", "wb") as f:
        f.write(data)

    # Send to BASNet service.
    logging.info(" > sending to BASNet...")
    # Convert string data to PIL Image
    img = Image.open(io.BytesIO(data))

    # Ensure i,qge size is under 1024
    if img.size[0] > 1024 or img.size[1] > 1024:
        img.thumbnail((1024, 1024))

    # Process Image
    res = basnet.run(np.array(img))

    # Save to buffer
    maskBuff = io.BytesIO()
    res.save(maskBuff, 'PNG')
    maskBuff.seek(0)

    # Print stats
    logging.info(f'Completed BASNet Processing in {time.time() - start:.2f}s')

    # Save mask locally.
    logging.info(" > saving results...")
    with open("mask_image.png", "wb") as f:
        f.write(maskBuff.read())

    logging.info(" > opening mask...")
    mask = Image.open("mask_image.png").resize([img.width, img.height]).convert("L")

    # Convert string data to PIL Image.
    logging.info(" > compositing final image...")

    empty = Image.new("RGBA", img.size, 0)
    cutImg = Image.composite(img, empty, mask)

    # Save locally.
    logging.info(" > saving final image...")
    cutImg.save("subject_image.png")

    # Save to buffer
    finalImgBuff = io.BytesIO()
    cutImg.save(finalImgBuff, "PNG")
    finalImgBuff.seek(0)

    # Print stats
    logging.info(f"Completed in {time.time() - start:.2f}s")

    # Return data
    return send_file(finalImgBuff, mimetype="image/png")


@app.route('/mask', methods=['GET'])
def mask():
    # open previously extracted image and its mask
    img = Image.open("original_image.jpg")
    mask = Image.open("mask_image.png").resize([img.width, img.height]).convert("L")

    # Save to buffer
    finalImgBuff = io.BytesIO()
    mask.save(finalImgBuff, "PNG")
    finalImgBuff.seek(0)

    return send_file(finalImgBuff, mimetype="image/png")


@app.route('/grayscale', methods=['POST'])
def grayscale():
    start = time.time()
    logging.info(" GRAYSCALE")

    # open previously extracted image and its mask
    img = Image.open("original_image.jpg")
    mask = Image.open("mask_image.png").resize([img.width, img.height]).convert("L")

    #convert original image to grayscale
    grayImg = img.convert("L")
    grayImg.save("gray_image.png")

    #invert the mask image
    invertMask = ImageOps.invert(mask)
    invertMask.save("invert_mask_image.png")

    # Composite grayscale background with color subject
    logging.info(" > compositing final image...")
    finalImg = Image.composite(grayImg, img, invertMask)

    # Save to buffer
    finalImgBuff = io.BytesIO()
    finalImg.save(finalImgBuff, "PNG")
    finalImgBuff.seek(0)

    # Print stats
    logging.info(f"Completed in {time.time() - start:.2f}s")

    # Return data
    return send_file(finalImgBuff, mimetype="image/png")


@app.route('/gray', methods=['GET'])
def gray():
    img = Image.open("gray_image.png")

    # Save to buffer
    finalImgBuff = io.BytesIO()
    img.save(finalImgBuff, "PNG")
    finalImgBuff.seek(0)

    return send_file(finalImgBuff, mimetype="image/png")


@app.route('/invertmask', methods=['GET'])
def invert_mask():
    img = Image.open("invert_mask_image.png")

    # Save to buffer
    finalImgBuff = io.BytesIO()
    img.save(finalImgBuff, "PNG")
    finalImgBuff.seek(0)

    return send_file(finalImgBuff, mimetype="image/png")


@app.route('/combine', methods=['POST'])
def combine():
    start = time.time()
    logging.info(" COMBINE")

    # Convert string of image data to uint8.
    if "data" not in request.files:
        return jsonify({"status": "error", "error": "missing file param `data`"}), 400
    data = request.files["data"].read()
    if len(data) == 0:
        return jsonify({"status:": "error", "error": "empty image"}), 400

    # Convert string data to PIL Image
    backgroundImg = Image.open(io.BytesIO(data))

    # Ensure i,qge size is under 1024
    if backgroundImg.size[0] > 1024 or backgroundImg.size[1] > 1024:
        backgroundImg.thumbnail((1024, 1024))

    backgroundImg.save("background_image.png")

    # open previously extracted image and its mask
    img = Image.open("original_image.jpg")
    mask = Image.open("mask_image.png").resize([backgroundImg.width, backgroundImg.height]).convert("L")

    #convert original image to grayscale
    grayImg = backgroundImg.convert("L")
    grayImg.save("gray_image.png")

    #invert the mask image
    invertMask = ImageOps.invert(mask)
    invertMask.save("invert_mask_image.png")

    # Composite grayscale background with color subject
    logging.info(" > compositing final image...")
    finalImg = Image.composite(grayImg, img.resize([backgroundImg.width, backgroundImg.height]), invertMask)

    # Save to buffer
    finalImgBuff = io.BytesIO()
    finalImg.save(finalImgBuff, "PNG")
    finalImgBuff.seek(0)

    # Return data
    return send_file(finalImgBuff, mimetype="image/png")


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
