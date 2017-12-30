import numpy as np
import json
from shutil import copy2
import os

from math import isnan, sqrt

from utils import full_size_image_path, new_image_path


def reorder_frames():
    """ Cleans frames that shouldn't be include in the video and
    reorder the frames. """
    with open('matching_data.json', 'r') as f:
        data = json.load(f)

    N = len(os.listdir('full_size_frames/'))

    # Filter out invalid frames:
    # Invalid frames have a low number of feature matching other images which
    # make the their score go high
    to_plot = np.zeros([N, N])
    for d in data:
        to_plot[d['frames'][0], d['frames'][1]] = compute_score(d)
    size = len(to_plot)
    invalid_frames = []
    for i in range(size):
        if np.median(np.concatenate((to_plot[:i, i], to_plot[i, (i+1):]))) >= 1000:
            invalid_frames.append(i)
    print("Invalid frames:", invalid_frames)

    clean_data = list(filter(lambda d: d['frames'][0] not in invalid_frames
                             and d['frames'][1] not in invalid_frames, data))
    data = clean_data

    for d in data[:]:
        data.append(generate_data_for_transpose(d))

    # Attempt 2
    img_orders = []
    median_weights = []
    for i in range(N):
        if i in invalid_frames:
            continue
        frames = list(filter(lambda x: x['frames'][0] == i, data)) + [{
                "frames": [i, i],
                "mean": 0,
                "median": 0,
                "matches": 0,
                "fraction": 0,
                "x": 0,
                "y": 0,
            }]
        sorted_frames = sorted(frames, key=lambda x:  np.sign(x['x']) * distance(x))
        img_order = [x['frames'][1] for x in sorted_frames]
        median_weight = [1/compute_score(x) if compute_score(x) != 0 else 0 for x in sorted_frames]
        img_orders.append(img_order)
        median_weights.append(median_weight)

    np_orders = np.array(img_orders)

    np_orders
    np_weights = np.array(median_weights)

    img_order = []

    for i in range(len(np_orders)):
        img_order += [most_common_weighted(list(np_orders[:, i]), list(np_weights[:, i]))]

    print("# of misplaced images:", compare_results(img_order))

    for i, n in enumerate(img_order):
        copy2(full_size_image_path(n), new_image_path(i))


####################
# Helper functions #
####################
def compute_score(d):
    """ Compute a score for a given pair of frame (the lower the
    closer the frames). """
    median = d['median'] if (not isnan(d['median']) and d['median'] != 0) else 1000
    return 1 / ((d['fraction'] + 0.0001) * (1 + d['matches'])) * median


def generate_data_for_transpose(d):
    """ Take a frame (i, j) and returns an entry for frame (j, i). """
    new_d = dict(d)
    new_d['frames'] = d['frames'][::-1]
    new_d['x'] = - d['x']
    new_d['y'] = - d['y']
    return new_d


def compare_results(img_order):
    """ Compute the number of frame in an incorrect position. The
    correct sequence have been generated manually after a good enough
    sequence was automatically generated. """
    good_sequence = [
        30, 1, 79, 23, 93, 66, 4, 51, 52, 54, 20, 72, 49, 59, 22, 32, 106, 64, 9, 104, 15, 18, 61,
        35, 108, 62, 3, 68, 109, 92, 41, 14, 48, 65, 97, 84, 81, 8, 53, 50, 94, 26, 11, 95, 55, 91,
        6, 110, 102, 98, 99, 34, 47, 74, 111, 40, 57, 85, 58, 16, 28, 86, 0, 25, 80, 21, 38, 19, 29,
        113, 24, 107, 60, 43, 27, 75, 63, 39, 71, 70, 105, 82, 89, 37, 33, 112, 31, 7, 87, 2, 13,
        77, 45, 103, 12, 44, 56, 5, 67, 96
    ]
    count = 0
    for i, order in enumerate(img_order):
        count += 1 if good_sequence[i] != order else 0
    return count


def distance(data):
    """ Compute euclidian distance. """
    return sqrt(data['x'] ** 2 + data['y'] ** 2)


def most_common(arr):
    """ Return the most frequent occurence in an array. """
    return max(set(arr), key=arr.count)


def most_common_weighted(arr, weights):
    """ Returns the most frequent occurence in array. The frequency
    is weighted by the array of weights. """
    frequencies = {}
    for i, e in enumerate(arr):
        if e not in frequencies.keys():
            frequencies[e] = weights[i]
        else:
            frequencies[e] += weights[i]
    return max(frequencies, key=frequencies.get)


if __name__ == '__main__':
    reorder_frames()
