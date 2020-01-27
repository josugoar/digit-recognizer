import numpy as np
import base64
import imageio
import cv2


def Vctr(b64, centroid=True):
    # Decode to rgb
    rgb = imageio.imread(base64.b64decode(b64))
    # Convert to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
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
         # Range through contours
        for cnt in contours:
            # Get bounding box
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
            # Center by centroid
            if centroid:
                temp_x = int((20 - cX) / 2)
                temp_y = int((20 - cY) / 2)
                base[temp_y: temp_y + 20, temp_x: temp_x + 20] = resized
            # Center by bounding box
            else:
                base[5:25, 5:25] = resized

            # Append image data
            ret.append({
                "base": base,
                "x": x,
                "y": y,
                "width": w,
                "height": h
            })

        return ret
    return
