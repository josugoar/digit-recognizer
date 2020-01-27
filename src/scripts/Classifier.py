from sklearn.preprocessing import MinMaxScaler, Binarizer
from sklearn.neural_network import BernoulliRBM
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline

from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from utils import plot_digits, plot_heatmap

import numpy as np
import joblib


class Clf:
    def grid_search(self, X, y, **params):
        return GridSearchCV(
            self.model,
            params,
            cv=2,
            verbose=True,
             n_jobs=-1
        ).fit(X, y).best_estimator_

    def score(self, X, y, cv=5):
        return np.mean(cross_val_score(self.model, X, y, cv=cv))

    def report(self, X, y):
        print(
            "Classification report for classifier %s:\n%s\n"
            % (self.model, classification_report(y, self.model.predict(X)))
        )

    def joblib(self, path="models/DigitClassifier.joblib"):
        with open(path, "wb") as f:
            joblib.dump(self.model, f)
        print(f"Pickled classifier at {path}")

    @staticmethod
    def plot_heatmap(X, y_true, y_pred):
        plot_heatmap(X, y_true, y_pred)

    @staticmethod
    def plot_digits(digits, labels=None, ticks=(3, 3), labels_pred=None):
        plot_digits(digits, labels=labels, ticks=ticks, labels_pred=labels_pred)


class RBM_LR(Clf):
    def __init__(
        self, penalty="l2", solver="newton-cg", learning_rate=0.01, C=1, random_state=None, verbose=False
    ):
        self.model = make_pipeline(
            MinMaxScaler(),
            Binarizer(threshold=0.5),
            BernoulliRBM(learning_rate=learning_rate, random_state=random_state),
            LogisticRegression(
                penalty=penalty,
                solver=solver,
                C=C,
                random_state=random_state,
                multi_class="multinomial",
            ),
            verbose=verbose
        )


class PCA_LR(Clf):
    def __init__(
        self, penalty="l2", solver="saga", C=1, random_state=None, verbose=False,
    ):
        self.model = make_pipeline(
            MinMaxScaler(),
            Binarizer(threshold=0.5),
            PCA(0.99, random_state=random_state),
            LogisticRegression(
                penalty=penalty,
                C=C,
                solver=solver,
                random_state=random_state,
                multi_class="multinomial",
            ),
            verbose=verbose,
        )
