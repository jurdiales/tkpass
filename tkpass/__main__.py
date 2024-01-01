import argparse
from . import tkpass

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--theme", default="light", 
                    help="options are light, dark, forestlight, forestdark", type=str)
args = parser.parse_args()

theme = args.theme
tkpass.run(theme)
