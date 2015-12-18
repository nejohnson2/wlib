import geopandas as gp
from spatial.spatial_utils import spatial_join

def get_population_for_dsny_section():
	'''Merge NYC Census Block population data
	with the DSNY section file

	Returns
	-------

	GeoDataFrame

	'''

	census = gp.GeoDataFrame.from_file('../Data/NYC_Census_Block/NYC_Census_Block.shp')

	dsny = gp.GeoDataFrame.from_file('../Data/DSNY_Sections/DSNY_sections.shp')

	sj = spatial_utils.spatial_join(census, dsny)

	return sj