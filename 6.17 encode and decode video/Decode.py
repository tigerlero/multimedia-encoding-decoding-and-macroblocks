from utils import *
import numpy as np


def Decode(first_matrix, diff, Q):
    n = len(diff)-1
    images = [None, first_matrix]
    for i in range(2, n+1):
        image = images[i-1] + np.multiply(diff[i], Q)
        image = np.clip(image, 0, 255)
        images.append(image)

    images = images[1:]
    return images



data = np.fromfile("save", dtype=np.int16)
w, h, fps, Q, frames_count = data[:5].astype(int)
first_matrix = data[5:w*h+5]
first_matrix = np.reshape(first_matrix, (h, w))
data = data[w*h+5:]
diff = np.reshape(data, (frames_count-1, h, w))


images = Decode(first_matrix, diff, Q)

BuildVideo(images, fps/2) #need to divide fps by 2. For some reason ffmpeg builds at twice the fps
CleanUp()
