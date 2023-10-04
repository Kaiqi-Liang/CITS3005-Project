# Ask about linking to repeated literals like delivery mode and level 

import json
import re
from rdflib import FOAF, BNode, Graph, Namespace, Literal, RDF, RDFS

g = Graph()

# Declare namespace
handbook = Namespace("https://handbooks.uwa.edu.au/")

################# Add initial classes
# Add general classes
g.add((handbook["unit"], RDF.type, RDFS.Class))
g.add((handbook["major"], RDF.type, RDFS.Class))

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
# Used in both unit and majors

# Unit relations
g.add((handbook["level"], RDF.type, RDF.Property)) # connect unit to int unit level
g.add((handbook["description"], RDF.type, RDF.Property)) # connect unit to literal description
g.add((handbook["assessment"], RDF.type, RDF.Property)) #connect unit to BN
g.add((handbook["contact"], RDF.type, RDF.Property)) #connect unit to BN
g.add((handbook["forHours"], RDF.type, RDF.Property)) #connect BN to int literal
g.add((handbook["outcome"], RDF.type, RDF.Property)) # connect unit to literal of outcomes
g.add((handbook["prerequisite_cnf"], RDF.type, RDF.Property)) # connect unit to BN
g.add((handbook["prerequisite"], RDF.type, RDF.Property)) # connect BN to BN
g.add((handbook["deliveryMode"], RDF.type, RDF.Property)) 

# Major relations
g.add((handbook["school"], RDF.type, RDF.Property)) 
g.add((handbook["course"], RDF.type, RDF.Property))
g.add((handbook["hasUnit"], RDF.type, RDF.Property)) 


# Process unit information
with open("units.json", "r") as units:
    for unit in json.load(units).values():
        code = handbook[f"unitdetails?code={unit['code']}"]

        g.add((code, RDF.type, handbook["unit"]))
        g.add((code, FOAF.name, Literal(unit["title"].strip())))
        g.add((code, handbook["level"], Literal(int(unit["level"].strip()))))
        g.add((code, handbook["deliveryMode"], Literal(unit["delivery_mode"].strip())))
        g.add((code, handbook["description"], Literal(unit["description"].strip())))

        for assessment in unit["assessment"]:
            assessment = assessment.lower() # make case insensitive
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
            for contact in unit["contact"]:
                contact = contact.lower()
                hours = unit["contact"][contact]
                node = BNode()
                g.add((code, handbook["contact"], node))
                if "lec" in contact:
                    g.add((node, RDF.type, handbook["lecture"]))
                elif "workshop" in contact or "seminar" in contact or "studio" in contact:
                    g.add((node, RDF.type, handbook["workshop"]))
                elif "prac" in contact:
                    g.add((node, RDF.type, handbook["practical"]))
                elif "tut" in contact:
                    g.add((node, RDF.type, handbook["tutorial"]))
                elif "lab" in contact:
                    g.add((node, RDF.type, handbook["lab"]))
                elif "field" in contact or "site" in contact:
                    g.add((node, RDF.type, handbook["fieldtrip"]))
                else:
                    g.add((node, RDF.type, handbook["other"]))
                
                g.add((node, handbook["forHours"], Literal(int(hours.strip())))) # add hours to blank node
        except KeyError:
            continue
            

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

# Process major information
with open("majors.json", "r") as majors:
    for major in json.load(majors).values():
        code = handbook[f"unitdetails?code={major['code']}"]
        g.add((code, RDF.type, handbook["major"]))

        g.add((code, FOAF.name, Literal(major["title"].strip())))
        g.add((code, handbook["school"], Literal(major["school"].strip())))
        g.add((code, handbook["description"], Literal(major["description"].strip())))
        
        for outcome in major["outcomes"]:
                g.add((code, handbook["outcome"], Literal(outcome.strip())))
        
        for course in major["courses"]:
                g.add((code, handbook["course"], Literal(outcome.strip())))
                
        for unit in major["units"]:
                unit_node = handbook[f"unitdetails?code={unit}"]
                g.add((code, handbook["hasUnit"], unit_node))



