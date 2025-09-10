import numpy as np
from file import *

NX = 177
NY = 168
NH = 24
RECL = 4 * NX * NY


DEFAULT_LANDUSE_FILE_PATH = "WRF_DATA_DEFAULT/landuse_fdx.dat"
DEFAULT_LANDUSEF_FILE_PATH = "WRF_DATA_DEFAULT/landuseF_fdx.dat"

OUTPUT_LANDUSE_FILE_PATH = "WRF_DATA/landuse_fdx.dat"
OUTPUT_LANDUSEF_FILE_PATH = "WRF_DATA/landuseF_fdx.dat"

alon, alat, rlui, hgt = read_landuse_file(DEFAULT_LANDUSE_FILE_PATH)
frac_r, frac_u = read_landuseF_file(DEFAULT_LANDUSEF_FILE_PATH)

alon = alon.copy()
alat = alat.copy()
rlui = rlui.copy()
hgt = hgt.copy()
frac_r = frac_r.copy()
frac_u = frac_u.copy()

y_start, y_end = 104, 114 + 1
x_start, x_end = 22, 30 + 1

# Edit rlui
rlui[y_start:y_end, x_start:x_end] = 24

# Edit frac_u and frac_r
frac_u[y_start:y_end, x_start:x_end] = 0.90
frac_r[y_start:y_end, x_start:x_end] = 0.1

write_landuse_file(OUTPUT_LANDUSE_FILE_PATH, alon, alat, rlui, hgt)
write_landuseF_file(OUTPUT_LANDUSEF_FILE_PATH, frac_r, frac_u)