import re
import csv
import json


#

class parsingfile():
    def __init__(self, inputstring):
        commentexpression = re.compile("#.*")

        # Comment Remover

        elements = commentexpression.split(inputstring)
        self.processedstring = r""
        for e in elements:
            self.processedstring += e

        ### Tabs and Linebreaks Removed

        spaced = self.processedstring.replace("{", " { ")
        spaced = spaced.replace("}", " } ")
        spaced = spaced.replace("=", " = ")
        spaced = spaced.replace("\"", " \" ")
        detabbed = spaced.replace("\t" or "\n", " ")

        # for char in self.processedstring:
        #     if char == "\t" or char == "\n":
        #         detabbed += " "
        #     elif char == "{" or char == "}" or char == "=" or char == "<" or char == ">" or char == '"':
        #         detabbed += (" " + char + " ")
        #
        #
        #     else:
        #         detabbed += char

        self.processedstring = detabbed

        # Split into blocks of text

        self.statements = []

        rawblocks = self.processedstring.split()

        nestedblocks = nestify(rawblocks)

        # Sorted into nested statements

        for tag, evaluator, value in zip(*[iter(nestedblocks)] * 3):
            self.statements.append(statement(tag, evaluator, value))

    def export(self):
        expstr = ""
        for statement in self.statements:
            expstr += statement.export()


class statement():
    def __init__(self, itag, ievaluator, ivalue):
        self.tag = itag
        self.evaluator = ievaluator
        self.values = []
        self.nested = False

        if type(ivalue) == list:
            if len(ivalue) > 0:
                if "=" in ivalue or "<" in ivalue or ">" in ivalue:
                    for tag, evaluator, value in zip(*[iter(ivalue)] * 3):
                        self.nested = True
                        self.values.append(statement(tag, evaluator, value))
                else:
                    for value in ivalue:
                        self.values.append(value)
            elif len(ivalue) == 0:
                self.values.append(None)
        else:
            self.values.append(ivalue)

    def export(self):
        exptstr = ""
        exptstr += self.tag + " " + self.evaluator + " "

        if self.nested:
            exptstr += "{\n"

        for substatement in self.values:
            if type(substatement) == statement:
                for line in substatement.export().splitlines():
                    exptstr += "\n\t" + line


            else:
                exptstr += self.values[0]

        return exptstr

    def __repr__(self):
        liststr = str(self.values)
        return self.tag + self.evaluator + "{" + liststr + "}"

    def __str__(self):
        liststr = str(self.values)
        return self.tag + self.evaluator + "{" + liststr + "}"





def nestify(blocklist):
    nesting = 0
    newlist = []

    # Hierarchy counter


    for block in blocklist:
        if block == "{":
            if nesting == 0:
                nestedlist = []
                nesting += 1
            elif nesting > 0:
                nesting += 1
                nestedlist.append(block)

        elif block == "}":
            nesting -= 1

            if nesting == 0:
                newlist.append(nestedlist)
                nestedlist == []

            elif nesting > 0:
                nestedlist.append(block)

        elif (block != "{" or block != "}") and nesting > 0:
            nestedlist.append(block)

        elif (block != "{" or block != "}") and nesting == 0:
            newlist.append(block)

    stringed_list = []
    string_concatenate = False
    expect_quote = False
    newstring = ""

    for block in newlist:
        if string_concatenate == False:
            if block == r'"':
                string_concatenate = True
            else:
                stringed_list.append(block)

        elif string_concatenate == True:
            if block == r'"' and expect_quote == False:
                string_concatenate = False
                stringed_list.append(newstring)
                newstring = ""

            elif block == r'"' and expect_quote == True:
                expect_quote = False
                newstring += block

            elif block == "\\":
                expect_quote = True
                newstring += block

            else:
                if len(newstring) == 0:
                    newstring += block

                else:
                    newstring += " " + block

    nestedlist = []

    for block in stringed_list:
        if type(block) != list:
            nestedlist.append(block)

        elif type(block) == list:
            nestedlist.append(nestify(block))

    return nestedlist

class game_object:
    """Generic object that represents any structure found within the game files. Used to implement common processes such as loading to and from the database."""
    def __init__(self):
        pass

    def export(self):
        pass

class scope_template(game_object):
    def __init__(self, name, description, examplestring, trigger, effect, fromscope, toscope, version, hidden=False):
        self.name = name
        self.description = description
        self.example = examplestring
        if trigger == "y":
            self.trigger_check_possible = True
        else:
            self.trigger_check_possible = False
        if effect == "y":
            self.effect_possible = True
        else:
            self.effect_possible = False
        self.fromscope = fromscope
        self.toscope = toscope
        self.version = version
        self.hidden= hidden


class command_template(game_object):
    def __init__(self, name, parameters, example, description, notes, version, scope):
        self.name = name
        self.parameters = parameters
        self.example = example
        self.description = description
        self.notes = notes
        self.version = version
        self.scope = scope


class trigger_template(game_object):
    def __init__(self, name, parameters, example, description, notes, version, scope):
        self.name = name
        self.parameters = []

        param_list = parameters.split()

        for parameter in param_list:
            if "£" in parameter:
                param_optional = True
                parameter = parameter.replace("£", "")
            else:
                param_optional = False

            if "#" in parameter:
                param_plural = True
                parameter = parameter.replace("#", "")
            else:
                param_plural = False

            if "%" in parameter:
                param_comparable = True
                parameter = parameter.replace("%", "")
            else:
                param_comparable = False

            if ">" in parameter:
                param_indented = True
                parameter = parameter.replace(">", "")
            else:
                param_indented = False

            parameter = parameter.replace("!", "")
            split_param = parameter.split(".")
#            print(parameter, split_param)

            if len(split_param) == 0:
                self.parameters.append(trigger_param(parameter, param_plural, param_comparable, param_indented, param_optional))
            else:
                self.parameters.append(trigger_param(split_param[0], param_plural, param_comparable, param_indented, param_optional, split_param[0]))

        self.example = example
        self.description = description
        self.notes = notes
        self.version = version
        self.scope = scope

class trigger_param(game_object):
    def __init__(self, type, plural, comparable, indented, optional, descriptor=None):
        self.descriptor = descriptor
        self.plural = plural
        self.comparable = comparable
        self.indented = indented
        self.optional= optional
        self.descriptor = descriptor

        if type == "boolean":
            self.param_type = bool
        elif type == "int":
            self.param_type = int
        elif type == "float":
            self.param_type = float
        elif type == "str":
            self.param_type = float
        else:
            pass


class modifier_template(game_object):
    def __init__(self, name, effect, example, modifier_type, usage):
        self.name = name
        self.effect = effect
        self.example = example
        self.modifier_type = modifier_type
        self.usage = usage


class nestable(game_object):
    def __init__(self, tag="FAILURE", evaluator="=", values=[], hidden=False):
        self.tag = tag
        self.values = values
        self.evaluator = evaluator
        self.hidden = hidden

    def __repr__(self):
        liststr = str(self.values)
        return self.tag + " : {" + liststr + " } "


    @staticmethod
    def parse(inputstatement):
        if inputstatement.tag in SCOPE_TEMPLATES:
            exp_object = scope("", [], "=", SCOPE_TEMPLATES[inputstatement.tag])
        elif inputstatement.tag in COMMAND_TEMPLATES:
            exp_object = command("", [], "=", COMMAND_TEMPLATES[inputstatement.tag])
        elif inputstatement.tag in TRIGGER_TEMPLATES:
            exp_object = trigger("", [], "=", TRIGGER_TEMPLATES[inputstatement.tag])
        elif inputstatement.tag in MODIFIER_TEMPLATES:
            exp_object = modifier("", [], "=", MODIFIER_TEMPLATES[inputstatement.tag])
        elif inputstatement.tag == "limit":
            exp_object = limit()
        elif inputstatement.tag == "random_list":
            exp_object = random_list()
        else:
            exp_object = nestable("", [], "=")
#            print(f"UNCLASSIFIED, {inputstatement.tag}, [{inputstatement.values}]")

        exp_object.tag = inputstatement.tag
        exp_object.values = []
        exp_object.evaluator = inputstatement.evaluator

        for value in inputstatement.values:
            if type(inputstatement.values[0]) != statement:
                exp_object.values.append(value)
            else:
                exp_object.values.append(nestable.parse(value))

        return exp_object


    def export(self):
        exportstr = ""

        exportstr += "\t" + self.tag + " " + self.evaluator + " "

        if len(self.values) == 0:
            exportstr += "{}"
        elif len(self.values) > 0 and (type(self.values[0]) is str or type(self.values[0]) is bool or type(self.values[0]) is int):
            if type(self.values[0]) is bool:
                if self.values[0] is True:
                    exportstr += "yes"
                if self.values[0] is False:
                    exportstr += "no"
            elif type(self.values[0]) is str:
                exportstr += self.values[0]
            elif type(self.values[0]) is int:
                exportstr += str(self.values[0])
        else:
            exportstr += "{\n"
            for value in self.values:
                sub_string = ""
                if type(value) is nestable or type(value) is modifier or type(value) is command or type(value) is trigger or type(value) is scope:
                    nest_str = value.export()
                    for line in nest_str.splitlines():
                        sub_string += "\t" + line + "\n"

                elif value is None:
                    sub_string += ""
                else:
                    sub_string += str(value)
                exportstr += sub_string
            exportstr += "\t}\n"



        exportstr += "\n"


        return exportstr


class scope(nestable):
    def __init__(self, tag, value, evaluator, template):
        super().__init__(tag, value, evaluator)
        self.template = template


class trigger(nestable):
    def __init__(self, tag, value, evaluator, template):
        super().__init__(tag, value, evaluator)
        self.template = template


class command(nestable):
    def __init__(self, tag, value, evaluator, template):
        super().__init__(tag, value, evaluator)
        self.template = template


class modifier(nestable):
    def __init__(self, tag, value, evaluator, template):
        super().__init__(tag, value, evaluator)
        self.template = template

class limit(nestable):
    def __init__(self, tag="limit", evaluator="",  values = [], template=""):
        super().__init__(tag, values, evaluator)

class random_list(nestable):
    def __init__(self, tag="limit", evaluator="",  values = [], template=""):
        super().__init__(tag, values, evaluator)


SCOPE_TEMPLATES = {}
COMMAND_TEMPLATES = {}
TRIGGER_TEMPLATES = {}
MODIFIER_TEMPLATES = {}

with open("scopes.csv", newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for scope_csv in csvreader:
        SCOPE_TEMPLATES[scope_csv["name"]] = scope_template(scope_csv["name"], scope_csv["description"],
                                                            scope_csv["example"], scope_csv["trigger"],
                                                            scope_csv["effect"], scope_csv["from"], scope_csv["to"],
                                                            scope_csv["version"])

with open("commands.csv", newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for command_csv in csvreader:
        COMMAND_TEMPLATES[command_csv["name"]] = command_template(command_csv["name"], command_csv["parameters"],
                                                                  command_csv["example"],
                                                                  command_csv["description"], command_csv["notes"],
                                                                  command_csv["version"], command_csv["scope"])

with open("triggers.csv", newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for trigger_csv in csvreader:
        TRIGGER_TEMPLATES[trigger_csv["name"]] = trigger_template(trigger_csv["name"], trigger_csv["parameters"],
                                                                  trigger_csv["examples"],
                                                                  trigger_csv["description"], trigger_csv["notes"],
                                                                  trigger_csv["version"], trigger_csv["scope"])

with open("modifiers.csv", newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for modifier_csv in csvreader:
        MODIFIER_TEMPLATES[modifier_csv["name"]] = modifier_template(modifier_csv["name"], modifier_csv["effect"],
                                                                     modifier_csv["example"],
                                                                     modifier_csv["modifier_type"],
                                                                     modifier_csv["usage"])



del (csvfile)
del (csvreader)

### test

# testopen = open(r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\events\AcePilots.txt", mode="r", encoding="utf-8-sig")
# testreader = testopen.read()
# test = parsingfile(testreader)
