import os
import csv
import logging
logging.basicConfig(level=logging.WARNING)

class CSVReader:
    """
    Class to read CSV files and provide relevant functionality.
    """

    def __init__(self, outfile):
        self.outfile = outfile


    def getScripts(self):
        """
        Get a list of all of the scripts that have already been run
        per the CSV file.
        """

        try:
            logging.info("Computing scripts that have already been run....")
            with open(self.outfile) as f:
                reader = csv.DictReader(f)
                result = list(set([os.path.abspath(row['generating_script']) for row in reader]))
                logging.info(f"{len(result)} scripts have already been run.")
                return result
        except IOError:
            logging.info(f"{self.outfile} does not exist.")
            return list()
                    
