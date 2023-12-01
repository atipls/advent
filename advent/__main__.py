
import argparse

arguments = argparse.ArgumentParser(description='Advent of Code 2023')

arguments.add_argument('day', type=int, help='Day to run')
arguments.add_argument('part', type=str, help='Part to run')

args = arguments.parse_args()

if args.day < 1 or args.day > 25:
    raise ValueError("Day must be between 1 and 25")

with open("year.txt", "r") as year_file:
    year = int(year_file.read().strip())

__import__(f"advent.{year}.{args.day}{args.part}")