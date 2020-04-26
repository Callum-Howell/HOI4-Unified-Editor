import re


#Classes

class localisation_file:
    def __init__(self, input_string, name):
        loc_lang_expression = re.compile("l_.+\s")
        self.name = name
        self.file_lang = loc_lang_expression.search(input_string).group()[2:-2]
        self.loc_dict = {}

        input_string = input_string[loc_lang_expression.search(input_string).end():]

        locexpression = re.compile(".+:.+\".+\"")
        keyexpression = re.compile(".+:")
        itemexpression = re.compile("\".+\"")

        loclist = locexpression.finditer(input_string)
        for localisation in loclist:
            self.loc_dict[keyexpression.search(localisation.group()).group()[1:-1]] = itemexpression.search(
                localisation.group()).group()

# Enable for key reading test in console
#        for value in self.loc_dict.items():
#            print(value[0])
#        print(self.file_lang)
