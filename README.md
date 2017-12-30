# Reorder frames

This program attempts to reorder the frames from a randomly shuffled video

It runs with opencv 3.4.0 and python 3.6.4.

Run the program with `python3 main.py`

## Image extraction
We start by creating folders and extracting the frames from the video into those folders with the
function `grab_frames`:

```
.
├── full_size_frames : contains the full resolution frames from the video
├── ordered_frames   : will contain the full resolution ordered frames
└── small_frames     : contains the 1/16 resolution frames from the video
```


## Feature extraction
Then, we extract features and we match them between each frames with the function
`extract_matching_data`. To avoid processing data every time we run the program, the matching
data are stored in the file `matching_data.json`.


## Dropping the unrelated frames
Then we drop the unrelated frames by computing a metric for proximity of the frames. Above a given
threshold, we can safely remove the frames. We manage to detect all the unrelated frames. It happens
in `reorder_frames`.

## Reordering the video
Finally, for each frame, we compute the position of all the other frames compared to reference
frame. We then have as much timelines as we have frames. We use this to compute the resulting
timeline, by getting the most frequent image for each position (we weight the frequencies by
the metric for proximity of the frames: the closer the frames seems to be, the more relevant the
information is). It also happens in `reorder_frames`.

To build the image you can run `ffmpeg -start_number 0 -i img%d.png -vcodec mpeg4 output.mp4` in
the `ordered_frames/` folder

## Result
We arrived at 5 frames misplaced out of 114 frames. With the video almost in order, it was easy to
handpick the misplaced frames and put the back into place to compare the two videos.


# Analysis
## Performance
After looking closely to the video, the global motion of the video from the right to the left stops
and then reverse a little at the very end. It's also at that point that we detect the misplaced
frames. (2 frames are duplicated and one if off by 1 as a result)

```
frame 44 is at position 92 and should be at position 95
frame 44 is at position 93 and should be at position 95
frame 56 is at position 95 and should be at position 96
frame 45 is at position 96 and should be at position 92
frame 45 is at position 97 and should be at position 92
# of misplaced images: 5
```

When we only use the most frequent position for each position we get 6 errors

```
frame 44 is at position 92 and should be at position 95
frame 12 is at position 93 and should be at position 94
frame 103 is at position 94 and should be at position 93
frame 5 is at position 95 and should be at position 97
frame 45 is at position 96 and should be at position 92
frame 45 is at position 97 and should be at position 92
# of misplaced images: 6
```

## Limits
The algorithm has no way of know in which direction the main mouvement is going (if the video was
filmed from left to right, it would generate the video in reverse).

It's also quite slow because we do n^2 matching (n being the number of frames), which is a costly
computation. For a larger scene, we should try to find a way to reduce the number of comparisons, maybe
by finding groups of similar frames by other means (picture histograms ?) and then doing the computation
withing those groups.

The algorithm seems to do ok when there is a clear trend in the movement of the
camera. When the movement slows down, it start to produce erroneous results. An idea to solve this
problem would be to evaluate the instantaneous speed of the motions and build an heuristic of where
the next frame should be.
