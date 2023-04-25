Getting Started
+++++++++++++++

Installation
============
It is first recommended to create a new python virtual environment, for examaple
using conda:

..  code-block:: bash

    conda create -n IQM_Vis python=3.9 -y
    conda activate IQM_Vis

Then install IQM-Vis from the PyPi index:

..  code-block:: bash

    pip install IQM-Vis


Testing the installation
========================
Run a demonstration example by running the python code:

..  code-block:: python

    import IQM_Vis
    IQM_Vis.examples.dataset.run()


Common Issues
=============
There are some know issues with some work arounds.

If you are getting the error 

..  code-block:: bash
    
    "Could not load the Qt platform plugin"

This is often to do with mismatched PyQt versions linked to different packages. First make sure you are using the latest version of IQM-Vis. This may require you to create a new python virtual environment from scratch and reinstall IQM-Vis.

then try first to uninstall opencv and change for opencv headless.

..  code-block:: bash
    
    pip uninstall opencv-python
    pip install opencv-python-headless

you can also try to install the extra libraries if you are using linux e.g.:

..  code-block:: bash

    sudo apt install libxcb-cursor0 

