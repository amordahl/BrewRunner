"""
Provides methods to run BREW and collect its output.
"""

from multiprocessing import Pool
import subprocess
import itertools
from BrewRunner.LogProcessor import LogProcessor
import logging
logging.basicConfig(level=logging.DEBUG)

BREW_PATH = "/home/reprodroid/reprodroid/amordahl-BREW/BREW/target/build/BREW-1.1.0-SNAPSHOT.jar"

def run_brew(config_file):
    """
    Run a single instance of BREW with a config file.
    Returns the output.
    """
    command = ['java', '-jar', BREW_PATH, '-c', config_file, '-reset', '-nogui']
    print(f"Running with config file {config_file}\nThis may take a while....")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
    print(f"Run with config file {config_file} finished. Processing results....")
    records = LogProcessor.extract_records(result)
    for r in records:
        r.set_generating_script(config_file)
        logging.info(f"Added {config_file} to r; r = {r.as_dict()}")
    return records


class Runner:
    """
    Static class that provides methods to run BREW and collect its output.
    """
    
    @staticmethod
    def run_all_instances(config_list, jobs, parent_dir):
        """
        Runs x BREW processes in parallel.

        Actually, for now, we'll iterate. I need to modify brew to stop 
        reading things in from memory before we can do parallel runs.
        """
        for c in config_list:
            output = run_brew(c)
            yield output
