import warnings
from typing import Tuple

import numpy as np
from cadquery import *
from cadquery.occ_impl.shapes import Shape


def import_brep(filename: str):
    """Imports a Brep CAD file and returns the contents as a CadQuery Shape
    object

    Args:
        filename: the filename of the brep file
    """

    my_brep = Shape.importBrep(filename)
    return my_brep


def get_part_id(
    shape_object,
    volume: float = None,
    center: Tuple[float, float, float] = None,
    bounding_box: Tuple[Tuple[float, float, float], Tuple[float, float, float]] = None,
    faces: int = None,
    volume_atol: float = 1e-8,
    center_atol: float = 1e-6,
    bounding_box_atol: float = 1e-8,
):

    volume_ids_matching = {}

    if center:
        volume_ids_matching_centers = []
        for counter, part in enumerate(shape_object.Solids(), 1):
            if (
                np.isclose(part.Center().x, center[0], atol=center_atol)
                and np.isclose(part.Center().y, center[1], atol=center_atol)
                and np.isclose(part.Center().z, center[2], atol=center_atol)
            ):
                volume_ids_matching_centers.append(counter)
        if len(volume_ids_matching_centers) == 0:
            warnings.warn(
                "No parts matching the specified center +/- tolerances were found"
            )
        else:
            volume_ids_matching["center"] = volume_ids_matching_centers

    if volume:
        volume_ids_matching_volume = []
        for counter, part in enumerate(shape_object.Solids(), 1):
            if np.isclose(part.Volume(), volume, atol=volume_atol):
                volume_ids_matching_volume.append(counter)
        if len(volume_ids_matching_volume) == 0:
            warnings.warn(
                "No parts matching the specified volume +/- tolerances were found"
            )
        else:
            volume_ids_matching["volume"] = volume_ids_matching_volume

    if faces:
        volume_ids_matching_faces = []
        for counter, part in enumerate(shape_object.Solids(), 1):
            if faces == len(part.Faces()):
                volume_ids_matching_faces.append(counter)
        if len(volume_ids_matching_faces) == 0:
            warnings.warn("No parts matching the specified number of faces were found")
        else:
            volume_ids_matching["faces"] = volume_ids_matching_faces

    if bounding_box:
        volume_ids_matching_bounding_box = []
        for counter, part in enumerate(shape_object.Solids(), 1):
            part_bb = (
                part.BoundingBox().xmin,
                part.BoundingBox().ymin,
                part.BoundingBox().zmin,
            ), (
                part.BoundingBox().xmax,
                part.BoundingBox().ymax,
                part.BoundingBox().zmax,
            )
            if (
                np.isclose(part_bb[0][0], bounding_box[0][0], atol=bounding_box_atol)
                and np.isclose(
                    part_bb[0][1], bounding_box[0][1], atol=bounding_box_atol
                )
                and np.isclose(
                    part_bb[0][2], bounding_box[0][2], atol=bounding_box_atol
                )
                and np.isclose(
                    part_bb[1][0], bounding_box[1][0], atol=bounding_box_atol
                )
                and np.isclose(
                    part_bb[1][1], bounding_box[1][1], atol=bounding_box_atol
                )
                and np.isclose(
                    part_bb[1][2], bounding_box[1][2], atol=bounding_box_atol
                )
            ):
                # print('match',bounding_box,part_bb)
                # todo check [1] coord
                volume_ids_matching_bounding_box.append(counter)
        if len(volume_ids_matching_bounding_box) == 0:
            warnings.warn("No parts matching the specified bounding boxes were found")
        else:
            volume_ids_matching["bounding_box"] = volume_ids_matching_bounding_box

    # print("volume numbers matching search criteria", volume_ids_matching)

    lists_of_matching_parts_separate = list(volume_ids_matching.values())
    lists_of_matching_parts = list(
        set.intersection(*map(set, lists_of_matching_parts_separate))
    )

    if len(lists_of_matching_parts) == 0:
        warnings.warn("No single part found that matches all criteria")

    return lists_of_matching_parts


def get_part_ids(shape_object, shape_properties: dict):
    key_and_part_id = []
    for key, value in shape_properties.items():
        matching_part_id = get_part_id(shape_object=shape_object, **value)
        # print(key, matching_part_id)
        key_and_part_id.append((key, matching_part_id))
    return key_and_part_id


def get_dict_of_part_ids(shape_object, shape_properties: dict):
    key_and_part_id = {}
    for key, value in shape_properties.items():
        matching_part_id = get_part_id(shape_object=shape_object, **value)
        if len(matching_part_id) > 1:
            raise ValueError(f"multiple matching volumes were found for {key}")
        # print(key, matching_part_id)
        key_and_part_id[matching_part_id[0]] = key
    return key_and_part_id
