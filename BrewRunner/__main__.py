import argparse
from BrewRunner.Runner import Runner
from BrewRunner.CSVWriter import CSVWriter
from BrewRunner.Record import Record

parser = argparse.ArgumentParser()
parser.add_argument('output_file')
parser.add_argument('category_parent_directory', help='The parent directory, under which each directory in the benchmark is the category.')
parser.add_argument('configs', nargs='+')
args = parser.parse_args()

num_jobs = 1
def main():
    for rlist in Runner.run_all_instances(args.configs, num_jobs, args.category_parent_directory):
        for r in rlist:
            r.set_category(args.category_parent_directory)
        CSVWriter.write_to_csv(args.output_file, rlist)

if __name__ == "__main__":
    main()
