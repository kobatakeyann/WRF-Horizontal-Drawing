from datetime import datetime

from arangement.replacement import DimensionArrayReplacement

wrfout_path = "/work1/kobatake_yusuke/WRF/analysis/drawing/data/wrfout/wrfout_nestingtest_d03_2023-08-21_00:00:00"
a = DimensionArrayReplacement(wrfout_path)
first = a.dataset["Time"].values[0]

# first = datetime(2023, 8, 21, 0, 0)
# print(first)
# print(a.dataset["Time"].sel(Time=first))
# pressure = (
#     a.dataset["PB"].isel(Time=0, south_north=0, west_east=0).values
#     + a.dataset["P"].isel(Time=0, south_north=0, west_east=0).values
# )

pressure = a.dataset["P_HYD"].isel(Time=0, south_north=0, west_east=0).values

# "QV"
# "T2"
# "QVAPOR"
# print(pressure / 100)
print(pressure / 100)
