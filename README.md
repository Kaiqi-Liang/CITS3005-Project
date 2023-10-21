# CITS3005-Project UWA Handbook

## Queries to answer

### Basic queries

- Find all units with more than 6 outcomes.
- Find all level 3 units that do not have an exam, and where none of their prerequisites have an exam.
- Find all units that appear in more than 3 majors.
- Basic search functionality: Given a query string (eg "environmental policy"), can you find the units that contain this string in the description or outcomes?

### Additional queries

- Find all the units outside of my major that have a certain prerequisite
- Find all the units that have less than 5 contact hours in total (summing all different types of contact hours)
- Rank the majors in the order of least number of contact hours that are not field trips
- Which majors don't have any participation or practical assessments
- Which majors can I transfer to from my current completed major so that I only have to take no more than 5 more units

## Categorisation

### Contact

- Lecture: "lecture"
- Practical classes: "practical"
- Tutorial
- Workshops: "seminar" "studio"
- Fieldtrip: "site visit"
- Labs
**Potential issues:**
- grouping of 'Lectures and practical hours' or 'lectures/computer labs' in many units
- contact hours that are not weekly - e.g., fieldtrips show as "1" but are really 1 x 2 Saturdays

## Constraints for SHACL

### Required

- Every prerequisite for a level X unit should not have a level higher than X
- No unit should be its own prerequisite
- No major should require more than 80 contact hours for the same level of units

### Additional

- The level of a unit should be the 5th character of the unit code
- A unit in a major cannot be a bridging unit for the same major
- Major has at least 1 units
- Major and units has exactly 1 code and name
- A major cannot contain more than 58 units (MJD-MUSDM has the most units), found by running

```python
max([len(major["units"]) for major in majors_json.values()])
```

- A unit cannot cannot have more than 26 outcomes (MJD-DENTS has the most outcomes), found by running

```python
max([len(unit["outcomes"]) for unit in units_json.values() if "outcomes" in unit])
```

- A contact hour must have one outgoing link to a positive integer

### Design decisions

- Not include prerequisites not in json to avoid empty units
- Not include prerequisites for major because it is just raw text
- Prerequisite level <= instead of < because of some units can have a prerequisite of the same level
