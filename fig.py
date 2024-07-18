import matplotlib.pyplot as plt
import numpy as np
import pickle
import io

num_rows = 10
num_cols = 1
fig, axs = plt.subplots(num_rows, num_cols, sharex=True)
for i in range(num_rows):
    ax = axs[i]
    ax.plot(np.arange(10), np.arange(10)**i)


def on_click(event):

    if not event.inaxes:
        return
    inx = list(fig.axes).index(event.inaxes)
    buf = io.BytesIO()
    pickle.dump(fig, buf)
    buf.seek(0)
    fig2 = pickle.load(buf)

    for i, ax in enumerate(fig2.axes):
        if i != inx:
            fig2.delaxes(ax)
        else:
            axes = ax

    fig2.show()


fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
