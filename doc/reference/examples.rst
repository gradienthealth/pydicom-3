.. _api_examples:

Example Datasets (:mod:`pydicom3.examples`)
==========================================

.. module:: pydicom3.examples
.. currentmodule:: pydicom3.examples

The ``examples`` module contains the following DICOM datasets:

+-------------------+---------------------------------------+----------------------+
| Module Attribute  | File                                  | SOP Class            |
+===================+=======================================+======================+
| ``ct``            | ``CT_small.dcm``                      | CT Image             |
+-------------------+---------------------------------------+----------------------+
| ``mr``            | ``MR_small.dcm``                      | MR Image             |
+-------------------+---------------------------------------+----------------------+
| ``rt_plan``       | ``rtplan.dcm``                        | RT Plan              |
+-------------------+---------------------------------------+----------------------+
| ``rt_dose``       | ``rtdose.dcm``                        | RT Dose              |
+-------------------+---------------------------------------+----------------------+
| ``rt_ss``         | ``rtstruct.dcm``                      | RT Structure Set     |
+-------------------+---------------------------------------+----------------------+
| ``overlay``       | ``examples_overlay.dcm``              | MR Image             |
+-------------------+---------------------------------------+----------------------+
| ``waveform``      | ``waveform_ecg.dcm``                  | 12 Lead ECG          |
+-------------------+---------------------------------------+----------------------+
| ``rgb_color``     | ``examples_rgb_color.dcm``            | US Image             |
+-------------------+---------------------------------------+----------------------+
| ``palette_color`` | ``OBXXXX1A.dcm``                      | US Image             |
+-------------------+---------------------------------------+----------------------+
| ``ybr_color``     | ``examples_ybr_color.dcm``            | US Multi-frame Image |
+-------------------+---------------------------------------+----------------------+
| ``jpeg2k``        | ``examples_jpeg2k.dcm``               | US Image             |
+-------------------+---------------------------------------+----------------------+
| ``dicomdir``      | ``DICOMDIR``                          | Media Storage        |
+-------------------+---------------------------------------+----------------------+


As well as the utility function:

.. autosummary::
   :toctree: generated/

   get_path


Usage
-----

The module attributes are all normal :class:`~pydicom3.dataset.FileDataset`
instances::

  >>> from pydicom3 import examples
  >>> type(examples.ct)
  <class 'pydicom3.dataset.FileDataset'>
  >>> examples.ct.PatientName
  'CompressedSamples^CT1'

Each time the module attribute is accessed a new
:class:`~pydicom3.dataset.FileDataset` instance  of the dataset will be returned::

  >>> examples.ct is examples.ct
  False
  >>> examples.ct == examples.ct
  True

Because of this, best practice is to assign the returned dataset to a local
variable::

   >>> ds = examples.ct

The :func:`~pydicom3.examples.get_path` function can be used to return the path
to an example dataset as a :class:`pathlib.Path` instance::

   >>> examples.get_path("ct")
   PosixPath('/home/user/pydicom/src/pydicom/data/test_files/CT_small.dcm')
