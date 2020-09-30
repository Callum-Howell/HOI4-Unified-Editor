import re
from hoi4parser import *

###

class ideologyfile(game_object):
    def __init__(self):
        self.ideologies = []

    @staticmethod
    def parse(inputstring):
        parsedfile = parsingfile(inputstring)

        export_obj = ideologyfile()

        for statement in parsedfile.statements:
            if statement.tag == "ideologies":
                for parsed_ideology in statement.values:
                    export_obj.ideologies.append(ideology.parse(parsed_ideology.tag, parsed_ideology.values))

        return export_obj

class ideology(game_object):
    def __init__(self, name="undefined"):
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

    @staticmethod
    def parse(ideology_name, inputvalues):
        export_obj = ideology(name=ideology_name)

        for value in inputvalues:
            if value.tag == "dynamic_faction_names":
                export_obj.dynamic_faction_names = value.values

            if value.tag == "color":
                export_obj.color = value.values

            if value.tag == "types":
                for sub_type in value.values:
                    export_obj.types.append(ideology_sub_type(sub_type.tag))

            if value.tag == "rules":
                for rule in value.values:
                    export_obj.rules.append(ideology_modifier(rule.tag, rule.values[0]))

            if value.tag == "can_host_government_in_exile" and value.values[0] == "yes":
                export_obj.can_host_exiles == True

            if value.tag == "war_impact_on_world_tension":
                export_obj.war_impact_on_wt = float(value.values[0])

            if value.tag == "faction_impact_on_world_tension":
                export_obj.faction_impact_on_wt == float(value.values[0])

            if value.tag == "modifiers":
                for substatement in value.values:
                    export_obj.modifiers.append(ideology_modifier(substatement.tag, substatement.values[0]))

            if value.tag == "faction_modifiers":
                if len(value.values) > 0:
                    for substatement in value.values:
                        if type(substatement) == statement:
                            export_obj.faction_modifiers.append(ideology_modifier(substatement.tag, substatement.values[0]))

            if value.tag[:2] == "ai":
                export_obj.ai_type = value.tag

        return export_obj



class ideology_sub_type(game_object):
    def __init__(self, name):
        self.name = name

class ideology_modifier(game_object):
    def __init__(self, itag, ivalue):
        self.tag = itag
        self.value = ivalue


### Hierarchy Slicer


#### Test

