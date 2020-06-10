clear:
	rm -f ./plots/*
	rm -f ./__pycache__/*

make:
	python3 main.py "maleplyty.txt"