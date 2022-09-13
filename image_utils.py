from skimage.transform import resize, rotate
import cv2
import os
import numpy as np


def load_image(image_path):
    return cv2.imread(image_path)

def load_and_crop_raw_real(image_path):
    image = cv2.imread(image_path)
    # Convert to gray scale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Add channel axis
    image = image[..., np.newaxis]
    # Crop to specified bounding box
    bbox = [80,25,530,475]
    x0, y0, x1, y1 = bbox
    image = image[y0:y1, x0:x1]
    # Resize to specified dims
    image = cv2.resize(image, (128, 128), interpolation=cv2.INTER_AREA)
    # Add channel axis
    image = image[..., np.newaxis]
    return image.astype(np.float32) / 255.0

def process_im(image, data_type='sim'):
    if data_type == 'real':
        image = image*255
        image = image.astype(np.uint8)
        # threshold_image
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, -30)
        image = image[..., np.newaxis]
    elif data_type == 'sim':
        # Convert to gray scale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Add channel axis
        image = image[..., np.newaxis]
    return image.astype(np.float32) / 255.0

def get_real_csv_given_sim(sim_csv):
    ''' try find equivelant real csv given a sim
        only works for standard dir structing
        will return sim_csv if can't find real csv'''
    dirs = sim_csv.split(os.sep)
    dirs[0] = os.sep
    dirs.pop(-3)       # remove 128x128
    dirs[-5] = 'real'  # swap sim for real
    real_csv = os.path.join(*dirs)
    if os.path.isfile(real_csv):
        return real_csv
    else:
        return sim_csv

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



if __name__ == '__main__':
    csv_file_sim = '/home/matt/summer-project/data/Bourne/tactip/sim/edge_2d/shear/128x128/csv_train/targets.csv'
    print(get_real_csv_given_sim(csv_file_sim))

    # dev image transformations
    image_file = '/home/matt/summer-project/data/Bourne/tactip/sim/edge_2d/shear/128x128/csv_train/images/image_6.png'
    image = load_image(image_file)
    params_dict = {'rotation':90, 'zoom_factor':.75, 'x_shift': 0.2, 'y_shift':0.1}
    params_dict = {'x_shift': 0.3, 'y_shift':-0.2}
    image_trans = transform_image(image, params_dict)

    # show images
    images_list = [image, image_trans]
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, len(images_list))
    fig.suptitle('image transformations')
    for i, im in enumerate(images_list):
        axs[i].imshow(im)
    plt.show()
