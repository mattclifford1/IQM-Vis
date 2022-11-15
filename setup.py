# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

from setuptools import setup, find_packages
# import IQM_VIS

setup(name='IQM-VIS',
      version='0.2.5.2',
      packages=find_packages(),
      install_requires=['numpy',
                        'opencv-python',
                        'scikit-image',
                        'PyQt6',
                        'matplotlib',
                        'torch',
                        'torchmetrics'],
      author="Matt Clifford",
      author_email="matt.clifford@bristol.ac.uk",
      description="Extendable user interface for the assessment of transformations on image metrics.")
