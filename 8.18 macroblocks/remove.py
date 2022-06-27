from utils import *
import numpy as np
import sys


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


def FindMatchingBlock(target, prev_matrix):
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
                bIndex = (i, j)

    return bIndex



VideoToFrames(sys.argv[1])
fps = GetFramerate(sys.argv[1])
frames_count = CountImages()
w, h = GetDimensions(sys.argv[1])
w, h = int(w), int(h)
k = 16
s = int(sys.argv[2]) # macro-block size
horizontal = w/s
vertical = h/s

background = ReadMatrix("temp/001.bmp")

prev_matrix = background
images = [background]
for z in range(2, frames_count+1):
    print "Frame {}/{}".format(z, frames_count)

    name = "temp/" + FindName(z)
    frame = ReadMatrix(name)

    blocks = BreakFrame(frame)

    # Calculate motion vectors; keep non-zero ones
    non_zero = {}
    for pos, target in blocks.items():
        bIndex = FindMatchingBlock(target, prev_matrix)

        if bIndex != (0, 0):
            # motion vector is non-zero, keep it
            non_zero[pos] = bIndex

    # Replace blocks with non-zero vectors by the corresponding blocks from the background
    for (i, j), vector in non_zero.items():
        frame[i*s:i*s+s, j*s:j*s+s] = background[i*s:i*s+s, j*s:j*s+s].copy()

    images.append(frame)
    prev_matrix = frame


images = np.asarray(images)
BuildVideo(images, fps)
CleanUp()
