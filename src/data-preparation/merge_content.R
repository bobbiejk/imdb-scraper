# install packages
require(dplyr)

# load data associated with content
load("./gen/data-preparation/temp/transform_producers.RData")
load("./gen/data-preparation/temp/transform_distributors.RData")
content_df <- read.csv("./gen/data-preparation/input/content.csv", sep = ",")

# add dummy of whether it is originals
content_df <- merge(content_df, originals_df, by="id")
# add dummy of whether it is exclusive
content_df <- merge(content_df, exclusive_df, by="id")

# create directory
dir.create("./gen/data-preparation/output")

# save merged data
save(content_df,file="./gen/data-preparation/output/content.RData")
