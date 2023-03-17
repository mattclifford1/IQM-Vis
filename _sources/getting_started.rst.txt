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
    IQM_Vis.examples.all.run()
