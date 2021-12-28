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
    matching_volume_ids = []
    for counter, part in enumerate(shape_object.Solids(), 1):
        print()
        print(counter)
        print(' volume', part.Volume())
        print(' faces', len(part.Faces()))

    for counter, part in enumerate(shape_object.Solids(), 1):
        if volume:
            if np.isclose(part.Volume(), volume, atol=volume_atol):
                print('matching volumes')
                matching_volume_ids.append(counter)

    for counter, part in enumerate(shape_object.Solids(), 1):
        if faces:
            if faces == len(part.Faces()):
                print('matching faces')
                matching_volume_ids.append(counter)
        # print('CenterOfBoundBox', part.CenterOfBoundBox)
        # print('faces', len(part.Faces()))
        # print('area', len(part.Area()))
    return list(set(matching_volume_ids))