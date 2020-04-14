import re
import csv

###

class parsingfile():
    def __init__(self, inputstring):
        commentexpression = re.compile("#.+")

### Comment Remover

        elements = commentexpression.split(inputstring)
        self.processedstring = r""
        for e in elements:
            self.processedstring += e

### Tabs and Linebreaks Removed

        detabbed = ""
        for char in self.processedstring:
            if char == "\t" or char == "\n":
                detabbed += " "
            elif char == "{" or char == "}" or char == "=" or char == "<" or char == ">":
                detabbed += (" " + char + " ")
            else:
                detabbed += char

        self.processedstring = detabbed

### Split into blocks of text

        self.statements = []

        rawblocks = self.processedstring.split()

        nestedblocks = nestify(rawblocks)


#### Sorted into nested statements

        for tag, evaluator, value in zip(*[iter(nestedblocks)]*3):
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
                    for tag, evaluator, value in zip(*[iter(ivalue)]*3):
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


# noinspection PyUnboundLocalVariable
def nestify(blocklist):
    nesting = 0
    newlist = []

##Hierarchy counter

##

    for block in blocklist:
        if block == "{":
            if nesting == 0:
                nestedlist = []
                nesting += 1
            elif nesting > 0:
                nesting +=1
                nestedlist.append(block)

        elif block == "}":
            nesting -=1

            if nesting == 0:
                newlist.append(nestedlist)
                nestedlist == []

            elif nesting > 0:
                nestedlist.append(block)

        elif (block != "{" or block != "}") and nesting > 0:
            nestedlist.append(block)

        elif (block != "{" or block != "}") and nesting == 0:
            newlist.append(block)

    nestedlist =[]

    for block in newlist:
        if type(block) != list:
            nestedlist.append(block)

        elif type(block) == list:
            nestedlist.append(nestify(block))


    return nestedlist




class scope_template():
    def __init__(self, name, description, examplestring , trigger , effect, fromscope, toscope, version):
        self.name = name
        self.description = description
        self.example = examplestring
        self.trigger = trigger
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
    def __init__(self, tag, evaluator, value, template):
        self.tag = tag
        self.values = []
        self.template = template

        if len(value) == 1:
            self.values.append(value)

        else:
            for substatement in value:
                if type(substatement) == statement:
                    if substatement.tag in SCOPE_TEMPLATE_DICT:
                        self.values.append(scope(substatement.tag, substatement.evaluator, substatement.values, SCOPE_TEMPLATE_DICT[substatement.tag]))
                    elif substatement.tag in COMMAND_TEMPLATE_DICT:
                        self.values.append(command(substatement.tag, substatement.evaluator, substatement.values, COMMAND_TEMPLATE_DICT[substatement.tag]))
                    elif substatement.tag in TRIGGER_TEMPLATE_DICT:
                        self.values.append(trigger(substatement.tag, substatement.evaluator, substatement.values, TRIGGER_TEMPLATE_DICT[substatement.tag]))
                    elif substatement.tag in MODIFIER_TEMPLATE_DICT:
                        self.values.append(modifier(substatement.tag, substatement.evaluator, substatement.values, MODIFIER_TEMPLATE_DICT[substatement.tag]))
                    else:
                        self.values.append(nestable(substatement.tag, substatement.evaluator, substatement.values, None))

                else:
                    self.values.append(substatement)


    def subnest(self):
        pass

class scope(nestable):
    def __init__(self, tag, value, evaluator, template):
        super().__init__(tag, value, evaluator, template)

class trigger(nestable):
    def __init__(self, tag, value, evaluator, template):
        super().__init__(tag, value, evaluator, template)

class command(nestable):
    def __init__(self, tag, value, evaluator, template):
        super().__init__(tag, value, evaluator, template)

class modifier(nestable):
    def __init__(self, tag, value, evaluator, template):
        super().__init__(tag, value, evaluator, template)

SCOPE_TEMPLATE_DICT = {}
COMMAND_TEMPLATE_DICT = {}
TRIGGER_TEMPLATE_DICT = {}
MODIFIER_TEMPLATE_DICT = {}

with open("scopes.csv", newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for scope_csv in csvreader:
        SCOPE_TEMPLATE_DICT[scope_csv["name"]] = scope_template(scope_csv["name"], scope_csv["description"], scope_csv["example"], scope_csv["trigger"], scope_csv["effect"], scope_csv["from"], scope_csv["to"], scope_csv["version"])

with open("commands.csv", newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for command_csv in csvreader:
        COMMAND_TEMPLATE_DICT[command_csv["name"]] = command_template(command_csv["name"], command_csv["parameters"], command_csv["example"], command_csv["description"], command_csv["notes"], command_csv["version"], command_csv["scope"])

with open("triggers.csv", newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for trigger_csv in csvreader:
        TRIGGER_TEMPLATE_DICT[trigger_csv["name"]] = trigger_template(trigger_csv["name"], trigger_csv["parameters"], trigger_csv["examples"], trigger_csv["description"], trigger_csv["notes"], trigger_csv["version"], trigger_csv["scope"])

with open("modifiers.csv", newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for modifier_csv in csvreader:
        MODIFIER_TEMPLATE_DICT[modifier_csv["name"]] = modifier_template(modifier_csv["name"], modifier_csv["effect"], modifier_csv["example"], modifier_csv["modifier_type"], modifier_csv["usage"])

del(csvfile)
del(csvreader)


### test

# testopen = open(r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\events\AcePilots.txt", mode="r", encoding="utf-8-sig")
# testreader = testopen.read()
# test = parsingfile(testreader)

