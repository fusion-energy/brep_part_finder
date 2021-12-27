

# Installation

```bash
conda create --name cadquery
conda activate cadquery
# requires cadquery version 2.2 or above
conda install -c cadquery -c conda-forge cadquery=master
pip install brep_part_finder
```

# Usage

```python
import brep_part_finder as bvf

bvf.import_brep('my_brep_file.brep')
part_id = bvf.find_part_id(volume=10, center_of_mass=(0,0,0), faces=6)

print(part_id)
```

```bash
>> 1
```
