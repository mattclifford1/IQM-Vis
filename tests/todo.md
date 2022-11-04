make API a new format

-> change rows to be independent (can have different metrics per row)
-> better handling of image data
-> better construction of widgets/layout


========
make class that has specific calls:
  - how to load an image   -> np array
  - .get_metrics           -> dict of values
  - .get_metric_images     -> dict of np images
  - (maybe put on the UI class) how to display images (e.g. what colour space)

 - start off by making a generic class constructor for this
 - get UI class to make UI items based on what the image data class returns

 ****** have got to changing the widget storing method *********
====

later
-> pass a generator to loop over the dataset
  - need to have __len__ and __call__ properties
-> can link image labels from dataset into metrics
-> show next arrows when generator used
