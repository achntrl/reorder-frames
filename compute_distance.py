import numpy as np
import cv2

from utils import image_path


def compute_distance(n1, n2):
    """ Compute some parameters bewteen two images matching features.
    The parameters are {
            "frames": [index of the 1st frame, index of the 2nd frame],
            "mean": mean of the distances of the matches,
            "median": median of the distances of the matches,
            "matches": number of matches,
            "fraction": fraction of good matches (in Lowe's sense) over
            the total number of matches,
            "x": mean displacement of the features on the x axis,
            "y": mean displacement of the features on the y axis,
        }
    This is vastly inspired by the tutorial from openCV:
    https://docs.opencv.org/3.3.0/dc/dc3/tutorial_py_matcher.html """
    imagePath1 = image_path(n1)
    imagePath2 = image_path(n2)

    img1 = cv2.imread(imagePath1, 0)
    img2 = cv2.imread(imagePath2, 0)

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    if len(kp1) < 2 or len(kp2) < 2:
        return {
            "frames": [n1, n2],
            "mean": 0,
            "median": 0,
            "matches": 0,
            "fraction": 0,
            "x": 0,
            "y": 0,
        }
    matches = flann.knnMatch(des1, des2, k=2)
    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]

    distances = [match[0].distance for i, match in enumerate(matches) if matchesMask[i][0] == 1]
    pts1 = [kp1[match[0].queryIdx].pt for i, match in enumerate(matches) if matchesMask[i][0] == 1]
    pts2 = [kp2[match[0].trainIdx].pt for i, match in enumerate(matches) if matchesMask[i][0] == 1]
    direction = np.array([[pt2[0] - pt1[0], pt2[1] - pt1[1]] for pt1, pt2 in zip(pts1, pts2)])
    median_direction = np.median(direction, axis=0)

    print("Finished", n1, n2)
    return {
        "frames": [n1, n2],
        "mean": np.mean(distances),
        "median": np.median(distances),
        "matches": len(distances),
        "fraction": len(distances) / len(matches) if len(matches) > 0 else 0,
        "x": median_direction[0] if len(direction) > 0 else 0,
        "y": median_direction[1] if len(direction) > 0 else 0,
    }
