# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from setuptools import setup, find_packages


def get_long_description():
    with open('README.md', encoding="utf-8") as f:
        text = f.read()
    return text


setup(name='IQM-VIS',
      version='0.2.5.25',
      packages=find_packages(),
      install_requires=['numpy',
                        'opencv-python',
                        'scikit-image',
                        'PyQt6',
                        'matplotlib',
                        'torch',
                        'torchmetrics'],
      # data_files=[('/', ['IQM_VIS/UI/style.css'])], # include non .py files needed
      author="Matt Clifford",
      author_email="matt.clifford@bristol.ac.uk",
      description="Extendable user interface for the assessment of transformations on image metrics.",
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      )
