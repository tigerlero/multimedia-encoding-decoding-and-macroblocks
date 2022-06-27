import numpy as np
from math import ceil
from PIL import Image
from subprocess import call, check_output


def FindName(i):
    name = str(i)
    if i < 10:
        name = "00{}".format(i)
    elif i < 100:
        name = "0{}".format(i)

    name += ".bmp"
    return name


def ReadMatrix(name):
    # When opening an image and exporting to numpy array, it gets typed
    # as an uint8 (for grayscale). To avoid overflow that would ruin the images,
    # we have to convert the array from uint8 to int.
    return np.asarray(Image.open(name).convert("L")).astype(int)


def VideoToFrames(video):
    # Break video into frames
    if CountImages() > 0:
        return

    command = "mkdir temp"
    call(command, shell=True)

    command = 'ffmpeg -i {} temp/$filename%03d.bmp'.format(video)
    call(command, shell=True)


def CountImages():
    command = "ls -d temp/[[:digit:]][[:digit:]][[:digit:]].bmp | wc -l"
    return int(check_output(command, shell=True))


def GetFramerate(video):
    command = "ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of default=noprint_wrappers=1:nokey=1 {}".format(video)
    f = check_output(command, shell=True).split('/')
    return int(ceil(float(f[0]) / float(f[1])))


def GetDimensions(video):
    command = "ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1 {}".format(video)
    output = check_output(command, shell=True).split('\n')
    w, h = output[0].split('=')[1], output[1].split('=')[1]
    return w, h


def CleanUp():
    command = 'rm *.bmp'
    call(command, shell=True)


def BuildVideo(images, fps, output):
    SaveImages(images)
    command = "ffmpeg -framerate {} -i %03d.bmp {}".format(fps, output)
    call(command, shell=True)


def SaveImages(images):
    images = images.astype(np.uint8)
    for i in range(len(images)):
        name = FindName(i+1)
        im = images[i]
        im = Image.fromarray(im, "L")
        im.save(name)
