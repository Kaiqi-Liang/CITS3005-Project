# CITS3005-Project UWA Handbook

## SPARQL Queries

### Basic

- Find all units with more than 6 outcomes
- Find all level 3 units that do not have an exam, and where none of their prerequisites have an exam.
- Find all units that appear in more than 3 majors.
- Basic search functionality: Given a query string (eg "environmental policy"), can you find the units that contain this string in the description or outcomes?

### Extra

Some of these queries might take a up to minutes to complete depending on your hardware

- Find all the units outside of my major that have a certain prerequisite
- Find all the units that have less than 2 contact hours in total (summing all different types of contact hours)
- Rank the majors in the order of least number of contact hours that are not field trips
- Which majors don't have any participation or test assessments
- Which majors can I transfer to from my current completed major so that I only have to take no more than 5 more units

## SHACL Constraints

### Required

- Every prerequisite for a level X unit should not have a level higher than X
- No unit should be its own prerequisite
- No major should require more than 80 contact hours for the same level of units

### Additional

- A major should have at least 1 units
- Every major and unit should have exactly 1 code and title
- A contact hour must have exactly one outgoing link to a positive integer
- A unit in a major cannot be a bridging unit for the same major
- The level of a unit should be the 5th character of the unit code
- A major cannot contain more than 58 units ([MJD-MUSDM](https://handbooks.uwa.edu.au/majordetails?code=MJD-MUSDM) has the most units), found by running

```python
max([len(major["units"]) for major in majors_json.values()])
```

- A unit or a major cannot have more than 39 outcomes ([DENTS5310](https://handbooks.uwa.edu.au/unitdetails?code=DENT5310) has the most outcomes), found by comparing the most outcomes a unit has and the most outcomes a major has

```python
max(max([len(unit["outcomes"]) for unit in units_json.values() if "outcomes" in unit]), max([len(major["outcomes"]) for major in majors_json.values() if "outcomes" in major]))
```
