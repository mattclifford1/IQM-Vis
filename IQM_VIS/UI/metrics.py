import numpy as np

from IQM_VIS.utils import gui_utils, plot_utils

class app_metrics:
    '''
    metrics/error info updaters
    '''
    def compute_metrics(self):
        for im_pair in self.im_pair_names:
            # compute metric scores
            metrics_values = {}
            for key in self.metrics_dict.keys():
                metrics_values[key] = self.metrics_dict[key](self.image_data[im_pair[0]], self.image_data[im_pair[1]])
            self.display_metrics(metrics_values, im_pair)
            # compute metric images
            for key in self.metrics_image_dict.keys():
                image_name = gui_utils.get_metric_image_name(key, im_pair)
                image_name = key+str(im_pair)
                self.image_data[image_name] = self.metrics_image_dict[key](self.image_data[im_pair[0]], self.image_data[im_pair[1]])

    def display_metrics(self, metrics, label):
        if self.metrics_info_format == 'graph':
            self.display_metrics_graph(metrics, label)
        else:
            self.display_metrics_text(metrics, label)

    def display_metrics_graph(self, metrics, label):
        bar_plt = plot_utils.bar_plotter(bar_names=[label[0]],
                                        var_names=list(metrics.keys()),
                                        ax=self.widgets['label'][str(label)+'_metrics_info'])
        bar_plt.plot(label[0], list(metrics.values()))
        bar_plt.show()

    def display_metrics_text(self, metrics, label, disp_len=5):
        text = ''
        for key in metrics.keys():
            metric = gui_utils.str_to_len(str(metrics[key]), disp_len, '0')
            text += key + ': ' + metric + '\n'
        self.widgets['label'][str(label)+'_metrics_info'].setText(text)

    def get_metrics_over_range(self):
        # compute all metrics over their range of params and get avg/std
        data_store = {}
        # initialise data_store
        for im_pair in self.im_pair_names:
            data_store[str(im_pair)] = {}
            for metric in self.metrics_dict.keys():
                data_store[str(im_pair)][metric] = {}
                for trans in self.sliders.keys():
                    data_store[str(im_pair)][metric][trans] = []

        # compute over all image transformations
        for im_pair in self.im_pair_names:
            for curr_trans in self.sliders.keys():
                for trans_value in self.sliders[curr_trans]['values']:
                    trans_im = self.image_data[im_pair[0]]
                    for other_trans in self.sliders.keys():
                        if other_trans != curr_trans:
                            ui_slider_value = self.im_trans_params[other_trans]
                            trans_im = self.sliders[other_trans]['function'](trans_im, ui_slider_value)
                        else:
                            trans_im = self.sliders[curr_trans]['function'](trans_im, trans_value)
                    for metric in self.metrics_dict.keys():
                        metric_score = self.metrics_dict[metric](self.image_data[im_pair[0]], trans_im)
                        data_store[str(im_pair)][metric][curr_trans].append(float(metric_score))
        self.plot_metrics_graphs(data_store)

    def plot_metrics_graphs(self, data_store):
        # plot
        for im_pair in self.im_pair_names:
            radar_plotter = plot_utils.radar_plotter(radar_names=list(self.metrics_dict.keys()),
                                            var_names=list(self.sliders.keys()),
                                            ax=self.widgets['graph'][str(im_pair)+'_metrics'])
            for metric in self.metrics_dict.keys():
                mean_value = []
                std_value = []
                transform = []
                for trans in self.sliders.keys():
                    transform.append(trans)
                    mean_value.append(np.mean(data_store[str(im_pair)][metric][trans]))
                    # std_value.append(np.std(data_store[str(im_pair)][metric][trans]))
                radar_plotter.plot(metric, mean_value)
            radar_plotter.show()
