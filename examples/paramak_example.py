import brep_part_finder as bpf
import paramak
import json

my_reactor = paramak.BallReactor()
# known details (volume, center, bounding box when CAD is created)
# printed using json dumps to make it more human readable
print(json.dumps(my_reactor.part_properties, indent=4))

# order of parts gets mixed when saved to brep file
my_reactor.export_brep("my_reactor.brep")

# brep file is imported
my_brep_part_properties = bpf.get_brep_part_properties("my_reactor.brep")

# request to find part ids that are mixed up in the Brep file
# using the volume, center, bounding box that we know about when creating the
# CAD geometry in the first place
key_and_part_id = bpf.get_dict_of_part_ids(
    brep_part_properties=my_brep_part_properties,
    shape_properties=my_reactor.part_properties,
)

print(key_and_part_id)
