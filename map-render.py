#!/usr/bin/python3
from noise import pnoise2, snoise2
import matplotlib.pyplot as plt
import argparse
import sys
import dungeonmap
import numpy as np
import cv2


def getMapMask(map, scale=16):
    height, width, maptiles = map.getMap()
    mask = np.array(maptiles)
    res1 = cv2.resize(mask, dsize=(width*scale, height*scale),
                      interpolation=cv2.INTER_NEAREST)
    res2 = cv2.merge([res1, res1, res1])
    return height, width, res2


def getNoiseMask(width, height):
    noisetile = []
    octaves = 4
    freq = 6
    for y in range(height):
        noisetile.append([])
        for x in range(width):
            noisetile[-1].append(snoise2(x / freq, y / freq, octaves))
    res1 = np.array(noisetile)
    res2 = cv2.merge([res1, res1, res1])

    return res2


def getSand(width, height):
    scale = 16
    mask = getNoiseMask(width*scale, height*scale)

    # create a light brown sample field
    lightbrown = np.zeros((width*scale, height*scale, 3), np.float)
    lightbrown[:] = (50.0, 69.0, 76.0)
    lightbrown /= 255.0  # scal from 0-255 to 0-1
    # create a dark brown sample field
    brown = np.zeros((width*scale, height*scale, 3), np.float)
    brown[:] = (31.0, 56.0, 65.0)
    brown /= 255.0
    res = (brown * (1.0 - mask) + (lightbrown * mask))
    return res


def drawmap(map):
    # img = cv.imread('/home/paulb/raytrace_challenge/latest.png')
    scale = 16
    height, width, mask = getMapMask(map, scale)

    # Create our color to use for the 'filled wall' texture
    black = np.zeros((width*scale, height*scale, 3), np.float)
    black[:] = (0.0, 0.0, 0.0)

    # create texture to use for sandy floor texture
    sand = getSand(width, height)

    # blend results
    res = sand * (1 - mask) + (black * mask)

    # convert to 8bit unsigned to save/display
    frame = 255 * res
    frame_int = np.array(frame, np.uint8)

    cv2.imshow('image', frame_int)
    cv2.waitKey()
    cv2.imwrite('output.jpg', frame_int)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Renders a map')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-size', nargs=2, type=int,
                       help="Size of the map in cell tiles width height. This is mutually exclusive with infile", metavar=('Width', 'Height'))
    group.add_argument('-infile', help='File to load map from')
    args = parser.parse_args()
    cave = dungeonmap.tilemap()

    if args.infile:
        cave.loadMapFromFile(args.infile)
    else:
        cave.createMap(width=args.size[0], height=args.size[1])
    drawmap(cave)
