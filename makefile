INPUT_PATH = maleplyty.txt
TIME_RUN_MINUTES = 3


make:
	python3 main.py $(INPUT_PATH) $(TIME_RUN_MINUTES)

clean:
	rm -f ./plots/*
	rm -f ./__pycache__/*
