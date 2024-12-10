.. _api_encoders:

Pixel Data Encoders (:mod:`pydicom3.pixels.encoders`)
====================================================

.. module:: pydicom3.pixels.encoders

:class:`~pydicom3.pixels.encoders.base.Encoder` class instances for compressing
(7FE0,0010) *Pixel Data*.

.. currentmodule:: pydicom3.pixels.encoders

.. autosummary::
   :toctree: generated/

   JPEGLSLosslessEncoder
   JPEGLSNearLosslessEncoder
   JPEG2000LosslessEncoder
   JPEG2000Encoder
   RLELosslessEncoder


Base encoder classes used by all encoders

.. currentmodule:: pydicom3.pixels.encoders.base

.. autosummary::
   :toctree: generated/

   Encoder
   EncodeRunner
