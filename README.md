# CITS3005-Project UWA Handbook

## Setup

List all the virtual environments on your system.

```bash
conda env list
```

If you see the error messsage `command not found` go install [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

Otherwise check the list of virtual environments on your system and make sure the name `kr` does not exist.

Then create a new virtual environment called `kr` with all the dependencies installed.

```bash
conda env create --file kr.yml
```

If it already exists rename the file `kr.yml` to something else that does not exist and run the command again with the new file name.

Put your openAI API key in an environment variable.

```bash
export OPENAI_API_KEY=openai-api-key
```

Activate the virtual environment and run the server code.

```bash
conda activate kr
python server.py
```

After roughly 5 seconds it will output a lot of relations the `Pellet` reasoner inserted, then it will print out the server is running on a URL, this URL must be the same as the `SERVER_URL` defined in the first line of the [JavaScript file](index.js), by default it will be `http://127.0.0.1:5000`. Once this is all set up open the [HTML file](index.html) in your browser.

```bash
open index.html
```

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
