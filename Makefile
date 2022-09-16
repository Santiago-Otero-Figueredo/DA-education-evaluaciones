
install:
	pip install -r requirements/production.txt

install-test:
	pip install -r requirements/test.txt

coverage:
	coverage run --source="." manage.py test ./itierra/$(app)

lint:
	@if [ "$(app)" = "" ]; then \
		pylint ./itierra/*/*.py --disable=C0114,R0901,C0115,E1101,R0903; \
	else \
		pylint ./itierra/$(app)/*.py --disable=C0114,R0901,C0115,E1101,R0903; \
	fi

code-checker:
	flake8 itierra/$(app) --exclude .git,__pycache__,"itierra/*/migrations/" 	--max-line-length 120 --ignore=E128,E124

coverage-test:
	coverage json --fail-under=$(limit)

coverage-report:
	coverage html --skip-covered --skip-empty --precision=2

coverage-report-json:
	coverage json --pretty-print

test: lint code-checker

remove-migrations-files:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete