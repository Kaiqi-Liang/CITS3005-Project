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

After about 5 seconds it will output a lot of relations the `Pellet` reasoner inserted, then it will print out the server is running on a URL, this URL must be the same as the `SERVER_URL` defined in the first line of the [JavaScript file](index.js), by default it will be `http://127.0.0.1:5000`. Once this is all set up open the [HTML file](index.html) in your browser.

```bash
open index.html
```

## User Interface

The user interface allows you to run 8 builtin [`SPARQL` queries](#sparql-queries) and validate `SHACL` constraint as well as any general query that you can come up with. Each query has 1 or 2 parameters you can set, if you don't enter anything the default values will be used which can be found on the instructions table in the user interface.

If you run the same query with the same parameters multiple times it will be much faster after the first time as the results are cached in the backend, this includes the `SHACL` constraint validation as the first time will take a really long time.

If the query returns no result it will show a message saying 'No matching result for the query', but if the server encountered any error at all it will simply say 'Something went wrong'.

## SPARQL Queries

### Basic

- Find units with more than 6 outcomes
- Find level 3 units that do not have an exam, and where none of their prerequisites have an exam.
- Find units that appear in more than 3 majors.
- Basic search functionality: Given a query string (eg "environmental policy"), can you find the units that contain this string in the description or outcomes?

### Extra

Some of these queries might take a up to minutes to complete depending on your hardware

- Find the units outside of my major that have a certain prerequisite
- Find the majors that have less than 2 contact hours in total that are not field trips(summing all different types of contact hours)
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
