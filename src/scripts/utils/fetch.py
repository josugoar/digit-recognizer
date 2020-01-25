from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

import numpy as np


def fetch(n_samples, test_size=0.2, random_state=None):
    """
    ### Parameters
    - n_samples: {int/"all", required} Number of samples to fetch
    - test_size: {float, optional (default: 0.2)} Percentage of test samples
    - random_state: {int/None, optional (default: None)} Train and test split randomness
    """

    assert isinstance(n_samples, int) or n_samples == "all"
    assert isinstance(test_size, float)
    assert isinstance(random_state, int) or random_state == None

    X, y = fetch_openml("mnist_784", version=1, return_X_y=True)

    if n_samples == "all":
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    else:
        rnd = np.random.RandomState(seed=random_state)
        idx = rnd.randint(y.size, size=n_samples)
        return train_test_split(
            X[idx, :], y[idx], test_size=test_size, random_state=random_state
        )
