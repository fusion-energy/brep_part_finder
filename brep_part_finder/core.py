from cadquery import *
from cadquery.occ_impl.shapes import Shape
import numpy as np


def import_brep(filename):
    my_brep = Shape.importBrep(filename)
    return my_brep

def get_part_id(
    shape_object,
    volume=None,
    volume_atol=1e-8,
    faces=None
):

    matching_criteria = 0

    volume_ids_matching = {}
    for counter, part in enumerate(shape_object.Solids(), 1):
        print()
        print(counter)
        print(' volume', part.Volume())
        print(' faces', len(part.Faces()))

    if volume:
        volume_ids_matching_volume = []
        matching_criteria=matching_criteria+1
        for counter, part in enumerate(shape_object.Solids(), 1):
            if np.isclose(part.Volume(), volume, atol=volume_atol):
                print('found matching volumes')
                volume_ids_matching_volume.append(counter)
        if len(volume_ids_matching_volume) == 0:
            print('No parts matching the specified volume +/- tolerances were found') 
        else:
            volume_ids_matching['volume'] = volume_ids_matching_volume

    if faces:
        volume_ids_matching_faces = []
        matching_criteria=matching_criteria+1
        for counter, part in enumerate(shape_object.Solids(), 1):
            if faces == len(part.Faces()):
                print('found matching faces')
                volume_ids_matching_faces.append(counter)
        if len(volume_ids_matching_faces) == 0:
            print('No parts matching the specified number of faces were found') 
        else:
            volume_ids_matching['faces'] = volume_ids_matching_faces

    lists_of_matching_parts_separate = list(volume_ids_matching.values())
    print('lists_of_matching_parts_separate',lists_of_matching_parts_separate)

    lists_of_matching_parts = list(set.intersection(*map(set, lists_of_matching_parts_separate)))

    if len(lists_of_matching_parts) == 0:
        print('No single part found that matches all criteria')
    # if len(lists_of_matching_parts) == 1:
    #     return lists_of_matching_parts[0]
    return lists_of_matching_parts

def get_part_ids(
    shape_object,
    shape_properties: dict
):
    key_and_part_id = []
    for key, value in shape_properties.items():
        mating_part_id = get_part_id(shape_object=shape_object, **value)
        print(key, mating_part_id)
        key_and_part_id.append((key, mating_part_id))
    return key_and_part_id

def get_dict_of_part_ids(
    shape_object,
    shape_properties: dict
):
    key_and_part_id = {}
    for key, value in shape_properties.items():
        mating_part_id = get_part_id(shape_object=shape_object, **value)
        if len(mating_part_id) > 1:
            raise ValueError(f'multiple matching volumes were found for {key}')
        print(key, mating_part_id)
        key_and_part_id[mating_part_id[0]] = key
    return key_and_part_id
