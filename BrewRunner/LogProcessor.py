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
        logging.debug(f'Parsing {raw_in.splitlines()}')
        for l in raw_in.splitlines():
            if l == delimit_line:
                # if record is not empty then add
                #  it to the list and clear the record
                if len(raw_record) > 0:
                    try:
                        r = Record(raw_record)
                        records.append(r)
                    except AttributeError as ae:
                        logging.warning("Record " + raw_record + " could"
                                        "not be converted to a record.")
                        logging.warning(str(ae))
                    raw_record = ""
            else:
                raw_record = raw_record + l
        # Catch last record
        try:
            r = Record(raw_record)
            records.append(r)
        except AttributeError as ae:
            logging.warning(f'Could not convert final record {raw_record}')
        logging.info(f'parsed {len(records)} records')
        return records
