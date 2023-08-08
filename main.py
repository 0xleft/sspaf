import os
import argparse

from core import render

def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument(type=str, help='render, publish, help', dest='operation')
    arguments.add_argument(type=str, help='path to the project', dest='path')

    args = arguments.parse_args()

    if args.operation == 'render':
        render.render(args.path)
    else:
        print('Operation not found')

if __name__ == '__main__':
    main()