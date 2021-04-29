import argparse
import os
import sys
from tqdm import tqdm
from BrewRunner.Runner import Runner
from BrewRunner.CSVWriter import CSVWriter
from BrewRunner.Record import Record
from BrewRunner.CSVReader import CSVReader

parser = argparse.ArgumentParser()
parser.add_argument('brew_jar')
parser.add_argument('output_file')
parser.add_argument('category_parent_directory', help='The parent directory, under wnhich each directory in the benchmark is the category.')
parser.add_argument('config')
parser.add_argument('-j', '--jobs', default=1, type=int)
parser.add_argument('-t', '--timeout', default="10m", type=str, help="timeout string (default 10m)")
parser.add_argument('-l', '--logs',
                    default="/home/asm140830/AndroidTA/AndroidTAEnvironment/results/run_logs", help="where to store the active running logs")
args = parser.parse_args()

import logging
logging.basicConfig(level=logging.DEBUG)

def main():
    config = os.path.abspath(args.config)
    reader = CSVReader(args.output_file)
    already_ran = reader.getScripts()
    logging.info(f"These scripts have already been run: {already_ran}")
    if config in already_ran:
        print(f"Config {config} has already been run. Exiting...")
        sys.exit(0)

    records = Runner.run_brew(config, args.brew_jar, args.logs, args.timeout)
    logging.info('BREW finished running.')
    logging.info('Now recording category information in records.')
    for record in tqdm(records):
        record.set_category(args.category_parent_directory)
    logging.info('Now writing to CSVs.')
    CSVWriter.write_to_csv(args.output_file, records)

if __name__ == "__main__":
    main()
