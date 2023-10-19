from rdflib import Graph
from ontology import graph
from pyshacl import validate

print(validate(graph, shacl_graph=Graph().parse("shacl.ttl"))[2])
