#!/usr/bin/python3
import argparse
import sys
import dungeonmap


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
    print(cave)
