from PIL import Image
import numpy as np


def get_grayscale(i, width, width_mosaic, j, height, height_mosaic, gray):
    for cur_width in range(i, min(i + width // width_mosaic, width)):
        for cur_height in range(j, min(j + height // height_mosaic, height)):
            red = matrix[cur_width][cur_height][0]
            green = matrix[cur_width][cur_height][1]
            blue = matrix[cur_width][cur_height][2]
            gray += (int(red) + int(green) + int(blue)) / 3
    return int(gray // 100)


def create_grey_picture(x, width, width_mosaic, y, height, height_mosaic, grayscale_step, grayscale):
    for cur_width in range(x, min(x + width // width_mosaic, width)):
        for cur_height in range(y, min(y + height // height_mosaic, height)):
            matrix[cur_width][cur_height] = [int(grayscale // 50 * grayscale_step) * grayscale_step * 50] * 3
    return matrix

img = Image.open("img2.jpg")
matrix = np.array(img)
width = len(matrix)
height = len(matrix[1])

width_mosaic = int(input())
height_mosaic = int(input())
grayscale_step = int(input())

i = 0
while i < width - 1:
    j = 0
    while j < height - 1:
        grayscale = get_grayscale(i, width, width_mosaic, j, height, height_mosaic, 0)
        matrix = create_grey_picture(i, width, width_mosaic, j, height, height_mosaic, grayscale_step, grayscale)
        j = j + height // height_mosaic
    i = i + width // width_mosaic
res = Image.fromarray(matrix)
res.save('res.jpg')