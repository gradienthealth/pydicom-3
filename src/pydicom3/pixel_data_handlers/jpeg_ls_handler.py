# Copyright 2008-2018 pydicom3 authors. See LICENSE file for details.
"""
Use the `jpeg_ls (pyjpegls) <https://github.com/pydicom/pyjpegls>`_ Python
package to decode *Pixel Data*.
"""
from typing import TYPE_CHECKING, cast

try:
    import numpy

    HAVE_NP = True
except ImportError:
    HAVE_NP = False

try:
    import jpeg_ls

    HAVE_JPEGLS = True
except ImportError:
    HAVE_JPEGLS = False

from pydicom3.encaps import generate_frames
from pydicom3.pixels.utils import pixel_dtype, get_nr_frames
import pydicom3.uid

if TYPE_CHECKING:  # pragma: no cover
    from pydicom3.dataset import Dataset


HANDLER_NAME = "JPEG-LS"

DEPENDENCIES = {
    "numpy": ("https://numpy.org/", "NumPy"),
    "jpeg_ls": ("https://github.com/pydicom/pyjpegls", "pyjpegls"),
}

SUPPORTED_TRANSFER_SYNTAXES = [
    pydicom3.uid.JPEGLSLossless,
    pydicom3.uid.JPEGLSNearLossless,
]


def is_available() -> bool:
    """Return ``True`` if the handler has its dependencies met."""
    return HAVE_NP and HAVE_JPEGLS


def needs_to_convert_to_RGB(ds: "Dataset") -> bool:
    """Return ``True`` if the *Pixel Data* should to be converted from YCbCr to
    RGB.

    This affects JPEG transfer syntaxes.
    """
    return False


def should_change_PhotometricInterpretation_to_RGB(ds: "Dataset") -> bool:
    """Return ``True`` if the *Photometric Interpretation* should be changed
    to RGB.

    This affects JPEG transfer syntaxes.
    """
    return False


def supports_transfer_syntax(transfer_syntax: pydicom3.uid.UID) -> bool:
    """Return ``True`` if the handler supports the `transfer_syntax`.

    Parameters
    ----------
    transfer_syntax : uid.UID
        The Transfer Syntax UID of the *Pixel Data* that is to be used with
        the handler.
    """
    return transfer_syntax in SUPPORTED_TRANSFER_SYNTAXES


def get_pixeldata(ds: "Dataset") -> "numpy.ndarray":
    """Return the *Pixel Data* as a :class:`numpy.ndarray`.

    Returns
    -------
    numpy.ndarray
        A correctly sized (but not shaped) numpy array of the *Pixel Data*.

    Raises
    ------
    ImportError
        If the required packages are not available.
    NotImplementedError
        If the transfer syntax is not supported.
    TypeError
        If the pixel data type is unsupported.
    """
    tsyntax = ds.file_meta.TransferSyntaxUID
    if tsyntax not in SUPPORTED_TRANSFER_SYNTAXES:
        raise NotImplementedError(
            f"The jpeg_ls does not support this transfer syntax {tsyntax.name}"
        )

    if not HAVE_JPEGLS:
        raise ImportError(
            "The jpeg_ls package is required to use pixel_array for this "
            f"transfer syntax {tsyntax.name}, and jpeg_ls could not be "
            "imported"
        )

    pixel_bytes = bytearray()

    nr_frames = get_nr_frames(ds, warn=False)
    for frame in generate_frames(ds.PixelData, number_of_frames=nr_frames):
        im = jpeg_ls.decode(numpy.frombuffer(frame, dtype="u1"))
        pixel_bytes.extend(im.tobytes())

    arr = numpy.frombuffer(pixel_bytes, pixel_dtype(ds))

    if should_change_PhotometricInterpretation_to_RGB(ds):
        ds.PhotometricInterpretation = "RGB"

    return cast("numpy.ndarray", arr)
