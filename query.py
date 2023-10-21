from ontology import graph

print("Find all units with more than 20 outcomes")
for r in graph.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?unit
    WHERE {
        ?unit rdf:type handbook:Unit ;
              handbook:HasOutcome ?outcome .
    }
    GROUP BY ?unit
    HAVING (COUNT(?outcome) > 20)
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
        FILTER(?level = 3) .

        FILTER NOT EXISTS {
            ?unit handbook:HasAssessment ?assessment .
            ?assessment rdf:type handbook:Exam .
        }

        FILTER NOT EXISTS {
            ?unit handbook:HasPrerequisites / handbook:UnitDisjunctContains / handbook:HasAssessment / rdf:type handbook:Exam .
        }
    }
    """
):
    print(r.unit)
print()

print("Find all units that appear in more than 5 majors.")
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
    HAVING (COUNT(?major) > 5)
    """
):
    print(r.unit)
print()

print("Basic search functionality")
query = input("What would you like the search? ")
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
print()

print("Find all the units outside of my major that have a certain prerequisite")
major_code = input("What's your major code? ")
unit_code = input("What's the prerequisite code? ")
for r in graph.query(
    f"""
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT DISTINCT ?unit
    WHERE {{
        ?major rdf:type handbook:Major ;
               handbook:HasCode ?major_code ;
               handbook:HasUnit ?unit .
        FILTER (!CONTAINS(?major_code, "{major_code}")) .

        ?unit handbook:HasPrerequisites / handbook:UnitDisjunctContains / handbook:HasCode ?unit_code .
        FILTER (CONTAINS(?unit_code, "{unit_code}")) .
    }}
    """
):
    print(r.unit)
print()

print(
    "Find all the units that have less than 2 contact hours in total (summing all different types of contact hours)"
)
for r in graph.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?unit
    WHERE {
        ?unit rdf:type handbook:Unit ;
              handbook:HasContactHour / handbook:HasHours ?hours
    }
    GROUP BY ?unit
    HAVING (SUM(?hours) < 2)
    """
):
    print(r.unit)
print()

print(
    "Rank the majors in the order of least number of contact hours that are not field trips"
)
for major, total_hours in graph.query(
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
    ORDER BY SUM(?hours)
    """
):
    print(f"{major}: {total_hours} hours")
print()

print("Which majors don't have any participation or test assessments")
for r in graph.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT DISTINCT ?major
    WHERE {
        ?major rdf:type handbook:Major .
        MINUS {
            ?major handbook:HasUnit ?unit .
            ?unit rdf:type handbook:Unit ;
                  handbook:HasAssessment ?assessment .
            ?assessment rdf:type handbook:Test .
        }
        MINUS {
            ?major handbook:HasUnit ?unit .
            ?unit rdf:type handbook:Unit ;
                  handbook:HasAssessment ?assessment .
            ?assessment rdf:type handbook:Participation .
        }
    }
    """
):
    print(r.major)
print()

print(
    "Which majors can I transfer to from my current completed major so that I only have to take no more than 5 more units"
)
major_code = input("What's your current major? ")
for major in graph.query(
    """
    PREFIX handbook: <https://handbooks.uwa.edu.au/>
    SELECT ?major
    WHERE {
        ?major rdf:type handbook:Major .
    }
"""
):
    code = major.major.split("=")[-1]
    if code == major_code:
        continue
    result = graph.query(
        f"""
        PREFIX handbook: <https://handbooks.uwa.edu.au/>
        SELECT (COUNT(?unit) as ?total)
        WHERE {{
            {{
                SELECT ?unit
                WHERE {{
                    ?major rdf:type handbook:Major ;
                           handbook:HasCode ?major_code ;
                           handbook:HasUnit ?unit .
                    FILTER (CONTAINS(?major_code, "{code}")) .
                }}
            }}
            MINUS
            {{
                SELECT ?unit
                where {{
                    ?major rdf:type handbook:Major ;
                       handbook:HasCode ?major_code ;
                       handbook:HasUnit ?unit .
                    FILTER (CONTAINS(?major_code, "{major_code}")) .
                }}
            }}
        }}
        """
    )
    if list(result)[0].total.toPython() > 5:
        continue
    print(code)
    print()
