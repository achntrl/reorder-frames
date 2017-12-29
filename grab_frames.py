import cv2

from utils import full_size_image_path, image_path


def grab_frames(videoPath):
    """ Turn the video into a serie of frames"""
    cap = cv2.VideoCapture(videoPath)

    count = 0

    print("Start grabbing frames.")
    ret, full_size_frame = cap.read()
    while (ret):
        # Resize to 1/4 so it doesn't take forever to match features
        frame = cv2.resize(full_size_frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        cv2.imwrite(full_size_image_path(count), full_size_frame)
        cv2.imwrite(image_path(count), frame)

        count += 1
        ret, full_size_frame = cap.read()

    print("All frames grabbed. There are %d frames" % count)
    cap.release()


if __name__ == '__main__':
    grab_frames('corrupted_video.mp4')
