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
        return self.name

    def __iter__(self):
        for event in self.event_list:
            yield event

    def __getitem__(self, item):
        return self.event_list[item]

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
        self.immediate = None

    @staticmethod
    def parse(inputstatement):
        export_obj = event()
        export_obj.eventtype = inputstatement.tag

        for substatement in inputstatement.values:
            if substatement.tag == "id":
                export_obj.id = substatement.values[0]
            elif substatement.tag == "title":
                export_obj.title.append(title.parse(substatement))
            elif substatement.tag == "desc":
                export_obj.desc.append(event_description.parse(substatement))
            elif substatement.tag == "picture":
                export_obj.picture = substatement.values[0]
            elif substatement.tag == "option":
                export_obj.options.append(option.parse(substatement))
            elif substatement.tag == "trigger":
                for trigger_statement in substatement.values:
                    if trigger_statement == None:
                        pass
                    else:
                        export_obj.triggers.append(nestable.parse(trigger_statement))

            elif substatement.tag == "mean_time_to_happen":
                export_obj.mtth = mean_time_to_happen.parser(substatement)
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
            elif substatement.tag == "immediate":
                export_obj.immediate = option.parse(inputstatement)


        export_obj.create_raw_text()

        return export_obj

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

#        if self.immediate != "Not Specified":
#            tempstr = str(self.immediate)
#            self.rawtext += "\timmediate = " + tempstr + "\n"


        self.rawtext += "\n}\n"

    def __str__(self):
        return self.id

    def __repr__(self):
        return "[E]" + self.id

    def export(self):
        self.create_raw_text()
        return self.rawtext

class option():
    def __init__(self, name="", ai_chance=[],effects=[],empty_hidden=False,original_recipient_only=False):
        self.name = name
        self.ai_chance = ai_chance
        self.effects = effects
        self.empty_hidden = empty_hidden
        self.original_recipient_only = original_recipient_only

    def __str__(self):
        return self.name

    def __repr__(self):
        return "[O]" + self.name

    @staticmethod
    def parse(inputstatement):
        export_obj = option()

        effects_list = []
        for substatement in inputstatement.values:
            if substatement is None:
                export_obj.empty_hidden = True

            else:
                if substatement.tag == "name":
                    export_obj.name = substatement.values[0]

                elif substatement.tag == "original_recipient_only":
                    export_obj.original_recipient_only = True

                elif substatement.tag == "ai_chance":
                    chance_list = []
                    for sub_nestable in substatement.values:
                        if sub_nestable is None:
                            pass
                        else:
                            chance_statement = nestable.parse(sub_nestable)
                            chance_list.append(chance_statement)
                    export_obj.ai_chance = chance_list

                else:
                    effects_list.append(nestable.parse(substatement))
        export_obj.effects = effects_list

        return export_obj



class event_description():
    def __init__(self, text="not specified", trigger_list=[]):
        self.text = text
        self.trigger_list = trigger_list



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
        if type(self.trigger_list) is None:
            exportstr += "desc = " + self.text
        else:
            exportstr += "desc = {\n\n"
            exportstr += "text = " + self.text + "\n"
            exportstr += "trigger = TO BE COMPLETED"
            exportstr += "\n}\n"
        return exportstr



class title():
    def __init__(self, text="not specified", trigger_list=[]):
        self.text = text
        self.trigger_list = trigger_list

    def export(self):
        exportstr = ""
        if self.trigger_list is None:
            exportstr += "title = " + self.text
        else:
            exportstr += "title = {\n\n"
            exportstr += "TO BE COMPLETED"
            exportstr += "\n}\n"

        return exportstr

    @staticmethod
    def parse(input_statement):

        export_obj = title("", [])

        for substatement in input_statement.values:
            if type(substatement) == statement:
                if substatement.tag == "text":
                    export_obj.text = substatement.values[0]
                elif substatement.tag == "trigger":
                    export_obj.trigger_list.append(nestable.parse(substatement))
            else:
                export_obj.text = substatement
                export_obj.trigger = None

        return export_obj


class mean_time_to_happen:
    def __init__(self, base=0, modifier_list=[]):
        self.base = base
        self.modifiers = modifier_list

    def export(self):
        print("MTTH = UNFINISHED")

    @staticmethod
    def parser(input_statement):
        export_obj = mean_time_to_happen()

        modifier_list = []

        for statement in input_statement.values:


            if statement.tag == "base" or statement.tag == "days":
                export_obj.base = int(statement.values[0])
            if statement.tag == "months":
                export_obj.base = int(statement.values[0]) * 30
            if statement.tag == "years":
                export_obj.base = int(statement.values[0]) * 365
            if statement.tag == "modifier":
                modifier_list.append(mtth_modifier.parse(statement))

        export_obj.modifiers = modifier_list

        return export_obj


class mtth_modifier:
    def __init__(self, factor=0, trigger_list=[]):
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
    def parse(input_statement):
        export_object = mtth_modifier()

        for statement in input_statement.values:
            if statement.tag == "factor":
                export_object.factor = input_statement.values[0]
            else:
                export_object.trigger_list.append(nestable.parse(statement))

        return export_object