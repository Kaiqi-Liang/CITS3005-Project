import json
import re
from owlready2 import *

onto = get_ontology("https://handbooks.uwa.edu.au/")
with onto:

    class Unit(Thing):
        pass

    class Major(Thing):
        pass

    class HasUnit(Major >> Unit):
        pass

    class HasSchool(Major >> str, FunctionalProperty):
        pass

    class Assessment(Thing):
        pass

    class Exam(Assessment):
        pass

    class Test(Assessment):
        pass

    class Assignment(Assessment):
        pass

    class Presentation(Assessment):
        pass

    class Participation(Assessment):
        pass

    class Practical(Assessment):
        pass

    class OtherAssessment(Assessment):
        pass

    class HasAssessment(Unit >> Assessment):
        pass

    class ContactHour(Thing):
        pass

    class Lecture(ContactHour):
        pass

    class Tutorial(ContactHour):
        pass

    class Lab(ContactHour):
        pass

    class Workshop(ContactHour):
        pass

    class FieldTrip(ContactHour):
        pass

    class Practice(ContactHour):
        pass

    class OtherContactHour(ContactHour):
        pass

    class HasContactHour(Unit >> ContactHour):
        pass

    class HasHours(ContactHour >> int, FunctionalProperty):
        pass

    class Level(Thing):
        pass

    class Level1(Level):
        pass

    class Level2(Level):
        pass

    class Level3(Level):
        pass

    class Level4(Level):
        pass

    class Level5(Level):
        pass

    class Level6(Level):
        pass

    class IsLevel(Unit >> Level, FunctionalProperty):
        pass

    class DeliveryMode(Thing):
        pass

    class Online(DeliveryMode):
        pass

    class Face2Face(DeliveryMode):
        pass

    class Hybrid(DeliveryMode):
        pass

    class HasCode(DataProperty, FunctionalProperty):
        domain = [Unit, Major]
        range = [str]

    class HasTitle(DataProperty, FunctionalProperty):
        domain = [Unit, Major]
        range = [str]

    class IsDeliveryMode(Unit >> DeliveryMode, FunctionalProperty):
        pass

    class UnitDisjunct(Thing):
        pass

    class UnitDisjuntContains(UnitDisjunct >> Unit):
        pass

    class HasPrerequisites(ObjectProperty):
        domain = [Unit, Major]
        range = [UnitDisjunct]

    class HasDescription(DataProperty, FunctionalProperty):
        domain = [Unit, Major]
        range = [str]

    class HasOutcome(Unit >> str):
        pass

    # Reuse the nodes for level
    level1 = Level1("level1")
    level2 = Level2("level2")
    level3 = Level3("level3")
    level4 = Level4("level4")
    level5 = Level5("level5")
    level6 = Level6("level6")

    with open("units.json", "r") as units, open("majors.json", "r") as majors:
        for unit in json.load(units).values():
            code = unit["code"].strip()
            unit_instance = Unit(f"unitdetails?code={code}")
            unit_instance.HasCode = code

            # Assign level for unit
            match int(unit["level"].strip()):
                case 1:
                    unit_instance.IsLevel = level1
                case 2:
                    unit_instance.IsLevel = level2
                case 3:
                    unit_instance.IsLevel = level3
                case 4:
                    unit_instance.IsLevel = level4
                case 5:
                    unit_instance.IsLevel = level5
                case 6:
                    unit_instance.IsLevel = level6
                case other:
                    raise ValueError("Level does not exist")

            unit_instance.HasTitle = unit["title"].strip()
            unit_instance.HasDescription = unit["description"].strip()

            if "online" in unit["delivery_mode"].lower():
                unit_instance.IsDeliveryMode = Online("online")
            elif "face" in unit["delivery_mode"].lower():
                unit_instance.IsDeliveryMode = Face2Face("face2face")
            else:
                unit_instance.IsDeliveryMode = Hybrid("hybrid")

            if "outcomes" in unit:
                unit_instance.HasOutcome = [
                    outcome.strip() for outcome in unit["outcomes"]
                ]

            # Cannot reuse the nodes for assessment as a unit might have multiple exams
            assessments = []
            for ast in unit["assessment"]:
                ast = ast.lower()
                if "exam" in ast or "final" in ast:
                    assessments.append(Exam())
                elif "test" in ast or "quiz" in ast or re.match("mid[- ]sem", ast):
                    assessments.append(Test())
                elif any(
                    search_term in ast
                    for search_term in ["report", "portfolio", "project", "assignment"]
                ):
                    assessments.append(Assignment())
                elif "presentation" in ast or "oral" in ast:
                    assessments.append(Presentation())
                elif "participation" in ast:
                    assessments.append(Participation())
                elif any(
                    search_term in ast
                    for search_term in ["prac", "trip", "site", "visit", "lab"]
                ):
                    assessments.append(Practical())
                else:
                    assessments.append(OtherAssessment())
            unit_instance.HasAssessment = assessments

            contact_hours = []
            if "contact" in unit:
                for cnt in unit["contact"]:
                    hours = int(unit["contact"][cnt].strip())
                    cnt = cnt.lower()
                    if "lec" in cnt:
                        lecture = Lecture()
                        lecture.HasHours = hours
                        contact_hours.append(lecture)
                    elif "workshop" in cnt or "seminar" in cnt or "studio" in cnt:
                        workshop = Workshop()
                        workshop.HasHours = hours
                        contact_hours.append(workshop)
                    elif "prac" in cnt:
                        practice = Practice()
                        practice.HasHours = hours
                        contact_hours.append(practice)
                    elif "tut" in cnt:
                        tut = Tutorial()
                        tut.HasHours = hours
                        contact_hours.append(tut)
                    elif "lab" in cnt:
                        lab = Lab()
                        lab.HasHours = hours
                        contact_hours.append(lab)
                    elif "field" in cnt or "site" in cnt:
                        field = FieldTrip()
                        field.HasHours = hours
                        contact_hours.append(field)
                    else:
                        other = OtherContactHour()
                        other.HasHours = hours
                        contact_hours.append(other)
                unit_instance.HasContactHour = contact_hours

            if "prerequisites_cnf" in unit:
                unit_disjuncts = []
                for unitset in unit["prerequisites_cnf"]:
                    units_contained = []
                    unit_disjunct = UnitDisjunct()
                    for prereq in unitset:
                        unit = Unit(f"unitdetails?code={prereq}")
                        units_contained.append(unit)
                    unit_disjunct.UnitDisjuntContains = units_contained
                    unit_disjuncts.append(unit_disjunct)
                unit_instance.HasPrerequisites = unit_disjuncts

        for major in json.load(majors).values():
            code = major["code"].strip()
            major_instance = Major(f"majordetails?code={code}")
            major_instance.HasCode = code

            major_instance.HasTitle = major["title"].strip()
            major_instance.HasDescription = major["description"].strip()
            major_instance.HasSchool = major["school"].strip()

            if "outcomes" in major:
                major_instance.HasOutcome = [
                    outcome.strip() for outcome in major["outcomes"]
                ]

            major_instance.HasUnit = [
                Unit(f"unitdetails?code={unit_code.strip()}")
                for unit_code in major["units"]
            ]

onto.save(file="handbook.xml", format="rdfxml")
graph = default_world.as_rdflib_graph()
