from BrewRunner.Record import Record
import logging
logging.basicConfig(level=logging.DEBUG)
class LogProcessor:
    """
    Class that processes a BREW log and transforms it into
    a dictionary with appropriate fields.
    """

    @staticmethod
    def extract_records(raw_in):
        """
        Accepts the raw input from BREW and returns a list of records.
        """
        delimit_line = "--BEGIN RUN--"
        
        records = list()
        raw_record = ""
        for l in raw_in.splitlines():
            print("line: " + l)
            if l == delimit_line:
                # if record is not empty then add
                #  it to the list and clear the record
                if len(raw_record) > 0:
                    logging.debug("Converting to record: " + raw_record)
                    try:
                        r = Record(raw_record)
                        logging.debug("Record: " + str(r.as_dict()))
                        records.append(r)
                    except AttributeError as ae:
                        logging.warning("Record " + raw_record + " could"
                                        "not be converted to a record.")
                        logging.warning(str(ae))
                    raw_record = ""
            else:
                raw_record = raw_record + l

        return records
