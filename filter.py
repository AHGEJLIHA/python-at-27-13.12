from PIL import Image
import numpy as np
img = Image.open("img2.jpg")
matrix = np.array(img)
width = len(matrix)
height = len(matrix[1])

i = 0
while i < width - 1:
    j = 0
    while j < height - 1:
        grey = 0
        for i1 in range(i, i + 10):
            for j1 in range(j, j + 10):
                red = matrix[i1][j1][0]
                green = matrix[i1][j1][1]
                blue = matrix[i1][j1][2]
                grey += (int(red) + int(green) + int(blue)) / 3
        grey = int(grey // 100)
        for n in range(i, i + 10):
            for n1 in range(j, j + 10):
                matrix[n][n1][0] = int(grey // 50) * 50
                matrix[n][n1][1] = int(grey // 50) * 50
                matrix[n][n1][2] = int(grey // 50) * 50
        j = j + 10
    i = i + 10
res = Image.fromarray(matrix)
res.save('res.jpg')
