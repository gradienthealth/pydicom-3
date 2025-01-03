# Copyright 2008-2024 pydicom3 authors. See LICENSE file for details.
"""Use pyjpegls <https://github.com/pydicom/pyjpegls> to decompress encoded
*Pixel Data*.

This module is not intended to be used directly.
"""
from typing import cast

from pydicom3 import uid
from pydicom3.pixels.utils import _passes_version_check
from pydicom3.pixels.decoders.base import DecodeRunner

try:
    import jpeg_ls

except ImportError:
    pass


DECODER_DEPENDENCIES = {
    uid.JPEGLSLossless: ("numpy", "pyjpegls>=1.5"),
    uid.JPEGLSNearLossless: ("numpy", "pyjpegls>=1.5"),
}


def is_available(uid: str) -> bool:
    """Return ``True`` if the decoder has its dependencies met, ``False`` otherwise"""
    return _passes_version_check("jpeg_ls", (1, 5))


def _decode_frame(src: bytes, runner: DecodeRunner) -> bytearray:
    """Return the decoded image data in `src` as a :class:`bytearray`."""
    buffer, info = jpeg_ls.decode_pixel_data(src)
    # Interleave mode 0 is colour-by-plane, 1 and 2 are colour-by-pixel
    if info["components"] > 1:
        if info["interleave_mode"] == 0:
            runner.set_option("planar_configuration", 1)
        else:
            runner.set_option("planar_configuration", 0)

    precision = info["bits_per_sample"]
    if 0 < precision <= 8:
        runner.set_option("bits_allocated", 8)
    elif 8 < precision <= 16:
        runner.set_option("bits_allocated", 16)

    return cast(bytearray, buffer)
