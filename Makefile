.PHONY: install run test migrate

install:
	pip install -r requirements.txt

run:
	python src/main/run.py

test:
	pytest test/

migrate:
	flask db migrate -m "Database migration."
	flask db upgrade
