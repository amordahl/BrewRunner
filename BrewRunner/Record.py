"""
Provides the Record class to store and process a record from BREW's logs.
Works on my modified version of BREW.
"""

import re
import os

class Record:
    """
    Represents a record of a run produced by BREW
    """

    def __init__(self, record):
        """
        Inits based off the raw record given.
        """
        self.record = record
        self.generating_script = None

    def get_is_true_positive(self):
        """
        Extracts whether the record is a true positive.
        """
        m = re.search(r"TruePositive\((\w*)\)", self.record)
        is_true_positive = bool(m.group(1))

    def get_apk(self):
        """
        Extracts the apk that the test case was for.
        """
        m = re.search(r"App\('(.*)'\)", self.record)
        apk = m.group(1)

    def get_category(self):
        """
        Extracts the category of the APK.
        Assuming each APK is in a folder containing its category.
        """
        apk = self.get_apk()
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
        out = dict()
        out['apk'] = self.get_apk()
        out['category'] = self.get_category()
        out['generating_script'] = self.generating_script
        out['true_positive'] = self.get_is_true_positive()
        out['successful'] = self.get_was_successful()
        
