import brep_part_finder as bpf
import paramak


my_reactor = paramak.BallReactor()
my_reactor.export_brep('my_reactor.brep')
print(my_reactor.volume())

my_reactor_brep_shapes = bpf.import_brep('my_reactor.brep')

part_id = bpf.find_part(
    shape_object = my_reactor_brep_shapes,
    volume=220932912,
    volume_atol=1e-6,
    faces=10
)

print(part_id)
