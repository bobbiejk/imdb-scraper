# make directory
dir.create("gen")
dir.create("gen/data-preparation")
dir.create("gen/data-preparation/output")

# copy the raw data into input folder
file.copy("./gen/data-preparation/temp/transform_releases.RData", "./gen/data-preparation/output/simultaneous.RData")