clean:
	find . -name '*.pyc' -exec rm --force {} + 
	find . -name '*.pyo' -exec rm --force {} + 
	name '*~' -exec rm --force {} 
	name 'log_* -exec rm --force {}

run:
	python server.py &
	python controller.py -c 1

