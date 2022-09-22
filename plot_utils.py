import numpy as np

'''
plot bar chart on matplotlib qt qidget
'''
class bar_plotter:
    def __init__(self, bar_names, var_names, ax):
            self.bar_names = bar_names
            self.var_names = var_names
            self.ax = ax
            self.ax.axes.clear()
            self.num_bars = len(self.bar_names)
            self.num_vars = len(self.var_names)
            self.bar_width = 1/(self.num_bars+1)
            self.bars = [np.arange(self.num_vars)]
            for i in range(1, self.num_bars):
                self.bars.append([x + self.bar_width for x in self.bars[i-1]])

    def plot(self, bar_name, var_values):
        i = self.bar_names.index(bar_name)
        self.ax.axes.bar(self.bars[i], var_values, width=self.bar_width, label=bar_name)

    def show(self):
        if len(self.bar_names) > 1:
            self.ax.axes.legend()
            self.ax.axes.set_xticks([r + self.bar_width for r in range(self.num_vars)], self.var_names)
        self.set_plot_lims()
        self.ax.fig.tight_layout()
        self.ax.draw()

    def set_plot_lims(self):
        y_lims = self.ax.axes.get_ylim()
        # self.ax.axes.set_ylim(min(0, y_lims[0], max(1, y_lims[1])))
        self.ax.axes.set_ylim(top= max(1, y_lims[1]))

'''
plot radar chart on matplotlib qt
'''
class radar_plotter:
    def __init__(self, radar_names, var_names, ax):
            self.radar_names = radar_names
            self.var_names = var_names
            self.ax = ax
            self.ax.axes.clear()
            self.num_radars = len(self.radar_names)
            self.num_vars = len(self.var_names)
            self.radar_angles = [n/float(self.num_vars)*2*np.pi for n in range(self.num_vars)]
            self.radar_angles += self.radar_angles[:1]   # circular plot closure

    def plot(self, radar_name, var_values):
        var_values.append(var_values[0])   # add start to end to close the circular plot
        p = self.ax.axes.plot(self.radar_angles, var_values, linewidth=1, linestyle='solid', label=radar_name)
        self.ax.axes.fill(self.radar_angles, var_values, color=p[0].get_color(), alpha=0.1)


    def show(self):
        # self.ax.axes.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        self.ax.axes.legend(fontsize='x-small', loc='upper left')
        self.ax.axes.set_xticks(self.radar_angles[:-1], self.var_names)
        self.set_plot_lims()
        # self.ax.fig.tight_layout()
        self.ax.draw()

    def set_plot_lims(self):
        y_lims = self.ax.axes.get_ylim()
        # self.ax.axes.set_ylim(min(0, y_lims[0], max(1, y_lims[1])))
        self.ax.axes.set_ylim(top= max(1, y_lims[1]))

if __name__ == '__main__':
    bar_names = ['MAE', 'MSE', '1-SSIM']
    var_names = ['rotation', 'blur', 'brightness']
    data = {
    'MAE': [0.2668716006335758, 0.051162821817256156, 0.3446149318700745],
    'MSE': [0.1271412351301738, 0.005791870333875219, 0.17419698209102666],
    '1-SSIM': [0.8360364398076421, 0.47519104253678096, 0.5506169538684411],
    }
