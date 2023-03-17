'''
blueprint for data loader API
'''
from abc import ABC, abstractmethod

class base_dataloader(ABC):
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
