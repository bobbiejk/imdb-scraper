# install packages
require(dplyr)

# load data associated with content
load("./gen/data-preparation/temp/transform_producers.RData")
load("./gen/data-preparation/temp/transform_distributors.RData")

# load data associated with releases
load("./gen/data-preparation/temp/transform_releases.RData")

# load data associated with reviews
load("./gen/data-preparation/temp/momentum.RData")

reviews_df <- momentum_df

# add exclusivity to the data set
reviews_df$exclusive <- 0

for (i in 1:nrow(reviews_df)){
  for (j in 1:nrow(exclusive_df)){
    
    # check of similar ids in which year the review has been written
    if (reviews_df$id[i] == exclusive_df$id[j]){
      review_year <- format(reviews_df$review_data[i], "%Y")
      
      # if this review year corresponds to a distributor year
      # check whether it was a Netflix exclusive that specific year
      if (review_year == exclusive_df$year[j]){
        reviews_df$exclusive[i] <- exclusive_df$exclusive[j]
      }
    }
  }
}

# add releasing and simultaneous dummy to the data set
reviews_df$releasing <- 0
reviews_df$simultaneous <- 0

for (i in 1:nrow(reviews_df)){
  print(i)
  for (j in 1:nrow(simultaneous_df)){
    
    # check of similar ids in order to check review is written during release period
    if (reviews_df$id[i] == simultaneous_df$imdb_id[j]){
      if (reviews_df$review_data[i] >= simultaneous_df$release_data[j] & reviews_df$review_data[i] < simultaneous_df$release_data[j] + 7 & !is.na(reviews_df$review_data[i]) & !is.na(simultaneous_df$release_data[j])){
        reviews_df$releasing[i] <- 1
        reviews_df$simultaneous[i] <- simultaneous_df$simultaneous[j]
      }
    }
  }
}

# create directory
dir.create("./gen/data-preparation/output")

# save merged data
save(reviews_df,file="./gen/data-preparation/temp/content.RData")
