from ontology import graph

'''
print("Find all units with more than 6 outcomes")
for r in graph.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?unit
    WHERE {
        ?unit rdf:type handbook:Unit ;
              handbook:HasOutcome ?outcome .
    }
    GROUP BY ?unit
    HAVING (COUNT(?outcome) > 6)
    """
):
    print(r.unit)
print()

print(
    "Find all level 3 units that do not have an exam, and where none of their prerequisites have an exam."
)
for r in graph.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?unit
    WHERE {
        ?unit rdf:type handbook:Unit ;
              handbook:IsLevel ?level .
        ?level rdf:type handbook:Level3 .

        FILTER NOT EXISTS {
            ?unit handbook:HasAssessment ?assessment .
            ?assessment rdf:type handbook:Exam .
        }

        FILTER NOT EXISTS {
            ?unit handbook:HasPrerequisites / handbook:UnitDisjuntContains / handbook:HasAssessment / rdf:type handbook:Exam .
        }
    }
    """
):
    print(r.unit)
print()

print("Find all units that appear in more than 3 majors.")
for r in graph.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?unit
    WHERE {
        ?unit rdf:type handbook:Unit .
        ?major handbook:HasUnit ?unit ;
               rdf:type handbook:Major .
    }
    GROUP BY ?unit
    HAVING (COUNT(?major) > 3)
    """
):
    print(r.unit)
print()

print("Basic search functionality")
query = input("What would you like the search: ")
for r in graph.query(
    f"""
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT DISTINCT ?unit
    WHERE {{
        ?unit rdf:type handbook:Unit ;
              handbook:HasOutcome ?outcome ;
              handbook:HasDescription ?description .
        FILTER (CONTAINS(LCASE(?outcome), LCASE("{query}")) || CONTAINS(LCASE(?description), LCASE("{query}"))) .
    }}
    """
):
    print(r.unit)

print("Find all the units outside of my major that have a certain prerequisite")
major_code = input("What's your major code? ")
unit_code = input("What's the prerequisite code? ")
for r in graph.query(
    f"""
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT DISTINCT ?unit
    WHERE {{
        ?major rdf:type handbook:Major ;
               handbook:HasUnit ?unit ;
               handbook:HasCode ?major_code .
        FILTER (!CONTAINS(?major_code, "{major_code}")) .

        ?unit handbook:HasPrerequisites /  handbook:UnitDisjuntContains / handbook:HasCode ?unit_code .
        FILTER (CONTAINS(?unit_code, "{unit_code}")) .
    }}
    """
):
    print(r.unit)
'''
print("Find all the units that have less than 5 contact hours in total (summing all different types of contact hours)")
for r in graph.query(
    f"""
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?unit
    WHERE {{
        ?unit rdf:type handbook:Unit ;
              handbook:HasContactHour / handbook:HasHours ?hours
    }}
    GROUP BY ?unit
    HAVING (SUM(?hours) < 5)
    """
):
    print(r.unit)

print("Rank the majors in the order of least number of contact hours that are not field trips")
for r in graph.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?major (SUM(?hours) as ?total_hours)
    WHERE {
        ?major handbook:HasUnit / handbook:HasContactHour ?contact_hour .
        FILTER NOT EXISTS {
            ?contact_hour rdf:type handbook:FieldTrip .
        }
        ?contact_hour handbook:HasHours ?hours .
    }
    GROUP BY ?major
    ORDER BY DESC(SUM(?hours))
    """
):
    print(r.major, r.total_hours)
    
print("Which majors can I transfer to from my current completed major so that I only have to take no more than 5 more units")
for r in graph.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?major
    WHERE {
        ?major handbook:HasUnit / handbook:HasContactHour ?contact_hour .
        FILTER NOT EXISTS {
            ?contact_hour rdf:type handbook:FieldTrip .
        }
        ?contact_hour handbook:HasHours ?hours .
    }
    GROUP BY ?major
    ORDER BY DESC(SUM(?hours))
    """
):
    print(r.major, r.total_hours)
