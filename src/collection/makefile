all: ../../data/imdb/distributors.csv

../../data/tmdb/releases.csv: tmdb.py ../../data/imdb/content.csv
	python tmdb.py

../../data/imdb/distributors.csv: imdb.py
	python imdb.py