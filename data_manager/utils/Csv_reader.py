from io import StringIO
from data_manager.utils.Reader import Reader
import csv

class Csv_reader(Reader):
    """
    Manage csv 
    """
    def __init__(self, reader):
        self.csv = csv.DictReader(StringIO(str(reader)), delimiter='|')
        # strip all the text
        self.list = []
        for i, row in enumerate(self.csv):
            read = {key.strip():value.strip() for key, value in zip(row.keys(), row.values()) if key}
            self.list.append(read)
        Reader.__init__(self, self.list, reader.get_path(), reader.get_line() +2, add_line = 0) # +1 for title line

