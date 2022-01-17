import brep_part_finder as bpf


# brep file is imported
my_brep_part_properties = bpf.get_brep_part_properties('ball_reactor.brep')

# from the printed json dictionary we know that there is are two parts with a
# volume 95467959.26023674 which is the blanket_rear_wall component
part_id = bpf.get_part_id(
    brep_part_properties = my_brep_part_properties,
    volume=95467959.26023674,
    volume_atol=1e-6,
)

# prints the part id found
print(f' there is {len(part_id)} with a matching volume')
print(f' the part id with a matching volume is {part_id}')
