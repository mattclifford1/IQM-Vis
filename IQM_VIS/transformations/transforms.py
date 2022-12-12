'''
Sample image transformations to get the user started with
'''
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from skimage.transform import resize, rotate
from skimage.util import img_as_ubyte
import cv2
import numpy as np


def rotation(image, param):
    return rotate(image, param)

def blur(image, param):
    if param == 1:
        return image
    elif param > 0:
        blur_odd = (int(param/2)*2) + 1    # need to make kernel size odd
        image = cv2.GaussianBlur(image,(blur_odd, blur_odd), cv2.BORDER_DEFAULT)
        if len(image.shape) == 2:
            image = np.expand_dims(image, axis=2)
    return image

def zoom(image, param):
    return zoom_image(image, param)

def x_shift(image, param):
    return translate_image(image, param, 0)

def y_shift(image, param):
    return translate_image(image, 0, param)

def brightness(image, param):
    return np.clip(image + param, 0, 1)

def translate_image(image, x_shift, y_shift):
    ''' x and y shift in range (-1, 1)'''
    if x_shift == 0 and y_shift == 0:
        return image
    original_size = image.shape
    canvas = np.zeros(original_size, dtype=image.dtype)
    prop_x = int(original_size[1]*abs(x_shift))
    prop_y = int(original_size[0]*abs(y_shift))
    if y_shift >= 0 and x_shift >= 0:
        canvas[prop_y:,prop_x:,:] = image[:original_size[0]-prop_y,:original_size[1]-prop_x,:]
    elif y_shift < 0 and x_shift >= 0:
        canvas[:original_size[0]-prop_y,prop_x:,:] = image[prop_y-original_size[0]:,:original_size[1]-prop_x,:]
    elif y_shift >= 0 and x_shift < 0:
        canvas[prop_y:,:original_size[1]-prop_x,:] = image[:original_size[0]-prop_y,prop_x-original_size[1]:,:]
    elif y_shift < 0 and x_shift < 0:
        canvas[:original_size[0]-prop_y:,:original_size[1]-prop_x,:] = image[prop_y-original_size[0]:,prop_x-original_size[1]:,:]
    return canvas

def zoom_image(image, factor):
    ''' digital zoom of image: scale_factor the % to zoom in by (for square zoom only)
        0.5  = 2x zoom out
        1 = normal size
        2 = 2x zoom in'''
    original_size = image.shape
    new_size_x = int(original_size[0]/factor)
    new_size_y = int(original_size[1]/factor)
    if factor > 1:
        start_point_x = int((original_size[0] - new_size_x)/2)
        start_point_y = int((original_size[1] - new_size_y)/2)
        image = image[start_point_x:start_point_x+new_size_x,
                      start_point_y:start_point_y+new_size_y,
                      :]
    elif factor < 1:
        new_size = (new_size_x, new_size_y, original_size[2]) if len(original_size) == 3 else (new_size_x, new_size_y)
        start_point_x = int((new_size_x - original_size[0])/2)
        start_point_y = int((new_size_y - original_size[1])/2)
        zoomed_out = np.zeros(new_size, dtype=image.dtype)
        zoomed_out[start_point_x:start_point_x+original_size[0],
                   start_point_y:start_point_y+original_size[1],
                   :] = image
        image = zoomed_out

    return resize(image, original_size)

def binary_threshold(image, param):
    image = img_as_ubyte(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, int(param))
    return image.astype(np.float32) / 255.0

def jpeg_compression(image, param=90):
    '''encode image using jpeg then decode
    - param: amount of compression
              100 returns identity image?
    '''
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), int(param)]
    encoder = '.jpg'
    return _encode_compression(image, encoder, encode_param)

def png_compression(image, param=9):
    '''encode image using png then decode (note png is lossless compression)
    - param: amount of compression
    '''
    encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), int(param)]
    encoder = '.png'
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
    return image
