.. _viewing_images:

Viewing Images
==============

.. rubric:: How to use other packages with pydicom3 to view DICOM images

Introduction
------------

*pydicom* is mainly concerned with getting at the DICOM data elements in files,
but it is often desirable to view pixel data as an image.
There are several options:

* Use any of the many `DICOM viewer
  <http://www.dclunie.com/medical-image-faq/html/part8.html#DICOMFileConvertorsAndViewers>`_
  programs available
* use pydicom3 with `matplotlib <https://matplotlib.org/>`_
* use pydicom3 with Python's stdlib `Tkinter <https://docs.python.org/3.4/library/tkinter.html>`_ module.
* use pydicom3 with `Pillow <https://python-pillow.org/>`_
* use pydicom3 with `wxPython <https://www.wxpython.org/>`_

Using pydicom3 with matplotlib
-----------------------------

`matplotlib <https://matplotlib.org/>`_ can be used with the :class:`numpy.ndarray` from
:attr:`Dataset.pixel_array<pydicom3.dataset.Dataset.pixel_array>` to display it::

  >>> import matplotlib.pyplot as plt
  >>> from pydicom3 import examples
  >>> ds = examples.ct
  >>> plt.imshow(ds.pixel_array, cmap=plt.cm.gray) # doctest: +ELLIPSIS
  <matplotlib.image.AxesImage object at ...>

.. image:: ./../../auto_examples/input_output/images/sphx_glr_plot_read_dicom_001.png
   :target: ./../../auto_examples/input_output/plot_printing_dataset.html
   :scale: 60
   :align: center
