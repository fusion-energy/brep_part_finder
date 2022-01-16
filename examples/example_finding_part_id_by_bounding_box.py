import brep_part_finder as bpf
import paramak
import json

my_reactor = paramak.BallReactor()
# known details (volume, center, bounding box when CAD is created)
# printed using json dumps to make it more human readable
print(json.dumps(my_reactor.part_properties, indent=4))

# order of parts gets mixed when saved to brep file
my_reactor.export_brep('my_reactor.brep')

# brep file is imported
my_reactor_brep_shapes = bpf.import_brep('my_reactor.brep')

# from the printed json dictionary we know that there is are two parts with a
# volume 95467959.26023674 which is the blanket_rear_wall component
part_id = bpf.get_part_id(
    shape_object = my_reactor_brep_shapes,
    bounding_box = [
            [
                -250.0000001,
                -250.0000001,
                -460.9997405464822
            ],
            [
                250.0000001,
                250.00000010000002,
                -311.13245981234695
            ]
        ],
    bounding_box_atol=1e-6,
)

# prints the part id found
print(f' there is {len(part_id)} with a matching volume')
print(f' the part id with a matching volume is {part_id}')
