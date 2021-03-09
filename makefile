all: data input transform merge
data: data/imdb/producers.csv data/imdb/distributors.csv data/imdb/content.csv
input: gen/data-preparation/temp/transform_distributors.RData
transform: gen/data-preparation/temp/transform_distributors.RData gen/data-preparation/temp/transform_producers.RData
merge: gen/data-preparation/output/data_imdb_merged.RData

# Transform data

gen/data-preparation/output/data_imdb_merged.RData: src/data-preparation/merge_imdb_data.R
	R CMD BATCH src/data-preparation/merge_imdb_data.R

gen/data-preparation/temp/transform_distributors.RData gen/data-preparation/temp/transform_producers.RData: gen/data-preparation/input/distributors.csv 
	R CMD BATCH src/data-preparation/transform_distributors.R
	R CMD BATCH src/data-preparation/transform_producers.R

gen/data-preparation/input/distributors.csv: data/imdb/distributors.csv
	R CMD BATCH src/data-preparation/update_input.R

# Download the datasets
data/imdb/producers.csv data/imdb/distributors.csv data/imdb/content.csv: src/data-preparation/imdb.py
	python src/data-preparation/imdb.py

data/trakt/watched.csv: src/data-preparation/unique_data.R \
			src/data-preparation/trakt.py
	R CMD BATCH src/data-preparation/unique_data.R
	python src/data-preparation/trakt.py
	