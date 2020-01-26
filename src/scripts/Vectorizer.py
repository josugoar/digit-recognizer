from sklearn.preprocessing import MinMaxScaler, StandardScaler, Binarizer
# from skimage.feature import hog

from sklearn.pipeline import make_pipeline


class Vectorizer:
    def __init__(self):
        self.model = make_pipeline(
            MinMaxScaler(),
            Binarizer(threshold=0.5)
        )

    def joblib(self, path="models/DigitVectorizer.joblib"):
        with open(path, "wb") as f:
            joblib.dump(self.model, f)
        print(f"Pickled vectorizer at {path}")

# hog(X_train[0].reshape(28, 28), orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1), transform_sqrt=True, block_norm="L1")
