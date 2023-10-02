import json
import re
from rdflib import FOAF, BNode, Graph, Namespace, Literal, RDF, RDFS

g = Graph()

# Declare namespace
handbook = Namespace("https://handbooks.uwa.edu.au/")

################# Add initial classes
# Add assessment types as classes
g.add((handbook["exam"], RDF.type, RDFS.Class))
g.add((handbook["test"], RDF.type, RDFS.Class))
g.add((handbook["presentation"], RDF.type, RDFS.Class))
g.add((handbook["participation"], RDF.type, RDFS.Class))
g.add((handbook["practical"], RDF.type, RDFS.Class))
g.add((handbook["other"], RDF.type, RDFS.Class))

# Add unit set class
g.add((handbook["unitset"], RDF.type, RDFS.Class))

# Add contact hour categories as classes
g.add((handbook["lecture"], RDF.type, RDFS.Class))
g.add((handbook["practical"], RDF.type, RDFS.Class))
g.add((handbook["tutorial"], RDF.type, RDFS.Class))
g.add((handbook["lab"], RDF.type, RDFS.Class))
g.add((handbook["workshop"], RDF.type, RDFS.Class))
g.add((handbook["fieldtrip"], RDF.type, RDFS.Class))
g.add((handbook["other"], RDF.type, RDFS.Class))

################# Add initial relations
g.add((handbook["level"], RDF.type, RDF.Property)) # connect unit to int unit level
g.add((handbook["description"], RDF.type, RDF.Property)) # connect unit to literal description
g.add((handbook["assessment"], RDF.type, RDF.Property)) #connect unit to BN
g.add((handbook["outcome"], RDF.type, RDF.Property)) # connect unit to literal of outcomes
g.add((handbook["prerequisite_cnf"], RDF.type, RDF.Property)) # connect unit to BN
g.add((handbook["prerequisite"], RDF.type, RDF.Property)) # connect BN to BN




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

        # TODO: will later connect major and units via handbook.unit (using code) rather than strings
        #try:
        #    for major in unit["majors"]:
        #        g.add((code, handbook["major"], handbook[major]))
        #except KeyError:
        #    pass

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
    #g.serialize("handbook.xml", "xml")
