'''
blueprint for data loader API
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License
from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np

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
    def get_reference_image_name(self) -> str:
        pass

    @abstractmethod
    def get_reference_image(self) -> np.ndarray:
        pass

    @abstractmethod
    def get_image_to_transform_name(self) -> str:
        pass

    @abstractmethod
    def get_image_to_transform(self) -> np.ndarray:
        pass

    @abstractmethod
    def get_metrics(self, transformed_image: np.ndarray, **kwargs) -> dict:
        pass

    @abstractmethod
    def get_metric_images(self, transformed_image: np.ndarray, **kwargs) -> dict:
        pass


class base_dataset_loader(base_dataloader):
    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __getitem__(self, i: int) -> None:
        pass

    @abstractmethod
    def get_reference_image_by_index(self, index: int) -> np.ndarray:
        pass
