def image_path(n):
    return "small_frames/img" + str(n) + ".png"


def full_size_image_path(n):
    return "full_size_frames/img" + str(n) + ".png"


def new_image_path(n):
    return "ordered_frames/img" + str(n) + ".png"


confirm_text = {
    'grab_frames': "Do you want to recapture the frames from the video?",
    'extract_matching_data': "Do you want to re-extract matching data?",
    'reorder_frames': "Do you want to reorder the frames?",
}


def confirm(func, *args):
    if input(confirm_text[func.__name__] + " (y/N) ").lower() == 'y':
        func(*args)
