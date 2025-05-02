# Configuration file for plotting WRF data
# configure domain, ticks
LON_LEFT = 129
LON_RIGHT = 132.37872
LAT_BOTTOM = 30.936047
LAT_TOP = 34.44063
LON_TICKS_INTERVAL = 0.5
LAT_TICKS_INTERVAL = 0.5
is_deg_min_format = True

# configure plain
is_surface = True
if is_surface:
    PRESSURE_PLAIN = None
else:
    PRESSURE_PLAIN = 850

# configure title
TITLE = "temperature"
TITLE_SIZE = 11

# shade
shade_plot = True
SHADE_VARNAME = "T2"  # Additional variable name: "precipitaion", "moisture_flux", "wind_divergence", "moisure_flux_divergence"
SHADE_MAX = 36
SHADE_MIN = 20
SHADE_INTERVAL = 0.5
SHADE_MULTIPLIER = 1
SHADE_ADDITION = -273.15
# color map
COLOR_MAP_NAME = "jet"
CBAR_UNIT = "[℃]"

# contour
contour_plot = True
CONTOUR_VARNAME = "HGT"
CONTOUR_MAX = 2150
CONTOUR_MIN = 150
CONTOUR_INTERVAL = 100
CONTOUR_MULTIPLIER = 1
CONTOUR_ADDITION = 0
CONTOUR_COLOR = "black"
plot_contour_label = False
CONTOUR_LABEL_INTERVAL = 2000

# vector
vector_plot = True
U_VEXTOR_VARNAME = "uvmet10"  # Additional variable name: moisture_flux
V_VEXTOR_VARNAME = "uvmet10"  # Additional variable name: moisture_flux
VECTOR_DENSITY = 25
VECTOR_REDUCTION_SCALE = 50
VECTOR_COLOR = "lightslategrey"
# vector legend
VECTOR_LEDEND_VALUE = 5
VECTOR_LEDEND_SIZE = 8
VECTOR_LEGEND_NAME = f"{VECTOR_LEDEND_VALUE} " + r"[$\mathrm{m\,s^{-1}}$]"

# gif and mp4
GIF_INTERVAL_TIME = 150
GIF_NAME = "horizontal_cross_section.gif"
MP4_FPS = 5.0
MP4_NAME = "horizontal_cross_section.mp4"
