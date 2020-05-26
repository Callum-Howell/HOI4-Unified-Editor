from events import *
import tkinter
from tkinter import ttk
import os
from localisation import *
from PIL import Image, ImageTk
from ideologies import *
from countries import *
import exceptions

# Classes

class app:
    def __init__(self, master):
        self.master = master
        self.filelocater()

    def filelocater(self):
        self.filelocaterframe = tkinter.Frame(self.master)
        self.filelocaterframe.grid()

        loc_label = tkinter.Label(self.filelocaterframe, text="File Location:")
        loc_label.grid(row=0, column=0)
        self.loc_string = tkinter.StringVar()
        loc_input = tkinter.Entry(self.filelocaterframe, textvariable=self.loc_string, width=100)
        loc_input.insert(0, "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")
        loc_input.grid(row=0, column=1)
        execute_button = tkinter.Button(self.filelocaterframe, text="Load Mod", command=self.loadmod)
        execute_button.grid(row=0, column=2)

    def loadmod(self):
        filelocation = self.loc_string.get()
        self.filelocaterframe.destroy()
        self.progbar = tkinter.ttk.Progressbar(self.master, mode="indeterminate")
        self.progbar.grid()
        self.mod = mod_file(filelocation)
        self.progbar.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.generateeventdisplay()
        self.addmenus()

    def generateeventdisplay(self):
        self.mainwindow.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.mainwindow.grid()
        eventdisplayinstance = event_editor_frame(self.mainwindow, self, self.mod.eventfileslist)

    def generatecountrydisplay(self):
        self.mainwindow.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.mainwindow.grid()
        countrydisplayinstance = country_editor_frame(self.mainwindow, self, self.mod.countrylist)

    def generate_ideology_display(self):
        self.mainwindow.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.mainwindow.grid()
        ideologydisplayinstance = ideology_editor_frame(self.mainwindow, self, self.mod.ideology_list)

    def addmenus(self):
        self.mainmenubar = tkinter.Menu(self.master)

        self.file_menu = tkinter.Menu(self.mainmenubar, tearoff=0)
        self.file_menu.add_command(label="Save to .Mod File")
        self.file_menu.add_command(label="Load from .Mod File")
        self.file_menu.add_command(label="Import HOI4 Mod")
        self.file_menu.add_command(label="Export as HOI4 Mod")
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        self.mainmenubar.add_cascade(label="File", menu=self.file_menu)

        self.event_menu = tkinter.Menu(self.mainmenubar, tearoff=0)
        self.event_menu.add_command(label="Events", command=self.generateeventdisplay)
        self.event_menu.add_command(label="Decisions")
        self.mainmenubar.add_cascade(label="Events", menu=self.event_menu)

        self.country_menu = tkinter.Menu(self.mainmenubar, tearoff=0)
        self.country_menu.add_command(label="Countries", command=self.generatecountrydisplay)
        self.country_menu.add_command(label="Cosmetic Tags")
        self.mainmenubar.add_cascade(label="Countries", menu=self.country_menu)

        self.common_menu = tkinter.Menu(self.mainmenubar, tearoff=0)
        self.common_menu.add_command(label="Localisation")
        self.common_menu.add_command(label="Ideologies", command=self.generate_ideology_display)
        self.mainmenubar.add_cascade(label="Common", menu=self.common_menu)

        self.master.config(menu=self.mainmenubar)


class editor_frame:
    def __init__(self, main_window, app, infolist, identifier):
        self.mainwindow = main_window
        self.app = app
        self.opsbar = ops_bar(self, self.mainwindow, self.app, infolist, identifier)

    def load(self, ideology_choice):
        del self.info_display
        self.info_display = ideology_info(self.mainwindow, self.app, self.opsbar.selector.get())


class base_info_frame:
    def __init__(self, editor_frame, app, selection):
        self.master = editor_frame
        self.info_frame = tkinter.Frame(self.master)
        self.info_frame.grid(row=1, column=0, sticky="NSEW")

    def refresh(self):
        self.info_frame.destroy()
        self.info_frame = tkinter.Frame(self.master)
        self.info_frame.grid(row=1, column=0, sticky="NSEW")


class ideology_editor_frame(editor_frame):
    def __init__(self, mainwindow, app, ideology_list):
        super().__init__(mainwindow, app, ideology_list, "name")
        self.info_display = ideology_info(self.mainwindow, self.app, self.opsbar.selector.get())


class ideology_info:
    def __init__(self, infoframe, app, selection):
        self.infoframe = tkinter.Frame(infoframe)
        self.infoframe.grid(row=1, column=0, sticky="NSEW")

        for id_check in app.mod.ideology_list:
            if id_check.name == selection:
                selected_ideology = id_check


class country_editor_frame(editor_frame):
    def __init__(self, mainwindow, app, country_list):
        super().__init__(mainwindow, app, country_list, "tag")

        self.info_frame = tkinter.Frame(self.mainwindow)
        self.info_frame.grid(row=1, column=0)
        self.info_display = self.load(self.opsbar.selector.get())

    def load(self, choice):
        self.info_frame.destroy()
        self.info_frame = tkinter.Frame(self.mainwindow)
        self.info_frame.grid(row=1, column=0)
        for country in self.app.mod.countrylist:
            if country.tag == choice:
                selectedcountry = country
        self.infodisplay = country_info_frame(self.info_frame, self.app, selectedcountry)


class ops_bar:
    def __init__(self, master_object, displayframe, app, choice_source, ident_attr):
        self.app = app
        self.opsframe = tkinter.Frame(displayframe, bd=3)
        self.displayframe = displayframe
        self.opsframe.grid(row=0, column=0, sticky="W")
        self.master_object = master_object

        vallist = []
        for choice in choice_source:
            vallist.append(getattr(choice, ident_attr))

        self.selector = tkinter.ttk.Combobox(self.opsframe, values=vallist)
        self.selector.insert(0, vallist[0])
        self.selector.grid(row=0, column=0)

        self.loadbutton = tkinter.Button(self.opsframe, text="Load", command=self.load_choice)
        self.loadbutton.grid(row=0, column=1)

    def load_choice(self):
        choice = self.selector.get()
        self.master_object.load(choice)

    def new_obj(self):
        pass

    def save_obj(self):
        pass

    def get(self):
        return self.selector.get()


class country_info_frame(base_info_frame):
    def __init__(self, displayframe, app, countrychoice):
        super().__init__(displayframe, app, countrychoice)

        self.country_notebook = tkinter.ttk.Notebook(self.info_frame)
        self.country_notebook.grid()

        self.main_info_frame = tkinter.Frame(self.country_notebook)
        self.country_notebook.add(self.main_info_frame, text="Main")
        self.example_label = tkinter.Label(self.main_info_frame, text=countrychoice.tag)
        self.example_label.grid()

        # Tech Display

        self.tech_frame = tkinter.Frame(self.country_notebook)
        self.country_notebook.add(self.tech_frame, text="Technologies")

        # Leader Display

        self.leader_frame = tkinter.Frame(self.country_notebook)
        self.country_notebook.add(self.leader_frame, text="Leaders")

        # OOB Display

        self.oob_frame = tkinter.Frame(self.country_notebook)
        self.country_notebook.add(self.oob_frame, text="OOB")


class event_editor_frame(editor_frame):
    def __init__(self, mainwindow, app, mod_event_files_list):
        super().__init__(mainwindow, app, mod_event_files_list, "name")
        self.app = app
        self.mainwindow = mainwindow


        self.sub_display_frame = tkinter.Frame(self.mainwindow)
        self.sub_display_frame.grid(row=0, column=0)

        self.load(mod_event_files_list[0].name)

    def load(self, choice_name):
        self.sub_display_frame.destroy()
        self.sub_display_frame = tkinter.Frame(self.mainwindow)
        self.sub_display_frame.grid(row=1, column=0)

        for event_file in self.app.mod.eventfileslist:
            if event_file.name == choice_name:
                selected_event_file = event_file
        self.info_frame = event_file_info_frame(self.sub_display_frame, selected_event_file, self.app)


class event_file_info_frame(base_info_frame):
    def __init__(self, master, event_file, app):
        super().__init__(master, app, event_file)

        self.loaded_event_file = event_file
        self.mapper = ui_mapper(self.loaded_event_file)

        self.event_selector = event_selector_box(self.info_frame, app, self, self.mapper)
        self.app = app



        self.event_notebook_frame = tkinter.Frame(self.info_frame)

        self.load(event_file.event_list[0])



    def load(self, selected_event):
        self.event_notebook_frame.destroy()

        self.displayed_event = selected_event
        self.event_notebook_frame = tkinter.Frame(self.info_frame)
        self.event_notebook_frame.grid(row=0, column=1, sticky="NSEW")

        self.event_notebook = ttk.Notebook(self.event_notebook_frame)
        self.event_notebook.grid()

        # Main Info

        self.basic_info_frame = tkinter.Frame(self.event_notebook)
        self.basic_info_frame.grid()

        self.id_label = tkinter.Label(self.basic_info_frame, text="ID")
        self.id_label.grid(row=0, column=0)

        self.event_notebook.add(self.basic_info_frame, text="Basic")

        # Triggers

        self.trigger_frame = tkinter.Frame(self.event_notebook)
        self.trigger_frame.grid()


        self.event_notebook.add(self.trigger_frame, text="Triggers")

        # options

        self.options_frame = tkinter.Frame(self.event_notebook)
        self.options_frame.grid()


        self.event_notebook.add(self.options_frame, text="Options")

        # Localisations

        self.localisations_frame = tkinter.Frame(self.event_notebook)

        event_keys = []

        for event_key in self.mapper["event_list"][self.event_selector.selection]["title"]:
            event_keys.append(event_key["text"])
        for event_key in self.mapper["event_list"][self.event_selector.selection]["desc"]:
            event_keys.append(event_key["text"])
        for event_key in self.mapper["event_list"][self.event_selector.selection]["options"]:
            event_keys.append(event_key["name"])

        self.loc_editor = localisation_editor(self.localisations_frame, event_keys, self.app)

        self.localisations_frame.grid()


        self.event_notebook.add(self.localisations_frame, text="Localisations")

        # Raw Text

class event_selector_box:
    def __init__(self, master, app, eventdisplay, mapper):

        self.master = master
        self.eventdisplay = eventdisplay

        self.mapper = mapper
        self.selection = 0

        self.eventselectorframe = tkinter.Frame(master, bd=3, relief=tkinter.RAISED)
        self.eventselectorframe.grid(row=0, column=0, sticky="NW")

        self.list_label = tkinter.Label(self.eventselectorframe, text="Event List")
        self.list_label.grid(row=0, column=0)

        self.selector_box = tkinter.Listbox(self.eventselectorframe, selectmode=tkinter.SINGLE)
        self.selector_box.grid(row=1, column=0)

        self.event_control_box = tkinter.Frame(self.eventselectorframe)
        self.event_control_box.grid(row=2, column=0)

        self.new_event_button = tkinter.Button(self.event_control_box, text="New")
        self.new_event_button.grid(row=0, column=0)

        self.load_event_button = tkinter.Button(self.event_control_box, text="Load", command=self.load)
        self.load_event_button.grid(row=0, column=1)

        self.delete_event_button = tkinter.Button(self.event_control_box, text="Delete")
        self.delete_event_button.grid(row=0, column=2)


        for event_map in self.mapper["event_list"]:
            self.selector_box.insert(tkinter.END, event_map["id"])


    def load(self):
        if len(self.selector_box.curselection()) == 0:
            self.selection = 0
        else:
            self.selection = self.selector_box.curselection()[0]

        self.eventdisplay.load(self.mapper["event_list"][self.selection])


class localisation_editor:
    def __init__(self, master, keys, app):
        self.loceditdialog = tkinter.Frame(master)
        self.loceditdialog.grid()

        self.keys = keys

        rowcounter = 0

        self.englabel = tkinter.Label(self.loceditdialog, text="English", relief="groove")
        self.englabel.grid(row=0, column=1, sticky="NSEW")

        self.fralabel = tkinter.Label(self.loceditdialog, text="French", relief="groove")
        self.fralabel.grid(row=0, column=2, sticky="NSEW")

        self.gerlabel = tkinter.Label(self.loceditdialog, text="German", relief="groove")
        self.gerlabel.grid(row=0, column=3, sticky="NSEW")

        self.spalabel = tkinter.Label(self.loceditdialog, text="Spanish", relief="groove")
        self.spalabel.grid(row=0, column=4, sticky="NSEW")

        self.pollabel = tkinter.Label(self.loceditdialog, text="Polish", relief="groove")
        self.pollabel.grid(row=0, column=5, sticky="NSEW")

        self.ruslabel = tkinter.Label(self.loceditdialog, text="Russian", relief="groove")
        self.ruslabel.grid(row=0, column=6, sticky="NSEW")

        self.porlabel = tkinter.Label(self.loceditdialog, text="Portuguese", relief="groove")
        self.porlabel.grid(row=0, column=7, sticky="NSEW")

        rowcounter = 1

        for key in self.keys:

            localisations = app.mod.loclookup(key)
            if localisations is None:
                localisations = "Loclookup failed"

            keylabel = tkinter.Label(self.loceditdialog, text=key, relief="groove")
            keylabel.grid(row=rowcounter, column=0, sticky="NSEW")

            eng_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            eng_entry.grid(row=rowcounter, column=1, sticky="NSEW")
            if "english" in localisations:
                eng_entry.insert(0.0, localisations["english"])
            else:
                eng_entry.insert(0.0, "Text Not Found")

            fra_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            fra_entry.grid(row=rowcounter, column=2, sticky="NSEW")

            if "french" in localisations:
                fra_entry.insert(0.0, localisations["french"])
            else:
                fra_entry.insert(0.0, "Text Not Found")

            ger_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            ger_entry.grid(row=rowcounter, column=3, sticky="NSEW")
            if "german" in localisations:
                ger_entry.insert(0.0, localisations["german"])
            else:
                ger_entry.insert(0.0, "Text Not Found")

            spa_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            spa_entry.grid(row=rowcounter, column=4, sticky="NSEW")
            if "spanish" in localisations:
                spa_entry.insert(0.0, localisations["spanish"])
            else:
                spa_entry.insert(0.0, "Text Not Found")

            pol_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            pol_entry.grid(row=rowcounter, column=5, sticky="NSEW")
            if "polish" in localisations:
                pol_entry.insert(0.0, localisations["polish"])
            else:
                pol_entry.insert(0.0, "Text Not Found")

            rus_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            rus_entry.grid(row=rowcounter, column=6, sticky="NSEW")
            if "russian" in localisations:
                rus_entry.insert(0.0, localisations["russian"])
            else:
                rus_entry.insert(0.0, "Text Not Found")

            por_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            por_entry.grid(row=rowcounter, column=7, sticky="NSEW")
            if "braz_por" in localisations:
                por_entry.insert(0.0, localisations["braz_por"])
            else:
                por_entry.insert(0.0, "Text Not Found")

            rowcounter += 1

class mod_file:
    def __init__(self, directory):
        self.directory = directory
        self.eventfileslist = []
        self.ideology_list = []

        self.ideology_load()

        for eventfileloc in os.listdir(directory + "\events\\"):
            fileloc = directory + "\events" + "\\" + eventfileloc
            opener = open(fileloc, mode="r", encoding="utf-8-sig")
            rawfilestring = opener.read()

            self.eventfileslist.append(event_file.parse(rawfilestring, eventfileloc))

        self.locfileslist = []
        for locfileloc in os.listdir(directory + "\localisation\\"):
            fileloc = directory + "\localisation" + "\\" + locfileloc
            opener = open(fileloc, mode="r", encoding="utf-8-sig")
            rawfilestring = opener.read()

            self.locfileslist.append(localisation_file(rawfilestring, locfileloc))

        self.countryload()

    def loclookup(self, key):
        langdict = {}
        for locfile in self.locfileslist:
            for loc in locfile.loc_dict.keys():
                if loc == key:
                    langdict[locfile.file_lang] = locfile.loc_dict[key]

        return langdict

    def ideology_load(self):
        if "common" in os.listdir(self.directory):
            if "ideologies" in os.listdir(self.directory + "\common"):
                for idfile in os.listdir(self.directory + "\common\ideologies"):
                    id_directory = self.directory + "\common\ideologies\\" + idfile
                    opener = open(id_directory, mode="r", encoding="utf-8-sig")
                    rawfilestring = opener.read()
                    parsedideologies = ideologyfile(rawfilestring)
                    for loaded_ideology in parsedideologies.ideologies:
                        self.ideology_list.append(loaded_ideology)

    def countryload(self):
        tagloc = self.directory + "\common\country_tags\\"
        self.countrylist = []
        for tagfile in os.listdir(tagloc):
            fileloc = tagloc + tagfile
            opener = open(fileloc, mode="r", encoding="utf-8")
            rawfilestring = opener.read()
            tagsearchexpression = re.compile("([A-Z]|[0-9]){3}.+=.+\"countries/.+.txt\"")
            filesearchexpression = re.compile("countries/.+.txt")

            for tagfind in tagsearchexpression.finditer(rawfilestring):
                tagfilestring = tagfind.group()
                for countryfile in os.listdir(self.directory + "\history\countries\\"):
                    if countryfile[:3] == tagfilestring[:3]:
                        fileloc = (self.directory + "\history\countries\\" + countryfile)
                        fileopener = open(fileloc, mode="r", encoding="utf-8-sig")
                        filereader = fileopener.read()
                        self.countrylist.append(country(filereader, countryfile[:3]))

class ui_mapper:
    def __init__(self, object):
        self.obj_type = type(object)
        self.attribute_mapper = {}

        for attribute_key, attribute_value in vars(object).items():
            if type(attribute_value) is bool:
                self.attribute_mapper[attribute_key] = tkinter.BooleanVar()
                self.attribute_mapper[attribute_key].set(attribute_value)

            elif type(attribute_value) is int:
                self.attribute_mapper[attribute_key] = tkinter.IntVar()
                self.attribute_mapper[attribute_key].set(attribute_value)

            elif type(attribute_value) is str:
                self.attribute_mapper[attribute_key] = tkinter.StringVar()
                self.attribute_mapper[attribute_key].set(attribute_value)

            elif type(attribute_value) is statement:
                raise exceptions.StatementError
            elif type(attribute_value) is list:
                input_list = []
                for list_variable in attribute_value:
                    if type(list_variable) == str or type(list_variable) == bool:
                        input_list.append(list_variable)
                    elif list_variable is None:
                        pass
                    else:
                        input_list.append(ui_mapper(list_variable))
                self.attribute_mapper[attribute_key] = input_list

    def __getitem__(self, item):
        selection = self.attribute_mapper[item]
        if type(selection) == tkinter.StringVar or type(selection) == tkinter.BooleanVar or type(selection) == tkinter.IntVar:
            return self.attribute_mapper[item].get()
        else:
            return self.attribute_mapper[item]

    def __setitem__(self, key, value):
        selection = self.attribute_mapper[key]
        if type(selection) == tkinter.StringVar or type(selection) == tkinter.BooleanVar or type(selection) == tkinter.IntVar:
            return self.attribute_mapper[key].set(value)
        else:
            return self.attribute_mapper[key].set(value)

    def create_new_object(self):
        export_object = self.obj_type()

        for attribute in self.attribute_mapper.items():
            print(attribute)
            if attribute[0] == "obj_type":
                pass
            elif type(attribute[1]) is list:
                input_list = []
                for value in attribute[1]:
                    if type(value) is ui_mapper:
                        input_list.append(value.create_new_object())
                    else:
                        input_list.append(value)
                setattr(export_object, attribute[0], input_list)
            elif type(attribute[1]) is ui_mapper:
                setattr(export_object, attribute[0], attribute[1].create_new_object())
            else:
                setattr(export_object, attribute[0], attribute[1])

        return export_object

def obj_check(a, c):
    for aval, cval in zip(vars(a), vars(c)):
        print(aval, getattr(a, aval), cval, getattr(c, cval))

def savecheck(func):
    pass

#

root = tkinter.Tk()

main_app = app(root)

root.mainloop()
