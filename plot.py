import numpy as np
import matplotlib.pyplot as plt
from file import *

NX = 177
NY = 168
NH = 24
RECL = 4 * NX * NY

LANDUSE_FILE_PATH = "WRF_DATA/landuse_fdx.dat"
LANDUSEF_FILE_PATH = "WRF_DATA/landuseF_fdx.dat"
TEMP_FILE_PATH = "temp_fdx.dat"

TEMP_1_FILE_PATH = "TEMPERATURE_DATA/default_temp.dat"
TEMP_2_FILE_PATH = "TEMPERATURE_DATA/nw_temp.dat"

# read data from files
alon, alat, rlui, hgt = read_landuse_file(LANDUSE_FILE_PATH)
frac_r, frac_u = read_landuseF_file(LANDUSEF_FILE_PATH)

def diff_temp(file1, file2):
    temp1 = read_temp_file(file1)
    temp2 = read_temp_file(file2)

    temp_data = np.zeros((NH, NY, NX), dtype=np.float32)
    for hour in range(NH):
        temp_data[hour] = temp2[hour] - temp1[hour]

    return temp_data

temp_data = diff_temp(TEMP_1_FILE_PATH, TEMP_2_FILE_PATH)

print(f"Temperature data shape: {temp_data.shape}")

# Print array shapes
print(f"alon shape: {alon.shape}")
print(f"alat shape: {alat.shape}")
print(f"rlui shape: {rlui.shape}")
print(f"hgt shape: {hgt.shape}")
print(f"frac_r shape: {frac_r.shape}")
print(f"frac_u shape: {frac_u.shape}")

# Create a figure with multiple subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Plot rlui data on first subplot
im1 = axes[0].pcolormesh(rlui, cmap='viridis', shading='auto')
fig.colorbar(im1, ax=axes[0], label='Land Use Index')
axes[0].set_title('Land Use Index (rlui)')
axes[0].set_xlabel('X Grid Point')
axes[0].set_ylabel('Y Grid Point')
axes[0].set_aspect('equal')

# Plot frac_u data on second subplot
im2 = axes[1].pcolormesh(frac_u, cmap='Reds', shading='auto')
fig.colorbar(im2, ax=axes[1], label='Urban Fraction')
axes[1].set_title('Urban Fraction (frac_u)')
axes[1].set_xlabel('X Grid Point')
axes[1].set_ylabel('Y Grid Point')
axes[1].set_aspect('equal')

plt.tight_layout()
plt.show()

# Find global min and max for consistent colorbar
temp_min = np.min(temp_data)
temp_max = np.max(temp_data)
print(f"Temperature range: {temp_min:.2f} to {temp_max:.2f}")

# Create interactive plot with slider
from matplotlib.widgets import Slider

# Create figure with space for slider
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.25)  # Make room for slider

# Initial hour to display
initial_hour = 0

# Helper function to convert hour index to time string
def hour_to_time_string(hour):
    # Convert 24-hour format to 12-hour format with AM/PM
    if hour == 0:
        return "12:00 AM MST"
    elif hour < 12:
        return f"{hour}:00 AM MST"
    elif hour == 12:
        return "12:00 PM MST"
    else:
        return f"{hour-12}:00 PM MST"

# Create the initial plot
im = ax.pcolormesh(temp_data[initial_hour], cmap='jet', shading='auto',
                   vmin=temp_min, vmax=temp_max)
time_string = hour_to_time_string(initial_hour)
title = ax.set_title(f'Temperature at {time_string}')
ax.set_xlabel('X Grid Point')
ax.set_ylabel('Y Grid Point')
ax.set_aspect('equal')
cbar = fig.colorbar(im, ax=ax, label='Temperature (C)')

# Create slider axis
slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])  # [left, bottom, width, height]
hour_slider = Slider(
    ax=slider_ax,
    label='Hour',
    valmin=0,
    valmax=23,
    valinit=initial_hour,
    valstep=1  # Integer steps
)

# Update function for slider
def update(val):
    hour = int(hour_slider.val)
    im.set_array(temp_data[hour].ravel())  # Update plot data
    time_string = hour_to_time_string(hour)
    title.set_text(f'Temperature at {time_string}')  # Update title with time
    fig.canvas.draw_idle()  # Redraw the figure

# Register the update function
hour_slider.on_changed(update)

plt.tight_layout()
plt.show()