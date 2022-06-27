from utils import *
import numpy as np
import sys


def Encode(first_matrix, Q, n):
    diff = [None, 0]
    prev_matrix = first_matrix
    for i in range(2, n+1):
        name = "temp/" + FindName(i)
        matrix = ReadMatrix(name)

        frame_diff = matrix - prev_matrix
        frame_diff = np.floor(np.divide(frame_diff, Q))

        diff.append(frame_diff)

        prev_matrix = matrix

    return np.asarray(diff[2:])



VideoToFrames(sys.argv[1])
fps = GetFramerate(sys.argv[1])
frames_count = CountImages()
Q = int(sys.argv[2])
w, h = GetDimensions(sys.argv[1])
first_matrix = ReadMatrix("temp/001.bmp")

diff = Encode(first_matrix, Q, frames_count)
SaveEncoding(first_matrix, diff, Q, fps, w, h, frames_count)
