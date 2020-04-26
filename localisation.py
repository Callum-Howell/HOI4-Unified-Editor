import re

#####Classes

class localisationfile():
    def __init__(self, inputstring, name):
        loc_langexpression = re.compile("l_.+\s")
        self.name = name
        self.file_lang = loc_langexpression.search(inputstring).group()[2:-2]
        self.loc_dict = {}

        inputstring = inputstring[loc_langexpression.search(inputstring).end():]

        locexpression = re.compile(".+:.+\".+\"")
        keyexpression = re.compile(".+:")
        itemexpression = re.compile("\".+\"")

        loclist = locexpression.finditer(inputstring)
        for localisation in loclist:
            self.loc_dict[keyexpression.search(localisation.group()).group()[1:-1]] = itemexpression.search(localisation.group()).group()

#Enable for key reading test in console
#        for value in self.loc_dict.items():
#            print(value[0])
#        print(self.file_lang)

#####
