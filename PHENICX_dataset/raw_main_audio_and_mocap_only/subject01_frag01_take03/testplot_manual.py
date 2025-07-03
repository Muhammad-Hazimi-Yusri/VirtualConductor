import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
import matplotlib.animation as animation

# Directory containing the CSV files
data_dir = os.path.dirname(__file__)

# List of joints to plot
joints = [
    'HEAD', 'LEFT_ELBOW', 'LEFT_FOOT', 'LEFT_HAND', 'LEFT_HIP', 'LEFT_KNEE', 'LEFT_SHOULDER', 'NECK',
    'RIGHT_ELBOW', 'RIGHT_FOOT', 'RIGHT_HAND', 'RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_SHOULDER', 'TORSO'
]

joint_xyz = {}
num_frames = None

# Load xyz data for each joint
for joint in joints:
    pattern = os.path.join(data_dir, f'JOINT_{joint}[*.csv')
    csv_files = sorted(glob.glob(pattern))
    xyz = []
    for file in csv_files:
        data = np.genfromtxt(file, delimiter=',', skip_header=1)
        xyz.append(data)
    xyz = np.stack(xyz, axis=1)  # Shape: (num_frames, 3)
    xyz = xyz[~np.isnan(xyz).any(axis=1)]
    xyz = xyz[~np.isinf(xyz).any(axis=1)]
    joint_xyz[joint] = xyz
    if num_frames is None:
        num_frames = xyz.shape[0]
    else:
        num_frames = min(num_frames, xyz.shape[0])  # Ensure all joints have the same frame count

# Swap Y and Z axes for all joints so Z is up
for joint in joint_xyz:
    joint_xyz[joint] = joint_xyz[joint][:, [0, 2, 1]]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define which joints are right-side
right_joints = [j for j in joints if j.startswith('RIGHT_')]

# Add a checkbox for right red toggle
side_checkbox_ax = fig.add_axes([0.01, 0.6, 0.15, 0.08])
side_checkbox = CheckButtons(side_checkbox_ax, ['Right Red Toggle'], [True])
right_red = [True]

# Plot handles for each joint
lines = {}
points = {}
colors = plt.cm.get_cmap('tab20', len(joints))
joint_colors = {joint: colors(idx) for idx, joint in enumerate(joints)}
for idx, joint in enumerate(joints):
    color = 'red' if (right_red[0] and joint in right_joints) else joint_colors[joint]
    lines[joint], = ax.plot([joint_xyz[joint][0,0]], [joint_xyz[joint][0,1]], [joint_xyz[joint][0,2]], marker='o', label=joint, color=color)
    points[joint], = ax.plot([joint_xyz[joint][0,0]], [joint_xyz[joint][0,1]], [joint_xyz[joint][0,2]], marker='o', color=color, linestyle='')

# Define skeletal connections as pairs of joint names
skeleton = [
    ('HEAD', 'NECK'),
    ('NECK', 'TORSO'),
    ('TORSO', 'LEFT_HIP'), ('TORSO', 'RIGHT_HIP'),
    ('LEFT_HIP', 'LEFT_KNEE'), ('LEFT_KNEE', 'LEFT_FOOT'),
    ('RIGHT_HIP', 'RIGHT_KNEE'), ('RIGHT_KNEE', 'RIGHT_FOOT'),
    ('TORSO', 'LEFT_SHOULDER'), ('TORSO', 'RIGHT_SHOULDER'),
    ('LEFT_SHOULDER', 'LEFT_ELBOW'), ('LEFT_ELBOW', 'LEFT_HAND'),
    ('RIGHT_SHOULDER', 'RIGHT_ELBOW'), ('RIGHT_ELBOW', 'RIGHT_HAND')
]

# Create line objects for bones
bone_lines = []
for (j1, j2) in skeleton:
    l, = ax.plot([], [], [], color='k', linewidth=2, alpha=0.5)
    bone_lines.append((l, j1, j2))

# Set axis limits based on all joints
all_xyz = np.concatenate([joint_xyz[joint][:num_frames] for joint in joints], axis=0)
ax.set_xlim(np.min(all_xyz[:, 0]), np.max(all_xyz[:, 0]))
ax.set_ylim(np.min(all_xyz[:, 1]), np.max(all_xyz[:, 1]))
ax.set_zlim(np.min(all_xyz[:, 2]), np.max(all_xyz[:, 2]))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('All Joints Motion')

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
    for idx, joint in enumerate(joints):
        xyz = joint_xyz[joint]
        # Set color based on right_red toggle
        if right_red[0] and joint in right_joints:
            lines[joint].set_color('red')
            points[joint].set_color('red')
        else:
            lines[joint].set_color(joint_colors[joint])
            points[joint].set_color(joint_colors[joint])
        if persistent[0]:
            lines[joint].set_data(xyz[:frame+1, 0], xyz[:frame+1, 1])
            lines[joint].set_3d_properties(xyz[:frame+1, 2])
        else:
            lines[joint].set_data([], [])
            lines[joint].set_3d_properties([])
        points[joint].set_data([xyz[frame, 0]], [xyz[frame, 1]])
        points[joint].set_3d_properties([xyz[frame, 2]])
    # Update bone lines
    for l, j1, j2 in bone_lines:
        xyz1 = joint_xyz[j1][frame]
        xyz2 = joint_xyz[j2][frame]
        l.set_data([xyz1[0], xyz2[0]], [xyz1[1], xyz2[1]])
        l.set_3d_properties([xyz1[2], xyz2[2]])
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

# Callback for right red toggle
def on_side_checkbox(label):
    right_red[0] = not right_red[0]
    update_plot(current_frame[0])
side_checkbox.on_clicked(on_side_checkbox)

update_plot(current_frame[0])
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
plt.show()
