import csv
import os
from BrewRunner.Record import Record

class CSVWriter:
    """
    Write records to CSV.
    """

    @staticmethod
    def write_to_csv(output_file, records):
        """
        Computes precisions and then writes to a csv.
        """
        CSVWriter.add_category_stats(records)
        CSVWriter.add_full_stats(records)

        csv_exists = os.path.exists(output_file)
        
        with open(output_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=records[0].keys())

            if not csv_exists:
                writer.writeheader()
            for r in records:
                writer.writerow(r.as_dict())
        

    class tpfp_tracker:
        def __init__(self):
            self.tp = 0
            self.fp = 0
            self.tn = 0
            self.fn = 0

        def add_record(self, record: Record):
            successful = record.get_was_successful()
            was_tp = record.get_is_true_positive()
            if successful and was_tp:
                self.tp += 1
            elif successful and not was_tp:
                self.fp += 1
            elif not successful and was_tp:
                self.fn += 1
            elif not successful and not was_tp:
                self.tn += 1

        def get_precision(self):
            return self.tp / float(self.tp + self.fp)

        def get_recall(self):
            return self.tp / float(self.tp + self.fn)
            
    @staticmethod
    def add_category_stats(records):
        """
        Adds precisions and recalls for each category.
        """
        categories = dict()
        
        for r in records:
            cat = r.get_category()
            if cat not in categories:
                categories[cat] = tpfp_tracker()
            categories[cat].add_record(r)
        
        for r in records:
            cat = r.get_category
            r["category_precision"] = categories[cat].get_precision()
            r["category_recall"] = categories[cat].get_recall()

    @staticmethod
    def add_full_stats(records):
        """
        Adds precision and recall for the entire dataset.
        """
        tracker = tpfp_tracker()
        for r in records:
            tracker.add_record(r)

        for r in records:
            r["run_precision"] = tracker.get_precision()
            r["run_recall"] = tracker.get_recall()
