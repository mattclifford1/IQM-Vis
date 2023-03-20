'''
blueprint for data loader API
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from abc import ABC, abstractmethod

class base_dataloader(ABC):
    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, metrics_dict):
        self._metrics = metrics_dict

    @property
    def metric_images(self):
        return self._metric_images

    @metric_images.setter
    def metric_images(self, metric_images_dict):
        self._metric_images = metric_images_dict

    @abstractmethod
    def get_reference_image_name(self):
        pass

    @abstractmethod
    def get_reference_image(self):
        pass

    @abstractmethod
    def get_image_to_transform_name(self):
        pass

    @abstractmethod
    def get_image_to_transform(self):
        pass

    @abstractmethod
    def get_metrics(self):
        pass

    @abstractmethod
    def get_metric_images(self):
        pass


class base_dataset_loader(base_dataloader):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self):
        pass
