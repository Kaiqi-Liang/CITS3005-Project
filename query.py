def units_with_more_outcomes(graph, outcomes: int):
    print(f"Find the units with more than {outcomes} outcomes")
    return [
        r.unit
        for r in graph.query(
            f"""
        SELECT ?unit
        WHERE {{
            ?unit rdf:type handbook:Unit ;
                  handbook:HasOutcome ?outcome .
        }}
        GROUP BY ?unit
        HAVING (COUNT(?outcome) > {outcomes})
        """
        )
    ]


def units_with_no_exam(graph, level: int):
    print(
        f"Find the level {level} units that do not have an exam, and where none of their prerequisites have an exam."
    )
    return [
        r.unit
        for r in graph.query(
            f"""
        SELECT ?unit
        WHERE {{
            ?unit rdf:type handbook:Unit ;
                  handbook:IsLevel ?level .
            FILTER(?level = {level}) .

            FILTER NOT EXISTS {{
                ?unit handbook:HasAssessment ?assessment .
                ?assessment rdf:type handbook:Exam .
            }}

            FILTER NOT EXISTS {{
                ?unit handbook:HasPrerequisites / handbook:UnitDisjunctContains / handbook:HasAssessment / rdf:type handbook:Exam .
            }}
        }}
        """
        )
    ]


def units_in_more_majors(graph, majors: int):
    print(f"Find the units that appear in more than {majors} majors.")
    return [
        r.unit
        for r in graph.query(
            f"""
        SELECT ?unit
        WHERE {{
            ?unit rdf:type handbook:Unit .
            ?major handbook:HasUnit ?unit ;
                   rdf:type handbook:Major .
        }}
        GROUP BY ?unit
        HAVING (COUNT(?major) > {majors})
        """
        )
    ]


def units_contains_query(graph, query: str):
    print(f"Find the units that contain '{query}' in the description or outcomes")
    return [
        r.unit
        for r in graph.query(
            f"""
        SELECT DISTINCT ?unit
        WHERE {{
            ?unit rdf:type handbook:Unit ;
                  handbook:HasOutcome ?outcome ;
                  handbook:HasDescription ?description .
            FILTER (CONTAINS(LCASE(?outcome), LCASE("{query}")) || CONTAINS(LCASE(?description), LCASE("{query}"))) .
        }}
        """
        )
    ]


def units_outside_major(graph, major_code: str, unit_code: str):
    print(
        f"Find the units outside of {major_code} that have a {unit_code} as a prerequisite"
    )
    return [
        r.unit
        for r in graph.query(
            f"""
        SELECT DISTINCT ?unit
        WHERE {{
            ?major rdf:type handbook:Major ;
                   handbook:HasCode ?major_code ;
                   handbook:HasUnit ?unit .
            FILTER (!CONTAINS(LCASE(?major_code), LCASE("{major_code}"))) .

            ?unit handbook:HasPrerequisites / handbook:UnitDisjunctContains / handbook:HasCode ?unit_code .
            FILTER (CONTAINS(LCASE(?unit_code), LCASE("{unit_code}"))) .
        }}
        """
        )
    ]


def majors_with_less_hours(graph, hours: int, contact_hour: str):
    print(
        f"Find the majors that have less than {hours} contact hours in total that are not {contact_hour} (summing all different types of contact hours across all units)"
    )
    return [
        r.major
        for r in graph.query(
            f"""
        SELECT ?major
        WHERE {{
            ?major handbook:HasUnit / handbook:HasContactHour ?contact_hour .
            FILTER NOT EXISTS {{
                ?contact_hour rdf:type handbook:{contact_hour} .
            }}
            ?contact_hour handbook:HasHours ?hours .
        }}
        GROUP BY ?major
        HAVING (SUM(?hours) < {hours})
        """
        )
    ]


def majors_without_assessments(graph, assessment: str):
    print(f"Which majors don't have any {assessment}")
    return [
        r.major
        for r in graph.query(
            f"""
        SELECT DISTINCT ?major
        WHERE {{
            ?major rdf:type handbook:Major .
            MINUS {{
                ?major handbook:HasUnit ?unit .
                ?unit rdf:type handbook:Unit ;
                      handbook:HasAssessment ?assessment .
                ?assessment rdf:type handbook:{assessment} .
            }}
        }}
        """
        )
    ]


def majors_with_less_units(graph, major_code: str, units: int):
    print(
        f"Which majors can I transfer to from my current completed major so that I only have to take no more than {units} more units"
    )
    for r in graph.query(
        """
        SELECT ?major
        WHERE {
            ?major rdf:type handbook:Major .
        }
    """
    ):
        code = r.major.split("=")[-1]
        if major_code.lower() in code.lower():
            continue
        result = graph.query(
            f"""
            SELECT (COUNT(?unit) as ?total)
            WHERE {{
                {{
                    SELECT ?unit
                    WHERE {{
                        ?major rdf:type handbook:Major ;
                               handbook:HasCode ?major_code ;
                               handbook:HasUnit ?unit .
                        FILTER (CONTAINS(LCASE(?major_code), LCASE("{code}"))) .
                    }}
                }}
                MINUS
                {{
                    SELECT ?unit
                    where {{
                        ?major rdf:type handbook:Major ;
                           handbook:HasCode ?major_code ;
                           handbook:HasUnit ?unit .
                        FILTER (CONTAINS(LCASE(?major_code), LCASE("{major_code}"))) .
                    }}
                }}
            }}
            """
        )
        if list(result)[0].total.toPython() > units:
            continue
        majors.append(r.major)
    return majors
