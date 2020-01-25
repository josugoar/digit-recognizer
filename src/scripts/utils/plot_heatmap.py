from sklearn.datasets import load_digits
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


def plot_heatmap(
    X, y_true, y_pred,
    labels=load_digits().target_names,
):
    """
    Plot heatmap of confusion matrix
    """
    # Plot data heatmap
    sns.heatmap(
        confusion_matrix(y_true, y_pred).T,
        square=True,
        annot=True,
        fmt="d",
        xticklabels=labels,
        yticklabels=labels,
    )
    # Plot parameters
    plt.xlabel("true_label")
    plt.ylabel("predicted_label")
    plt.ylim(len(labels), 0)
    plt.show()