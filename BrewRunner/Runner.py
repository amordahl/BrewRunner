"""
Provides methods to run BREW and collect its output.
"""

from multiprocessing import Pool
import subprocess
import itertools
from BrewRunner.LogProcessor import LogProcessor

BREW_PATH = "/home/reprodroid/reprodroid/amordahl-BREW/BREW/target/build/BREW-1.1.0-SNAPSHOT.jar"
class Runner:
    """
    Static class that provides methods to run BREW and collect its output.
    """

    @staticmethod
    def run_brew(config_file):
        """
        Run a single instance of BREW with a config file.
        Returns the output.
        """
        command = ['java', '-jar', BREW_PATH, '-c', config_file, '-nogui']
        result = subproces.run(command, stderr=subprocess.STDOUT)
        records = LogProcessor.extract_records(result.stdout)
        for r in records:
            r.generating_script = config_file
        return records


    @staticmethod
    def run_all_instances(config_list, jobs):
        """
        Runs x BREW processes in parallel.
        """
        
        p = Pool(jobs)
        outputs = p.map(Runner.run_brew, config_list)
        return list(itertools.chain.from_iterable(outputs))
