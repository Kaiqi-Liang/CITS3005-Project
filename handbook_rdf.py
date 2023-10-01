import json
import re
from rdflib import FOAF, BNode, Graph, Namespace, Literal, RDF

g = Graph()
handbook = Namespace("https://handbooks.uwa.edu.au/")

with open("units.json", "r") as units:
    for unit in json.load(units).values():
        code = handbook[f"unitdetails?code={unit['code']}"]

        g.add((code, RDF.type, handbook["unit"]))
        g.add((code, FOAF.name, Literal(unit["title"].strip())))
        g.add((code, handbook["level"], Literal(int(unit["level"].strip()))))

        g.add((code, handbook["description"], Literal(unit["description"].strip())))

        for assessment in unit["assessment"]:
            node = BNode()
            g.add((code, handbook["assessment"], node))
            if "exam" in assessment or "final" in assessment:
                g.add((node, RDF.type, handbook["exam"]))
            elif "test" in assessment or "quiz" in assessment or re.match('mid[- ]sem', assessment):
                g.add((node, RDF.type, handbook["test"]))
            elif "report" in assessment or "portfolio" in assessment or "project" in assessment or "assignment" in assessment:
                g.add((node, RDF.type, handbook["assignment"]))
            elif "presentation" in assessment or "oral" in assessment:
                g.add((node, RDF.type, handbook["presentation"]))
            elif "participation" in assessment:
                g.add((node, RDF.type, handbook["participation"]))
            elif "practical" in assessment or "trip" in assessment or "site" in assessment or "visit" in assessment or "lab" in assessment:
                g.add((node, RDF.type, handbook["practical"]))
            else:
                g.add((node, RDF.type, handbook["other"]))

        try:
            for major in unit["majors"]:
                g.add((code, handbook["major"], handbook[major]))
        except KeyError:
            pass

        try:
            for outcome in unit["outcomes"]:
                g.add((code, handbook["outcome"], Literal(outcome.strip())))
        except KeyError:
            print(f"{unit['code']} has no outcomes")

        try:
            for prerequisites in unit["prerequisites_cnf"]:
                node = BNode()
                g.add(
                    (
                        code,
                        handbook["prerequisite_cnf"],
                        node,
                    )
                )
                g.add(
                    (
                        node,
                        RDF.type,
                        handbook['unitset'],
                    )
                )
                for prerequisite in prerequisites:
                    if re.search("[A-Z]{4}[1-9][0-9]{3}", prerequisite):
                        g.add(
                            (
                                node,
                                handbook["prerequisite"],
                                handbook[f"unitdetails?code={prerequisite}"],
                            )
                        )
        except KeyError:
            continue
    print()
    g.serialize("handbook.xml", "xml")
