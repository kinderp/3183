class CellFormatFactory(object):
    """Format triple quote text str in a TableView cell

    Sometimes using format str method with keywords (or **kwargs)
    cab be problematic because some keys, coming from your data
    source, are missing.

    CellFormatFactory modifies your text deleting row with missing keys.
    To be more clear:
    It gets a text like below:

        '''
            <b>{family_name}</b><br/>
            <b>{first_name}</b><br/>
            <i>{username}</i><br/>
            {email}<br/>
            <b>Division:</> {division}<br/>
        '''

    and  a formatting dict:

        {
            "family_name": "Rossi",
            "first_name": "",
            "username": "Mario",
            "email": " ",
            "division": None,
        }

    And delete a text row if the corresponding key in
    formatting dict is equal to:

        1. None
        2. ""
        3. " "

    (e.g.)

    this code:

        from toet.utils import CellFormatFactory
        rawtext = '''
                    <b>{family_name}</b><br/>
                    <b>{first_name}</b><br/>
                    <i>{username}</i><br/>
                    {email}<br/>
                    <b>Division:</> {division}<br/>
                  '''

        formatting = {
                        "family_name": "Rossi",
                        "first_name": "",
                        "username": "Mario",
                        "email": " ",
                        "division": None,
        }

        cell = CellFormatFactory(rawtext, formatting)
        print("{:cell}".format(cell))

    produces this output:

        <b>Rossi</b><br/>
        <i>Mario</i><br/>

    """
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
