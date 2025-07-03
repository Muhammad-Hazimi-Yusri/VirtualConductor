import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
import matplotlib.animation as animation
import re
from functools import partial

# --- Settings ---
# Dynamically find all subject/fragment folders
folder_pattern = re.compile(r'subject\d+_frag\d+_take\d+')
all_folders = [f for f in os.listdir(os.path.dirname(__file__)) if os.path.isdir(os.path.join(os.path.dirname(__file__), f)) and folder_pattern.match(f)]
subject_dirs = [os.path.join(os.path.dirname(__file__), f) for f in all_folders]
subject_labels = all_folders

# Fix MatplotlibDeprecationWarning for get_cmap
try:
    subject_colors = plt.colormaps.get_cmap('tab20').colors[:len(subject_dirs)]
except AttributeError:
    subject_colors = plt.cm.get_cmap('tab20', len(subject_dirs)).colors[:len(subject_dirs)]

# Group by fragment
frag_types = sorted(set(f.split('_')[1] for f in all_folders))
frag_to_folders = {frag: [i for i, f in enumerate(all_folders) if frag in f] for frag in frag_types}

joints = [
    'HEAD', 'LEFT_ELBOW', 'LEFT_FOOT', 'LEFT_HAND', 'LEFT_HIP', 'LEFT_KNEE', 'LEFT_SHOULDER', 'NECK',
    'RIGHT_ELBOW', 'RIGHT_FOOT', 'RIGHT_HAND', 'RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_SHOULDER', 'TORSO'
]

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

joint_xyz_all = []
num_frames_all = []
for sdir in subject_dirs:
    joint_xyz = {}
    num_frames = None
    for joint in joints:
        pattern = os.path.join(sdir, f'JOINT_{joint}*.csv')
        csv_files = sorted(glob.glob(pattern))
        xyz = []
        for file in csv_files:
            data = np.genfromtxt(file, delimiter=',', skip_header=1)
            xyz.append(data)
        xyz = np.stack(xyz, axis=1)
        xyz = xyz[~np.isnan(xyz).any(axis=1)]
        xyz = xyz[~np.isinf(xyz).any(axis=1)]
        joint_xyz[joint] = xyz[:, [0, 2, 1]]  # Swap Y/Z
        if num_frames is None:
            num_frames = xyz.shape[0]
        else:
            num_frames = min(num_frames, xyz.shape[0])
    # Center all joints so that TORSO is at (0,0) in the horizontal plane (X,Y)
    torso_xy = joint_xyz['TORSO'][:num_frames, :2]  # X, Y only
    for joint in joints:
        joint_xyz[joint][:num_frames, 0] -= torso_xy[:, 0]
        joint_xyz[joint][:num_frames, 1] -= torso_xy[:, 1]
    joint_xyz_all.append(joint_xyz)
    num_frames_all.append(num_frames)

num_frames = min(num_frames_all)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot handles for each subject, joint, and bone
lines = [[None for _ in joints] for _ in subject_dirs]
points = [[None for _ in joints] for _ in subject_dirs]
bone_lines = [[None for _ in skeleton] for _ in subject_dirs]

for subj_idx, (joint_xyz, color, label) in enumerate(zip(joint_xyz_all, subject_colors, subject_labels)):
    for j_idx, joint in enumerate(joints):
        lines[subj_idx][j_idx], = ax.plot([joint_xyz[joint][0,0]], [joint_xyz[joint][0,1]], [joint_xyz[joint][0,2]], marker='o', label=f'{label} {joint}' if joint=='HEAD' else "", color=color)
        points[subj_idx][j_idx], = ax.plot([joint_xyz[joint][0,0]], [joint_xyz[joint][0,1]], [joint_xyz[joint][0,2]], marker='o', color=color, linestyle='')
    for b_idx, (j1, j2) in enumerate(skeleton):
        bone_lines[subj_idx][b_idx], = ax.plot([], [], [], color=color, linewidth=2, alpha=0.5)

# Set axis limits based on all joints
all_xyz = np.concatenate([joint_xyz[joint][:num_frames] for joint_xyz in joint_xyz_all for joint in joints], axis=0)
ax.set_xlim(np.min(all_xyz[:, 0]), np.max(all_xyz[:, 0]))
ax.set_ylim(np.min(all_xyz[:, 1]), np.max(all_xyz[:, 1]))
ax.set_zlim(np.min(all_xyz[:, 2]), np.max(all_xyz[:, 2]))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Overlay: Two Subjects Motion')

# Slider for frame control
slider_ax = fig.add_axes([0.2, 0.02, 0.6, 0.03])
frame_slider = Slider(slider_ax, 'Frame', 0, num_frames-1, valinit=0, valstep=1)

# Checkbox for persistent mode
checkbox_ax = fig.add_axes([0.01, 0.7, 0.15, 0.1])
checkbox = CheckButtons(checkbox_ax, ['Persistent'], [False])

# Play button
button_ax = fig.add_axes([0.85, 0.02, 0.1, 0.04])
play_button = Button(button_ax, 'Play')

persistent = [False]
playing = [False]
current_frame = [0]
ani = [None]

# Only use checkboxes for subjects, not for 'All frag', 'Check All', 'Uncheck All'
checkbox_labels = subject_labels
checkbox_states = [True] * len(subject_labels)
checkbox_ax = fig.add_axes([0.81, 0.2, 0.18, 0.6])  # Move to right side
subject_checkbox = CheckButtons(checkbox_ax, checkbox_labels, checkbox_states)

# Add buttons for 'All frag' and 'Check All/Uncheck All'
button_axes = {}
frag_buttons = {}
button_y = 0.85
for frag in frag_types:
    ax_btn = fig.add_axes([0.81, button_y, 0.18, 0.04])
    frag_buttons[frag] = Button(ax_btn, f'All {frag}')
    button_axes[frag] = ax_btn
    button_y += 0.05
ax_check_all = fig.add_axes([0.81, button_y, 0.09, 0.04])
check_all_button = Button(ax_check_all, 'Check All')
ax_uncheck_all = fig.add_axes([0.90, button_y, 0.09, 0.04])
uncheck_all_button = Button(ax_uncheck_all, 'Uncheck All')

# Move visible_subjects definition to before update_plot and all its uses
visible_subjects = [True] * len(subject_dirs)

# Animation function
def update_plot(frame):
    for subj_idx, joint_xyz in enumerate(joint_xyz_all):
        visible = visible_subjects[subj_idx]
        color = subject_colors[subj_idx]
        for j_idx, joint in enumerate(joints):
            lines[subj_idx][j_idx].set_visible(visible)
            points[subj_idx][j_idx].set_visible(visible)
            if visible:
                if persistent[0]:
                    lines[subj_idx][j_idx].set_data(joint_xyz[joint][:frame+1, 0], joint_xyz[joint][:frame+1, 1])
                    lines[subj_idx][j_idx].set_3d_properties(joint_xyz[joint][:frame+1, 2])
                else:
                    lines[subj_idx][j_idx].set_data([], [])
                    lines[subj_idx][j_idx].set_3d_properties([])
                points[subj_idx][j_idx].set_data([joint_xyz[joint][frame, 0]], [joint_xyz[joint][frame, 1]])
                points[subj_idx][j_idx].set_3d_properties([joint_xyz[joint][frame, 2]])
        for b_idx, (j1, j2) in enumerate(skeleton):
            bone_lines[subj_idx][b_idx].set_visible(visible)
            if visible:
                xyz1 = joint_xyz[j1][frame]
                xyz2 = joint_xyz[j2][frame]
                bone_lines[subj_idx][b_idx].set_data([xyz1[0], xyz2[0]], [xyz1[1], xyz2[1]])
                bone_lines[subj_idx][b_idx].set_3d_properties([xyz1[2], xyz2[2]])
    fig.canvas.draw_idle()

current_frame[0] = int(frame_slider.val)
update_plot(current_frame[0])

def on_slider(val):
    frame = int(val)
    current_frame[0] = frame
    update_plot(frame)

frame_slider.on_changed(on_slider)

def on_checkbox(label):
    persistent[0] = not persistent[0]
    update_plot(current_frame[0])

checkbox.on_clicked(on_checkbox)

def on_play(event):
    current_frame[0] = int(frame_slider.val)
    update_plot(current_frame[0])
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

# Update update_plot to only show selected subjects
visible_subjects = [True] * len(subject_dirs)

# Checkbox callback for subjects/frags/all
updating_checkboxes = [False]  # Use a mutable object to allow modification in nested scope

def on_subject_checkbox(label):
    if updating_checkboxes[0]:
        return
    idx = checkbox_labels.index(label)
    visible_subjects[idx] = not visible_subjects[idx]
    updating_checkboxes[0] = True
    for i in range(len(subject_labels)):
        if visible_subjects[i] != subject_checkbox.get_status()[i]:
            subject_checkbox.set_active(i)
    updating_checkboxes[0] = False
    update_plot(current_frame[0])
subject_checkbox.on_clicked(on_subject_checkbox)

def on_frag_button(frag, event):
    for i in frag_to_folders[frag]:
        visible_subjects[i] = True
    updating_checkboxes[0] = True
    for i in range(len(subject_labels)):
        if visible_subjects[i] != subject_checkbox.get_status()[i]:
            subject_checkbox.set_active(i)
    updating_checkboxes[0] = False
    update_plot(current_frame[0])
for frag in frag_types:
    frag_buttons[frag].on_clicked(partial(on_frag_button, frag))

def on_check_all(event):
    for i in range(len(visible_subjects)):
        visible_subjects[i] = True
    updating_checkboxes[0] = True
    for i in range(len(subject_labels)):
        if visible_subjects[i] != subject_checkbox.get_status()[i]:
            subject_checkbox.set_active(i)
    updating_checkboxes[0] = False
    update_plot(current_frame[0])
check_all_button.on_clicked(on_check_all)

def on_uncheck_all(event):
    for i in range(len(visible_subjects)):
        visible_subjects[i] = False
    updating_checkboxes[0] = True
    for i in range(len(subject_labels)):
        if visible_subjects[i] != subject_checkbox.get_status()[i]:
            subject_checkbox.set_active(i)
    updating_checkboxes[0] = False
    update_plot(current_frame[0])
uncheck_all_button.on_clicked(on_uncheck_all)

update_plot(current_frame[0])
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
plt.show()
