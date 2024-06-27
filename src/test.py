import xarray as xr

from arangement.replacement import DimensionArrayReplacement

wrfout_path = "/work1/kobatake_yusuke/WRF/analysis/drawing/data/wrfout/wrfout_nestingtest_d03_2023-08-21_00:00:00"

a = DimensionArrayReplacement(wrfout_path)
first = a.dataset["Time"].values[0]
from datetime import datetime

first = datetime(2023, 8, 21, 0, 0)
print(first)
print(a.dataset["Time"].sel(Time=first))
