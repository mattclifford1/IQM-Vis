'''
matplotlib plotting helpers
TODO: write dev_resources/docs how to use these (currently just have to look at the UI code)
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
from __future__ import annotations

from functools import partial
import math
from typing import Any, Optional

import numpy as np
import scipy.stats

import IQM_Vis
from IQM_Vis.utils import image_utils, gui_utils

'''
plot bar chart on matplotlib qt qidget
'''
class bar_plotter:
    '''Grouped bar chart rendered on a matplotlib Qt canvas.'''

    def __init__(self, bar_names: list, var_names: list, ax: Any, lim: float) -> None:
        '''Args:
            bar_names: Names of the bar groups (e.g. metric names).
            var_names: Names of the x-axis variables (e.g. transform names).
            ax: A :class:`~IQM_Vis.utils.gui_utils.MplCanvas` instance.
            lim: Minimum upper y-axis limit.
        '''
        self.bar_names = bar_names
        self.var_names = var_names
        self.ax = ax
        self.lim = lim
        self.ax.axes.clear()
        self.num_bars = len(self.bar_names)
        self.num_vars = len(self.var_names)
        self.bar_width = 1/(self.num_bars+1)
        self.bars = [np.arange(self.num_vars)]
        for i in range(1, self.num_bars):
            self.bars.append([x + self.bar_width for x in self.bars[i-1]])

    def plot(self, bar_name: str, var_values: list) -> None:
        if len(self.bar_names) > 1:
            i = self.bar_names.index(bar_name)
            self.ax.axes.bar(self.bars[i], var_values, width=self.bar_width, label=bar_name)
        else:
            self.ax.axes.bar(self.var_names, var_values)

    def show(self) -> None:
        self.set_style()
        self.ax.draw()

    def set_style(self) -> None:
        if len(self.bar_names) > 1:
            self.ax.axes.legend()
            self.ax.axes.set_xticks([r + self.bar_width for r in range(self.num_vars)], self.var_names)
        self.set_plot_lims()
        self.ax.figure.tight_layout()

    def set_plot_lims(self) -> None:
        y_lims = self.ax.axes.get_ylim()
        # self.ax.axes.set_ylim(min(0, y_lims[0], max(1, y_lims[1])))
        self.ax.axes.set_ylim(top=max(self.lim, y_lims[1]))

'''
line plot of matplotlib qt widget
'''
class line_plotter:
    '''Line plot rendered on a matplotlib Qt canvas.'''

    def __init__(self, ax: Any, x_label: str = '', y_label: str = '', lim: float = 1) -> None:
        '''Args:
            ax: A :class:`~IQM_Vis.utils.gui_utils.MplCanvas` instance.
            x_label: Label for the x-axis.
            y_label: Label for the y-axis.
            lim: Minimum upper y-axis limit.
        '''
        self.ax = ax
        self.ax.axes.clear()
        self.x_label = x_label
        self.y_label = y_label
        self.lim = lim

    def plot(self, x: list, y: list, label: str) -> None:
        self.ax.axes.plot(x, y, label=label)

    def show(self) -> None:
        self.set_style()
        self.ax.draw()

    def set_style(self) -> None:
        self.ax.axes.legend()
        self.ax.axes.set_xlabel(self.x_label)
        self.set_plot_lims()
        self.ax.figure.tight_layout()

    def set_plot_lims(self) -> None:
        y_lims = self.ax.axes.get_ylim()
        # self.ax.axes.set_ylim(min(0, y_lims[0], max(1, y_lims[1])))
        self.ax.axes.set_ylim(top=max(self.lim, y_lims[1]))

'''
plot radar chart on matplotlib qt widget
'''
class radar_plotter:
    '''Radar / spider chart rendered on a polar matplotlib Qt canvas.'''

    def __init__(self, radar_names: list, var_names: list, ax: Any, lim: float = 1) -> None:
        '''Args:
            radar_names: Names of the data series (e.g. metric names).
            var_names: Names of the polygon vertices (e.g. transform names).
            ax: A polar :class:`~IQM_Vis.utils.gui_utils.MplCanvas` instance.
            lim: Minimum upper radial limit.
        '''
        self.radar_names = radar_names
        self.var_names = var_names
        self.ax = ax
        self.lim = lim
        self.ax.axes.clear()
        self.num_radars = len(self.radar_names)
        self.num_vars = len(self.var_names)
        self.radar_angles = [n/float(self.num_vars)*2*np.pi for n in range(self.num_vars)]
        self.radar_angles += self.radar_angles[:1]   # circular plot closure

    def plot(self, radar_name: str, var_values: list) -> None:
        var_values.append(var_values[0])   # add start to end to close the circular plot
        p = self.ax.axes.plot(self.radar_angles, var_values, linewidth=1, linestyle='solid', label=radar_name)
        self.ax.axes.fill(self.radar_angles, var_values, color=p[0].get_color(), alpha=0.1)

    def show(self) -> None:
        self.set_style()
        self.ax.draw()

    def set_style(self) -> None:
        # self.ax.axes.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        self.ax.axes.legend(fontsize='x-small', loc='upper left')
        self.ax.axes.set_xticks(self.radar_angles[:-1], self.var_names)
        self.set_plot_lims()
        # self.ax.fig.tight_layout()

    def set_plot_lims(self) -> None:
        y_lims = self.ax.axes.get_ylim()
        # self.ax.axes.set_ylim(min(0, y_lims[0], max(1, y_lims[1])))
        self.ax.axes.set_ylim(top=max(self.lim, y_lims[1]))

'''
scatter plotter on matplotlib qt widget
'''
class scatter_plotter:
    '''Interactive scatter plot rendered on a matplotlib Qt canvas.'''

    def __init__(self, ax: Any, x_label: str = '', y_label: str = '', lim: float = 1) -> None:
        '''Args:
            ax: A :class:`~IQM_Vis.utils.gui_utils.MplCanvas` instance.
            x_label: Label for the x-axis.
            y_label: Label for the y-axis.
            lim: Minimum upper y-axis limit.
        '''
        self.ax = ax
        self.ax.axes.clear()
        self.x_label = x_label
        self.y_label = y_label
        self.lim = lim

    def plot(self, x: list, y: list, annotations: Optional[list] = None,
             error: Optional[list] = None) -> None:
        self.sc = self.ax.axes.scatter(x, y, picker=True, color='blue')
        if annotations != None:
            self.annotations = annotations
        if error != None or error != []:
            self.ax.axes.errorbar(x, y, yerr=error, fmt="o", capsize=3, color='black')

    def show(self) -> None:
        self.set_style()
        self.ax.draw()

    def set_style(self) -> None:
        self.ax.axes.set_xlabel(self.x_label)
        self.ax.axes.set_ylabel(self.y_label)
        # self.set_plot_lims()
        self.ax.figure.tight_layout()

    def set_plot_lims(self) -> None:
        y_lims = self.ax.axes.get_ylim()
        self.ax.axes.set_ylim(top=max(self.lim, y_lims[1]))

'''
metric averaging functions to get metric values over a range of transformation
'''
def get_all_slider_values(transforms: dict, num_steps: int = 11) -> list:
    if num_steps == 1:
        raise ValueError(f'number of steps cannot be 1')
    if num_steps == 2:
        return [transforms['min'], transforms['max']]
    float_stabiliser = 100    # work around since computer can't represent e.g. 0.2 very well
    num_steps -= 1    # since we are using steps then appending stop value
    range = transforms['max'] - transforms['min']
    # make sure if it's an int then we dont return step values that are floats
    if isinstance(transforms['min'], int) and isinstance(transforms['max'], int):
        num_steps = min(range, num_steps)
    steps = range/num_steps
    if isinstance(transforms['min'], int) and isinstance(transforms['max'], int):
        steps = int(steps)
    values = np.arange(start=transforms['min']*float_stabiliser,
                       stop=transforms['max']*float_stabiliser, 
                       step=steps*float_stabiliser)
    values = list(values/float_stabiliser)
    if transforms['max'] not in values:
        values.append(transforms['max'])
    return values

def get_all_single_transform_params(transforms: dict, num_steps: int = 11) -> list:
    ''' get a list of all the individual transforms with a single parameter value
        useful when doing experiments to make a dataset '''
    list_of_single_trans = []
    for trans_name, trans_data in transforms.items():  # loop over all transformations
        if num_steps == 'from_dict':
            steps = trans_data['num_steps']
        else:
            steps = num_steps
        for val in get_all_slider_values(trans_data, num_steps=steps):
            list_of_single_trans.append({trans_name: val})

    return list_of_single_trans

def compute_metric_for_human_correlation(data_store: Any, transforms: dict, metric_params: dict,
                                          trans_str_values: list, metric: str) -> dict:
    scores = {}
    for trans_str in trans_str_values:
        trans, trans_value = gui_utils.get_trans_dict_from_str(trans_str)
        if trans in transforms.keys():
            single_trans = {trans: transforms[trans]}
        else:
            iqm_vis_trans = IQM_Vis.transforms.get_all_transforms()
            if trans in iqm_vis_trans.keys():
                single_trans = {trans: iqm_vis_trans[trans]}
            else:
                raise Exception(f"Cannot find transformation {trans} in provided transforms or any default transforms, please provide an implimentation of {trans} when contructing the UI.")
        single_param_dict = {trans: trans_value}
        trans_im = image_utils.get_transform_image(data_store, single_trans, single_param_dict) # initialse image
        metric_scores = data_store.get_metrics(trans_im, metric, **metric_params)
        scores[trans_str] = metric_scores[metric]
    return scores

def compute_metrics_over_range_single_trans(data_store: Any, transforms: dict, metric_params: dict,
                                              metrics_to_use: list, pbar_signal=None,
                                              stop_flag: Optional[list] = None,
                                              num_steps: int = 11) -> Optional[dict]:
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
    for metric in metrics_to_use:
        results[metric] = {}
        for tran in transforms:
            results[metric][tran] = {'param_values': [], 'scores': []}

    # get bar info (the lazy way)
    if pbar_signal != None:
        len_loop = 0
        for i, curr_trans in enumerate(transforms):
            for trans_value in get_all_slider_values(transforms[curr_trans], num_steps=num_steps):
                len_loop += 1
    pbar_counter = 0

    # compute over all image transformations
    for curr_trans in transforms:  # loop over all transformations
        single_trans = {curr_trans: transforms[curr_trans]}
        all_param_values = get_all_slider_values(
            transforms[curr_trans], num_steps=num_steps)
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

def compute_metrics_over_range(data_store: Any, transforms: dict, transform_values: dict,
                                metric_params: dict, metrics_to_use: list, pbar_signal=None,
                                stop_flag: Optional[list] = None,
                                num_steps: int = 11) -> Optional[dict]:
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
            for trans_value in get_all_slider_values(transforms[curr_trans], num_steps=num_steps):
                len_loop += 1
    pbar_counter = 0

    # compute over all image transformations
    for curr_trans in transforms:  # loop over all transformations
        for trans_value in get_all_slider_values(transforms[curr_trans], num_steps=num_steps):   # all values of the parameter
            vary_one_value = transform_values.copy()
            vary_one_value[curr_trans] = trans_value   # set to the varying value in this range loop
            trans_im = image_utils.get_transform_image(data_store, transforms, vary_one_value)     # initialse image
            metric_scores = data_store.get_metrics(trans_im, metrics_to_use, **metric_params)
            for metric in metric_scores:
                results[metric][curr_trans]['scores'].append(float(metric_scores[metric]))
                # and store the input trans values for plotting
                results[metric][curr_trans]['param_values'] = get_all_slider_values(
                    transforms[curr_trans], num_steps=num_steps)

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

def get_radar_plots_avg_plots(results: dict, metrics_names: list,
                               transformation_names: list, axes: Any,
                               lim: float = 1) -> radar_plotter:
    '''
    plot results on a polar axes -> radar/spider plot
    '''
    radar_plt = radar_plotter(radar_names=metrics_names,
                                    var_names=transformation_names,
                                    ax=axes,
                                    lim=lim)
    if transformation_names == []:
        return radar_plt
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

def get_transform_range_plots(results: dict, transform: str, axes: Any,
                               lim: float = 1) -> line_plotter:
    '''
    plot a single transform range graph of all metrics
    '''
    plot = line_plotter(axes, transform, 'Values', lim=lim)
    for metric in results:
        plot.plot(results[metric][transform]['param_values'], results[metric][transform]['scores'], metric)
    return plot

def get_correlation_plot(human_scores: dict, metric_scores: dict, axes: Any,
                          metric: str, change_trans_value_signal) -> scatter_plotter:
    '''
    scatter plot for correlations
    '''
    sp = scatter_plotter(axes,
                x_label=metric,
                y_label='Human Score')
    x = []
    y = []
    e = []
    labels = []
    for trans in human_scores['mean']:
        x.append(metric_scores[metric][trans])
        y.append(human_scores['mean'][trans])
        try:
            std = human_scores['std'][trans]
        except KeyError:
            std = 0
        if math.isnan(std):
            std = 0
        e.append(std)
        name, value = gui_utils.get_trans_dict_from_str(trans)
        labels.append(f'{name}={value}')
    sp.plot(x, y, annotations=labels, error=e)
    # make interactive hover for points
    annot = sp.ax.axes.annotate("", xy=(0, 0), xytext=(0, 0), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->")
                        )
    annot.set_visible(False)
    sp.ax.figure.canvas.mpl_connect(
        "motion_notify_event", partial(hover_scatter, sp, annot))
    sp.ax.figure.canvas.mpl_connect(
        "pick_event", partial(click_scatter, sp, change_trans_value_signal))
    # get correlation as title
    pear = scipy.stats.pearsonr(x, y)
    spear = scipy.stats.spearmanr(x, y)
    sp.ax.axes.set_title(
        f"Spearman's: {spear.correlation:.4f}\n  Pearson's: {pear.statistic:.4f}")
    return sp

def click_scatter(_plot: scatter_plotter, change_trans_value_signal, event) -> None:
    ''' send signal of which data point was clicked '''
    change_trans_value_signal.emit(_plot.annotations[event.ind[0]])

def hover_scatter(_plot: scatter_plotter, annot, event) -> None:
    vis = annot.get_visible()
    # if event.inaxes == _plot.ax.axes:
    cont, ind = _plot.sc.contains(event)
    if cont:
        update_annot(ind, _plot, annot)
        annot.set_visible(True)
        _plot.ax.figure.canvas.draw_idle()
    else:
        if vis:
            annot.set_visible(False)
            _plot.ax.figure.canvas.draw_idle()

def update_annot(ind: dict, _plot: scatter_plotter, annot) -> None:
    pos = _plot.sc.get_offsets()[ind["ind"][0]].copy()
    xlims = _plot.ax.axes.get_xlim()
    x_range = xlims[1] - xlims[0]
    x_middle = xlims[0] + x_range/2
    if pos[0] > x_middle:
        pos[0] -= x_range/2
    # else:
    #     pos[0] += xlim/5
    annot.xy = pos
    text = ""
    for i in ind['ind']:
        if text != "":
            text += "\n"
        text += f"{_plot.annotations[i]}"
    annot.set_text(text)
