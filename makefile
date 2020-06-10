INPUT_PATH = maleplyty.txt


make:
	python3 main.py $(INPUT_PATH)

clean:
	rm -f ./plots/*
	rm -f ./__pycache__/*
