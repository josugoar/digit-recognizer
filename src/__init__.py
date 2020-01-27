from flask import Flask, render_template, url_for, request, jsonify
from flask_restful import Resource, Api
from flask_caching import Cache
from flask_flatpages import FlatPages

import base64
import imageio

from .scripts import Vctr
import joblib
import os


class Predict(Resource):
    Clf = joblib.load("src/scripts/models/DigitClassifier.joblib")

    def post(self):
        # Initialize save counter
        if request.json["save"]:
            if len(os.listdir("src/data")):
                ls = sorted(os.listdir("src/data"), key=lambda l: int(l.split(".")[0]))
                idx = int(ls[-1].split(".")[0])
            else:
                idx = 0
        else:
            idx = None

        # Get base64
        b64 = request.json["image"]
        # Decode to rgb
        rgb = imageio.imread(base64.b64decode(b64))
        # Convert to MNIST
        ret = Vctr(rgb)

        # Range through images
        if ret:
            for img in ret:
                # Get base
                base = img.pop("base", None).reshape(1, -1)
                # Predict labels & probability
                img["label"] = Predict.Clf.predict(base)[0]
                img["probability"] = Predict.Clf.predict_proba(base).tolist()
                # Save to database
                if idx:
                    idx += 1
                    cv2.imwrite(f"src/data/{idx}.jpg", base)

            return jsonify(ret)
        return


# TODO: SQLAlquemy database
class Data(Resource):
    data = []

    def get(self):
        return Data.data

    def put(self):
        return "Data added successfully"


app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={"CACHE_TYPE": "simple"})
pages = FlatPages(app)


@app.route("/")
@cache.cached(timeout=50)
def index():
    return render_template(
        "index.html",
        title="Digit Recognizer",
        cnv_msg="Start drawing!"
    )

@app.route("/docs/")
def docs():
    return pages.get("docs").html

@app.route("/model/")
def model():
    config = {
        "Vctr": {
            "input": ["rgb-image"],
            "output": ["base", "bounding-box"],
            "steps": ["grayscale", "blur", "threshold", "contours", "centroid"]
        },
        "Clf": {
            "input": ["28*28-pixels"],
            "output": ["label", "probability"],
            "steps": ["minmax-scale", "binarize", "Restricted-Boltzmann-Machine", "Logistic-Regression"]
        }
    }

    return jsonify(config)


api.add_resource(Predict, "/model/predict/")
api.add_resource(Data, "/model/data/")
