# make directory
dir.create("gen")
dir.create("gen/analysis")
dir.create("gen/analysis/input")

# copy the raw data into input folder
file.copy("./gen/data-preparation/output/content.RData", "./gen/analysis/input/content.Rdata")
file.copy("./gen/data-preparation/output/momentum.RData", "./gen/analysis/input/momentum.Rdata")
file.copy("./gen/data-preparation/output/simultaneous.RData", "./gen/analysis/input/simultaneous.Rdata")