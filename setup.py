# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
from setuptools import setup, find_packages


def get_long_description():
    with open('README.md', encoding="utf-8") as f:
        text = f.read()
    return text

def get_version():
    with open('VERSION') as f:
        ver = f.read()
    while ver[-1] == '\n':
        ver = ver[:-1]
    return ver

setup(name='IQM-Vis',
      version=get_version(),
      packages=find_packages(),
      include_package_data=True,
      install_requires=['numpy',
                        'opencv-python',
                        'scikit-image',
                        'PyQt6',
                        'matplotlib',
                        'torch',
                        'torchmetrics'],
      author="Matt Clifford",
      author_email="matt.clifford@bristol.ac.uk",
      description="Extendable user interface for the assessment of transformations on image metrics.",
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      )
