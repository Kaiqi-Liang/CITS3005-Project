from handbook_rdf import g

print("Find all units with more than 6 outcomes")
for r in g.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?unit
    WHERE {
        ?unit rdf:type handbook:unit ;
                handbook:outcome ?outcome .
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
for r in g.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?unit
    WHERE {
        ?unit rdf:type handbook:unit ;
                handbook:level ?level .
        FILTER (?level = 3) .
        FILTER NOT EXISTS {
            ?unit handbook:assessment handbook:exam .
        }
        FILTER NOT EXISTS {
            ?unit handbook:prerequisite ?prereq .
            ?prereq handbook:assessment handbook:exam .
        }
    }
    """
):
    print(r.unit)
print()

print("Find all units that appear in more than 3 majors.")
for r in g.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?unit
    WHERE {
        ?unit rdf:type handbook:unit ;
                handbook:major ?major .
    }
    GROUP BY ?unit
    HAVING (COUNT(?major) > 3)
    """
):
    print(r.unit)
print()

print("Basic search functionality")
query = input()
for r in g.query(
    f"""
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT DISTINCT ?unit
    WHERE {{
        ?unit rdf:type handbook:unit ;
                handbook:outcome ?outcome ;
                handbook:description ?description .
        FILTER (CONTAINS(LCASE(?outcome), LCASE("{query}")) || CONTAINS(LCASE(?outcome), LCASE("{query}"))) .
    }}
    """
):
    print(r.unit)
