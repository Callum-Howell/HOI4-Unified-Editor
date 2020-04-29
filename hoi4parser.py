import re
import csv


###

class parsingfile():
    def __init__(self, inputstring):
        commentexpression = re.compile("#.*")

        # Comment Remover

        elements = commentexpression.split(inputstring)
        self.processedstring = r""
        for e in elements:
            self.processedstring += e

        ### Tabs and Linebreaks Removed

        detabbed = ""
        for char in self.processedstring:
            if char == "\t" or char == "\n":
                detabbed += " "
            elif char == "{" or char == "}" or char == "=" or char == "<" or char == ">" or char == '"':
                detabbed += (" " + char + " ")


            else:
                detabbed += char

        self.processedstring = detabbed

        ### Split into blocks of text

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


class scope_template():
    def __init__(self, name, description, examplestring, trigger, effect, fromscope, toscope, version):
        self.name = name
        self.description = description
        self.example = examplestring
        self.trigger = trigger
        self.eeffect = effect
        self.fromscope = fromscope
        self.toscope = toscope
        self.version = version


class command_template():
    def __init__(self, name, parameters, example, description, notes, version, scope):
        self.name = name
        self.parameters = parameters
        self.example = example
        self.description = description
        self.notes = notes
        self.version = version
        self.scope = scope


class trigger_template():
    def __init__(self, name, parameters, example, description, notes, version, scope):
        self.name = name
        self.parameters = parameters
        self.example = example
        self.description = description
        self.notes = notes
        self.version = version
        self.scope = scope


class modifier_template():
    def __init__(self, name, effect, example, modifier_type, usage):
        self.name = name
        self.effect = effect
        self.example = example
        self.modifier_type = modifier_type
        self.usage = usage


class nestable():
    def __init__(self, tag, evaluator, value):
        self.tag = tag
        self.values = []
        self.evaluator = evaluator

        if len(value) == 1:
            self.values.append(value)

        else:
            for substatement in value:
                if type(substatement) == statement:
                    if substatement.tag in SCOPE_TEMPLATES:
                        self.values.append(scope(substatement.tag, substatement.evaluator, substatement.values,
                                                 SCOPE_TEMPLATES[substatement.tag]))
                    elif substatement.tag in COMMAND_TEMPLATES:
                        self.values.append(command(substatement.tag, substatement.evaluator, substatement.values,
                                                   COMMAND_TEMPLATES[substatement.tag]))
                    elif substatement.tag in TRIGGER_TEMPLATES:
                        self.values.append(trigger(substatement.tag, substatement.evaluator, substatement.values,
                                                   TRIGGER_TEMPLATES[substatement.tag]))
                    elif substatement.tag in MODIFIER_TEMPLATES:
                        self.values.append(modifier(substatement.tag, substatement.evaluator, substatement.values,
                                                    MODIFIER_TEMPLATES[substatement.tag]))
                    else:
                        self.values.append(nestable(substatement.tag, substatement.evaluator, substatement.values))

                else:
                    self.values.append(substatement)

    def __repr__(self):
        return self.export()

    def export(self):
        exportstr = ""

        exportstr += self.tag + " " + self.evaluator + " "

        for value in self.values:
            if len(self.values) == 1 and type(value) is not nestable:
                exportstr += value

            elif type(value) == nestable:
                value.export()

            else:
                pass

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
