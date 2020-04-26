import re
from hoi4parser import *

###

class ideologyfile():
    def __init__(self, inputstring):
        parsedfile = parsingfile(inputstring)

        self.ideologies = []

        for statement in parsedfile.statements:
            if statement.tag == "ideologies":
                for parsed_ideology in statement.values:
                    self.ideologies.append(ideology(parsed_ideology.tag, parsed_ideology.values))

class ideology():
    def __init__(self, name, inputvalues):
        self.name = name
        self.types =[]
        self.dynamic_faction_names = []
        self.color = 0, 0, 0
        self.rules = []
        self.modifiers = []
        self.faction_modifiers = []
        self.can_host_exiles = False
        self.can_collaborate = False
        self.war_impact_on_wt = 0
        self.faction_impact_on_wt = 0
        self.ai_type = None

        for value in inputvalues:
            if value.tag == "dynamic_faction_names":
                self.dynamic_faction_names = value.values

            if value.tag == "color":
                self.color = value.values

            if value.tag == "types":
                for sub_type in value.values:
                    self.types.append(ideology_sub_type(sub_type.tag))

            if value.tag == "rules":
                for rule in value.values:
                    self.rules.append(modifier(rule.tag, rule.values[0]))

            if value.tag == "can_host_government_in_exile":
                self.can_host_exiles == True

            if value.tag == "war_impact_on_world_tension":
                self.war_impact_on_wt = float(value.values[0])

            if value.tag == "faction_impact_on_world_tension":
                self.faction_impact_on_wt == float(value.values[0])

            if value.tag == "modifiers":
                for substatement in value.values:
                    self.modifiers.append(modifier(substatement.tag, substatement.values[0]))

            if value.tag == "faction_modifiers":
                if len(value.values) > 0:
                    for substatement in value.values:
                        if type(substatement) == statement:
                            self.faction_modifiers.append(modifier(substatement.tag, substatement.values[0]))

            if value.tag[:2] == "ai":
                self.ai_type = value.tag



class ideology_sub_type():
    def __init__(self, name):
        self.name = name

class modifier():
    def __init__(self, itag, ivalue):
        self.tag = itag
        self.value = ivalue


### Hierarchy Slicer


#### Test

