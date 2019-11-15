from BrewRunner.Record import Record

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
        delimit_line = ""
        
        records = list()
        raw_record = list()
        for l in raw_in:
            if l == delimit_line:
                # if record is not empty then add
                #  it to the list and clear the record
                if len(raw_record) > 0:
                    records.append(Record(raw_record))
                    raw_record = list()
            else:
                raw_record.append(l)

        return records
