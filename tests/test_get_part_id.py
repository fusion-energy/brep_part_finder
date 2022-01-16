
import unittest
import brep_part_finder as bpf
import paramak


class TestShape(unittest.TestCase):
    def setUp(self):

        
        my_reactor = paramak.BallReactor()
        my_reactor.export_brep('my_reactor.brep')
        self.my_reactor_brep_shapes = bpf.get_brep_part_properties('my_reactor.brep')

    def test_finding_part_id_with_volume(self):
        """"""

        part_id = bpf.get_part_id(
            # brep_part_properties = my_reactor_brep_shapes,
            brep_part_properties = self.my_reactor_brep_shapes,
            volume=95467959.26023674,
            volume_atol=1e-6,
        )

        assert part_id == [6]

    def test_finding_part_id_with_center(self):
        """"""

        part_id = bpf.get_part_id(
            # brep_part_properties = my_reactor_brep_shapes,
            brep_part_properties = self.my_reactor_brep_shapes,
            center=(-0.006133773543690803, 7.867805031206607e-10, 7.70315160988196e-12),
            center_atol=1e-6,
        )

        assert part_id == [6]

    def test_finding_part_id_with_bounding_box(self):
        """"""

        part_id = bpf.get_part_id(
            # brep_part_properties = my_reactor_brep_shapes,
            brep_part_properties = self.my_reactor_brep_shapes,
            bounding_box=[[-570.5554844464615, -570.5554844464615, -453.27123145033755], [570.5554844464615, 570.5554844464615, 453.27123145033755]],
            bounding_box_atol=1e-6,
        )

        assert part_id == [6]


if __name__ == "__main__":
    unittest.main()
