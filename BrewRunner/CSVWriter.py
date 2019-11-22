import csv
import os
import statistics
from BrewRunner.Record import Record
import logging
logging.basicConfig(level=logging.DEBUG)
from decimal import *

class CSVWriter:
    """
    Write records to CSV.
    """

    @staticmethod
    def write_to_csv(output_file, records):
        """
        Computes precisions and then writes to a csv.
        """
        records = [r.as_dict() for r in records]
        CSVWriter.add_category_stats(records)
        CSVWriter.add_full_stats(records)

        csv_exists = os.path.exists(output_file)
        
        with open(output_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=records[0].keys())

            if not csv_exists:
                writer.writeheader()
            writer.writerows(records)
        

    class tpfp_tracker:
        def __init__(self):
            self.tp = 0
            self.fp = 0
            self.tn = 0
            self.fn = 0

        def add_record(self, record):
            successful = record['successful']
            was_tp = record['true_positive']
            if successful and was_tp:
                self.tp += 1
            elif successful and not was_tp:
                self.tn += 1
            elif not successful and was_tp:
                self.fn += 1
            elif not successful and not was_tp:
                self.fp += 1

        def get_precision(self):
            try:
                logging.debug("Precision: " + str(self.tp) + "/(" +
                              str(self.tp) + "+" + str(self.fp) + ")")
                p = Decimal(self.tp) / Decimal(self.tp + self.fp)
            except:
                p = 0
            return float(p)
        
        def get_recall(self):
            try:
                r = Decimal(self.tp) / Decimal(self.tp + self.fn)
            except:
                r = 0
            return float(r)
            
    @staticmethod
    def add_category_stats(records):
        """
        Adds precision, recalls, and f-measures for each category.
        """
        categories = dict()
        
        for r in records:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = CSVWriter.tpfp_tracker()
            categories[cat].add_record(r)
        
        for r in records:
            cat = r["category"]
            logging.debug("For cat " + cat + ", tp:" + str(categories[cat].tp) +
                          " fp:" + str(categories[cat].fp) + " tn:" + str(categories[cat].tn) +
                          " fn:" + str(categories[cat].fn))
            prec = categories[cat].get_precision()
            r["category_precision"] = prec
            recall = categories[cat].get_recall()
            r["category_recall"] = recall
            r["category_fmeasure"] = statistics.harmonic_mean([prec, recall])

    @staticmethod
    def add_full_stats(records):
        """
        Adds precision, recall, and f measure for the entire dataset.
        """
        tracker = CSVWriter.tpfp_tracker()
        for r in records:
            tracker.add_record(r)

        for r in records:
            prec = tracker.get_precision()
            r["run_precision"] = prec
            recall = tracker.get_recall()
            r["run_recall"] = recall
            r["run_fmeasure"] = statistics.harmonic_mean([prec, recall])
