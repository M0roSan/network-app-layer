clean:
	rm log_* --force

run:
	python server.py &
	python controller.py -c 1

