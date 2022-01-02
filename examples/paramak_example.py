import brep_part_finder as bpf
import paramak


my_reactor = paramak.BallReactor()
my_reactor.export_brep('my_reactor.brep')
print(my_reactor.part_properties)

my_reactor_brep_shapes = bpf.import_brep('my_reactor.brep')

# part_id = bpf.get_part_id(
#     shape_object = my_reactor_brep_shapes,
#     volume=220932912,
#     volume_atol=1e-6,
#     faces=1
# )

# print(part_id)


key_and_part_id = bpf.get_dict_of_part_ids(
    shape_object = my_reactor_brep_shapes,
    shape_properties = my_reactor.part_properties
    # {
        # 'blanket':{
        #     'volume':220932912,
        #     'volume_atol':1e-6,
        #     # 'faces':1
        # },
        # 'firstwall':{
        #     'volume':4335397.861953917,
        #     'volume_atol':1e-6,
        #     # 'faces':1
        # },
        # 'rearwall':{
        #     'volume':18686741.13418987,
        #     'volume_atol':1e-6,
        #     # 'faces':1
        # }
    # }
)

print(key_and_part_id)