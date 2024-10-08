'''
noise transformations
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

from abc import ABC, abstractmethod
import numpy as np
import warnings

# Suppress the specific DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning,
                        message="__array_wrap__ must accept context and return_scalar arguments")


class _base_noise(ABC):
    def __init__(self, acceptable_percent=0.9, max_iter=50, reject_low_noise=False, **kwargs):
        self._setup_args(**kwargs)
        self.acceptable_percent = acceptable_percent
        self.max_iter = max_iter
        self.reject_low_noise = reject_low_noise
        self.num_rejected = 0

    def _setup_args(self, **kwargs):
        pass

    @abstractmethod
    def _make_noisey_image(self, img, np=np):
        # uses any args on self for parameters
        # must return x_noisey, additive_noise
        pass

    def __call__(self, img, param=0):
        '''
        will return a noisy image with noise level according to 'param'
        highest noise will be returned if noise level is too low acccording to acceptable_percent
        '''
        self.num_rejected = 0
        self.actual_noise = 0
        if param is not None:
            self.param = param
        return self._call_single(img)

    def _call_single(self, img, np=np):
        '''
        make noisy image until either acceptable percent is reached or max_iter is reached
        will return the highest noise level if noise level is too low acccording to acceptable_percent
        '''
        for _ in range(self.max_iter):
            x_noisey, additive_noise = self._make_noisey_image(img)
            # check noise level and actual noise level reduced after clipping
            expected_noise = np.sqrt(np.mean(np.square(additive_noise)))
            if self.reject_low_noise == False:
                return x_noisey
            else:
                curr_actual_noise = np.sqrt(np.mean(np.square(x_noisey - img)))
                # option to reject and redo the noise if too low (recursion)
                if curr_actual_noise >= self.acceptable_percent * expected_noise:
                    return x_noisey
                elif curr_actual_noise > self.actual_noise:
                    self.num_rejected += 1
                    self.actual_noise = curr_actual_noise
                    best = x_noisey
                else:
                    self.num_rejected += 1
        return best


class noise_hypersphere(_base_noise):
    '''Add random noise on a hypersphere with radius epsilon. Image is clipped to the range (0, 1)

    Args:
        image (np.array): image to have noise added
        std (float): epsilon of the hypersphere radius of noise.
                         (Defaults to 0)

    Returns:
        image (np.array): adjusted image
    '''
    def _setup_args(self, epsilon=1, seed=True):
        self.param = epsilon
        self.seed = seed

    def _make_noisey_image(self, img):
        if self.param <= 0:
            return img, 0.0
        if self.seed:
            np.random.seed(42)
        noise = np.random.randn(*img.shape)
        noise_norm = noise / np.linalg.norm(noise.reshape(-1))
        additive_noise = self.param * noise_norm
        unclipped = img + additive_noise
        x_noisey = np.clip(unclipped, 0, 1)
        return x_noisey, additive_noise


class Gaussian_noise(_base_noise):
    '''Add Gaussian noise to image. Image is clipped to the range (0, 1)

    Args:
        image (np.array): image to have Gaussian noise added
        std (float): Standard deviation of the Gaussian noise.
                         (Defaults to 0)

    Returns:
        image (np.array): adjusted image
    '''
    def _setup_args(self, std=0, seed=True):
        self.param = std
        self.seed = seed

    def _make_noisey_image(self, img):
        if self.param <= 0:
            return img, 0.0
        if self.seed:
            np.random.seed(42)
        additive_noise = np.random.normal(
            loc=0, scale=self.param, size=img.shape)
        unclipped = img + additive_noise
        x_noisey = np.clip(unclipped, 0, 1)
        return x_noisey, additive_noise
    

def salt_and_pepper_noise(image, prob=0):
    '''
    Add salt and pepper noise to image

    Args: 
        image (np.array): image to be compressed
        prob: Probability of the noise (Defaults to 0).

    Returns:
        image (np.array): image with salt and pepper noise
    '''
    if prob == 0:
        return image
    min_val = 0
    max_val = 1
    image = image.copy()
    if len(image.shape) == 2:
        black = min_val
        white = max_val
    else:
        colorspace = image.shape[2]
        if colorspace == 3:  # RGB
            black = np.array([min_val, min_val, min_val], dtype='float')
            white = np.array([max_val, max_val, max_val], dtype='float')
        else:  # RGBA
            black = np.array(
                [min_val, min_val, min_val, max_val], dtype='float')
            white = np.array(
                [max_val, max_val, max_val, max_val], dtype='float')
    probs = np.random.random(image.shape[:2])
    image[probs < (prob / 2)] = black
    image[probs > 1 - (prob / 2)] = white
    return np.clip(image, 0, 1)


if __name__ == '__main__':
    import numpy as np
    image = np.random.rand(256, 256, 3)
    noise = Gaussian_noise()
    noise(image, 0)
    # noise(image, 0.1)
