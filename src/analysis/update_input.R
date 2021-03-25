# make directory
dir.create("gen")
dir.create("gen/analysis")
dir.create("gen/analysis/input")

# copy the raw data into input folder
file.copy("./gen/data-preparation/output/reviews.RData", "./gen/analysis/input/reviews.Rdata")
