all: data input transform merge
data: data/imdb/producers.csv data/imdb/distributors.csv data/imdb/content.csv
input: gen/data-preparation/temp/transform_distributors.RData
transform: gen/data-preparation/temp/transform_distributors.RData gen/data-preparation/temp/transform_producers.RData
merge: gen/data-preparation/output/data_imdb_merged.RData

# Transform data

gen/data-preparation/output/data_imdb_merged.RData: src/data-preparation/merge_imdb_data.R
	RScript src/data-preparation/merge_imdb_data.R

gen/data-preparation/temp/transform_distributors.RData gen/data-preparation/temp/transform_producers.RData: gen/data-preparation/input/distributors.csv 
	RScript src/data-preparation/transform_distributors.R
	RScript src/data-preparation/transform_producers.R

gen/data-preparation/input/distributors.csv: data/imdb/distributors.csv
	RScript src/data-preparation/update_input.R