import numpy as np


class RunLength:
    matrix = None
    enc_matrix = None
    x = None
    y = None
    qval = None

    def __init__(self, matrix=None, encoding=None, qval=None):
        """Default constructor. Takes in the original matrix or the encoding of the image,
        along with the quantization value."""
        self.matrix = matrix
        self.encoding = encoding
        self.qval = qval


    def quantize(self):
        m = np.divide(self.matrix, float(self.qval))
        return np.floor(m).astype(int)

    def dequantize(self, matrix):
        m = np.multiply(matrix, float(self.qval))
        return np.floor(m).astype(int)


    def encode(self):
        """Method used to encode images to the RLE format"""
        matr = self.quantize()

        # Flatten the array
        matrNew = np.hstack(matr)

        self.x = len(matr)
        self.y = len(matr[0])

        counter = 0
        last_color = matrNew[0]
        result = ""

        # Check every color in the array
        for color in matrNew:
            # If the color is the same as the last one, increase the counter, else append the counter along with the color to the result
            if color != last_color:
                # The result follows this form: [counter;color]
                result += str(counter) + ';' + str(last_color) + ';'
                last_color = color
                counter = 1
            else:
                counter += 1

        # Append the final color to the result, along with its counter
        result += str(counter) + ";" + str(last_color)

        self.encoding = result
        return result

    def decode(self):
        """Method used to decode RLE encoded images"""
        matr = []
        # for i in range(self.x):
        #     matr.append([])

        for line in self.encoding:
            l = line.split(";")
            times, color = l[0], l[1]
            # Append each color X times
            for time in range(int(times)):
                matr.append(int(color))

        # Restore the array to its original size
        matrFinal = np.reshape(matr, (-1, self.y))

        # Return the dequantized array
        return self.dequantize(matrFinal)
