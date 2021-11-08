from PIL import Image
import numpy as np

def get_grey_shade(i, width, width_mosaic, j, height, height_mosaic, matrix, grey):
    for cur_width in range(i, min(width, i + width_mosaic)):
        for cur_height in range(j, min(height, j + height_mosaic)):
            red = matrix[cur_width][cur_height][0]
            green = matrix[cur_width][cur_height][1]
            blue = matrix[cur_width][cur_height][2]
            grey += (int(red) + int(green) + int(blue)) / 3
    return grey

def create_new_picture(i, width, width_mosaic, j, height, height_mosaic, matrix, greyscale):
    for cur_width in range(i, min(width, i + width_mosaic)):
        for cur_height in range(j, min(height, j + height_mosaic)):
            for cur_RGB in range(0, 3):
                matrix[cur_width][cur_height][cur_RGB] = int(grey // 50) * 50 * greyscale

    return matrix

img = Image.open("img2.jpg")
matrix = np.array(img)
width = len(matrix)
height = len(matrix[1])

input_data = input().split(" ")
greyscale = int(input())
width_mosaic = int(input_data[0])
height_mosaic = int(input_data[1])

i = 0
while i < width - 1:
    j = 0
    while j < height - 1:
        grey = int(get_grey_shade(i, width, width_mosaic, j, height, height_mosaic, matrix, 0) // 100)
        new_matrix = create_new_picture(i, width, width_mosaic, j, height, height_mosaic, matrix, greyscale)
        j = j + height_mosaic
    i = i + width_mosaic
res = Image.fromarray(new_matrix)
res.save('res.jpg')
