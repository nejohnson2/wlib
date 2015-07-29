# Homemade Libraries

This is an experiment to develop my own python libraries for analyzeing various datasets.  In 
particular the NYC Pluto Data and the LEHD data.  There are four libraries: *spatial*, *ds_utilities*, *lehd* and *waste*.

## LEHD Library


---

## Spatial Library


This is a library focused on working with spatial data.  There is a module *census*, *pluto* and *spatial_utils*.

*Census Module*
Functions:

- download_pophu: this downloads a shapefile that contains population and housing units. 
- sub_census: subset data based on the counties.  Default is NYC counties.

```python
import census

df = census.download_pophu(state=['36'])
df = census.sub_census(df, counties=['005','047','061','081','085'])

```

*PLUTO Module*
Functions:

- read_pluto()
- download_files()
- download_all_pluto()
- subset_zip()

```python
import pluto

pluto.download_all_pluto()
df = pluto.read_pluto()
```

*Spatial_utils*
Functions:

- spatial_join
- join_files

---

## Waste
A module to do repetative operations on the DSNY waste data.


---

## ds_utilities
These are utility functions where doing data science.