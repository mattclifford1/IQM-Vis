Getting Started
+++++++++++++++

Installation
============
It is important to run IQM-Vis in a fresh python virtual environment. This is so that there will be no dependancy clashes with the required libraries. Python version 3.9 is recommended, but newer versions should work as well.

You can make a new environment by using anaconda (conda):

..  code-block:: bash

    conda create -n IQM_Vis python=3.9 -y
    conda activate IQM_Vis

If you have a GPU and would like to use CUDA then at this point head over to the pytorch website and download the relevent packages e.g.

If you don't have a GPU then you can skip this step.

..  code-block:: bash

    conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia

Now we can install IQM-Vis from the PyPi index:

..  code-block:: bash

    pip install IQM-Vis


Testing the installation
========================
Run a demonstration example by running the python code:

..  code-block:: python

    import IQM_Vis
    IQM_Vis.make_UI()


Common Issues
=============
There are some know issues with some work arounds.

There are some dependancy conflicts with python 3.11, we recommend 3.9 or 3.10.

.. If you having any issues, please use python 3.9 and install the pinned dependancies found `here <https://github.com/mattclifford1/IQM-Vis/blob/main/requirements-pinned.txt>`_.

If you are using Ubuntu and getting the error 

..  code-block:: bash
    
    "Could not load the Qt platform plugin"

Then you will be missing some libraries which you can install with:

..  code-block:: bash

    sudo apt install libxcb-cursor0 

If this does not solve the problem then first make sure you are using the latest version of IQM-Vis. It is best to create a new python virtual environment from scratch and reinstall IQM-Vis.

.. then try first to uninstall opencv and change for opencv headless.

.. ..  code-block:: bash
    
..     pip uninstall opencv-python
..     pip install opencv-python-headless
  

