from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


def plot_pca(pca, X, explained_variance_=False, xlims=None):
    """
    Plot PCA explained variance and explained variance ratio
    """
    # Fit data
    pca.fit(X)
    # Plot parameters
    plt.title("PCA")
    plt.xlabel("number_of_components")
    plt.ylabel("explained_variance_ratio")
    # Cumulative explained variance ratio
    plt.plot(np.cumsum(pca.explained_variance_ratio_), label="explained_variance_ratio")
    # Explained variance
    if explained_variance_:
        plt.plot(pca.explained_variance_, label="explained_variance")
    # Check for limits
    if xlims:
        plt.xlim(xlims[0], xlims[1])
    plt.legend(loc="upper left")
    plt.show()