from flask import Flask, render_template, url_for, request, jsonify
from flask_restful import Resource, Api
from flask_caching import Cache

import cv2
import imageio

import base64
import os


class Model(Resource):
    def get(self):
        return {"models": ["PCA_LR", "RBM_LR"]}

    def put(self):
        return "Model changed successfully"


class Predict(Resource):
    def post(self):
        # Get data
        raw = request.json["image"]

        # Decode from base64
        decoded = imageio.imread(base64.b64decode(raw))
        # Convert to grayscale
        grayscale = cv2.cvtColor(decoded, cv2.COLOR_BGR2GRAY)
        # Apply binary threshold
        _, thresh = cv2.threshold(grayscale, thresh=127, maxval=255, type=0)
        # Find contorns
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize empty data holder
        ret = []
        # Get last stored file
        idx = int(os.listdir("src/data")[-1][0])
        # Draw bounding box
        for cnt in contours:
            # Get box size
            x, y, w, h = cv2.boundingRect(cnt)
            ret.append({
                "x": x,
                "y": y,
                "width": w,
                "height": h
            })
            # Save to database
            idx += 1
            roi = thresh[y: y + h, x: x + w]
            cv2.imwrite(f"src/data/{idx}.jpg", roi)
            # Draw rectangle
            cv2.rectangle(thresh, pt1=(x, y), pt2=(x + w, y + h), color=127, thickness=3)

        # Draw bounding contour
        cv2.drawContours(thresh, contours, contourIdx=-1, color=127, thickness=3)

        # Show image
        if request.json["preprocess"]:
            cv2.imshow("img", thresh)
            cv2.waitKey(0)

        return jsonify(ret)


class Data(Resource):
    data = []

    def get(self):
        return Data.data

    def post(self):
        return "Data added successfully"


app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.route("/")
@cache.cached(timeout=50)
def sketch():
    return render_template("index.html")


api.add_resource(Model, "/model/")
api.add_resource(Predict, "/model/predict/")
api.add_resource(Data, "/model/data/")