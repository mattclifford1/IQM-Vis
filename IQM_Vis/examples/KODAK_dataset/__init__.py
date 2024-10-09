import os
import glob

dir = os.path.dirname(os.path.abspath(__file__))

KODAK_IMAGES = glob.glob(os.path.join(dir, '*'))
# remove and folders
KODAK_IMAGES = [f for f in KODAK_IMAGES if os.path.isfile(f)]
KODAK_IMAGES.sort()
