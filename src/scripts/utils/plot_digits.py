import matplotlib.pyplot as plt


def plot_digits(
    digits,
    labels=None,
    resolution=(28, 28),
    ticks=(3, 3),
    labels_pred=None,
    title=None,
    cmap="binary",
):
    """
    Plot grid of multiple given images
    """
    # Define subplots
    fig, axs = plt.subplots(ticks[0], ticks[1], subplot_kw=dict(xticks=[], yticks=[]))
    # Set title if provided
    if title:
        fig.suptitle(title)
    axs = axs.ravel()
    # Get total ticks
    ticks_total = ticks[0] * ticks[1]
    # Iterate over each tick
    for i in range(ticks_total):
        # Get current axes
        ax = axs[i]
        # Show digit
        ax.imshow(digits[i].reshape(resolution[0], resolution[1]), cmap=cmap)
        # Show labels
        if labels is not None:
            if labels_pred is None:
                color = "black"
            # Compare true and predicted labels
            else:
                # Correctly predicted
                if labels[i] == labels_pred[i]:
                    color = "green"
                # Incorrectly predicted
                else:
                    color = "red"
            ax.text(0.5, 0.5, labels[i], color=color)
    plt.show()
