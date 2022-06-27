from PIL import Image
import numpy as np
from rle import RunLength


# Open the image and convert it to Greyscale
im = Image.open("image.bmp").convert("L")
# Uncomment to show the original image
#im.show()

# Get the image's matrix
matrix = np.asarray(im.copy())

# The quantization value
qval = 25

# Encode the image
rl = RunLength(matrix=matrix, qval=qval)
encoded = rl.encode()

f = open("save.txt", "w")
f.write("{};{};{};{}".format(rl.x, rl.y, qval, encoded))
f.close()


print "Encoding complete!"
