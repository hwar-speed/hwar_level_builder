class CsvReader:
    def __init__(self, path, delimiter=','):
        self.path = path
        self.delimiter = delimiter
        self.data = self.read_csv()

    def read_csv(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()
        header = lines[0].strip().split(self.delimiter)
        data = []
        for line in lines[1:]:
            data.append(dict(zip(header, line.strip().split(self.delimiter))))
        return data