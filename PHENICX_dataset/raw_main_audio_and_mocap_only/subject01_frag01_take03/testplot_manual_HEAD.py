import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
import matplotlib.animation as animation

# Directory containing the CSV files
data_dir = os.path.dirname(__file__)

# Find all JOINT_HEAD CSV files
csv_files = sorted(glob.glob(os.path.join(data_dir, "JOINT_HEAD[*.csv")))

# Read each axis data from the corresponding file
xyz = []
for file in csv_files:
    data = np.genfromtxt(file, delimiter=',', skip_header=1)
    xyz.append(data)
xyz = np.stack(xyz, axis=1)  # Shape: (num_frames, 3)

# Remove any NaN or Inf values
xyz = xyz[~np.isnan(xyz).any(axis=1)]
xyz = xyz[~np.isinf(xyz).any(axis=1)]

num_frames = xyz.shape[0]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initial plot
line, = ax.plot([xyz[0,0]], [xyz[0,1]], [xyz[0,2]], marker='o', label='Trajectory')
point, = ax.plot([xyz[0,0]], [xyz[0,1]], [xyz[0,2]], marker='o', color='r', linestyle='', label='Current Point')
ax.set_xlim(np.min(xyz[:, 0]), np.max(xyz[:, 0]))
ax.set_ylim(np.min(xyz[:, 1]), np.max(xyz[:, 1]))
ax.set_zlim(np.min(xyz[:, 2]), np.max(xyz[:, 2]))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('JOINT_HEAD Motion')

# Slider for frame control
slider_ax = fig.add_axes([0.2, 0.02, 0.6, 0.03])
frame_slider = Slider(slider_ax, 'Frame', 0, num_frames-1, valinit=0, valstep=1)

# Checkbox for persistent mode
checkbox_ax = fig.add_axes([0.01, 0.7, 0.15, 0.1])
checkbox = CheckButtons(checkbox_ax, ['Persistent'], [True])

# Play button
button_ax = fig.add_axes([0.85, 0.02, 0.1, 0.04])
play_button = Button(button_ax, 'Play')

persistent = [True]
playing = [False]
current_frame = [0]
ani = [None]

# Animation function
def update_plot(frame):
    if persistent[0]:
        line.set_data(xyz[:frame+1, 0], xyz[:frame+1, 1])
        line.set_3d_properties(xyz[:frame+1, 2])
    else:
        line.set_data([], [])
        line.set_3d_properties([])
    point.set_data([xyz[frame, 0]], [xyz[frame, 1]])
    point.set_3d_properties([xyz[frame, 2]])
    fig.canvas.draw_idle()

# Ensure current_frame is set to the slider's value at start and plot is updated
current_frame[0] = int(frame_slider.val)
update_plot(current_frame[0])

# Slider callback
def on_slider(val):
    frame = int(val)
    current_frame[0] = frame
    update_plot(frame)

frame_slider.on_changed(on_slider)

# Checkbox callback
def on_checkbox(label):
    persistent[0] = not persistent[0]
    update_plot(current_frame[0])

checkbox.on_clicked(on_checkbox)

# Play button callback and animation
def on_play(event):
    # Always sync current_frame to slider before playing
    current_frame[0] = int(frame_slider.val)
    update_plot(current_frame[0])  # Ensure plot is updated before animation
    if not playing[0]:
        playing[0] = True
        play_button.label.set_text('Pause')
        ani[0] = animation.FuncAnimation(fig, animate, frames=range(current_frame[0], num_frames), interval=1000/30, blit=False, repeat=False)
    else:
        playing[0] = False
        play_button.label.set_text('Play')
        if ani[0] is not None:
            ani[0].event_source.stop()

def animate(frame):
    if not playing[0]:
        return
    current_frame[0] = frame
    update_plot(frame)
    frame_slider.set_val(frame)
    if frame == num_frames - 1:
        playing[0] = False
        play_button.label.set_text('Play')

play_button.on_clicked(on_play)

plt.show()
