from flask import Flask, render_template, url_for, request, jsonify
from flask_restful import Resource, Api
from flask_caching import Cache

from skimage.feature import hog
import numpy as np
import cv2
import imageio

import base64
import os


class Model(Resource):
    def get(self):
        # TODO: model selection template
        return {"models": ["PCA_LR", "RBM_LR"]}

    def put(self):
        # TODO: change prediction model
        return "Model changed successfully"


class Predict(Resource):
    def post(self):
        # Get data
        raw = request.json["image"]
        show = request.json["show"]
        save = request.json["save"]

        # Decode from base64
        decode = imageio.imread(base64.b64decode(raw))
        # Convert to grayscale
        gray = cv2.cvtColor(decode, cv2.COLOR_BGR2GRAY)
        # Blur to filter noise
        blur = cv2.blur(gray, (5, 5))
        # Apply binary threshold
        _, thresh = cv2.threshold(blur, thresh=127, maxval=255, type=0)
        # Find contorns
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize empty data holder
        ret = []
        # Get last stored file
        # TODO: Create database
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
            equalN = np.zeros((N, N))
            equalN[temp_y: temp_y + h, temp_x: temp_x + w] = roi

            # Resize perserving aspect ratio
            resized = cv2.resize(equalN, dsize=(20, 20), interpolation=cv2.INTER_AREA)

            # Compute moments
            M = cv2.moments(resized)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            base = np.zeros((28, 28))

            #--------------------------------------
            # # Center by bounding box
            # base[5:25, 5:25] = resized
            #--------------------------------------

            # Center by centroid
            temp_x = int((20 - cX) / 2)
            temp_y = int((20 - cY) / 2)
            base[temp_y: temp_y + 20, temp_x: temp_x + 20] = resized

            # OPTIONAL: Scale stroke width
            # preprocess = cv2.dilate(base, (3, 3))

            # TODO: Get hog features & predict label
            hog_fd = hog(base, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1))
            pred = "0"

            # Test purposes only #
            cv2.imshow("img", base)
            cv2.waitKey(0)
            #--------------------#

            # TODO: Save to database
            if save:
                idx += 1
                cv2.imwrite(f"src/data/{idx}.jpg", base)

            # Append image data
            ret.append({
                # TODO: Add prediction result
                "pred": pred,
                "x": x,
                "y": y,
                "width": w,
                "height": h
            })

            if show:
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


# TODO: SQLAlquemy database here
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
