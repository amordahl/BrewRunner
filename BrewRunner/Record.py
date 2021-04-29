"""
Provides the Record class to store and process a record from BREW's logs.
Works on my modified version of BREW.
"""
from collections import OrderedDict
import re
import os
import logging
logging.basicConfig(level=logging.DEBUG)


class Record:
    """
    Represents a record of a run produced by BREW
    """

    def __init__(self, record):
        """
        Inits based off the raw record given.
        """
        logging.debug(f'Creating record based off of AQL text: {record}')
        self.record = record
        self.generating_script = None
        self.is_true_positive = self.get_is_true_positive()
        self.category = None
        self.apk = self.get_apk()
        self.successful = self.get_was_successful()
        self.time = self.get_time()
        logging.debug('Record creation complete.')

    def get_time(self):
        """
        Extracts the time the record reported
        """
        m = re.search(r"EXECUTION_TIME=(\d+)", self.record)
        result = m.group(1)
        return int(result)

    def get_is_true_positive(self):
        """
        Extracts whether the record is a true positive.
        """
        m = re.search(r"TruePositive\((\w*)\)", self.record)
        result = m.group(1)
        if result.upper() == "TRUE":
            return True
        else:
            return False

    def get_apk(self):
        """
        Extracts the apk that the test case was for.
        """
        m = re.search(r"App\('([^\)]*)'\)", self.record)
        apk = m.group(1)
        return apk

    def set_generating_script(self, gs):
        self.generating_script = gs
        
    def set_category(self, parent_dir):
        """
        Based off the parent directory supplied (i.e., the directory
        that contains all of the category files.
        """

        # Keep reducing the apk name until we get to the parent;
        #  its child is the category.
        if not parent_dir.endswith('/'):
            parent_dir = f'{parent_dir}/'
        if not self.apk.startswith(parent_dir):
            logging.critical(f'Could not determine category of apk. Supplied category directory is {parent_dir}. APK is located in {self.apk}.')
        else:
            self.category = self.apk[len(parent_dir):].split('/')[0]
            logging.info(f'Category is {self.category}')
    
    def get_category(self):
        """
        Extracts the category of the APK.
        Assuming each APK is in a folder containing its category.
        """
        m = re.search(r"'?([^'\ ]*)", self.apk)
        apk = m.group(1)
        return os.path.basename(os.path.dirname(apk))

    def get_was_successful(self):
        """
        Extracts whether the test case was reported as successful or not.
        """
        if "Successful!" in self.record:
            return True
        elif "Failed!" in self.record:
            return False
        else:
            raise ValueError("Record does not have successful or failed in it.")

    def as_dict(self):
        out = OrderedDict()
        out['apk'] = self.apk
        out['category'] = self.category
        out['generating_script'] = self.generating_script
        out['true_positive'] = self.is_true_positive
        out['successful'] = self.successful
        out['time'] = self.time
        return out
        
