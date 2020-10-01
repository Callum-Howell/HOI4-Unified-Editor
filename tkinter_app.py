import tkinter
from tkinter import ttk
import os
from PIL import Image, ImageTk
from mod import *
import exceptions
import sqlite3

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
        execute_button = tkinter.Button(self.filelocaterframe, text="Load Mod", command=self.load_from_base_files)
        execute_button.grid(row=0, column=2)

    def load_from_base_files(self):
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
        self.mainwindow = tkinter.Frame(self.master, bd=5)
        self.mainwindow.grid(sticky="NSEW")
        eventdisplayinstance = event_editor_frame(self.mainwindow, self, self.mod.event_files_dict)

    def generatecountrydisplay(self):
        self.mainwindow.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.mainwindow.grid()
        countrydisplayinstance = country_editor_frame(self.mainwindow, self, self.mod.country_dict)

    def generate_ideology_display(self):
        self.mainwindow.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.mainwindow.grid()
        ideologydisplayinstance = ideology_editor_frame(self.mainwindow, self, self.mod.ideology_dict)

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
    def __init__(self, main_window, app, infolist):
        self.mainwindow = main_window
        self.app = app
        self.opsbar = ops_bar(self, self.mainwindow, self.app, infolist)

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
        super().__init__(mainwindow, app, ideology_list)
        self.info_display = ideology_info(self.mainwindow, self.app, self.opsbar.selector.get())


class ideology_info:
    def __init__(self, infoframe, app, selection):
        self.infoframe = tkinter.Frame(infoframe)
        self.infoframe.grid(row=1, column=0, sticky="NSEW")


class country_editor_frame(editor_frame):
    def __init__(self, mainwindow, app, country_list):
        super().__init__(mainwindow, app, country_list)

        self.info_frame = tkinter.Frame(self.mainwindow)
        self.info_frame.grid(row=1, column=0)
        self.info_display = self.load(self.opsbar.selector.get())

    def load(self, choice):
        self.info_frame.destroy()
        self.info_frame = tkinter.Frame(self.mainwindow)
        self.info_frame.grid(row=1, column=0)

        self.infodisplay = country_info_frame(self.info_frame, self.app, self.app.mod.country_dict[choice])


class ops_bar:
    def __init__(self, master_object, displayframe, app, choice_source):
        self.app = app
        self.opsframe = tkinter.Frame(displayframe, bd=3)
        self.displayframe = displayframe
        self.opsframe.grid(row=0, column=0, sticky="W")
        self.master_object = master_object

        vallist = []
        for choice in choice_source:
            vallist.append(choice)

        self.selector = tkinter.ttk.Combobox(self.opsframe, values=vallist)
        self.selector.insert(0, vallist[0])
        self.selector.grid(row=0, column=0)

        self.new_button = tkinter.Button(self.opsframe, text="New", command=self.new_file)
        self.new_button.grid(row=0, column=1)

        self.load_button = tkinter.Button(self.opsframe, text="Load", command=self.load_choice)
        self.load_button.grid(row=0, column=3)

        self.save_button = tkinter.Button(self.opsframe, text="Save", command=self.save_choice)
        self.save_button.grid(row=0, column=2)

        self.rename_button = tkinter.Button(self.opsframe, text="Re-Name", command=self.rename_file)
        self.rename_button.grid(row=0, column=4)

        self.preview_button = tkinter.Button(self.opsframe, text="Preview", command=self.preview_file)
        self.preview_button.grid(row=0, column=5)

    def load_choice(self):
        choice = self.selector.get()
        self.master_object.load(choice)

    def new_file(self):
        self.master_object.new()

    def rename_file(self):
        self.master_object.rename()

    def save_choice(self):
        choice = self.selector.get()
        self.master_object.save(choice)

    def preview_file(self):
        pass

    def get(self):
        return self.selector.get()

    def preview(self):
        self.master_object.preview()


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
    def __init__(self, mainwindow, app, mod_event_files_dict):
        super().__init__(mainwindow, app, mod_event_files_dict)
        self.app = app
        self.mainwindow = mainwindow


        self.sub_display_frame = tkinter.Frame(self.mainwindow)
        self.sub_display_frame.grid(row=0, column=0, sticky="NSEW")

        self.load([*mod_event_files_dict][0])

    def load(self, choice_name):
        self.sub_display_frame.destroy()
        self.sub_display_frame = tkinter.Frame(self.mainwindow)
        self.sub_display_frame.grid(row=1, column=0)

        for event_file in self.app.mod.event_files_dict:
            if event_file == choice_name:
                selected_event_file = self.app.mod.event_files_dict[event_file]

        self.mapper = ui_mapper(selected_event_file)

        self.info_frame = event_file_info_frame(self.sub_display_frame, selected_event_file, self.app, self.mapper)

    def new(self):
        pass

    def save(self, choice_name):
        self.app.mod.event_files_dict[choice_name] = self.mapper.create_new_object()
        self.load([*self.app.mod.event_files_dict][0])



class event_file_info_frame(base_info_frame):
    def __init__(self, master, event_file, app, mapper):
        super().__init__(master, app, event_file)

        self.loaded_event_file = event_file
        self.mapper = mapper

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
        self.event_notebook.grid(sticky="NSEW")

        # Main Info

        self.basic_info_frame = tkinter.Frame(self.event_notebook, bd=3)
        self.basic_info_frame.grid()

        self.id_box = text_var_entry(self.basic_info_frame, "ID", self.mapper["event_list"][self.event_selector.selection]["id"], 0)


        # Titles

        self.title_frame = tkinter.LabelFrame(self.basic_info_frame, bd=1, relief="solid", text="Titles")
        self.title_frame.grid(row=1, column=0)

        rowcount = 0
        for title in self.mapper["event_list"][self.event_selector.selection]["title"]:
            title_box = text_var_entry(self.title_frame, rowcount, title["text"], rowcount)
            rowcount += 1

        self.event_notebook.add(self.basic_info_frame, text="Basic")

        # Triggers

        self.trigger_frame = tkinter.Frame(self.event_notebook)
        self.trigger_frame.grid()

        self.triggered_only_button = tkinter.Checkbutton(self.trigger_frame, text="Is Triggered Only", variable=self.mapper["event_list"][self.event_selector.selection]["triggered_only"])
        self.triggered_only_button.grid(row=0, column=0)

        self.static_trigger_frame = tkinter.LabelFrame(self.trigger_frame, text="Exclusive Triggers", bd=1, relief="solid")
        self.static_trigger_frame.grid(row=1, column=0)

        self.mtth_frame = tkinter.LabelFrame(self.trigger_frame, text="Mean Time To Happen", bd=1,
                                                       relief="solid")
        self.mtth_frame.grid(row=2, column=0)

        self.base_editor = int_var_entry(self.mtth_frame, "Base", self.mapper["event_list"][self.event_selector.selection]["mtth"], 0)


        self.event_notebook.add(self.trigger_frame, text="Triggers")

        # options

        self.options_frame = tkinter.Frame(self.event_notebook)
        self.options_frame.grid()


        self.event_notebook.add(self.options_frame, text="Options")

        # Localisations

        self.localisations_frame = tkinter.Frame(self.event_notebook)

        event_keys = []

        for event_key in self.mapper["event_list"][self.event_selector.selection]["title"]:
            event_keys.append(event_key["text"].get())
        for event_key in self.mapper["event_list"][self.event_selector.selection]["desc"]:
            event_keys.append(event_key["text"].get())
        for event_key in self.mapper["event_list"][self.event_selector.selection]["options"]:
            event_keys.append(event_key["name"].get())

        self.loc_editor = localisation_editor(self.localisations_frame, event_keys, self.app)

        self.localisations_frame.grid()


        self.event_notebook.add(self.localisations_frame, text="Localisations")

        # Raw Text

        self.raw_text_frame = tkinter.Frame(self.event_notebook)

        self.raw_text_box = tkinter.Text(self.raw_text_frame)
        self.raw_text_box.insert(0.0, self.mapper["event_list"][self.event_selector.selection]["rawtext"].get())
        self.raw_text_box.grid()

        self.event_notebook.add(self.raw_text_frame, text="Raw Text")

    def new_event(self):
        pass



class event_selector_box:
    def __init__(self, master, app, eventdisplay, mapper):

        self.master = master
        self.eventdisplay = eventdisplay

        self.mapper = mapper
        self.selection = 0

        self.eventselectorframe = tkinter.Frame(master, bd=3, relief=tkinter.RAISED)
        self.eventselectorframe.grid(row=0, column=0, sticky="NSEW")

        self.list_label = tkinter.Label(self.eventselectorframe, text="Event List")
        self.list_label.grid(row=0, column=0)

        self.selector_box = tkinter.Listbox(self.eventselectorframe, selectmode=tkinter.BROWSE)
        self.selector_box.grid(row=1, column=0, sticky="NS")

        self.event_control_box = tkinter.Frame(self.eventselectorframe)
        self.event_control_box.grid(row=2, column=0)

        self.new_event_button = tkinter.Button(self.event_control_box, text="New")
        self.new_event_button.grid(row=0, column=0)

        self.load_event_button = tkinter.Button(self.event_control_box, text="Load", command=self.load)
        self.load_event_button.grid(row=0, column=1)

        self.delete_event_button = tkinter.Button(self.event_control_box, text="Delete")
        self.delete_event_button.grid(row=0, column=2)


        for event_map in self.mapper["event_list"]:
            self.selector_box.insert(tkinter.END, event_map["id"].get())

        self.selector_box.bind('<Double-Button>', self.load)

    def load(self, *args):
        if len(self.selector_box.curselection()) == 0:
            self.selection = 0
        else:
            self.selection = self.selector_box.curselection()[0]

        self.eventdisplay.load(self.mapper["event_list"][self.selection])

class tk_var_widgit:
    def __init__(self, master, label, var, rowcount):
        self.var_frame = tkinter.Frame(master)
        self.var_frame.grid(row=rowcount, column = 0)

        self.var_label = tkinter.Label(self.var_frame, text=label)
        self.var_label.grid(row=0, column=0)

        self.var = None

    def get(self):
        return self.var.get()

class text_var_entry(tk_var_widgit):
    def __init__(self, master, label, var, rowcount):
        super().__init__(master, label, var, rowcount)
        self.var = var
        self.text_entry = tkinter.Entry(self.var_frame, textvariable=self.var, width=30)
        self.text_entry.grid(row=0, column=1)

class bool_var_button(tk_var_widgit):
    def __init__(self, master, label, var, rowcount):
        super().__init__(master, label, var, rowcount)
        self.var = var

class int_var_entry(tk_var_widgit):
    def __init__(self, master, label, var, rowcount):
        super().__init__(master, label, var, rowcount)
        self.var = var
        self.int_entry = tkinter.Spinbox(self.var_frame, textvariable=self.var, width=30)
        self.int_entry.grid(row=0, column=1)

class nestable_editor:
    def __init__(self):
        pass

class nestable_frame:
    def __init__(self):
        pass

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

class ui_mapper:
    """The UI Mapper coordinates between a Tkinter window and and the python object it edits."""
    def __init__(self, object):
        """Takes an existing python object and creates a mirrored version with Tkinter variables for its attributes.

            Ints, Floats, Booleans, and Strings are represented with TkinterVars.

            Lists are kept, with contained objects converted.

            For all other classes, a sub-ui_mapper is created.
        """


        self.obj_type = type(object)
        self.attribute_mapper = {}
#        print(object)

        for attribute_key, attribute_value in vars(object).items():
            if attribute_value is None:
                self.attribute_mapper[attribute_key] = None
            elif type(attribute_value) is bool:
                self.attribute_mapper[attribute_key] = tkinter.BooleanVar()
                self.attribute_mapper[attribute_key].set(attribute_value)

            elif type(attribute_value) is int:
                self.attribute_mapper[attribute_key] = tkinter.IntVar()
                self.attribute_mapper[attribute_key].set(attribute_value)

            elif type(attribute_value) is str:
                self.attribute_mapper[attribute_key] = tkinter.StringVar()
                self.attribute_mapper[attribute_key].set(attribute_value)
                self.attribute_mapper[attribute_key].trace_add("write", null)

            elif type(attribute_value) is float:
                self.attribute_mapper[attribute_key] = tkinter.DoubleVar()
                self.attribute_mapper[attribute_key].set(attribute_value)

            elif type(attribute_value) is statement:
                print(attribute_key, attribute_value)
                raise exceptions.StatementError

            elif type(attribute_value) is list:
                input_list = []
                for list_variable in attribute_value:
                    if type(list_variable) == str or type(list_variable) == bool:
                        input_list.append(list_variable)
                    elif list_variable is None:
                        pass
                    elif issubclass(type(list_variable), game_object):
                        input_list.append(ui_mapper(list_variable))
                    else:
                        pass
                self.attribute_mapper[attribute_key] = input_list

            elif issubclass(type(attribute_value), game_object):
                self.attribute_mapper[attribute_key] = ui_mapper(attribute_value)

            else:
                pass

    def __getitem__(self, item):
        selection = self.attribute_mapper[item]
        if type(selection) == tkinter.StringVar or type(selection) == tkinter.BooleanVar or type(selection) == tkinter.IntVar:
            return self.attribute_mapper[item]
        else:
            return self.attribute_mapper[item]


    def create_new_object(self): 
        """Returns an object with the attributes that now exist"""

        export_object = self.obj_type()
        for attribute in self.attribute_mapper.items():
            if type(attribute[1]) is list:
                input_list = []
                for value in attribute[1]:
                    if type(value) is ui_mapper:
                        input_list.append(value.create_new_object())
                    else:
                        input_list.append(value)
                setattr(export_object, attribute[0], input_list)
            elif type(attribute[1]) is ui_mapper:
                setattr(export_object, attribute[0], attribute[1].create_new_object())
            elif type(attribute[1]) is tkinter.StringVar or type(attribute[1]) is tkinter.IntVar or type(attribute[1]) is tkinter.BooleanVar:
                setattr(export_object, attribute[0], attribute[1].get())
            else:
                setattr(export_object, attribute[0], attribute[1])

        return export_object

def null(var, index, mode):
    print(var, mode)

def obj_check(a, c):
    for aval, cval in zip(vars(a), vars(c)):
        print(aval, getattr(a, aval), cval, getattr(c, cval))

def savecheck(func):
    pass

#

root = tkinter.Tk()
#root.state("zoomed")

main_app = app(root)

root.mainloop()
