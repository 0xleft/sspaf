import os
import argparse

from sspaf.core import render, serve, publish, create

def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument(type=str, help='render, publish, help', dest='operation')
    arguments.add_argument(type=str, help='path to the project', dest='path')

    args = arguments.parse_args()

    if args.operation == 'render':
        render.render(args.path)
    elif args.operation == 'serve':
        serve.serve(args.path)
    elif args.operation == 'publish':
        publish.publish(args.path)
    elif args.operation == 'create':
        create.create(args.path)
    else:
        print('Operation not found')

if __name__ == '__main__':
    main()