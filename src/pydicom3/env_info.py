# Copyright 2020 pydicom3 authors. See LICENSE file for details.
"""
Gather system information and version information for pydicom3 and auxiliary
modules.

The output is a GitHub-flavoured markdown table whose contents can help
diagnose any perceived bugs in pydicom3. This can be pasted directly into a new
GitHub bug report.

This file is intended to be run as an executable module.
"""

import importlib
import platform
import sys
from types import ModuleType
from typing import cast


def main() -> None:
    version_rows = [("platform", platform.platform()), ("Python", sys.version)]

    modules = (
        "pydicom3",
        "gdcm",
        "jpeg_ls",
        "numpy",
        "PIL",
        "pylibjpeg",
        "openjpeg",
        "libjpeg",
    )
    for module in modules:
        try:
            m = importlib.import_module(module)
        except ImportError:
            version = "_module not found_"
        else:
            version = extract_version(m) or "**cannot determine version**"

        version_rows.append((module, version))

    print_table(version_rows)


def print_table(version_rows: list[tuple[str, str]]) -> None:
    row_format = "{:12} | {}"
    print(row_format.format("module", "version"))
    print(row_format.format("------", "-------"))
    for module, version in version_rows:
        # Some version strings have multiple lines and need to be squashed
        print(row_format.format(module, version.replace("\n", " ")))


def extract_version(module: ModuleType) -> str | None:
    if module.__name__ == "gdcm":
        return cast(str | None, getattr(module, "GDCM_VERSION", None))

    return cast(str | None, getattr(module, "__version__", None))


if __name__ == "__main__":
    main()
