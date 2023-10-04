from owlready2 import get_ontology, Thing, ObjectProperty
from rdflib import BNode, Literal

onto = get_ontology("https://handbooks.uwa.edu.au/")
with onto:
	class Unit(Thing): pass
	class Major(Thing): pass

	class Assessment(Thing): pass
	class Exam(Assessment): pass
	class Test(Assessment): pass
	class Presentation(Assessment): pass
	class Participation(Assessment): pass
	class Practical(Assessment): pass
	class Other(Assessment): pass
	class Outcome(Assessment): pass

	class ContactHour(Thing): pass
	class Level(Thing): pass
	class Level1(Level): pass
	class Level2(Level): pass
	class Level3(Level): pass
	class Level4(Level): pass
	class Level5(Level): pass
	class Level6(Level): pass

	class DeliveryMode(Thing): pass
	class Online(DeliveryMode): pass
	class Face2Face(DeliveryMode): pass
	class Hybrid(DeliveryMode): pass

	class HasPrerequisite(ObjectProperty):
		domain = [Unit, Major]
		range = [Unit]

	class Description(ObjectProperty):
		domain = [Unit, Major]
		range = [Literal]

	class HasAssessment(ObjectProperty):
		domain = [Unit]
		range = [BNode]

	class AssessmentType(ObjectProperty):
		domain = [BNode]
		range = [Assessment]

