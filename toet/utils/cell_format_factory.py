class CellFormatFactory(object):
    def __init__(self, rawtext, formatting, delimeter='\n'):
        self.formatting = formatting
        self.rawtext = rawtext
        self.delimeter = delimeter
        self.splitted_in_rows = self.rawtext.split(self.delimeter)

        def create_index():
            tmp = {}
            for splitted in self.splitted_in_rows:
                start = splitted.find("{") + 1
                end = splitted.find("}")
                key = splitted[start:end]
                tmp[key] = splitted
            return tmp
        self.index = create_index()

    def __format__(self, format):
        if format == 'cell':
            black_list = []
            for key in self.formatting:
                if ( self.formatting[key] == "" or
                     self.formatting[key] == " " or
                     self.formatting[key] is None
                ):
                    self.splitted_in_rows.remove(self.index[key])
                    black_list.append(key)

        for elem in black_list:
            del self.formatting[elem]

        result = "\n".join(self.splitted_in_rows).format(**self.formatting)
        return result
