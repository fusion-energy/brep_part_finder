from cadquery import *
from cadquery.occ_impl.shapes import Shape
import numpy as np


def import_brep(filename):
    my_brep = Shape.importBrep(filename)
    return my_brep

def find_part(
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
    return lists_of_matching_parts