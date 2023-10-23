import json
import signal
import openai
from flask import Flask, request
from flask_cors import CORS
from owlready2 import sync_reasoner_pellet, default_world
from rdflib import Graph
from pyshacl import validate
from ontology import onto, NAMESPACE
from query import (
    majors_with_less_hours,
    majors_with_less_units,
    majors_without_assessments,
    units_contains_query,
    units_in_more_majors,
    units_outside_major,
    units_with_more_outcomes,
    units_with_no_exam,
)

onto.save("handbook.owl")
sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
graph = default_world.as_rdflib_graph()
graph.bind("handbook", NAMESPACE)

app = Flask(__name__)
CORS(app)

try:
    with open("cache.json", "r") as cache_json:
        cache = json.load(cache_json)
except FileNotFoundError:
    cache = {
        "query1": {},
        "query2": {},
        "query3": {},
        "query4": {},
        "query5": {},
        "query6": {},
        "query7": {},
        "query8": {},
        "other": {},
    }


def cleanup(*_):
    print("Writing cache to disk")
    with open("cache.json", "w") as cache_json:
        json.dump(cache, cache_json, indent=4)
    exit()


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


@app.route("/query1", methods=["post"])
def query1():
    outcomes = request.json["outcomes"]
    if not outcomes:
        outcomes = "6"
    if outcomes in cache["query1"]:
        return cache["query1"][outcomes]
    result = units_with_more_outcomes(graph, outcomes)
    cache["query1"][outcomes] = result
    return result


@app.route("/query2", methods=["post"])
def query2():
    level = request.json["level"]
    if not level:
        level = "3"
    if level in cache["query2"]:
        return cache["query2"][level]
    result = units_with_no_exam(graph, level)
    cache["query2"][level] = result
    return result


@app.route("/query3", methods=["post"])
def query3():
    majors = request.json["majors"]
    if not majors:
        majors = "3"
    if majors in cache["query3"]:
        return cache["query3"][majors]
    result = units_in_more_majors(graph, majors)
    cache["query3"][majors] = result
    return result


@app.route("/query4", methods=["post"])
def query4():
    query = request.json["query"].lower()
    if not query:
        query = "environmental policy"
    if query in cache["query4"]:
        return cache["query4"][query]
    result = units_contains_query(graph, query)
    cache["query4"][query] = result
    return result


@app.route("/query5", methods=["post"])
def query5():
    major_code = request.json["major_code"].lower()
    if not major_code:
        major_code = "cyber"
    unit_code = request.json["unit_code"].lower()
    if not unit_code:
        unit_code = "cits2200"
    key = major_code + unit_code
    if key in cache["query5"]:
        return cache["query5"][key]
    result = units_outside_major(graph, major_code, unit_code)
    cache["query5"][key] = result
    return result


@app.route("/query6", methods=["post"])
def query6():
    hours = request.json["hours"]
    if not hours:
        hours = "2"
    contact_hour = request.json["contact_hour"]
    if not contact_hour:
        contact_hour = "FieldTrip"
    key = hours + contact_hour
    if key in cache["query6"]:
        return cache["query6"][key]
    result = majors_with_less_hours(graph, hours, contact_hour)
    cache["query6"][key] = result
    return result


@app.route("/query7", methods=["post"])
def query7():
    assessment = request.json["assessment"]
    if not assessment:
        assessment = "Exam"
    if assessment in cache["query7"]:
        return cache["query7"][assessment]
    result = majors_without_assessments(graph, assessment)
    cache["query7"][assessment] = result
    return result


@app.route("/query8", methods=["post"])
def query8():
    major_code = request.json["major_code"].lower()
    if not major_code:
        major_code = "cmpsc"
    units = request.json["units"]
    if not units:
        units = "5"
    key = major_code + units
    if key in cache["query8"]:
        return cache["query8"][key]
    result = majors_with_less_units(graph, major_code, int(units))
    cache["query8"][key] = result
    return result


@app.route("/shacl")
def shacl():
    print("Running SHACL to validate the handbook ontology")
    if "shacl" in cache:
        return cache["shacl"]
    shacl = validate(
        Graph().parse("handbook.owl"), shacl_graph=Graph().parse("shacl.ttl")
    )[2]
    cache["shacl"] = shacl
    return shacl


@app.route("/other", methods=["post"])
def other():
    query = request.json["query"]
    if not query:
        query = 'Find the majors that are in the school of "Physics, Mathematics and Computing'
    if query.lower() in cache["other"]:
        return cache["other"][query.lower()]
    prompt = """
    This is the ontology created using `owlready2`.
    ```python
    class Unit(Thing): pass
    class Major(Thing): pass
    AllDisjoint([Unit, Major])
    class HasUnit(Major >> Unit): pass
    class HasSchool(Major >> str, FunctionalProperty): pass
    class HasBridging(Major >> Unit): pass
    class Assessment(Thing): pass
    class Exam(Assessment): pass
    class Test(Assessment): pass
    class Assignment(Assessment): pass
    class Presentation(Assessment): pass
    class Participation(Assessment): pass
    class Practical(Assessment): pass
    class OtherAssessment(Assessment): pass
    class HasAssessment(Unit >> Assessment): pass
    class ContactHour(Thing): pass
    class Lecture(ContactHour): pass
    class Tutorial(ContactHour): pass
    class Lab(ContactHour): pass
    class Workshop(ContactHour): pass
    class FieldTrip(ContactHour): pass
    class Practice(ContactHour): pass
    class OtherContactHour(ContactHour): pass
    class HasContactHour(Unit >> ContactHour): pass
    class HasHours(ContactHour >> int, FunctionalProperty): pass
    class IsLevel(Unit >> int, FunctionalProperty): pass
    class DeliveryMode(Thing): pass
    class Online(DeliveryMode): pass
    class Face2Face(DeliveryMode): pass
    class Hybrid(DeliveryMode): pass
    class IsDeliveryMode(Unit >> DeliveryMode, FunctionalProperty): pass
    class UnitDisjunct(Thing): pass
    class UnitDisjunctContains(UnitDisjunct >> Unit): pass
    class HasPrerequisites(Unit >> UnitDisjunct): pass
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
    ```
    You are a helpful knowledge base assistant. You are to generate SPARQL queries for a given prompt assuming the namespace is already set to `handbook`.
    """
    for choice in openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "find the units with more than 6 outcomes"},
            {
                "role": "assistant",
                "content": """
                SELECT ?unit
                WHERE {
                    ?unit rdf:type handbook:Unit ;
                          handbook:HasOutcome ?outcome .
                }
                GROUP BY ?unit
                HAVING (COUNT(?outcome) > 6)
                """,
            },
            {"role": "user", "content": query},
        ],
        n=3,
    )["choices"]:
        sparql = choice.message.content
        print(sparql, end="\n\n")
        try:
            result = list(graph.query(sparql))
            if len(result) > 0:
                cache["other"][query.lower()] = result
                return result
        except:
            continue
    return []


if __name__ == "__main__":
    app.run()
