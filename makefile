all: input inspection transform merge descriptives input2 analysis

input: gen/data-preparation/input/distributors.csv
inspection: gen/data-preparation/output/raw_inspection.html
transform: gen/data-preparation/temp/transform_distributors.RData gen/data-preparation/temp/transform_producers.RData gen/data-preparation/temp/transform_releases.RData gen/data-preparation/temp/transform_reviews.RData
merge: gen/data-preparation/output/reviews.RData
descriptives: gen/data-preparation/output/descriptives.html
input2: gen/analysis/input/reviews.RData
analysis: gen/analysis/output/analysis.html

# regression analysis

gen/analysis/output/analysis.html: src/analysis/update_output.R src/analysis/analysis.Rmd 
	RScript src/analysis/update_output.R
	R -e "rmarkdown::render('src/analysis/analysis.Rmd', output_file = '../../gen/analysis/output/analysis.html')"

# set data to gen/analysis/input

gen/analysis/input/reviews.RData: src/analysis/update_input.R
	RScript src/analysis/update_input.R

# descriptive analysis after data preparation

gen/data-preparation/output/descriptives.html: src/data-preparation/descriptives.Rmd 
	R -e "rmarkdown::render('src/data-preparation/descriptives.Rmd', output_file = '../../gen/data-preparation/output/descriptives.html')"

# merge data

gen/data-preparation/output/reviews.RData: src/data-preparation/merge.R
	RScript src/data-preparation/merge.R

# transform data

gen/data-preparation/temp/transform_reviews.RData: gen/data-preparation/input/reviews.csv src/data-preparation/transform_reviews.R
	RScript src/data-preparation/transform_reviews.R

gen/data-preparation/temp/transform_releases.RData: gen/data-preparation/input/releases.csv src/data-preparation/transform_releases.R
	RScript src/data-preparation/transform_releases.R

gen/data-preparation/temp/transform_producers.RData: gen/data-preparation/input/producers.csv src/data-preparation/transform_producers.R
	RScript src/data-preparation/transform_producers.R

gen/data-preparation/temp/transform_distributors.RData: gen/data-preparation/input/distributors.csv src/data-preparation/transform_distributors.R
	RScript src/data-preparation/transform_distributors.R

# raw data inspection

gen/data-preparation/output/raw_inspection.html: src/data-preparation/raw_inspection.Rmd 
	R -e "rmarkdown::render('src/data-preparation/raw_inspection.Rmd', output_file = 'gen/data-preparation/output/raw_inspection.html')"

# set data to gen/data-preparation/input

gen/data-preparation/input/distributors.csv: data/imdb/distributors.csv src/data-preparation/update_input.R
	RScript src/data-preparation/update_input.R

# download data

data/imdb/distributors.csv: src/data-preparation/download_files.R
	RScript src/data-preparation/download_files.R