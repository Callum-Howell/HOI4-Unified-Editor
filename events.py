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

    def __len__(self):
        return len(self.event_list)


# class eventfile():
#     def __init__(self, eventfile, filename):
#         readyfile = self.despacer(eventfile)
#         self.name = filename
#         self.eventify(readyfile)
#
#
#
#     def despacer(self, file):
#         despacedstring = ""
#         for character in file:
#             if character == " ":
#                 pass
#
#             else:
#                 despacedstring += character
# #        print(despacedstring)
#         return despacedstring
#
#     def eventify(self, file):
#
# # First the namespace is isolated
#
#         namespaceexpression = re.compile("add_namespace=.+(#|)")
#         self.namespace = namespaceexpression.search(file).group()[14:]
#
# # Then the beginning each event is found
#
#         eventexpression = re.compile("(^country_event=|^news_event=|^unit_leader_event=|^state_event=)", re.MULTILINE)
#
#         filereader = file
#         eventstringlist = []
#         searcher = True
#         while searcher == True:
#             search = eventexpression.search(filereader)
#             try:
#                 evtstring = hierarchyslice(filereader, search.end())
#                 eventstringlist.append([evtstring, search.group()])
#                 filereader = filereader[search.end()+1:]
#             except:
#                 break
#
#
# # Finally, they are converted to event objects
#
#         self.eventlist = []
#         for eventstring in eventstringlist:
#             self.eventlist.append(event(eventstring[0], eventstring[1]))
#
#
#     def findevent(self, searchid):
#         for event in self.eventlist:
#             if event.id == searchid:
#                 return event
#

class event():
    def __init__(self, inputstatement):

        self.eventtype = inputstatement.tag
        self.rawtext = ""

        self.id = "Not Specified"
        self.title = "Not Specified"
        self.desc = []
        self.picture = "Not Specified"
        self.options = []
        self.triggers = []
        self.mtth = "Not Specified"
        self.fireonlyonce = "Not Specified"
        self.triggeredonce = False
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
                self.title = substatement.values[0]
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
                    self.triggeredonce = True
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
            elif substatement.tag == "immediate":
                self.immediate = substatement.values[0]


        self.create_raw_text()

    def create_raw_text(self):
        self.rawtext = ""
        self.rawtext += self.eventtype + " = {\n\n"

        self.rawtext += "\tid = " + self.id + "\n"
        # print(self.title)
        # self.rawtext += "\ttitle = " + self.title + "\n"

        self.rawtext += "}"

    def export(self):
        self.create_raw_text()
        return self.rawtext



# class event():
#     def __init__(self, inputstring, eventtype):
#         self.rawtext = eventtype + inputstring
#         idexpression = re.compile("id=.+")
#         titleexpression = re.compile("title=.+")
#         descexpression = re.compile("desc=.+")
#         pictureexpression = re.compile("picture=.+")
#         optionsexpression = re.compile("option=")
#         triggerexpression = re.compile("trigger=.+")
#         mtthexpression = re.compile("mean_time_to_happen=.+")
#         fireonceexpression = re.compile("fire_only_once=.+")
#
#         triggeredonlyexpression = re.compile("is_triggered_only.+")
#         timeoutexpression = re.compile("timeout_days=.+")
#         fireforsenderexpression = re.compile("fire_for_sender=.+")
#
#         hiddenexpression = re.compile("hidden=.+")
#         exclusiveexpression = re.compile("exclusive=.+")
#         majorexpression = re.compile("major=.+")
#         showmajorexpression = re.compile("show_major=.+")
#         immediateexpression =  re.compile("immediate=.+")
#
#         try:
#             self.id = idexpression.search(inputstring).group()[3:]
#         except:
#             self.id = "Null"
#         try:
#             self.title = titleexpression.search(inputstring).group()[6:]
#         except:
#             self.title = "Null"
#
#
#         self.desc = []
#         desciter = descexpression.finditer(inputstring)
#         for descrun in desciter:
#             descslice = hierarchyslice(inputstring, descrun.end())
#             self.desc.append(description(descslice))
#
#         try:
#             self.picture = pictureexpression.search(inputstring).group()[12:]
#         except:
#             self.picture = "Null"
#
#         try:
#             self.trigger = trigger(hierarchyslice(inputstring, triggerexpression.search(inputstring).end()))
#         except:
#             self.trigger = "Null"
#
#         try:
#             self.mtth = mtthexpression.search(inputstring).group()
#         except:
#             self.mtth = "Null"
#         try:
#             self.fireonlyonce = fireonceexpression.search(inputstring).group()
#         except:
#             self.fireonlyonce = "Null"
#         try:
#             self.triggeredonce = triggeredonlyexpression.search(inputstring).group()
#         except:
#             self.triggeredonce = "Null"
#         try:
#             self.timeout = timeoutexpression.search(inputstring).group()
#         except:
#             self.timeout = "Null"
#         try:
#             self.fireforsender = fireforsenderexpression.search(inputstring).group()
#         except:
#             self.fireforsender = "Null"
#         try:
#             self.hidden = hiddenexpression.search(inputstring).group()
#         except:
#             self.hidden = False
#         try:
#             self.exclusive = exclusiveexpression.search(inputstring).group()
#         except:
#             self.exclusive = "Null"
#         try:
#             self.major = majorexpression.search(inputstring).group()
#         except:
#             self.major = "Null"
#         try:
#             self.show_major = showmajorexpression.search(inputstring).group()
#         except:
#             self.show_major = "Null"
#         try:
#             self.immediate = immediateexpression.search(inputstring).group()
#         except:
#             self.immediate = "Null"
#
#         self.options = []
#         optionsiter = optionsexpression.finditer(inputstring)
#         for optionrun in optionsiter:
#             optionslice = hierarchyslice(inputstring, optionrun.end())
#             self.options.append(option(optionslice))

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
        for substatement in inputstatement.values:
            if type(substatement) == statement:
                if substatement.tag == "text":
                    self.text = substatement.values[0]
                elif substatement.tag == "trigger":
                    self.trigger = substatement.values[0]
            else:
                self.text = substatement
                self.trigger = None


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


###Fuctions

def hierarchyslice(string, start):
    bracketcount = 0
    processedstring = ""
    for character in string[start:]:
        if character == "\t":
            pass
        if character == "}":
            bracketcount -= 1
        if character == "{":
            bracketcount += 1
        if bracketcount == 0:
            break
        processedstring += character

    return processedstring


def linefy(string):
    lineexpression = re.compile("\n.+")
    linelist = []
    for line in lineexpression.finditer(string):
        linelist.append(line.group())
    return linelist

###
