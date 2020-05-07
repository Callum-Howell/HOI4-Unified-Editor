import re
from hoi4parser import *


###Hoi4 Unified Editor

###classes

class event_file():
    def __init__(self, name="Unnamed"):
        self.name = name

        self.name_spaces = []
        self.event_list = []


    def __len__(self):
        return len(self.event_list)

    def __repr__(self):
        return "[event_file]" + self.name + "[\\event_file]"

    def __str__(self):
        return self.export()

    def export(self):
        exportstr = ""
        exportstr += "#" + self.name[:-4] + "\n\n"

        for name_space in self.name_spaces:
            exportstr += "add_namespace = " + name_space + "\n"


        for event in self.event_list:
            exportstr += event.export()

        return exportstr

    @staticmethod
    def parse(event_txt_file, filename):
        export_object = event_file()

        export_object.name = filename
        parsed_file = parsingfile(event_txt_file)
        export_object.name_spaces = []
        export_object.event_list = []
        for statement in parsed_file.statements:
            if statement.tag == "add_namespace":
                export_object.name_spaces.append(statement.values[0])
            elif statement.tag == "country_event" or statement.tag == "news_event" or statement.tag == "unit_leader_event" or statement.tag == "state_event":
                export_object.event_list.append(event.parse(statement))

        return export_object

class event():
    def __init__(self):

        self.eventtype = "Undefined"
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

    @staticmethod
    def parse(inputstatement):
        export_obj = event()
        export_obj.eventtype = inputstatement.tag

        for substatement in inputstatement.values:
            if substatement.tag == "id":
                export_obj.id = substatement.values[0]
            elif substatement.tag == "title":
                export_obj.title.append(title.parser(substatement))
            elif substatement.tag == "desc":
                export_obj.desc.append(event_description.parse(substatement))
            elif substatement.tag == "picture":
                export_obj.picture = substatement.values[0]
            elif substatement.tag == "option":
                export_obj.options.append(option(substatement))
            elif substatement.tag == "trigger":
                for trigger_statement in substatement.values:
                    if trigger_statement == None:
                        pass
                    elif trigger_statement.tag in TRIGGER_TEMPLATES:
                        export_obj.triggers.append(nestable.parse(trigger_statement))

            elif substatement.tag == "mean_time_to_happen":
                export_obj.mtth = substatement.values[0]
            elif substatement.tag == "fire_only_once":
                export_obj.fireonlyonce = substatement.values[0]
            elif substatement.tag == "is_triggered_only":
                if substatement.values[0] == "yes":
                    export_obj.triggered_only = True
            elif substatement.tag == "timeout_days":
                export_obj.timeout = substatement.values[0]
            elif substatement.tag == "fire_for_sender":
                export_obj.fireforsender = substatement.values[0]
            elif substatement.tag == "hidden":
                if substatement.values[0] == "yes":
                    export_obj.hidden = True
            elif substatement.tag == "exclusive":
                export_obj.exclusive = substatement.values[0]
            elif substatement.tag == "major":
                export_obj.major = substatement.values[0]
            elif substatement.tag == "show_major":
                export_obj.showmajor = substatement.values[0]
#            elif substatement.tag == "immediate":
#                export_obj.immediate = substatement.values[0]

        export_obj.create_raw_text()

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


                # elif substatement.tag in SCOPE_TEMPLATES:
                #     self.effects.append(scope(substatement.tag, substatement.evaluator, substatement.values, SCOPE_TEMPLATES[substatement.tag]))
                #
                # elif substatement.tag in TRIGGER_TEMPLATES:
                #     self.effects.append(trigger(substatement.tag, substatement.evaluator, substatement.values, TRIGGER_TEMPLATES[substatement.tag]))
                #
                # elif substatement.tag in MODIFIER_TEMPLATES:
                #     self.effects.append(modifier(substatement.tag, substatement.evaluator, substatement.values, MODIFIER_TEMPLATES[substatement.tag]))
                #
                # elif substatement.tag in COMMAND_TEMPLATES:
                #     self.effects.append(command(substatement.tag, substatement.evaluator, substatement.values, COMMAND_TEMPLATES[substatement.tag]))
                else:
                    self.effects.append(nestable.parse(substatement))



class event_description():
    def __init__(self, text, trigger):
        self.text = text
        self.trigger = trigger



    @staticmethod
    def parse(inputstatement):
        exp_obj = event_description("", [])
        for substatement in inputstatement.values:
            if type(substatement) == statement:
                if substatement.tag == "text":
                    exp_obj.text = substatement.values[0]
                elif substatement.tag == "trigger":
                    exp_obj.trigger = nestable.parse(substatement)
            else:
                exp_obj.text = substatement

        return exp_obj


    def export(self):
        exportstr = ""
        if type(self.trigger) is None:
            exportstr += "desc = " + self.text
        else:
            exportstr += "desc = {\n\n"
            exportstr += "text = " + self.text + "\n"
            exportstr += "trigger = TO BE COMPLETED"
            exportstr += "\n}\n"
        return exportstr



class title():
    def __init__(self, text, trigger_list):
        self.text = "not specified"
        self.trigger = []

    def export(self):
        exportstr = ""
        if self.trigger is None:
            exportstr += "title = " + self.text
        else:
            exportstr += "title = {\n\n"
            exportstr += "TO BE COMPLETED"
            exportstr += "\n}\n"

        return exportstr

    @staticmethod
    def parser(input_statement):

        export_object = title("", [])

        for substatement in input_statement.values:
            if type(substatement) == statement:
                if substatement.tag == "text":
                    export_object.text = substatement.values[0]
                elif substatement.tag == "trigger":
                    export_object.trigger = nestable.parse(substatement)
            else:
                export_object.text = substatement
                export_object.trigger = None

        return export_object


class mean_time_to_happen:
    def __init__(self, base, modifier_list):
        self.base = base
        self.modifiers = modifier_list



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


    def export(self):
        exportstr = "modifier = {\n"

        exportstr += "\tfactor = " + str(self.factor)
        for trigger in self.trigger_list:
            exportstr += "\t" + trigger.export()

        exportstr += "}\n"

        return exportstr

    @staticmethod
    def parser(input_statement):
        export_object = mean_time_to_happen(0, [])

        for statement in input_statement.values:
            if statement.tag == "factor":
                export_object.factor = input_statement.values[0]
            else:
                export_object.trigger_list.append(nestable.parse(statement))

        return export_object