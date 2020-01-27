from flask import Flask, render_template, url_for, send_from_directory, request, jsonify
from flask_restful import Resource, Api
from flask_caching import Cache
from flask_flatpages import FlatPages
from flask_sqlalchemy import SQLAlchemy

from .scripts import Vctr
import imageio
import joblib
import os


app = Flask(__name__)
app.config["FLATPAGES_ROOT"] = "static/pages/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///digit.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
cache = Cache(app, config={"CACHE_TYPE": "simple"})
pages = FlatPages(app)
db = SQLAlchemy(app)


class Predict(Resource):

    Clf = joblib.load("src/scripts/models/DigitClassifier.joblib")

    def post(self):

        def save(base, label):
            # Initialize save counter
            if len(os.listdir("src/data")):
                ls = sorted(os.listdir("src/data"),
                            key=lambda l: int(l.split(".")[0]))
                idx = int(ls[-1].split(".")[0]) + 1
            else:
                idx = 1
            # Save to database
            imageio.imwrite(f"src/data/{idx}.jpg", base)
            db.session.add(Digit(digit_id=idx, pred=label))
            return 1

        def pred(img):
            # Get base
            base = img.pop("base", None)
            # Predict labels and probability
            label = Predict.Clf.predict(base.reshape(1, -1))[0]
            proba = Predict.Clf.predict_proba(base.reshape(1, -1)).tolist()
            save(base, label)
            return label, proba

        # Vectorize image
        ret = Vctr(request.json["image"])
        if ret:
            # Range through images
            for img in ret:
                # Store prediction
                img["label"], img["probability"] = pred(img)
            db.session.commit()
            return jsonify(ret)
        return


class Digit(db.Model):

    digit_id = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    pred = db.Column(db.String(1), nullable=False)
    true = db.Column(db.String(1))

    def __str__(self):
        return f"Digit('{self.digit_id}', '{self.pred}', '{self.true}')"


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
            "input": ["base64"],
            "output": ["base", "bounding-box"],
            "steps": ["decode", "grayscale", "blur", "threshold", "contours", "centroid"]
        },
        "Clf": {
            "input": ["28*28-pixels"],
            "output": ["label", "probability"],
            "steps": ["minmax-scale", "binarize", "restricted-boltzmann-machine", "logistic-regression"]
        }
    }

    return jsonify(config)


@app.route("/model/data/")
def data():
    return render_template("database.html", digits=Digit.query.all())


@app.route("/model/data/<digit_id>")
def digit(digit_id):
    return send_from_directory("data/", f"{digit_id}.jpg", as_attachment=True)


api.add_resource(Predict, "/model/predict/")
