from flask import Flask, render_template, make_response, url_for, request, jsonify
from flask_restful import Resource, Api
from flask_caching import Cache
from flask_flatpages import FlatPages

# from skimage.feature import hog
import numpy as np
import cv2
import imageio

import base64
import joblib
import os


class Predict(Resource):
    RBM_LR = joblib.load("src/scripts/models/RBM_LR.joblib")
    PCA_LR = joblib.load("src/scripts/models/PCA_LR.joblib")

    def post(self):
        # Get data
        raw = request.json["image"]
        show = request.json["show"]
        save = request.json["save"]

        # Decode from base64 to rgb
        decode = imageio.imread(base64.b64decode(raw))
        # Convert to grayscale
        gray = cv2.cvtColor(decode, cv2.COLOR_BGR2GRAY)
        # Blur to filter noise
        blur = cv2.blur(gray, (5, 5))
        # Apply binary threshold
        _, thresh = cv2.threshold(blur, thresh=127, maxval=255, type=0)
        # Find contourns
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check for no contours
        if contours:
            # Initialize empty data holder
            ret = []

            # Get last saved file
            if save:
                if len(os.listdir("src/data")):
                    ls = sorted(os.listdir("src/data"), key=lambda l: int(l.split(".")[0]))
                    idx = int(ls[-1].split(".")[0])
                else:
                    idx = 0

            # Range through contours
            for cnt in contours:
                # Get box size
                x, y, w, h = cv2.boundingRect(cnt)
                roi = thresh[y: y + h, x: x + w]

                # Center by maximum size
                N = np.maximum(w, h)
                temp_x = int((N - w) / 2)
                temp_y = int((N - h) / 2)
                boxed = np.zeros((N, N))
                boxed[temp_y: temp_y + h, temp_x: temp_x + w] = roi

                # Resize perserving aspect ratio
                resized = cv2.resize(boxed, dsize=(20, 20), interpolation=cv2.INTER_AREA)

                # Compute moments
                M = cv2.moments(resized)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                base = np.zeros((28, 28))

                # Center by bounding box
                #---------------------------
                # base[5:25, 5:25] = resized
                #---------------------------

                # Center by centroid
                temp_x = int((20 - cX) / 2)
                temp_y = int((20 - cY) / 2)
                base[temp_y: temp_y + 20, temp_x: temp_x + 20] = resized

                # TODO: Get hog features
                # H = hog(base, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1))

                # Predict label
                label = Predict.RBM_LR.predict(base.reshape(1, -1))[0]

                # Append image data
                ret.append({
                    "label": label,
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                })

                # Save to database
                if save:
                    idx += 1
                    cv2.imwrite(f"src/data/{idx}.jpg", base)

                if show:
                    cv2.imshow("img", base)
                    cv2.waitKey(0)

                    # Draw bounding box
                    cv2.rectangle(thresh, pt1=(x, y), pt2=(x + w, y + h), color=127, thickness=3)

                    # Draw momments
                    M = cv2.moments(roi)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(thresh, center=(x + cX, y + cY), radius=3, color=127, thickness=-1)

                    # Draw bounding contour
                    cv2.drawContours(thresh, contours, contourIdx=-1, color=127, thickness=3)

                    # Put text
                    cv2.putText(thresh, pred, org=(x, y - 10), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=100, thickness=3)

            # Show image
            if show:
                cv2.imshow("img", thresh)
                cv2.waitKey(0)

            return jsonify(ret)

        else:
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
    return pages.get("README").html

@app.route("/model/")
def model():
    config = {
        "Vctr": {
            "input": ["rgb(a)-image"],
            "output": ["bounding-box", "hog-fts"],
            "steps": ["grayscale", "blur", "contours", "centroid", "minmax-scale", "binarize", "hog"]
        },
        "PCA_LR": {
            "input": ["hog-fts"],
            "output": ["label", "score"],
            "steps": ["Principal-Component-Analysis", "Logistic-Regression"]
        },
        "RBM_LR": {
            "input": ["hog-fts"],
            "output": ["label", "score"],
            "steps": ["Restricted-Boltzmann-Machine", "Logistic-Regression"]
        }
    }

    return jsonify(config)


api.add_resource(Predict, "/model/predict/")
api.add_resource(Data, "/model/data/")
