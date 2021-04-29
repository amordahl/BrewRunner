"""
Provides methods to run BREW and collect its output.
"""

from multiprocessing import Pool
from functools import partial
import datetime
import subprocess
import itertools
import os
from BrewRunner.LogProcessor import LogProcessor
import logging
logging.basicConfig(level=logging.WARNING)

class Runner:
    ## Sets the path where the logs are written
    @staticmethod
    def run_brew(config_file, brew_path, log_path, timeout):
        """
        Run a single instance of BREW with a config file.
        Returns the output.
        
        Writes the data to a log file.
        """
        # Generate log file
        log_file = os.path.join(log_path, f"{os.path.basename(config_file)}_"
                                f"{str(datetime.datetime.now()).replace(' ', '_')}.txt")
        command = f"java -jar {brew_path} -c {config_file} -nogui -t {timeout} > {log_file}"
    
        logging.debug(f"Command: {command}")
        logging.info(f"Running with config file {config_file}\n"
                     "This may take a while....")

        # Run the command, shell=True to support the output redirection
        subprocess.run(command, shell=True)
        
        # Grab the input from the log file
        with open(log_file) as f:
            result = f.read()
            
        logging.info(f"Run with config file {config_file} finished "
                     f"(log in {log_file}). Processing results....")

        # Extract records from logProcessor
        records = LogProcessor.extract_records(result)

        # Iterate over records and add the config file as the generating config
        for r in records:
            r.set_generating_script(config_file)

        return records
