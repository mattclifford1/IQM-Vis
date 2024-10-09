IQMs
++++

What is an IQM?
===============
Image quality metrics (IQMs) serve as an objective evaluation of the quality of an image and attempt to capture how humans perceive differences between images. Reference IQMs compare a reference image, and the same image with a distortion applied to it. 
The goal is to recreate how humans perceive this difference according to human psychophysical experiments. 

They are utilised in scenarios such as loss functions for deep learning models and benchmarking the performance of image processing algorithms where human evaluation is too expensive to obtain. 


Different types of IQMs
=======================
There are a plethora of IQMs to choose from, the simplest being a metric in Euclidean space such as the mean squared error. In traditional perceptual literature, IQMs can be categorised into two groups. 
The first group consists of metrics, like the structural similarity (SSIM) index, which operate on the premise that the image's structure remains unchanged despite the presence of distortion. 
These metrics adhere to the principle of structural similarity. The second group aims to measure how the visibility of error i.e. how much distortion is visible to humans. Recent literature utilises deep learning models in an attempt to mimic human perception by correlating the model’s response with image quality ratings from human experiments.


How to Choose an IQM For Your Task?
===================================
The process of evaluating IQMs is both qualitative and quantitative. It is necessary to gather empirical data on the response profiles of different IQMs with respect to  specific image distortions and parameter ranges. 
It is also important for a human to oversee the images produced from the distortion process to give context to the image data. 
The practitioner may also require specific behaviour from an IQM, which is not observable in just measuring correlation between human ratings and distances given by the IQM. 
For example, invariances are often extremely important. This type of evaluation and experimentation lends itself best to interactive and graphical software, which is why we have created IQM-Vis!