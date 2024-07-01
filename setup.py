# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

from setuptools import setup, find_packages
import os


def get_version():
    info = {}
    with open(os.path.join('IQM_Vis', 'version.py')) as ver_file:
        exec(ver_file.read(), info)
    return info['__version__']


def get_long_description():
    with open('README.md', encoding="utf-8") as f:
        text = f.read()
    return text


def dependencies_from_file(file_path):
    required = []
    with open(file_path) as f:
        for l in f.readlines():
            l_c = l.strip()
            # get not empty lines and ones that do not start with python
            # comment "#" (preceded by any number of white spaces)
            if l_c and not l_c.startswith('#'):
                required.append(l_c)
    return required


setup(name='IQM-Vis',
      version=get_version(),
      packages=find_packages(),
      include_package_data=True,
      install_requires=dependencies_from_file('./requirements.txt'),
      author="Matt Clifford",
      author_email="matt.clifford@bristol.ac.uk",
      description="Extendable user interface for the assessment of transformations on image metrics.",
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      )
