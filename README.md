# Homemade Libraries

This is an experiment to develop my own python libraries for analyzeing various datasets.  In 
particular the NYC Pluto Data and the LEHD data.

## Example Usage

```python
from wlib import pluto

pluto.download_files(unzip=True)
df = pluto.read_pluto(dpath, bor, cols)

```