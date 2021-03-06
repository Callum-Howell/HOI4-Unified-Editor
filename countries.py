from hoi4parser import *

class country(game_object):
    def __init__(self):
        self.tag = "Undefined"

        self.oob ="Not Specified"
        self.capital = "Not Specified"
        self.stability = "Not Specified"
        self.research = "Not Specified"
        self.war_support ="Not Specified"
        self.technologies = []

    @staticmethod
    def parse(maincountryinputstring, tag):
        export_obj = country()

        parsedfile = parsingfile(maincountryinputstring)

        for statement in parsedfile.statements:
            if statement.tag == "capital":
                export_obj.capital = statement.values[0]
            elif statement.tag == "oob":
                export_obj.oob = statement.values[0]
            elif statement.tag == "set_research_slots":
                export_obj.research = statement.values[0]
            elif statement.tag == "set_war_support":
                export_obj.war_support = statement.values[0]
            elif statement.tag == "set_technology":
                for tech_statement in statement.values:
                    export_obj.technologies.append(tech_statement)

        SCOPE_TEMPLATES[tag] = scope_template(tag, "Targets a specific country by tag", "FRA = { ... /}", True, False, "anywhere", "country", "1.0", True)

        return export_obj



class countrypolitics(game_object):
    def __init__(self):
        self.rulingparty = None
        self.lastelection = None
        self.election_frequency = None
        self.elections_allowed = None

class country_leader(game_object):
    def __init__(self):
        pass


class army_leader(game_object):
    def __init__(self, rank=[]):
        self.rank = rank


###

