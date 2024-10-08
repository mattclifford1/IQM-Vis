'''
Sample image transformations to get the user started with
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

from skimage.transform import resize
from skimage.util import img_as_ubyte
import cv2
import numpy as np


def brightness(image, value=0):
    '''Adjust image brightness. Image is clipped to the range (0, 1)

    Args:
        image (np.array): image to have its brightness adjusted
        value (float): value to adjust all pixels by in the range (-1, 1).
                         (Defaults to 0)

    Returns:
        image (np.array): adjusted image
    '''
    if value == 0:
        return image
    return np.clip(image + value, 0, 1)


def binary_threshold(image, threshold=100):
    '''conver image to binary at a given threshold

    Args:
        image (np.array): image to be thresholded
        threshold (int): threshold value in the range (1, 255)
                     (Defaults to 100)

    Returns:
        image (np.array): thresholded image (float32 in range 0, 1)
    '''
    image = img_as_ubyte(image)
    if len(image.shape) > 2:
        if image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, int(threshold))
    if len(image.shape) == 2:
        image = np.stack((image,)*3, axis=-1)
    return np.clip(image.astype(np.float32) / 255.0, 0, 1)


def jpeg_compression(image, compression=101):
    '''encode image using jpeg then decode

    Args:
        image (np.array): image to be compressed
        compression (int): amount of jpeg compression, higher is better quality. 
                     101 returns identity image.
                     (Defaults to 101)

    Returns:
        image (np.array): jpeg compressed image
    '''
    if compression == 101:
        return image
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), int(compression)]
    encoder = '.jpg'
    return _encode_compression(image, encoder, encode_param)


def _encode_compression(image, encoder, encode_param, uint=True):
    '''
        generic image encoder for jpeg, png etc
        using https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html to encode/decode
        for encode types: https://docs.opencv.org/3.4/d6/d87/imgcodecs_8hpp.html
    '''
    original_size = image.shape
    if uint == True:
        # jpeg/png encoder needs uint images not float
        image = img_as_ubyte(image)
    # encode image
    result, encoded_image = cv2.imencode(encoder, image, encode_param)
    # decode image
    decoded_image = cv2.imdecode(encoded_image, 1)
    if uint == True:
        # return to float type
        image = decoded_image.astype(np.float32) / 255.0
    # have to resize as jpeg can sometimes change the size of an image
    if image.shape != original_size:
        image = resize(image, original_size)
    return np.clip(image, 0, 1)


def contrast(image, contrast=1.0):
    """adjust the contrast of an image

    Args:
        image (np.array): image to have contrast adjusted
        contrast (float): amount of contrast to adjust by. 
            Values less that 1 will decrease contrast, 
            Values higher than 1 will increase the contrast.
            (Defaults to 1.0).

    Returns:
        image (np.array): image with contrast adjusted
    """
    if contrast == 1:
        return image
    image = img_as_ubyte(image)  # convert to 255 max value
    # need to zero center the data so we only adjust for contrast
    brightness = int(round(255*(1-contrast)/2))
    image = cv2.addWeighted(image, contrast, image, 0, brightness)
    return np.clip(image/255, 0, 1)


def hue(image, h=0):
    """adjust the hue of an image

    Args:
        image (np.array): image to have hue adjusted
        h (float): amount of hue to adjust by. 
            (Defaults to 0).

    Returns:
        image (np.array): image with hue adjusted
    """
    return _adjust_HSV(image, h, channel=0)


def saturation(image, sat=0):
    """adjust the saturation of an image

    Args:
        image (np.array): image to have saturation adjusted
        sat (float): amount of saturation to adjust by. 
            (Defaults to 0).

    Returns:
        image (np.array): image with saturation adjusted
    """
    return _adjust_HSV(image, sat, channel=1)


def brightness_hsv(image, b=0):
    """adjust the brightness of an image

    Args:
        image (np.array): image to have brightness adjusted
        b (float): amount of brightness to adjust by. 
            (Defaults to 0).

    Returns:
        image (np.array): image with brightness adjusted
    """
    return _adjust_HSV(image, b, channel=2)


def _adjust_HSV(image, value, channel):
    '''
    adjust hue, saturation or brightness of an image,
    image is float between 0, 1 and value is between -1 and 1
    channels:
        0 = hue
        1 = saturation
        2 = brightness
    '''
    if value == 0:
        return image
    image = img_as_ubyte(image)
    # convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # normalise between 0, 1
    hsv = hsv.astype(np.float32)
    hsv[:, :, 0] = hsv[:, :, 0]/179
    hsv[:, :, 1:] = hsv[:, :, 1:]/255
    # add the adjustment to the required channel
    hsv[:, :, channel] += value
    # account for hue colours being radial
    if channel == 0:
        hsv[:, :, channel] = np.mod(
            hsv[:, :, channel], 1)
    # reset to 0, 1 bounds
    hsv = np.clip(hsv, 0, 1)
    # convert back to RGB
    hsv[:, :, 0] = hsv[:, :, 0]*179
    hsv[:, :, 1:] = hsv[:, :, 1:]*255
    hsv = hsv.astype(np.uint8)
    return np.clip(cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)/255, 0, 1)


def blur(image, kernel_size=1):
    '''Gaussian Blur on an image

    Args:
        image (np.array): image to be rotated
        kernel_size (int): size of the convolutional kernel, will be converted
                           to an odd number. 1 is no blur.
                           (Defaults to 1)

    Returns:
        image (np.array): rotated image
    '''
    if kernel_size == 1:
        return image
    elif kernel_size > 0:
        blur_odd = (int(kernel_size/2)*2) + 1    # need to make kernel size odd
        image = cv2.GaussianBlur(
            image, (blur_odd, blur_odd), cv2.BORDER_DEFAULT)
        if len(image.shape) == 2:
            image = np.expand_dims(image, axis=2)
    return np.clip(image, 0, 1)
