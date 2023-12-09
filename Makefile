install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	pytest -vv test_search_pubmed.py

format:
	black *.py

lint: 
	pylint --disable C,R *.py

run: 
	python search_pubmed.py -m pmc -f 2021-01-01 -u 2021-02-01 -s bmj -o out.csv

all: install lint test format
