#!/usr/bin/python3
import unittest
import random


# generates a tile map using the scheme here
# http://roguebasin.roguelikedevelopment.org/index.php?title=Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels

class tilemap:
    '''class to generate a dungeonmap map using cellular automata '''
    initfillpercent = 0.45
    width = 0
    height = 0
    tiles = []
    empty = ' '
    wall = '#'

    def __init__(self, fillpercent=0.45, width=20, height=20):
        self.initfillpercent = fillpercent
        self.width = width
        self.height = height
        assert width >= 3
        assert height >= 3
        # iterate over the non border segments
        self.tiles = self.emptyCave(self.empty)
        for row in self.tiles[1:-1]:
            for index in range(1, len(row)-1):
                WinitP = random.random()
                if WinitP < self.initfillpercent:
                    row[index] = self.wall

    def __repr__(self):
        retstring = ""
        for a in self.tiles:
            retstring = "{}\n{}".format(retstring, "".join(a))
        return retstring

    def getWalls(self, row, col, n=1):
        # check the coords, we shouldn't get called if the coords are 0 or dims-1
        count = 0
        for i in range(row-n, row+n+1):
            for j in range(col-n, col+n+1):
                if i < 0 or j < 0 or i >= self.height or j >= self.width:
                    continue
                if(self.tiles[i][j] == self.wall):
                    count += 1
        return count

    def emptyCave(self, fill):
        return [[self.wall for z in range(self.width)]] + [[self.wall]+[' ' for y in range(self.width-2)] + [self.wall] for x in range(self.height-2)] + [[self.wall for z in range(self.width)]]

    def generate(self, ca_rule1):
        # create a new fuly walled map
        # iterate over all the internal tiles of the current map
        # generate new tiles in the new map
        newmap = self.emptyCave(self.wall)
        for row in range(1, self.height-1):
            for col in range(1, self.width-1):
                newmap[row][col] = ca_rule1(row, col)
        self.tiles = newmap

    def iterate1(self):
        for i in range(5):
            self.generate(self.ca_rule1)

    def iterate2(self):
        for i in range(5):
            self.generate(self.ca_rule2)

    def iterate3(self):
        for i in range(4):
            self.generate(self.ca_rule3)
        for i in range(2):
            self.generate(self.ca_rule1)

    def ca_rule1(self, row, col):
        # looks at the surrounding tiles and returne empty or full based on those
        # this version looks at the just the adjacent tiles, and expects to not hit the edges
        count = self.getWalls(row, col)
        if count >= 5:
            return self.wall
        return self.empty

    def ca_rule2(self, row, col):
        # looks at the surrounding tiles and returne empty or full based on those
        # this version looks at the just the adjacent tiles, and expects to not hit the edges
        if self.getWalls(row, col) >= 5:
            return self.wall
        if self.getWalls(row, col, 2) == 0:
            return self.wall
        return self.empty

    def ca_rule3(self, row, col):
        # looks at the surrounding tiles and returne empty or full based on those
        # this version looks at the just the adjacent tiles, and expects to not hit the edges
        if self.getWalls(row, col) >= 5:
            return self.wall
        if self.getWalls(row, col, 2) <= 2:
            return self.wall
        return self.empty

    def postfill(self):
        # pick a point on the map, if it is open, do a flood fill
        # then turn non filled areas into wall
        # afterwards check that the size of the filled area > some percentage if it isn't we didn't pick
        # a good starting point,
        print(".")

    def mapfromfile(self, infile):
        data = []
        height = 0
        lineLenght = -1
        try:
            for line in open(infile):
                strippedline = line.rstrip('\n')
                newlinelength = len(strippedline)
                if newlinelength == 0:
                    continue  # skip blank lines
                height += 1

                if lineLenght == -1:
                    lineLenght = newlinelength
                if newlinelength != lineLenght:
                    print("Lines of different length")
                    return 0, 0, None
                currow = []
                data.append(currow)
                for char in strippedline:
                    if not char in ['#', ' ']:
                        print("Unrecognized map tile {} ".format(char))
                        return 0, 0, None
                    data[-1].append(char)
            self.tiles = data
            self.height = height
            self.width = lineLenght
            return self.height, self.width, self.tiles
        except:
            print("Unable to open file {}".format(infile))
            return 0, 0, None


class TestStringMethods(unittest.TestCase):
    # todo add some real unit tests
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
