import argparse
from BrewRunner.Runner import Runner
from BrewRunner.CSVWriter import CSVWriter
from BrewRunner.Record import Record

parser = argparse.ArgumentParser()
parser.add_argument('output_file')
parser.add_argument('configs', nargs='+')
args = parser.parse_args()

num_jobs = 1
def main():
    records = Runner.run_all_instances(args.configs, num_jobs)
    CSVWriter.write_to_csv(args.output_file, records)

if __name__ == "__main__":
    main()
