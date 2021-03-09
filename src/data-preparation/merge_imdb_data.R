# install packages
require(dplyr)

# load data associated with content
load("./gen/data-preparation/temp/transform_producers.RData")
load("./gen/data-preparation/temp/transform_distributors.RData")
content_df <- read.csv("./gen/data-preparation/input/content.csv", sep = ";")

# merge data 
df_imdb_merged_half <- merge(content_df, originals_df, by="id")
df_imdb_merged <- merge(df_imdb_merged_half, exclusive_df, by="id")

# create directory
dir.create("./gen/data-preparation/output")

# save merged data
save(df_imdb_merged,file="./gen/data-preparation/output/data_imdb_merged.RData")
