# make directory
dir.create("gen")
dir.create("gen/data-preparation")
dir.create("gen/data-preparation/input")

# copy the raw data into input folder
file.copy("./data/imdb/content.csv", "./gen/data-preparation/input/content.csv")
file.copy("./data/imdb/distributors.csv", "./gen/data-preparation/input/distributors.csv")
file.copy("./data/imdb/producers.csv", "./gen/data-preparation/input/producers.csv")
file.copy("./data/imdb/reviews.csv", "./gen/data-preparation/input/reviews.csv")
file.copy("./data/tmdb/releases.csv", "./gen/data-preparation/input/releases.csv")
