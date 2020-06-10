from conv import convolved_2d
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

'''
Basic idea is to split 'colour_map.png' image to 20x20 squares
and after that to map them to 0 and 1 -> 1 if the square is all
black and 0 in any other case.
Player can move only on fields with value 1.
'''


def get_grid():
    grid = []

    while not grid:
        try:
            grid = np.load('grid/grid' + '.npy')
            return grid
        except IOError:
            print("For some reason file with grid does not exist, so let's create one :)")
            run()


def only_ones(ntuple):
    sum_of_all = sum(list(map(sum, ntuple)))
    count_all = 400

    avg = sum_of_all / count_all
    if avg > 0.9:     # if average is near 1
        return True

    return False


def run():
    im = Image.open('grid/colour_map.png')

    width, height = im.size
    pixels_mapped = np.zeros(shape=(width, height))

    for x in range(width):
        for y in range(height):
            r, g, b, _ = im.getpixel((x, y))

            if r == 0 and g == 0 and b == 0:  # if pixel is black then map pixel to 1
                pixels_mapped[x, y] = 1
            else:
                pixels_mapped[x, y] = 0

    pixels_mapped = np.array(pixels_mapped).T

    # because cells are 20x20, this is image (width / 20) * (height / 20) = 870
    grid = np.zeros(870)
    br = 0
    for ntuple in convolved_2d(pixels_mapped, kernel_size=20, stride=20):
        if only_ones(ntuple):
            grid[br] = 1

        br += 1

    grid = np.reshape(grid, (-1, 30))

    # this has to be done by hand because fields are not all black but
    # they are needed for ghosts to get out
    grid[12, 14] = 1
    grid[12, 15] = 1
    grid[13, 14] = 1
    grid[13, 15] = 1
    # print(grid)

    # save grid to a file 'grid.npy'
    np.save('grid/grid', grid)

    # uncomment next two lines if you want to get grid as image
    # plt.imshow(grid)
    # plt.savefig('grid/grid_as_image.png')
