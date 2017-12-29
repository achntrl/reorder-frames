import os

from extract_matching_data import extract_matching_data
from grab_frames import grab_frames
from reorder_frames import reorder_frames
from utils import confirm


directories = ['small_frames/', 'full_size_frames/', 'ordered_frames/']
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

confirm(grab_frames, 'corrupted_video.mp4')
confirm(extract_matching_data)
confirm(reorder_frames)
