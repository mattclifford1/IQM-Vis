''' thread and signal classes to makethe UI smoother
    useful info about PyQt6 threads: https://www.pythontutorial.net/pyqt/pyqt-qthread/'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from IQM_Vis.utils import plot_utils

import time


class get_range_results_worker(QObject):
    progress = pyqtSignal(int)
    current_image = pyqtSignal(str)
    completed = pyqtSignal(dict)
    stopped = pyqtSignal(bool)

    @pyqtSlot(dict)
    def do_work(self, data):
        t0 = time.time()

        metric_over_range_results = []
        max_val = 0
        self.stop_flag = [False]
        for i, data_store in enumerate(data['data_stores']):
            self.current_image.emit(f'Getting range plot values for {data_store.get_reference_image_name()} progress:')
            results = plot_utils.compute_metrics_over_range_single_trans(data_store,
                data['trans'],
                data['metric_params'],
                data['metrics_to_use'],
                pbar_signal=self.progress,
                stop_flag=self.stop_flag,
                num_steps=data['num_steps'])
            if self.stop_flag[0] == True:
                self.stopped.emit(True)
                return
            metric_over_range_results.append(results)
            # see max metric values
            for _, metric in results.items():
                for trans, data in metric.items():
                    for val in data['scores']:
                        max_val = max(max_val, val)
        data_return = {'metric_over_range_results': metric_over_range_results,
                       'max_val': max_val}
        self.completed.emit(data_return)

        # t1 = time.time()
        # print(f'time: {t1-t0}')

    def stop(self):
        if hasattr(self, 'stop_flag'):
            # use a mutable data type (list) as can pass as a reference (ish) then
            self.stop_flag[0] = True

    def __del__(self):
        # close app upon garbage collection
        self.stop()