from utils import *
import numpy as np
import sys



def Difference(A, B):
    return A - B



VideoToFrames(sys.argv[1])
fps = GetFramerate(sys.argv[1])
frames_count = CountImages()
w, h = GetDimensions(sys.argv[1])
w, h = int(w), int(h)
k = 16

first_matrix = ReadMatrix("temp/001.bmp")

prev_matrix = first_matrix
error_frames = []
for z in range(2, frames_count+1):
    name = "temp/" + FindName(z)
    frame = ReadMatrix(name)

    diff = Difference(frame, prev_matrix)
    error_frames.append(diff)

    prev_matrix = frame


images = np.asarray(error_frames)
BuildVideo(images, fps, "out_simple.avi")
CleanUp()
