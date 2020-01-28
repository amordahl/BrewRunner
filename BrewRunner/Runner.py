"""
Provides methods to run BREW and collect its output.
"""

from multiprocessing import Pool
import subprocess
import itertools
import os
from BrewRunner.LogProcessor import LogProcessor
import logging
logging.basicConfig(level=logging.DEBUG)

BREW_PATH = "/home/reprodroid/reprodroid/amordahl-BREW/BREW/target/build/BREW-1.1.0-SNAPSHOT.jar"
TIMEOUT = '10m'
def run_brew(config_file):
    """
    Run a single instance of BREW with a config file.
    Returns the output.
    """
    command = ['java', '-jar', BREW_PATH, '-c', config_file, '-reset', '-nogui', '-t', TIMEOUT]
    logging.info(f"Running with config file {config_file}\nThis may take a while....")
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode()
    logging.debug(result)
    logging.info(f"Run with config file {config_file} finished. Processing results....")
    records = LogProcessor.extract_records(result)
    for r in records:
        r.set_generating_script(config_file)
    logging.debug("Returning successfully to pool")
    return records

class Runner:
    """
    Static class that provides methods to run BREW and collect its output.
    """
    
    @staticmethod
    def run_all_instances(brew_jar, config_list, jobs, parent_dir, timeout):
        """
        Runs x BREW processes in parallel.
        """
        global BREW_PATH
        BREW_PATH = brew_jar
        global TIMEOUT
        TIMEOUT = timeout
        # break list into chunks of size jobs
        chunks = [config_list[i * jobs:(i+1) * jobs] for i in\
                  range((len(config_list) + jobs - 1) // jobs)]
        for c in chunks:
            logging.debug(f"Chunk is {str(c)}")
            p = Pool(len(c))
            output = p.map(run_brew, c)
            logging.info("Chunk finished running. Returning results now.")
            yield [o for o in output if o is not None]
