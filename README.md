This a prototype sytem of PPDPES


start server:

	python manage.py runserver 0.0.0.0:8888

1) Test:

    python -m unittest discover . "_test.py"

2) worker:

    celery -A ppdpes worker --loglevel=info

3) anon JSON

	{"anon":{"k":10, "data": 1000, "qi":[1,2,3]}}

4) eval JSON

	{"eval":["k","qi","data"]}

