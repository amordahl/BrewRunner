import argparse
import os

from BrewRunner.Runner import Runner
from BrewRunner.CSVWriter import CSVWriter
from BrewRunner.Record import Record
from BrewRunner.CSVReader import CSVReader

parser = argparse.ArgumentParser()
parser.add_argument('brew_jar')
parser.add_argument('output_file')
parser.add_argument('category_parent_directory', help='The parent directory, under which each directory in the benchmark is the category.')
parser.add_argument('configs', nargs='+')
parser.add_argument('-j', '--jobs', default=1, type=int)
parser.add_argument('-t', '--timeout', default="10m", type=str, help="timeout string (default 10m)")
args = parser.parse_args()

import logging
logging.basicConfig(level=logging.DEBUG)

def main():
    # rlist is a list of lists
    configs = [os.path.abspath(c) for c in args.configs]
    reader = CSVReader(args.output_file)
    already_ran = reader.getScripts()
    logging.info(f"These scripts have already been run: {already_ran}")
    configs = [c for c in configs if c not in already_ran]
    for rlist in Runner.run_all_instances(args.brew_jar,
                                          configs,
                                          args.jobs,
                                          args.category_parent_directory,
                                          args.timeout):
        logging.debug(str(rlist))
        for r in rlist:
            for record in r:
                record.set_category(args.category_parent_directory)
            CSVWriter.write_to_csv(args.output_file, r)

if __name__ == "__main__":
    main()
