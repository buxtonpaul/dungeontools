#!/usr/bin/python3
import argparse
import sys
import dungeonmap


class mapper_app:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Renders a map',
            usage='''map-render <command> [<args>]

                    create   create a new map with the given dimensions
                    fromfile load from the given path
            ''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def fromfile(self):
        parser = argparse.ArgumentParser(
            description='Load a map from an input file <infile>')
        # prefixing the argument with -- means it's optional
        parser.add_argument('infile')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        cave = dungeonmap.tilemap(width=3, height=3)
        cave.mapfromfile(args.infile)
        print(cave)

    def create(self):
        parser = argparse.ArgumentParser(
            description='Create a map with the given dimensions <width> <height>')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('width', nargs='?', default='30', type=int)
        parser.add_argument('height', nargs='?', default='30', type=int)
        args = parser.parse_args(sys.argv[2:])

        cave = dungeonmap.tilemap(width=args.width, height=args.height)
        cave.iterate3()
        print(cave)


if __name__ == '__main__':
    mapper_app()
