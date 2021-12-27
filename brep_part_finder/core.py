from cadquery import *
from cadquery.occ_impl.shapes import Shape

def import_brep(filename):
    my_brep = Shape.importBrep(filename)
    return my_brep

def find_part(shape_object, volume=None):
    for part in shape_object.Solids():
        print('volume', part.Volume())
        # print('CenterOfBoundBox', part.CenterOfBoundBox)
        # print('faces', len(part.Faces()))
        # print('area', len(part.Area()))
