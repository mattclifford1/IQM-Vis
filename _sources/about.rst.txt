About IQM-Vis
+++++++++++++++

What IQM-Vis Offers
===================
IQM-Vis enables quick access to visualising image distortions and evaluating IQMs through a simple and convenient python graphical interface. It provides many standard distortions and IQMs out of the box. Adding custom distortions, IQMs and image datasets is also straightforward. 
Comparison graphs of IQMs are automatically generated as well as the option to compare with human scores to understand on what particular distortions or images the metric fails. This improves the quality and timescale of the IQM evaluation process. 
IQM-Vis manages the data storage from the experiments and shows the results with correlation plots against desired IQMs. Any image distortions which do not conform to the correlation can be selected for further analysis of the image properties.

Built in functionality
======================
IQM-Vis offers many stanard distortions and IQMs to use out of the box (see the documentation for more details). 
IQM-Vis includes image pre processing features such as image resizing, cropping (for use with translation and rotation transforms). 
It also includes screen calibration capabilites in the form of display size and luminance correction so that the images can be viewed truthfully.


Human Perception Experiments
============================

IQM-Vis has functionality for conducting human perception experiments. This feature enables practitioners to analyse custom distortions and image datasets, which is crucial for real-world design and evaluation of IQMs. IQM-Vis facilitates the management and analysis of the collected data.

Experiment participants provide the ordinal orderings of the perceived quality of an image exposed to specific distortion.
This is achieved by the process of recursively picking the highest quality image out of a pair with respect to an undistorted reference image. The ordering of the images is calculated from an underlying sorting algorithm (quick sort).

See the "Running an Experiment" tutorial for further details on experiments.


Software
========
IQM-Vis is implemented in Python, the graphical user interface (GUI) is developed using PyQt6, the image handling and processing is covered by OpenCV. 
Numpy is used for image distortions and other backend tasks and many of the IQMs provided take advantage of the pytorch framework to enable GPU hardware acceleration
