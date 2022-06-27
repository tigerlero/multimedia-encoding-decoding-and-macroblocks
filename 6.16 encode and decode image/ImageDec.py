from PIL import Image
import numpy as np
from rle import RunLength


try:
    f = open("save.txt", "r")
    contents = f.read().split(';')
    f.close()
except IOError:
    print "image_enc.json not found. Have you encoded the image?"
    exit(1)


x, y, qval = int(contents[0]), int(contents[1]), int(contents[2])
enc = contents[3:]

encoded = []
for i in range(0, len(enc), 2):
    times, digit = enc[i], enc[i+1]
    encoded.append("{};{}".format(times, digit))


rl = RunLength(encoding=encoded, qval=qval)
# Pass in the image's dimensions
rl.x = x
rl.y = y

# Decode it
dec =  np.asarray(rl.decode())
print dec


image = Image.fromarray(np.uint8(dec))
image.show()
image.save("output.bmp")

print "Decoding complete!"
