all: input transform output
input: gen/data-preparation/temp/transform_distributors.RData
transform: gen/data-preparation/temp/transform_distributors.RData gen/data-preparation/temp/transform_producers.RData gen/data-preparation/temp/transform_releases.RData
output: gen/data-preparation/output/content.RData gen/data-preparation/output/simultaneous.RData gen/data-preparation/output/momentum.RData

# Transform data

gen/data-preparation/output/momentum.RData: src/data-preparation/get_momentum.R
	RScript src/data-preparation/get_momentum.R

gen/data-preparation/output/simultaneous.RData: src/data-preparation/update_output.R
	RScript src/data-preparation/update_output.R

gen/data-preparation/output/content.RData: src/data-preparation/merge_content.R
	RScript src/data-preparation/merge_content.R

gen/data-preparation/temp/transform_distributors.RData gen/data-preparation/temp/transform_producers.RData gen/data-preparation/temp/transform_releases.RData: gen/data-preparation/input/distributors.csv 
	RScript src/data-preparation/transform_distributors.R
	RScript src/data-preparation/transform_producers.R
	RScript src/data-preparation/transform_reviews.R
	RScript src/data-preparation/transform_releases.R

gen/data-preparation/input/distributors.csv: data/imdb/distributors.csv
	RScript src/data-preparation/update_input.R