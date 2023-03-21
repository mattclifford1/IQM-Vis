'''
matplotlib plotting helpers
TODO: write docs how to use these (currently just have to look at the UI code)
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import numpy as np
from IQM_Vis.utils import image_utils

'''
plot bar chart on matplotlib qt qidget
'''
class bar_plotter:
    def __init__(self, bar_names, var_names, ax, lim):
            self.bar_names = bar_names
            self.var_names = var_names
            self.ax = ax
            self.lim =lim
            self.ax.axes.clear()
            self.num_bars = len(self.bar_names)
            self.num_vars = len(self.var_names)
            self.bar_width = 1/(self.num_bars+1)
            self.bars = [np.arange(self.num_vars)]
            for i in range(1, self.num_bars):
                self.bars.append([x + self.bar_width for x in self.bars[i-1]])

    def plot(self, bar_name, var_values):
        if len(self.bar_names) > 1:
            i = self.bar_names.index(bar_name)
            self.ax.axes.bar(self.bars[i], var_values, width=self.bar_width, label=bar_name)
        else:
            self.ax.axes.bar(self.var_names, var_values)

    def show(self):
        self.set_style()
        self.ax.draw()

    def set_style(self):
        if len(self.bar_names) > 1:
            self.ax.axes.legend()
            self.ax.axes.set_xticks([r + self.bar_width for r in range(self.num_vars)], self.var_names)
        self.set_plot_lims()
        self.ax.figure.tight_layout()

    def set_plot_lims(self):
        y_lims = self.ax.axes.get_ylim()
        # self.ax.axes.set_ylim(min(0, y_lims[0], max(1, y_lims[1])))
        self.ax.axes.set_ylim(top= max(self.lim, y_lims[1]))

'''
line plot of matplotlib qt widget
'''
class line_plotter:
    def __init__(self, ax, x_label, y_label, lim=1):
        self.ax = ax
        self.ax.axes.clear()
        self.x_label = x_label
        self.y_label = y_label
        self.lim = lim

    def plot(self, x, y, label):
        self.ax.axes.plot(x, y, label=label)

    def show(self):
        self.set_style()
        self.ax.draw()

    def set_style(self):
        self.ax.axes.legend()
        self.ax.axes.set_xlabel(self.x_label)
        self.set_plot_lims()
        self.ax.figure.tight_layout()

    def set_plot_lims(self):
        y_lims = self.ax.axes.get_ylim()
        # self.ax.axes.set_ylim(min(0, y_lims[0], max(1, y_lims[1])))
        self.ax.axes.set_ylim(top= max(self.lim, y_lims[1]))

'''
plot radar chart on matplotlib qt widget
'''
class radar_plotter:
    def __init__(self, radar_names, var_names, ax, lim=1):
            self.radar_names = radar_names
            self.var_names = var_names
            self.ax = ax
            self.lim = lim
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
        self.set_style()
        self.ax.draw()

    def set_style(self):
        # self.ax.axes.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        self.ax.axes.legend(fontsize='x-small', loc='upper left')
        self.ax.axes.set_xticks(self.radar_angles[:-1], self.var_names)
        self.set_plot_lims()
        # self.ax.fig.tight_layout()

    def set_plot_lims(self):
        y_lims = self.ax.axes.get_ylim()
        # self.ax.axes.set_ylim(min(0, y_lims[0], max(1, y_lims[1])))
        self.ax.axes.set_ylim(top= max(self.lim, y_lims[1]))


'''
metric averaging functions to get metric values over a range of transformation
'''
def get_all_slider_values(transforms, num_steps=10):
    range = transforms['max'] - transforms['min']
    # make sure if it's an int then we dont return step values that are floats
    if isinstance(transforms['min'], int) and isinstance(transforms['max'], int):
        num_steps = min(range, num_steps)
    steps = range/num_steps
    if type(transforms['min']) == int:
        steps = int(steps)
    values = list(np.arange(start=transforms['min'], stop=transforms['max'], step=steps))
    values.append(transforms['max'])
    return values

def get_all_single_transform_params(transforms):
    ''' get a list of all the individual transforms with a single parameter value
        useful when doing experiments to make a dataset '''
    list_of_single_trans = []
    for curr_trans in transforms:  # loop over all transformations
        for val in get_all_slider_values(transforms[curr_trans]):
            list_of_single_trans.append({curr_trans: val})
    return list_of_single_trans

def compute_metrics_over_range_single_trans(data_store, transforms, metric_params, metrics_to_use, pbar_signal=None, stop_flag=None):
    ''' compute metrics over a range of trans

    Args:
        data_store: object containing metrics and image
        transforms (dict): containing trans functions and min/max/initial values

    Returns:
        results (dict): results of IQM values at each transform value across its
                        whole paramter rance for the reference image
    '''
    # compute all metrics over their range of params and get avg/std
    results = {}
    # initialise results
    for metric in data_store.metrics:
        results[metric] = {}
        for tran in transforms:
            results[metric][tran] = {'param_values': [], 'scores': []}

    # get bar info (the lazy way)
    if pbar_signal != None:
        len_loop = 0
        for i, curr_trans in enumerate(transforms):
            for trans_value in get_all_slider_values(transforms[curr_trans]):
                len_loop += 1
    pbar_counter = 0

    # compute over all image transformations
    for curr_trans in transforms:  # loop over all transformations
        single_trans = {curr_trans: transforms[curr_trans]}
        all_param_values = get_all_slider_values(transforms[curr_trans])
        for trans_value in all_param_values:
            single_param_dict = {curr_trans: trans_value}
            trans_im = image_utils.get_transform_image(data_store, single_trans, single_param_dict) # initialse image
            metric_scores = data_store.get_metrics(trans_im, metrics_to_use, **metric_params)
            for metric in metric_scores:
                results[metric][curr_trans]['scores'].append(float(metric_scores[metric]))
                # and store the input trans values for plotting
                results[metric][curr_trans]['param_values'] = all_param_values

                # end if flag says to stop
                if stop_flag != None:
                    if stop_flag[0] == True:
                        # reset pbar
                        if pbar_signal != None:
                            pbar_signal.emit(0)
                        return

            # send signal to progress bar if provided
            if pbar_signal != None:
                pbar_counter += 1
                if pbar_counter == len_loop:
                    pbar_signal.emit(0)
                else:
                    pbar_signal.emit(int(((pbar_counter)/len_loop)*100))
    return results

def compute_metrics_over_range(data_store, transforms, transform_values, metric_params, metrics_to_use, pbar_signal=None, stop_flag=None):
    '''
    compute metrics over a range of trans (when using non initial values for other transforms)
    currently this method is not being used and instead using the simpler compute_metrics_over_range_single_trans

    Args:
        data_store: object containing metrics and image
        transforms (dict): containing trans functions and min/max/initial values
        transform_values (dict): containing the fixed current transform parameter values

    Returns:
        results (dict): results of IQM values at each transform value across its
                        whole paramter rance for the reference image
    '''
    # compute all metrics over their range of params and get avg/std
    results = {}
    # initialise results
    for metric in data_store.metrics:
        results[metric] = {}
        for tran in transforms:
            results[metric][tran] = {'param_values': [], 'scores': []}

    # get bar info (the lazy way)
    if pbar_signal != None:
        len_loop = 0
        for i, curr_trans in enumerate(transforms):
            for trans_value in get_all_slider_values(transforms[curr_trans]):
                len_loop += 1
    pbar_counter = 0

    # compute over all image transformations
    for curr_trans in transforms:  # loop over all transformations
        for trans_value in get_all_slider_values(transforms[curr_trans]):   # all values of the parameter
            vary_one_value = transform_values.copy()
            vary_one_value[curr_trans] = trans_value   # set to the varying value in this range loop
            trans_im = image_utils.get_transform_image(data_store, transforms, vary_one_value)     # initialse image
            metric_scores = data_store.get_metrics(trans_im, metrics_to_use, **metric_params)
            for metric in metric_scores:
                results[metric][curr_trans]['scores'].append(float(metric_scores[metric]))
                # and store the input trans values for plotting
                results[metric][curr_trans]['param_values'] = get_all_slider_values(transforms[curr_trans])

                # end if flag says to stop
                if stop_flag != None:
                    if stop_flag[0] == True:
                        # reset pbar
                        if pbar_signal != None:
                            pbar_signal.emit(0)
                        return

            # send signal to progress bar if provided
            if pbar_signal != None:
                pbar_counter += 1
                if pbar_counter == len_loop:
                    pbar_signal.emit(0)
                else:
                    pbar_signal.emit(int(((pbar_counter)/len_loop)*100))
    return results

def get_radar_plots_avg_plots(results, metrics_names, transformation_names, axes, lim=1):
    '''
    plot results on a polar axes -> radar/spider plot
    '''
    radar_plt = radar_plotter(radar_names=metrics_names,
                                    var_names=transformation_names,
                                    ax=axes,
                                    lim=lim)
    for metric in metrics_names:
        mean_value = []
        # std_value = []
        transform = []
        for tran in transformation_names:
            transform.append(tran)
            mean_value.append(np.mean(results[metric][tran]['scores']))
            # std_value.append(np.std(results[metric][tran]['scores']))
        radar_plt.plot(metric, mean_value)
    radar_plt.set_style()
    return radar_plt

def get_transform_range_plots(results, transform, axes, lim=1):
    '''
    plot a single transform range graph of all metrics
    '''
    plot = line_plotter(axes, transform, 'Values', lim=lim)
    for metric in results:
        plot.plot(results[metric][transform]['param_values'], results[metric][transform]['scores'], metric)
    return plot
