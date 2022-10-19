# Author: Matt Clifford <matt.clifford@bristol.ac.uk>

from setuptools import setup, find_packages
import IQM_VIS

setup(name='IQM-VIS',
      version='0.1',
      packages=find_packages(),
      install_requires=['numpy', 'opencv-python', 'scikit-image', 'PyQt6', 'matplotlib'],
      author="Matt Clifford",
      author_email="matt.clifford@bristol.ac.uk",
      description="Extendable user interface for the assessment of transformations on image metrics.")
