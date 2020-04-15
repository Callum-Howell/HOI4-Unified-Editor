from events import *
import tkinter
from tkinter import ttk
import os
import re
from localisation import *
from PIL import Image, ImageTk
from ideologies import *
from countries import *


# Classes

class app():
    def __init__(self, master):
        self.master = master
        self.filelocater()

    def filelocater(self):
        self.filelocaterframe = tkinter.Frame(self.master)
        self.filelocaterframe.grid()

        loclabel = tkinter.Label(self.filelocaterframe, text="File Location:")
        loclabel.grid(row=0, column=0)
        self.locstring = tkinter.StringVar()
        locinput = tkinter.Entry(self.filelocaterframe, textvariable=self.locstring, width=100)
        locinput.insert(0, "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")
        locinput.grid(row=0, column=1)
        executebutton = tkinter.Button(self.filelocaterframe, text="Load Mod", command=self.loadmod)
        executebutton.grid(row=0, column=2)

    def loadmod(self):
        filelocation = self.locstring.get()
        self.filelocaterframe.destroy()
        self.progbar = tkinter.ttk.Progressbar(self.master, mode="indeterminate")
        self.progbar.grid()
        self.mod = modfile(filelocation)
        self.progbar.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.generateeventdisplay()
        self.addmenus()

    def generateeventdisplay(self):
        self.mainwindow.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.mainwindow.grid()
        eventdisplayinstance = eventdisplay(self.mainwindow, self)

    def generatecountrydisplay(self):
        self.mainwindow.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.mainwindow.grid()
        countrydisplayinstance = country_display(self.mainwindow, self)

    def generate_ideology_display(self):
        self.mainwindow.destroy()
        self.mainwindow = tkinter.Frame(self.master)
        self.mainwindow.grid()
        ideologydisplayinstance = ideology_display(self.mainwindow, self)

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


class ideology_display():
    def __init__(self, mainwindow, app):
        self.mainwindow = mainwindow
        self.app = app

        self.opsbar = opsbar(self.mainwindow, self.app, self.app.mod.ideology_list, "name")

        self.info_display = ideology_info(self.mainwindow, self.app, self.opsbar.selector.get())



class ideology_info():
    def __init__(self, infoframe, app, selection):
        self.infoframe = tkinter.Frame(infoframe)
        self.infoframe.grid(row=1, column=0, sticky="NSEW")

        for id_check in app.mod.ideology_list:
            if id_check.name == selection:
                    selected_ideology = id_check

        self.i_namedisplay = evardisplayframe(self.infoframe, "Name", selected_ideology.name, 0)


class country_display():
    def __init__(self, mainwindow, app):
        self.mainwindow = mainwindow
        self.app = app

        self.countrydisplayframe = tkinter.Frame(mainwindow)
        self.countrydisplayframe.grid()

        self.opsbar = opsbar(self, self.countrydisplayframe, self.app, self.app.mod.countrylist, "tag")

        self.infoframe = tkinter.Frame(self.countrydisplayframe)
        self.infoframe.grid(row=1, column=0)
        self.infodisplay = self.load(self.opsbar.selector.get())

    def load(self, choice):
        self.infoframe.destroy()
        self.infoframe = tkinter.Frame(self.countrydisplayframe)
        self.infoframe.grid(row=1, column=0)
        for country in self.app.mod.countrylist:
            if country.tag == choice:
                selectedcountry = country
        self.infodisplay = countryinfodisplay(self.infoframe, self.app, selectedcountry)


class opsbar():
    def __init__(self, master_object, displayframe, app, choice_source, ident_attr):
        self.app = app
        self.opsframe = tkinter.Frame(displayframe)
        self.displayframe = displayframe
        self.opsframe.grid(row=0, column=0)
        self.master_object = master_object

        vallist = []
        for choice in choice_source:
            vallist.append(getattr(choice, ident_attr))

        self.selector = tkinter.ttk.Combobox(self.opsframe, values=vallist)
        self.selector.insert(0, vallist[0])
        self.selector.grid(row=0, column=0)

        self.loadbutton = tkinter.Button(self.opsframe, text="Load", command=self.loadchoice)
        self.loadbutton.grid(row=0, column=1)

    def loadchoice(self):
        choice = self.selector.get()
        self.master_object.load(choice)


class countryinfodisplay():
    def __init__(self, displayframe, app, countrychoice):
        self.countrynotebook = tkinter.ttk.Notebook(displayframe)
        self.countrynotebook.grid()

        self.maininfoframe = tkinter.Frame(self.countrynotebook)
        self.countrynotebook.add(self.maininfoframe, text="Main")
        self.examplelabel = tkinter.Label(self.maininfoframe, text=countrychoice.tag)
        self.examplelabel.grid()

        ###

        self.techframe = tkinter.Frame(self.countrynotebook)
        self.countrynotebook.add(self.techframe, text="Technologies")

        ###

        self.leaderframe = tkinter.Frame(self.countrynotebook)
        self.countrynotebook.add(self.leaderframe, text="Leaders")

        ###

        self.oobframe = tkinter.Frame(self.countrynotebook)
        self.countrynotebook.add(self.oobframe, text="OOB")


class eventdisplay():
    def __init__(self, mainwindow, app):
        self.app = app
        self.mainwindow = mainwindow
        self.opsinstance = eventopsbar(self.mainwindow, app, self)

        self.varsubframe = tkinter.Frame(self.mainwindow)
        self.varsubframe.grid(row=1, column=0)

        self.eventselectorinstance = eventselectorbox(self.varsubframe, app, self, self.getloadedfile())
        self.eventinfoinstance = eventinfodisplay(self.varsubframe, self.getloadedfile().eventlist[0], self.app)

    def getloadedfile(self):
        loadedfile = self.opsinstance.returnfile()
        for eventfile in self.app.mod.eventfileslist:
            if eventfile.name == loadedfile:
                return eventfile

    def loadneweventfile(self):
        self.varsubframe.destroy()
        self.varsubframe = tkinter.Frame(self.mainwindow)
        self.varsubframe.grid(row=1, column=0)

        self.eventselectorinstance = eventselectorbox(self.varsubframe, app, self, self.getloadedfile())
        self.eventinfoinstance = eventinfodisplay(self.varsubframe, self.getloadedfile().eventlist[0], self.app)

    def loadinfo(self, event):
        self.varsubframe.destroy()
        self.varsubframe = tkinter.Frame(self.mainwindow)
        self.varsubframe.grid(row=1, column=0)

        self.eventselectorinstance = eventselectorbox(self.varsubframe, app, self, self.getloadedfile())
        self.eventinfoinstance = eventinfodisplay(self.varsubframe, event, self.app)


class eventopsbar():
    def __init__(self, master, app, eventdisplay):
        eventopsframe = tkinter.Frame(master)
        eventopsframe.grid(row=0, column=0, sticky="W")

        eventboxlabel = tkinter.Label(eventopsframe, text="Event File:")
        eventboxlabel.grid(row=0, column=0)

        vallist = []
        for eventfile in app.mod.eventfileslist:
            vallist.append(eventfile.name)

        self.selectedfile = tkinter.StringVar()
        self.fileselector = ttk.Combobox(eventopsframe, values=vallist, textvariable=self.selectedfile)
        self.fileselector.set(vallist[0])
        self.fileselector.grid(row=0, column=1)

        loadbutton = tkinter.Button(eventopsframe, text="Load", command=eventdisplay.loadneweventfile)
        loadbutton.grid(row=0, column=2)

    def returnfile(self):
        return self.fileselector.get()


class eventselectorbox():
    def __init__(self, master, app, eventdisplay, eventfile):
        eventselectorframe = tkinter.Frame(master)
        eventselectorframe.grid(row=0, column=0, sticky="NW")
        templabel = tkinter.Label(eventselectorframe, text="Events to go here")
        templabel.grid()

        eventlistlabel = tkinter.Label(eventselectorframe, text="Event List")
        eventlistlabel.grid(row=0, column=0)

        buttoncount = 1
        for event in eventfile.eventlist:
            newbutton = eventbutton(eventselectorframe, event, buttoncount, eventdisplay)
            buttoncount += 1


class eventbutton():
    def __init__(self, master, event, buttoncount, eventdisplay):
        self.evtdisplay = eventdisplay
        self.event = event
        buttoninstance = tkinter.Button(master, text=event.id, command=self.loadeventinfo)
        buttoninstance.grid(column=0, row=buttoncount, sticky="NSEW")

    def loadeventinfo(self):
        self.evtdisplay.loadinfo(self.event)


class eventinfodisplay():
    def __init__(self, master, event, app):
        self.app = app
        self.event = event

        self.eventnotebook = tkinter.ttk.Notebook(master)
        self.eventnotebook.grid(row=0, column=1)

        self.infodisplayframe = tkinter.Frame(self.eventnotebook)
        self.eventnotebook.add(self.infodisplayframe, text="Event Information")

        self.infopanels = tkinter.Frame(self.infodisplayframe, relief="groove", bd=3)
        self.infopanels.grid(row=0, column=0, sticky="NSEW")

        self.idframe = evardisplayframe(self.infopanels, "ID", event.id, 0)
        self.titleframe = evardisplayframe(self.infopanels, "Title", event.title, 1)

        self.descframe = evardisplayframe(self.infopanels, "Description", event.desc[0].text, 2)

        self.mtthframe = evardisplayframe(self.infopanels, "Mean Time to Happen", event.mtth, 3)

        #### Photo Display

        self.picturedisplayframe = tkinter.Frame(self.infodisplayframe, relief="groove", bd=3)
        self.picturedisplayframe.grid(row=0, column=1, sticky="NSEW")

        photostr = event.picture[4:]
        if photostr + ".dds" in os.listdir(app.mod.directory + "\gfx\event_pictures\\"):
            photoloc = (app.mod.directory + "\gfx\event_pictures\\" + photostr + ".dds")
            raweventphoto = Image.open(photoloc)
            displayphoto = ImageTk.PhotoImage(raweventphoto)

            self.photolabel = tkinter.Label(self.picturedisplayframe, image=displayphoto, background="black")
            self.photolabel.image = displayphoto
            self.photolabel.grid(row=0, column=0)

        else:
            self.photolabel = tkinter.Label(self.picturedisplayframe, text="Picture Not Found")
            self.photolabel.grid()

            self.picframe = evardisplayframe(self.picturedisplayframe, "Picture", event.picture, 1)

        #### Triggers Display

        self.triggerframe = tkinter.Frame(self.infodisplayframe, relief="groove", bd=3)
        self.triggerframe.grid(row=1, column=0, sticky="NSEW")

        self.triggeredbutton = tkinter.Radiobutton(self.triggerframe, text="Is Triggered Only")
        self.triggeredbutton.grid(row=0, column=0)

        #### Options Display

        self.optionsframe = tkinter.Frame(self.infodisplayframe, relief="groove", bd=3)
        self.optionsframe.grid(row=1, column=1, sticky="NSEW")

        self.templabel = tkinter.Label(self.optionsframe, text="OPTIONS GO HERE")
        self.templabel.grid()

        ### Locedit Page

        self.loceditpage = tkinter.Frame(self.eventnotebook)
        self.eventnotebook.add(self.loceditpage, text="Localisations")

        keycounter = [event.title]

        for desc in event.desc:
            keycounter.append(desc.text)

        self.titleLocEdit = loceditor(self.loceditpage, keycounter, app)

        #### Raw Text Page

        self.rawtextpage = tkinter.Frame(self.eventnotebook)
        self.eventnotebook.add(self.rawtextpage, text="Raw Text")

        self.rawtextedit = tkinter.Text(self.rawtextpage, width=100)
        self.rawtextedit.insert(0.0, event.rawtext)
        self.rawtextedit.grid()

    def titleeditor(self):
        titleeditdialog = loceditor(self.event.title, self.app)


class evardisplayframe():
    def __init__(self, master, varname, initvalue, order, *additional_widgets):
        self.displayframe = tkinter.Frame(master)
        self.displayframe.grid(row=order, column=0, sticky="E")

        self.varlabel = tkinter.Label(self.displayframe, text=varname)
        self.inputvariable = tkinter.StringVar()
        self.varlabel.grid(row=0, column=0, sticky="W")
        self.entrybox = tkinter.Entry(self.displayframe, textvariable=self.inputvariable)
        self.entrybox.insert(0, initvalue)
        self.entrybox.grid(row=0, column=1, sticky="E")


# noinspection PyTypeChecker
class loceditor():
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
            if localisations == None:
                localisations = "Loclookup failed"

            keylabel = tkinter.Label(self.loceditdialog, text=key, relief="groove")
            keylabel.grid(row=rowcounter, column=0, sticky="NSEW")

            eng_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            eng_entry.grid(row=rowcounter, column=1, sticky="NSEW")
            try:
                eng_entry.insert(0.0, localisations["english"])
            except:
                eng_entry.insert(0.0, "Text Not Found")

            fra_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            fra_entry.grid(row=rowcounter, column=2, sticky="NSEW")

            try:
                fra_entry.insert(0.0, localisations["french"])
            except:
                fra_entry.insert(0.0, "Text Not Found")

            ger_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            ger_entry.grid(row=rowcounter, column=3, sticky="NSEW")
            try:
                ger_entry.insert(0.0, localisations["german"])
            except:
                ger_entry.insert(0.0, "Text Not Found")

            spa_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            spa_entry.grid(row=rowcounter, column=4, sticky="NSEW")
            try:
                spa_entry.insert(0.0, localisations["spanish"])
            except:
                spa_entry.insert(0.0, "Text Not Found")

            pol_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            pol_entry.grid(row=rowcounter, column=5, sticky="NSEW")
            try:
                pol_entry.insert(0.0, localisations["polish"])
            except:
                pol_entry.insert(0.0, "Text Not Found")

            rus_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            rus_entry.grid(row=rowcounter, column=6, sticky="NSEW")
            try:
                rus_entry.insert(0.0, localisations["russian"])
            except:
                rus_entry.insert(0.0, "Text Not Found")

            por_entry = tkinter.Text(self.loceditdialog, width=20, height=5)
            por_entry.grid(row=rowcounter, column=7, sticky="NSEW")
            try:
                por_entry.insert(0.0, localisations["braz_por"])
            except:
                por_entry.insert(0.0, "Text Not Found")

            rowcounter += 1


class mtthbutton():
    def __init__(self, master, num):
        self.triggeredonly = tkinter.BooleanVar()
        self.radbutton = tkinter.Radiobutton(master, text="Triggered Only?", variable=self.triggeredonly)
        self.radbutton.grid(row=0, column=num)


class modfile():
    def __init__(self, directory):
        self.directory = directory
        self.eventfileslist = []
        self.ideology_list = []

        self.ideology_load()

        for eventfileloc in os.listdir(directory + "\events\\"):
            fileloc = directory + "\events" + "\\" + eventfileloc
            opener = open(fileloc, mode="r", encoding="utf-8-sig")
            rawfilestring = opener.read()

            self.eventfileslist.append(eventfile(rawfilestring, eventfileloc))

        self.locfileslist = []
        for locfileloc in os.listdir(directory + "\localisation\\"):
            fileloc = directory + "\localisation" + "\\" + locfileloc
            opener = open(fileloc, mode="r", encoding="utf-8-sig")
            rawfilestring = opener.read()

            self.locfileslist.append(localisationfile(rawfilestring, locfileloc))

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


def savecheck(func):
    pass


######


######

root = tkinter.Tk()

mainapp = app(root)

root.mainloop()
