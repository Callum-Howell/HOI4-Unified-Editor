import re
from hoi4parser import *


###Hoi4 Unified Editor

###classes

class event_file():
    def __init__(self, event_txt_file, filename):
        self.name = filename
        self.parsed_file = parsingfile(event_txt_file)

        self.name_spaces = []
        self.event_list = []

        for statement in self.parsed_file.statements:
            if statement.tag == "add_namespace":
                self.name_spaces.append(statement.values[0])

            elif statement.tag == "country_event" or statement.tag == "news_event" or statement.tag == "unit_leader_event" or statement.tag == "state_event":
                self.event_list.append(event(statement))

        print(self)

    def __len__(self):
        return len(self.event_list)

    def __repr__(self):
        return self.export()

    def export(self):
        exportstr = ""
        exportstr += "#" + self.name[:-4] + "\n\n"

        for name_space in self.name_spaces:
            exportstr += "add_namespace = " + name_space + "\n"


        for event in self.event_list:
            exportstr += event.export()

        return exportstr





class event():
    def __init__(self, inputstatement):

        self.eventtype = inputstatement.tag
        self.rawtext = ""

        self.id = "Not Specified"
        self.title = []
        self.desc = []
        self.picture = "Not Specified"
        self.options = []
        self.triggers = []
        self.mtth = "Not Specified"
        self.fireonlyonce = "Not Specified"
        self.triggered_only = False
        self.timeout = "Not Specified"
        self.fireforsender = "Not Specified"
        self.hidden = False
        self.exclusive = "Not Specified"
        self.major = "Not Specified"
        self.showmajor = "Not Specified"
        self.immediate = "Not Specified"

        for substatement in inputstatement.values:
            if substatement.tag == "id":
                self.id = substatement.values[0]
            elif substatement.tag == "title":
                self.title.append(title(substatement))
            elif substatement.tag == "desc":
                self.desc.append(event_description(substatement))
            elif substatement.tag == "picture":
                self.picture = substatement.values[0]
            elif substatement.tag == "option":
                self.options.append(option(substatement))
            elif substatement.tag == "trigger":
                for trigger_statement in substatement.values:
                    if trigger_statement == None:
                        pass

                    elif trigger_statement.tag in TRIGGER_TEMPLATE_DICT:
                        self.triggers.append(trigger(trigger_statement.tag,
                                                     trigger_statement.values,
                                                     trigger_statement.evaluator,
                                                     TRIGGER_TEMPLATE_DICT[trigger_statement]))
                    else:
                        self.triggers.append(nestable(trigger_statement.tag, trigger_statement.values, trigger_statement.evaluator))

            elif substatement.tag == "mean_time_to_happen":
                self.mtth = substatement.values[0]
            elif substatement.tag == "fire_only_once":
                self.fireonlyonce = substatement.values[0]
            elif substatement.tag == "is_triggered_only":
                if substatement.values[0] == "yes":
                    self.triggered_only = True
            elif substatement.tag == "timeout_days":
                self.timeout = substatement.values[0]
            elif substatement.tag == "fire_for_sender":
                self.fireforsender = substatement.values[0]
            elif substatement.tag == "hidden":
                if substatement.values[0] == "yes":
                    self.hidden = True
            elif substatement.tag == "exclusive":
                self.exclusive = substatement.values[0]
            elif substatement.tag == "major":
                self.major = substatement.values[0]
            elif substatement.tag == "show_major":
                self.showmajor = substatement.values[0]
#            elif substatement.tag == "immediate":
#                self.immediate = substatement.values[0]


        self.create_raw_text()

    def create_raw_text(self):
        self.rawtext = ""
        self.rawtext += self.eventtype + " = {\n\n"

        if self.id != "Not Specified":
            self.rawtext += "\tid = " + self.id + "\n"

        for title in self.title:
            title_text = title.export()
            for line in title_text.splitlines():
                self.rawtext += "\t" + line
            self.rawtext += "\t\n"

        for desc in self.desc:
            desc_text = desc.export()
            for line in desc_text.splitlines():
                self.rawtext += "\t" + line
            self.rawtext += "\t\n"

        if self.picture != "Not Specified":
            self.rawtext += "\tpicture = " + self.picture + "\n"

        if self.fireonlyonce != "Not Specified":
            self.rawtext += "\tfire_only_once = yes\n"

        if self.triggered_only != False:
            self.rawtext += "\tis_triggered_only = yes\n"

        if self.timeout != "Not Specified":
            self.rawtext += "\ttimeout_days = " + self.timeout + "\n"

        if self.fireforsender != "Not Specified":
            self.rawtext += "\tfire_for_sender = " + self.fireforsender + "\n"

        if self.hidden != False:
            self.rawtext += "\thidden = yes\n"

        if self.exclusive != "Not Specified":
            self.rawtext += "\texclusive = " + self.exclusive + "\n"

        if self.major != "Not Specified":
            self.rawtext += "\tmajor = " + self.major + "\n"

        if self.showmajor != "Not Specified":
            self.rawtext += "\tshow_major = TODO#INCOMPLETE\n"

        if self.immediate != "Not Specified":
            self.rawtext += "\timmediate = " + self.immediate + "\n"


        self.rawtext += "\n}\n"

    def export(self):
        self.create_raw_text()
        return self.rawtext

class option():
    def __init__(self, inputstatement):
        self.name = ""
        self.ai_chance = []
        self.effects = []
        self.empty_hidden = False
        self.original_recipient_only = False

        for substatement in inputstatement.values:
            if substatement is None:
                self.empty_hidden = True

            else:
                if substatement.tag == "name":
                    self.name = substatement.values[0]

                elif substatement.tag == "original_recipient_only":
                    self.original_recipient_only = True

                elif substatement.tag == "ai_chance":
                    for sub_nestable in substatement.values:
                        self.ai_chance.append(nestable(substatement.tag, substatement.evaluator, substatement.values))

                elif substatement.tag in SCOPE_TEMPLATE_DICT:
                    self.effects.append(scope(substatement.tag, substatement.evaluator, substatement.values, SCOPE_TEMPLATE_DICT[substatement.tag]))

                elif substatement.tag in TRIGGER_TEMPLATE_DICT:
                    self.effects.append(trigger(substatement.tag, substatement.evaluator, substatement.values, TRIGGER_TEMPLATE_DICT[substatement.tag]))

                elif substatement.tag in MODIFIER_TEMPLATE_DICT:
                    self.effects.append(modifier(substatement.tag, substatement.evaluator, substatement.values, MODIFIER_TEMPLATE_DICT[substatement.tag]))

                elif substatement.tag in COMMAND_TEMPLATE_DICT:
                    self.effects.append(command(substatement.tag, substatement.evaluator, substatement.values, COMMAND_TEMPLATE_DICT[substatement.tag]))
                else:
                    self.effects.append(nestable(substatement.tag, substatement.evaluator, substatement.values))






class event_description():
    def __init__(self, inputstatement):
        self.trigger = None
        for substatement in inputstatement.values:
            if type(substatement) == statement:
                if substatement.tag == "text":
                    self.text = substatement.values[0]
                elif substatement.tag == "trigger":
                    self.trigger = substatement.values[0]
            else:
                self.text = substatement

    def __repr__(self):
        return self.export()

    def export(self):
        exportstr = ""
        if type(self.trigger) is None:
            exportstr += "desc = " + self.text

        else:
            exportstr += "desc = {\n\n"

            exportstr += "text = " + self.text + "\n"
            exportstr += "trigger = TO BE COMPLETED\n"

            exportstr += "\n}\n"

        return exportstr



class title():
    def __init__(self, inputstatement):
        for substatement in inputstatement.values:
            if type(substatement) == statement:
                if substatement.tag == "text":
                    self.text = substatement.values[0]
                elif substatement.tag == "trigger":
                    self.trigger = substatement.values[0]
            else:
                self.text = substatement
                self.trigger = None

    def __repr__(self):
        return self.export()

    def export(self):
        exportstr = ""
        if self.trigger is None:
            exportstr += "title = " + self.text

        else:
            exportstr += "title = {\n\n"

            exportstr += "TO BE COMPLETED"

            exportstr += "\n}\n"

        return exportstr

class mean_time_to_happen:
    def __init__(self, base, modifier_list):
        self.base = base
        self.modifiers = modifier_list

    def __repr__(self):
        return self.export()

    def export(self):
        pass

    @staticmethod
    def parser(input_statement):
        export_object = mean_time_to_happen(0, [])

        for statement in input_statement.values:

            if statement.tag == "base" or "days":
                export_object.base = int(statement.values[0])
            if statement.tag == "months":
                export_object.base = int(statement.values[0]) * 30
            if statement.tag == "years":
                export_object.base = int(statement.values[0]) * 365
            if statement.tag == "modifier":
                export_object.modifiers.append(mtth_modifier.parser(statement))


        return export_object


class mtth_modifier:
    def __init__(self, factor, trigger_list):
        self.factor = factor
        self.trigger_list = trigger_list

    @staticmethod
    def parser(input_statement):
        export_object = mean_time_to_happen(0, [])

        for statement in input_statement.values:
            if statement.tag == "factor":
                export_object.factor = input_statement.values[0]

            elif statement.tag in SCOPE_TEMPLATE_DICT:
                export_object.trigger_list.append(scope(statement.tag, statement.evaluator, statement.values, SCOPE_TEMPLATE_DICT[statement.tag]))

            elif statement.tag in TRIGGER_TEMPLATE_DICT:
                export_object.trigger_list.append(trigger(statement.tag, statement.evaluator, statement.values, TRIGGER_TEMPLATE_DICT[statement.tag]))

            elif statement.tag in MODIFIER_TEMPLATE_DICT:
                export_object.trigger_list.append(modifier(statement.tag, statement.evaluator, statement.values, MODIFIER_TEMPLATE_DICT[statement.tag]))

            elif statement.tag in COMMAND_TEMPLATE_DICT:
                export_object.trigger_list.append(command(statement.tag, statement.evaluator, statement.values, COMMAND_TEMPLATE_DICT[statement.tag]))
            else:
                export_object.trigger_list.append(nestable(statement.tag, statement.evaluator, statement.values))

        return export_object