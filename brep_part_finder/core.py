from turtle import shape
import warnings
from collections.abc import Iterable
from typing import Tuple, Union
from os import PathLike
import numpy as np
from cadquery import *
from cadquery.occ_impl.shapes import Shape
import cadquery as cq


def get_part_properties_from_shape(shape: Shape) -> dict:
    """Accepts a cadquery solid object and returns the unique
    identify details of the solid

    Args:
        filename: the filename of the brep file
    """

    part_details = {}
    part_details["center_x"] = shape.Center().x
    part_details["center_y"] = shape.Center().y
    part_details["center_z"] = shape.Center().z

    part_details["volume"] = shape.Volume()

    part_details["bounding_box_xmin"] = shape.BoundingBox().xmin
    part_details["bounding_box_ymin"] = shape.BoundingBox().ymin
    part_details["bounding_box_zmin"] = shape.BoundingBox().zmin
    part_details["bounding_box_xmax"] = shape.BoundingBox().xmax
    part_details["bounding_box_ymax"] = shape.BoundingBox().ymax
    part_details["bounding_box_zmax"] = shape.BoundingBox().zmax

    return part_details


def convert_shape_to_iterable_of_shapes(shapes):

    if isinstance(shapes, cq.occ_impl.shapes.Compound):
        # brep route
        iterable_solids = shapes.Solids()
    elif isinstance(shapes, cq.Workplane):
        # workplane route
        iterable_solids = shapes.val().Solids()
    else:
        iterable_solids = shapes.Solids()

    return iterable_solids


def get_part_properties_from_shapes(shapes: Iterable) -> dict:
    """Accepts a cadquery.occ_impl.shapes object and returns the unique
    identify details of each Solid

    Args:
        filename: the filename of the brep file
    """

    if not isinstance(shapes, Iterable):
        iterable_of_shapes = convert_shape_to_iterable_of_shapes(shapes)
    else:
        iterable_of_shapes = shapes

    all_part_details = {}
    for counter, part in enumerate(iterable_of_shapes, 1):
        part_details = get_part_properties_from_shape(part)
        all_part_details[counter] = part_details

    return all_part_details


def get_part_properties_from_file(filename: Union[str, PathLike]):
    """Imports a Brep CAD file and returns the unique identify details of each Solid

    Args:
        filename: the filename of the brep file
    """

    shapes = Shape.importBrep(filename)

    my_brep_part_details = get_part_properties_from_shapes(shapes)

    return my_brep_part_details


def get_part_id(
    brep_part_properties: dict,
    center_x: float = None,
    center_y: float = None,
    center_z: float = None,
    volume: float = None,
    bounding_box_xmin: float = None,
    bounding_box_ymin: float = None,
    bounding_box_zmin: float = None,
    bounding_box_xmax: float = None,
    bounding_box_ymax: float = None,
    bounding_box_zmax: float = None,
    volume_atol: float = 1e-6,
    center_atol: float = 1e-6,
    bounding_box_atol: float = 1e-6,
):
    """Finds the key within a dictionary of parts that matches the user
    specified arguments for volume, center, bounding_box within the provided
    tolerances

    Arguments:
        brep_part_properties: a dictionary with the part id number as the key
            and a dictionary of values for the part properties. For example
            {1: {'Center.x':0, 'Center.y':0, 'Center.z':0, 'Volume':10, ....}}
        volume: the volume of the part to find.
        center: a tuple of x,y,z coordinates
        bounding_box: a tuple of two coordinates where the coordinates are the
            lower left and upper right corners of the bounding box.
        volume_atol: absolute tolerance acceptable on the volume comparision
        center_atol: absolute tolerance acceptable on the center comparision
        bounding_box_atol: absolute tolerance acceptable on the bounding box comparision
    """

    part_ids_matching = {}

    properties = [center_x, center_y, center_z, volume, bounding_box_xmin, bounding_box_ymin, bounding_box_zmin, bounding_box_xmax, bounding_box_ymax, bounding_box_zmax]
    properties_names = ["center_x", "center_y", "center_z", "volume", "bounding_box_xmin", "bounding_box_ymin", "bounding_box_zmin", "bounding_box_xmax", "bounding_box_ymax", "bounding_box_zmax"]
    tolerances = [center_atol, center_atol, center_atol, volume_atol, bounding_box_atol, bounding_box_atol, bounding_box_atol, bounding_box_atol, bounding_box_atol, bounding_box_atol]
    
    for property, names, tolerance in zip(properties, properties_names, tolerances):
        if property is not None:
            part_ids_matching_property = []
            for key, value in brep_part_properties.items():
                if np.isclose(value[names], property, atol=tolerance):
                    part_ids_matching_property.append(key)
            if len(part_ids_matching_property) == 0:
                warnings.warn(
                    f"No parts matching the specified {names} +/- tolerances were found"
                )
            else:
                part_ids_matching[names] = part_ids_matching_property

    lists_of_matching_parts_separate = list(part_ids_matching.values())

    if lists_of_matching_parts_separate == []:
        warnings.warn("No single part found that matches all criteria")
        print("search criteria are:")
        print(" volume", volume)
        print(" center_x", center_x)
        print(" center_y", center_y)
        print(" center_z", center_z)
        print(" bounding_box_xmin", bounding_box_xmin)
        print(" bounding_box_ymin", bounding_box_ymin)
        print(" bounding_box_zmin", bounding_box_zmin)
        print(" bounding_box_xmax", bounding_box_xmax)
        print(" bounding_box_ymax", bounding_box_ymax)
        print(" bounding_box_zmax", bounding_box_zmax)
        print(' with tolerances')
        print("  volume_atol", volume_atol)
        print("  center_atol", center_atol)
        print("  bounding_box_atol", bounding_box_atol)
        raise ValueError('No matching part found')

    lists_of_matching_parts = list(
        set.intersection(*map(set, lists_of_matching_parts_separate))
    )

    if len(lists_of_matching_parts) == 0:
        warnings.warn("No single part found that matches all criteria")

    return lists_of_matching_parts


def get_part_ids(
    brep_part_properties,
    shape_properties: list,
    volume_atol: float = 1e-6,
    center_atol: float = 1e-6,
    bounding_box_atol: float = 1e-6,
):
    key_and_part_id = []
    for entry in shape_properties:
        key = entry[0]
        value = entry[1]
        matching_part_id = get_part_id(
            brep_part_properties=brep_part_properties,
            volume_atol=volume_atol,
            center_atol=center_atol,
            bounding_box_atol=bounding_box_atol,
            **value,
        )
        key_and_part_id.append((key, matching_part_id))
    return key_and_part_id


def get_dict_of_part_ids(
    brep_part_properties: dict,
    shape_properties: dict,
    volume_atol: float = 1e-6,
    center_atol: float = 1e-6,
    bounding_box_atol: float = 1e-6,
):
    """finds the brep id that matches the shape ids and returns a linking"""
    key_and_part_id = {}

    for key, value in shape_properties:

        if isinstance(value, dict):
            # check if value is a list of dictionaries or a dictionary
            matching_part_id = get_part_id(
                brep_part_properties=brep_part_properties,
                volume_atol=volume_atol,
                center_atol=center_atol,
                bounding_box_atol=bounding_box_atol,
                **value,
            )
            if len(matching_part_id) > 1:
                raise ValueError(f"multiple matching volumes were found for {key}")
            # todo check that key is not already in use
            key_and_part_id[matching_part_id[0]] = key

        else:
            msg = "shape_properties must be a dictionary of dictionaries"
            raise ValueError(msg)
    return key_and_part_id
