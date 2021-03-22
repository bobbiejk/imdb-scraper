all: input transform merge
input: gen/data-preparation/input/distributors.csv
transform: gen/data-preparation/temp/transform_distributors.RData gen/data-preparation/temp/transform_producers.RData gen/data-preparation/temp/transform_releases.RData
merge: gen/data-preparation/output/reviews.RData

# merge data

gen/data-preparation/output/reviews.RData: src/data-preparation/merge.R
	RScript src/data-preparation/merge.R

# transform data

gen/data-preparation/temp/transform_distributors.RData gen/data-preparation/temp/transform_producers.RData gen/data-preparation/temp/transform_releases.RData: gen/data-preparation/input/distributors.csv 
	RScript src/data-preparation/transform_distributors.R
	RScript src/data-preparation/transform_producers.R
	RScript src/data-preparation/transform_reviews.R
	RScript src/data-preparation/transform_releases.R

# set data to data-preparation/input

gen/data-preparation/input/distributors.csv: data/imdb/distributors.csv
	RScript src/data-preparation/update_input.R