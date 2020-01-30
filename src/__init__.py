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
    Clf = joblib.load("src/scripts/models/RBM_LR.joblib")

    def post(self):
        def save(base, label):
            # Get label list
            ls = [int(l[2:-5]) for l in os.listdir("src/data") if l[0] == label]
            # Initialize save counter
            if ls:
                idx = max(ls) + 1
                # Check for missing index
                for i, l in enumerate(sorted(ls)):
                    if l != i:
                        idx = i
                        break
            else:
                idx = 0
            # Save to database
            imageio.imwrite(f"src/data/{label}({idx}).jpg", base)
            db.session.add(Digit(digit_id=f"{label}({idx}).jpg", pred=label))

        def pred(img):
            # Get base
            base = img.pop("base", None)
            # Predict labels and probability
            label = Predict.Clf.predict(base.reshape(1, -1))[0]
            proba = Predict.Clf.predict_proba(base.reshape(1, -1)).tolist()
            if request.json["save"]:
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
    digit_id = db.Column(db.String(10), primary_key=True, unique=True, nullable=False)
    pred = db.Column(db.String(1), nullable=False)

    def __str__(self):
        return f"Digit('{self.digit_id}', '{self.pred}')"

    def clean_db():
        db.drop_all()
        db.create_all()
        if os.listdir("src/data"):
            for digit in os.listdir("src/data"):
                db.session.add(Digit(digit_id=digit, pred=digit[0]))
            db.session.commit()


@app.route("/")
@cache.cached(timeout=50)
def index():
    return render_template(
        "index.html",
        title="Digit Recognizer",
        cnv_msg="Start drawing!"
    )


@app.route("/info/")
def info():
    return pages.get("info").html


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
            "steps": ["minmax-scale", "binarize", ["restricted-boltzmann-machine", "principal-component-analisys"], "logistic-regression"]
        }
    }

    return jsonify(config)


@app.route("/model/data/")
def data():
    return render_template("database.html", digits=Digit.query.all())


@app.route("/model/data/<digit_id>")
def digit(digit_id):
    return send_from_directory("data/", str(digit_id), as_attachment=True)


api.add_resource(Predict, "/model/predict/")


Digit.clean_db()
