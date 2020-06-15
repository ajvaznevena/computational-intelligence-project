from conv import convolved_2d
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from game_constants import CELL_SIZE

'''
Basic idea is to split 'colour_map.png' image to 20x20 squares
and after that to map them to 0 and 1 -> 1 if the square is all
black and 0 in any other case.
Player can move only on fields with value 1.
'''

grid = []


def get_grid():
    global grid

    if not grid == []:
        return grid

    try:
        grid = np.load('grid/grid' + '.npy')
        return grid

    except IOError:
        print("For some reason file with grid does not exist, so let's create one :)")
        run()


def only_ones(ntuple):
    sum_of_all = sum(list(map(sum, ntuple)))
    count_all = CELL_SIZE * CELL_SIZE

    avg = sum_of_all / count_all
    if avg > 0.9:     # if average is near 1 (cell is mostly black)
        return True

    return False


def run():
    """ Maps level image to grid """

    img = Image.open('grid/colour_map.png')

    imgWidth, imgHeight = img.size
    pixels_mapped = np.zeros(shape=(imgWidth, imgHeight))

    for x in range(imgWidth):
        for y in range(imgHeight):
            r, g, b, _ = img.getpixel((x, y))

            if (r, g, b) == (0, 0, 0):      # if pixel is black then map pixel to 1
                pixels_mapped[x, y] = 1
            else:
                pixels_mapped[x, y] = 0

    pixels_mapped = np.array(pixels_mapped).T

    newGrid = np.zeros(int(imgWidth / CELL_SIZE) * int(imgHeight / CELL_SIZE))
    counter = 0
    for ntuple in convolved_2d(pixels_mapped, kernel_size=CELL_SIZE, stride=CELL_SIZE):
        if only_ones(ntuple):
            newGrid[counter] = 1

        counter += 1

    newGrid = np.reshape(newGrid, (-1, int(imgWidth / CELL_SIZE)))

    # this has to be done by hand because cells which are needed
    # for ghosts to get out are not all black
    newGrid[12, 14] = 1
    newGrid[12, 15] = 1
    newGrid[13, 14] = 1
    newGrid[13, 15] = 1
    # print(newGrid)

    # save grid to a file 'grid.npy'
    np.save('grid/grid', newGrid)

    # uncomment next two lines if you want to get grid as image
    # plt.imshow(newGrid, cmap='gray')
    # plt.savefig('grid/grid_as_image.png')
