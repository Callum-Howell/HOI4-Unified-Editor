from events import *
import os
from localisation import *
from ideologies import *
from countries import *

class mod_file:
    def __init__(self, directory):
        self.directory = directory
        self.event_files_dict = {}
        self.ideology_dict = {}
        self.country_dict = {}

        self.ideology_load()

        self.countryload()

        for eventfileloc in os.listdir(directory + "\events\\"):
            fileloc = directory + "\events" + "\\" + eventfileloc
            opener = open(fileloc, mode="r", encoding="utf-8-sig")
            rawfilestring = opener.read()

            temp_file = event_file.parse(rawfilestring, eventfileloc)
            self.event_files_dict[temp_file.name] = temp_file

        self.locfileslist = []
        for locfileloc in os.listdir(directory + "\localisation\\"):
            fileloc = directory + "\localisation" + "\\" + locfileloc
            opener = open(fileloc, mode="r", encoding="utf-8-sig")
            rawfilestring = opener.read()

            self.locfileslist.append(localisation_file(rawfilestring, locfileloc))


    def loclookup(self, key):
        langdict = {}
        for locfile in self.locfileslist:
            if key in locfile.loc_dict:
                langdict[locfile.file_lang] = locfile.loc_dict[key]

        return langdict

    def ideology_load(self):
        if "common" in os.listdir(self.directory):
            if "ideologies" in os.listdir(self.directory + "\common"):
                for idfile in os.listdir(self.directory + "\common\ideologies"):
                    id_directory = self.directory + "\common\ideologies\\" + idfile
                    opener = open(id_directory, mode="r", encoding="utf-8-sig")
                    rawfilestring = opener.read()
                    parsedideologies = ideologyfile.parse(rawfilestring)
                    for loaded_ideology in parsedideologies.ideologies:
                        self.ideology_dict[loaded_ideology.name] = loaded_ideology

    def countryload(self):
        tagloc = self.directory + "\common\country_tags\\"
        self.country_dict = {}
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
                        self.country_dict[countryfile[:3]] = country.parse(filereader, countryfile[:3])