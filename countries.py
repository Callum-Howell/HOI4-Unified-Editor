import re
from hoi4parser import *

class country():
    def __init__(self, maincountryinputstring, tag):
        self.tag = tag

        self.parsedfile = parsingfile(maincountryinputstring)

        self.oob ="Not Specified"
        self.capital = "Not Specified"
        self.stability = "Not Specified"
        self.research = "Not Specified"
        self.war_support ="Not Specified"
        self.technologies = []

        for statement in self.parsedfile.statements:
            if statement.tag == "capital":
                self.capital = statement.values[0]
            elif statement.tag == "oob":
                self.oob = statement.values[0]
            elif statement.tag == "set_research_slots":
                self.research = statement.values[0]
            elif statement.tag == "set_war_support":
                self.war_support = statement.values[0]
            elif statement.tag == "set_technology":
                for tech_statement in statement.values:
                    self.technologies.append(tech_statement)

#         capitalexpression = re.compile("capital.+=.[0-9]+")
#         oobexpression = re.compile("oob.+=.+\".+\"")
#         researchexpression = re.compile("set_research_slots.+=.+[0-9]+")
#         stabilityexpression = re.compile("set_stability.+=.+[0-9].[0-9]")
#         warsupportexpression = re.compile("set_war_support.+=.+[0-9].[0-9]")
#         technologyexpression = re.compile("set_technology", re.MULTILINE)
#
#         try:
#             self.oob = oobexpression.search(maincountryinputstring).group()
#         except:
#             self.oob = "Not Specified"
#         try:
#             self.capital = capitalexpression.search(maincountryinputstring).group()
#         except:
#             self.capital = "Not Specified"
#         try:
#             self.stability = stabilityexpression.search(maincountryinputstring).group()
#         except:
#             self.stability = "Not Specified"
#         try:
#             self.research = researchexpression.search(maincountryinputstring).group()
#         except:
#             self.research = "Not Specified"
#         try:
#             self.war_support = warsupportexpression.search(maincountryinputstring).group()
#         except:
#             self.war_support = "Not Specified"
#
#
#         self.techlist = []
#
#         techloc = technologyexpression.search(maincountryinputstring).end() + 3
#         techstring = hierarchyslice(maincountryinputstring, techloc)
#         indivtechfinder = re.compile("[^\t|\n|#|{|}].+=.+\w+")
#
#         for tech in indivtechfinder.finditer(techstring):
#             self.techlist.append(tech.group())
#
# ### Input Leaders
#
#         polleaderexpression = re.compile("[^#]create_country_leader = ")
#         corpsleaderexpression = re.compile("create_corps_commander = ")
#         fieldmarshallexpression = re.compile("create_field_marshal = ")
#
#         self.polleaders = []
#
#         for polleader in polleaderexpression.finditer(maincountryinputstring):
#             polstring = hierarchyslice(maincountryinputstring, polleader.end())
#             self.polleaders.append(country_leader(polstring))

class countrypolitics():
    def __init__(self, inputstring):
        self.rulingparty = None
        self.lastelection = None
        self.election_frequency = None
        self.elections_allowed = None

class country_leader():
    def __init__(self, inputstring):
        namexpression = re.compile("name.+")
        descexpression = re.compile("desc.+")
        pictureexpression = re.compile("picture.+")
        expireexpression = re.compile("expire.+")
        ideologyexpression = re.compile("ideology.+")
        traitsexpression = re.compile("traits = ")

        try:
            self.name = namexpression.search(inputstring).group()[8:-1]
        except:
            self.name = None
        try:
            self.desc = descexpression.search(inputstring).group()[8:-1]
        except:
            self.desc = None
        try:
            self.picture = pictureexpression.search(inputstring).group()[11:-1]
        except:
            self.picture = None
        try:
            self.expiry = expireexpression.search(inputstring).group()[10:-1]
        except:
            self.expiry = None
        try:
            self.ideology = ideologyexpression.search(inputstring).group()[11:]
        except:
            self.ideology = None

        self.traits = []
        traitfinder = re.compile("([a-z]|_)+")

        try:
            traitstring = hierarchyslice(inputstring, traitsexpression.search(inputstring).end())
            for trait in traitfinder.finditer(traitstring):
                print(trait.group())
                self.traits.append(trait.group())
        except:
            pass

class army_leader():
    def __init__(self, rank, inputstring):
        self.rank = rank


###

def hierarchyslice(string, start):
    processedstring = ""
    bracketcount = 0

    for character in string[start:]:
        if character == "\t":
            pass
        if character == "}":
            bracketcount = bracketcount - 1
        if character == "{":
            bracketcount += 1
        processedstring += character
        if bracketcount == 0:
            break


    return processedstring