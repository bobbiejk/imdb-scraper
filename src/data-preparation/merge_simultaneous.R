# needed package
require(dplyr)

# make directory
dir.create("gen")
dir.create("gen/data-preparation")
dir.create("gen/data-preparation/output")

# file load
load("./gen/data-preparation/temp/transform_releases.RData")
load("./gen/data-preparation/output/content.RData")

# copy the raw data into input folder
left_join(simultaneous_df, content_df, by=c("imdb_id"="id"))