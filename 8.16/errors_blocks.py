from utils import *
import numpy as np
import sys



def Difference(A, B):
    return A - B


def BreakFrame(frame):
    blocks = {}
    for i in range(horizontal):
        for j in range(vertical):
            blocks[(i, j)] = frame[i*s:i*s+s, j*s:j*s+s]

    return blocks


def SumAbsoluteDifferences(candidate, target):
    diff = target - candidate
    diff = np.absolute(diff)
    return diff.sum()


def FindMatchingBlock(pos, target, prev_matrix):
    best, bIndex = 256*w*h, (None, None)
    for i in range(-s, s+1):
        for j in range(-s, s+1):
            x, y = pos[0]*s + i, pos[1]*s + j
            if x < 0 or x+s >= w:
                break
            if y < 0 or y+s >= h:
                continue

            candidate_block = prev_matrix[x:x+s, y:y+s]

            SAD = SumAbsoluteDifferences(candidate_block, target)
            if SAD < best:
                best = SAD
                bIndex = (x, y)

    return bIndex



VideoToFrames(sys.argv[1])
fps = GetFramerate(sys.argv[1])
frames_count = CountImages()
w, h = GetDimensions(sys.argv[1])
w, h = int(w), int(h)
k = 16
s = 16 # macro-block size
horizontal = w/s
vertical = h/s

first_matrix = ReadMatrix("temp/001.bmp")

prev_matrix = first_matrix
error_frames = []
for z in range(2, frames_count+1):
    print "Frame {}/{}".format(z, frames_count)

    name = "temp/" + FindName(z)
    frame = ReadMatrix(name)
    blocks = BreakFrame(frame)

    error_frame = Difference(frame, prev_matrix)
    for (i, j), target in blocks.items():
        x, y = FindMatchingBlock((i, j), target, prev_matrix)

        original_block = frame[i*s:i*s+s, j*s:j*s+s]
        reference_block = prev_matrix[x:x+s, y:y+s]
        error_frame[i*s:i*s+s, j*s:j*s+s] = Difference(original_block, reference_block)


    error_frames.append(error_frame)
    prev_matrix = frame


error_frames = np.asarray(error_frames)
BuildVideo(error_frames, fps, "out_blocks.avi")
CleanUp()
