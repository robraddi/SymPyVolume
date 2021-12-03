
def get_pickables(ax):
    """Return a dictionary of matplotlib axis objects"""
    pickables = {}
    legend = ax.legend(fancybox=True, shadow=True)
    line_labels = legend.get_lines()
    for i,line in enumerate(ax.get_lines()):
        line_labels[i].set_picker(True)
        line_labels[i].set_pickradius(5)
        pickables[line_labels[i]] = line
    return pickables

def make_interactive(fig, axes):
    """Take a matplotlib figure object and a list of matplotlib axis objects to
    render an interactive plot.
    NOTE: Can only be used in Jupyter notebooks and Jupyter lab. Also, must
    have `%matplotlib widget` at the top of cell in Jupyter Notebook.
    """

    pickables = {}
    for ax in axes:
        pickables.update(get_pickables(ax))

    def on_pick(event):
        leg = event.artist
        visible = leg.get_visible()
        visible = not visible
        pickables[leg].set_visible(visible)
        leg.set_visible(visible)
        fig.canvas.draw()
        fig.tight_layout()

    fig.canvas.mpl_connect('pick_event', on_pick)
    fig.canvas.toolbar_visible = True
    fig.canvas.header_visible = False
    fig.canvas.resizable = True
    fig.set_size_inches(8, 4)
    fig.tight_layout()
