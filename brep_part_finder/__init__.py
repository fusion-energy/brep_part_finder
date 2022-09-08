try:
    from importlib.metadata import version, PackageNotFoundError
except (ModuleNotFoundError, ImportError):
    from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("brep_part_finder")
except PackageNotFoundError:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)

__all__ = ["__version__"]


from .core import (
    get_brep_part_properties,
    get_brep_part_properties_from_shape,
    get_part_id,
    get_part_ids,
    get_dict_of_part_ids,
)
