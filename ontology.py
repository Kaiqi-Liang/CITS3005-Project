import json
import re
from owlready2 import *

NAMESPACE = "https://handbooks.uwa.edu.au/"
onto = get_ontology(NAMESPACE)
with onto:

    class Unit(Thing):
        pass

    class Major(Thing):
        pass

    AllDisjoint([Unit, Major])

    class HasUnit(Major >> Unit):
        pass

    class HasSchool(Major >> str, FunctionalProperty):
        pass

    class HasBridging(Major >> Unit):
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

    class IsLevel(Unit >> int, FunctionalProperty):
        pass

    class DeliveryMode(Thing):
        pass

    class Online(DeliveryMode):
        pass

    class Face2Face(DeliveryMode):
        pass

    class Hybrid(DeliveryMode):
        pass

    class IsDeliveryMode(Unit >> DeliveryMode, FunctionalProperty):
        pass

    class UnitDisjunct(Thing):
        pass

    class UnitDisjunctContains(UnitDisjunct >> Unit):
        pass

    class HasPrerequisites(Unit >> UnitDisjunct):
        pass

    class HasCode(DataProperty, FunctionalProperty):
        domain = [Unit | Major]
        range = [str]

    class HasTitle(DataProperty, FunctionalProperty):
        domain = [Unit | Major]
        range = [str]

    class HasDescription(DataProperty, FunctionalProperty):
        domain = [Unit | Major]
        range = [str]

    class HasOutcome(DataProperty):
        domain = [Unit | Major]
        range = [str]

    class HasRequiredText(DataProperty):
        domain = [Unit | Major]
        range = [str]

    imp = Imp()
    imp.set_as_rule(
        "Major(?m), HasUnit(?m, ?u), HasOutcome(?u, ?o) -> HasOutcome(?m, ?o)"
    )
    imp.set_as_rule(
        "Major(?m), HasUnit(?m, ?u), HasRequiredText(?u, ?t) -> HasRequiredText(?m, ?t)"
    )
    imp.set_as_rule(
        "Unit(?u), HasPrerequisites(?u, ?d1), UnitDisjunctContains(?d1, ?p1), HasPrerequisites(?p1, ?d2), UnitDisjunctContains(?d2, ?p2) -> UnitDisjunctContains(?d1, ?p2)"
    )

    with open("units.json", "r") as units, open("majors.json", "r") as majors:
        units_json = json.load(units)
        for unit in units_json.values():
            code = unit["code"].strip()
            unit_instance = Unit(f"unitdetails?code={code}")
            unit_instance.HasCode = code
            unit_instance.IsLevel = int(unit["level"].strip())
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
                    if hours == 0:
                        # in case of the crawler failed to get a positive number of hours
                        continue
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
                    for prereq in unitset:
                        if prereq in units_json:
                            # if a prerequisite is a unit that does not exist do not add it
                            units_contained.append(Unit(f"unitdetails?code={prereq}"))
                    if len(units_contained) > 0:
                        # if none of the units exist do not create an empty unitset disjunct
                        unit_disjunct = UnitDisjunct()
                        unit_disjunct.UnitDisjunctContains = units_contained
                        unit_disjuncts.append(unit_disjunct)
                if len(unit_disjuncts) > 0:
                    unit_instance.HasPrerequisites = unit_disjuncts

            if "text" in unit:
                unit_instance.HasRequiredText = [text.strip() for text in unit["text"]]

        for major in json.load(majors).values():
            code = major["code"].strip()
            major_instance = Major(f"majordetails?code={code}")
            major_instance.HasCode = code

            major_instance.HasTitle = major["title"].strip()
            major_instance.HasDescription = major["description"].strip()
            major_instance.HasSchool = major["school"].strip()

            major_instance.HasUnit = [
                Unit(f"unitdetails?code={unit_code.strip()}")
                for unit_code in major["units"]
                if unit_code in units_json
            ]

            if "outcomes" in major:
                major_instance.HasOutcome = [
                    outcome.strip() for outcome in major["outcomes"]
                ]

            if "bridging" in major:
                major_instance.HasBridging = [
                    Unit(f"unitdetails?code={unit_code.strip()}")
                    for unit_code in major["bridging"]
                    if unit_code in units_json
                ]
