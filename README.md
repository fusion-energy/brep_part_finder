

# Installation

```bash
conda create --name cadquery
conda activate cadquery
# requires cadquery version 2.2 or above
conda install -c cadquery -c conda-forge cadquery=master
pip install brep_part_finder
```

# Usage

To view the properties of the parts in the Brep file the first stage is to import the package and make use of the ```get_brep_part_properties``` function.

```
import brep_part_finder as bvf

my_brep_part_properties = bvf.get_brep_part_properties('my_brep_file.brep')

print(my_brep_part_properties)
>>> {
   {1: {'Center.x': 0.7933449634987255, 'Center.y': 1.8474827903995146e-14, 'Center.z': 2.656701907148416e-13, 'Volume': 10, 'BoundingBox.xmin': -430.0005742501733, 'BoundingBox.ymin': -430.0005742501733, 'BoundingBox.zmin': -300.00303966383916, 'BoundingBox.xmax': 430.0005742501733, 'BoundingBox.ymax': 430.0005742501733, 'BoundingBox.zmax': 300.0030396638392}, 2: {'Center.x': 1.825955110995004e-15, 'Center.y': 6.0659368027766e-16, 'Center.z': -8.936439131457902e-14, 'Volume': 10, 'BoundingBox.xmin': -40.0, 'BoundingBox.ymin': -40.0, 'BoundingBox.zmin': -460.0, 'BoundingBox.xmax': 40.0, 'BoundingBox.ymax': 40.0, 'BoundingBox.zmax': 460.0}, 3: {'Center.x': 2.0868058411371474e-14, 'Center.y': 3.4033195329656346e-15, 'Center.z': -9.411932877099948e-14, 'Volume': 10, 'BoundingBox.xmin': -100.0000001, 'BoundingBox.ymin': -100.0000001, 'BoundingBox.zmin': -460.0000001, 'BoundingBox.xmax': 100.0000001, 'BoundingBox.ymax': 100.0000001, 'BoundingBox.zmax': 460.0000001} 
}
```

From the above dictionary it is possible to identify parts from their central of mass (x,y,z coordinate), volume and bounding box. This can be done manually or one can pass the required properties into the ```find_part_id``` or ```find_part_ids``` functions to identify the part numbers of solids automatically.

A minimal example that finds the part id numbers with matching volumes
```python
import brep_part_finder as bvf

my_brep_part_properties = bvf.get_brep_part_properties('my_brep_file.brep')
part_id = bvf.find_part_id(
    brep_part_properties=my_brep_part_properties,
    volume=10,

)

print(part_id)
>> [1, 3, 4]
```

The above example found 3 part ids with matching volumes.

The follow example also specifies the center of mass which helps narrow down the part ids to just to matching parts.
```python
import brep_part_finder as bvf

my_brep_part_properties = bvf.get_brep_part_properties('my_brep_file.brep')
part_id = bvf.find_part_id(
    brep_part_properties=my_brep_part_properties,
    volume=10,
    center_of_mass=(0,0,0),
)

print(part_id)
>> [1, 3]
```

In the this example the bounding box of the part has also been specified and these three pieces of information are enough to find one part that matches all three criteria.
```python
import brep_part_finder as bvf

my_brep_part_properties = bvf.get_brep_part_properties('my_brep_file.brep')
part_id = bvf.find_part_id(
    brep_part_properties=my_brep_part_properties,
    volume=10,
    center_of_mass=(0,0,0),
    bounding_box = [[10,10,10], [-10,-10,10]]
)

print(part_id)
>> [3]
```

# Combining with Paramak

When reactor models made with Paramak are exported to Brep files it is likely that the order of parts in the Brep file does not match the order of parts within the Paramak object. Therefore this program is useful when identifying parts in the Brep file. See the [paramak_example](https://github.com/fusion-energy/brep_part_finder/blob/main/examples/paramak_example.py) file in the examples folder of this repository.
