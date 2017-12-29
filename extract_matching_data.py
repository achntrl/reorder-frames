from itertools import combinations
import json
import os
from multiprocessing import Pool

from compute_distance import compute_distance


def extract_matching_data():
    """ Call compute_distance on each pair of frame and store the data
    in matching_data.json. """

    N = len(os.listdir('full_size_frames/'))
    frames = [i for i in range(N)]

    # result = []
    with Pool(processes=4) as pool:
        procs = [pool.apply_async(compute_distance, (frame1, frame2,)) for frame1, frame2 in combinations(frames, 2)]
        # for frame1, frame2 in combinations(frames, 2):
        #     result.append(compute_distance(frame1, frame2))
        result = [res.get() for res in procs]
    print('Done')
    with open('matching_data.json', 'w') as f:
        f.write(json.dumps(result, indent=2))


if __name__ == '__main__':
    extract_matching_data()
