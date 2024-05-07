#!/bin/python
import argparse
import json

def loadJson(args):
    with open(args.src) as f:
        data = json.load(f)
    return data

def writeJson(args, data):
    with open(args.dest, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def sort(args):
    data = loadJson(args)
    newData = dict(sorted(data.items(), key=lambda item: item[0]))
    writeJson(args, newData)

parser = argparse.ArgumentParser(description='Sort a JSON dictionary according to keys')
parser.add_argument('src', metavar='source', type=str, help='The source JSON file to read.')
parser.add_argument('dest', metavar='destination', type=str, help='The destination JSON file to generate.')

sort(parser.parse_args())
