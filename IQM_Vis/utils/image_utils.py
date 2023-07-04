'''
image helper functions
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
import os
import PIL
import cv2
import numpy as np
from skimage.transform import resize
from skimage.color import rgb2lab, lab2rgb
from skimage.util import img_as_ubyte

def get_transform_image(data_store, transform_functions, transform_params):
    '''transform image with image post processing

    Args:
        data_store: IQM_Vis data_api
        transform_functions: dict holding transforms
                               (each key is the name of transform, items have key 'function')
        transform_params:  dict holding the parameters for transforms (corresponding to keys in transform_functions)

    Return:
        image: processed numpy image
    '''
    image = data_store.get_image_to_transform()
    for key in transform_functions:
        image = transform_functions[key]['function'](image, transform_params[key])
    if hasattr(data_store, 'image_post_processing'):
        if data_store.image_post_processing is not None:
            image = data_store.image_post_processing(image)
    return image

def load_image(image_path):
    '''
    load image as RGB float
    '''
    if not os.path.isfile(image_path):
        raise ValueError(f'Image file: {image_path} does not exist')
    img = PIL.Image.open(image_path)
    img = np.array(img)
    if img.dtype == 'uint8':
        img = img/255
    if img.shape[2] > 3:
        img = img[:, :, :3]
    return img

def save_image(img, path):
    ''' save image as ubyte '''
    img = PIL.Image.fromarray(img_as_ubyte(img))
    img.save(path)

def resize_to_longest_side(im, side=128):
    '''
    resize image to longest side
    '''
    shape = im.shape
    if shape[0] > shape[1]:
        scale = side/shape[0]
        size = (side, int(shape[1]*scale))
    else:
        scale = side/shape[1]
        size = (int(shape[0]*scale), side)
    im = resize_image(im, size)
    return im

def resize_image(img, size=128):
    '''
    resize image to square or specified size
    '''
    if isinstance(size, int):
        size = (size, size)
    img = cv2.resize(img, (size[1], size[0]), interpolation=cv2.INTER_LINEAR)  # cv2 much faster than skimage

    # can change to PIL code below but only works with uint8 images
    # img = PIL.Image.fromarray(img_as_ubyte(img))
    # img = img.resize(size)
    # img = np.array(img)/255

    return img

def crop_centre(image, scale_factor=2, keep_size=True):
    ''' crop to the centre of the image, note this will return a small image size
        so it best used as post processing

    Args:
        image (np.array): image to be cropped
        scale_factor (float): the percentage to zoom in by (for square crop only).
                              0.5  = 2x zoom out
                              1 = normal size
                              2 = 2x zoom in
                              (Defaults to 2 - half the size)
        keep_size (bool): resize image to the original size after cropping (Defaults to True)

    Returns:
        image (np.array): cropeed image
    '''
    original_size = image.shape
    new_size_x = int(original_size[0]/scale_factor)
    new_size_y = int(original_size[1]/scale_factor)
    if scale_factor > 1:
        start_point_x = int((original_size[0] - new_size_x)/2)
        start_point_y = int((original_size[1] - new_size_y)/2)
        image = image[start_point_x:start_point_x+new_size_x,
                      start_point_y:start_point_y+new_size_y,
                      :]
    elif scale_factor < 1:
        new_size = (new_size_x, new_size_y, original_size[2]) if len(original_size) == 3 else (new_size_x, new_size_y)
        start_point_x = int((new_size_x - original_size[0])/2)
        start_point_y = int((new_size_y - original_size[1])/2)
        zoomed_out = np.zeros(new_size, dtype=image.dtype)
        zoomed_out[start_point_x:start_point_x+original_size[0],
                   start_point_y:start_point_y+original_size[1],
                   :] = image
        image = zoomed_out
    
    if keep_size == True:
        image = resize_image(image, (original_size[0], original_size[1]))

    return image

def calibrate_brightness(im, rgb_brightness, display_brightness, ubyte=True):
    if rgb_brightness == display_brightness:
        return im
    if ubyte == True:
        im = im/255
    im_lab = rgb2lab(im)
    scale = rgb_brightness/display_brightness
    scaled_brightness = im_lab[:, :, 0]*scale
    clipped = np.clip(scaled_brightness, 0, 100)
    im_lab[:, :, 0] = clipped
    rgb = lab2rgb(im_lab)
    if ubyte == True:
        rgb = img_as_ubyte(rgb)
    return rgb
