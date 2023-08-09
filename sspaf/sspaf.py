import os
import argparse

from sspaf.core import render, serve, publish, create

def args_error():

    print("""
(: SSPAF a superglued single page aooplication framework :)

Author: plusleft

Usage: sspaf <operation> <path>

Operations:
    render: render the project to the output folder
    serve: serve the project on port 8080
    publish: create a production ready version of the project
    create: initialize the blueprint for a new project

Path:
    path to the project

Examples:
    sspaf serve .
    sspaf publish /home/plusleft/myproject
    sspaf create /home/plusleft/myproject
""")
    
    exit(1)

def main():
    arguments = argparse.ArgumentParser()
    arguments.error = args_error
    arguments.add_argument(type=str, help='render, publish, create, serve', dest='operation')
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