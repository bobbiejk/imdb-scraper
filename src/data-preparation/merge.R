# install packages
require(dplyr)

# load data associated with content
load("./gen/data-preparation/temp/transform_producers.RData")
load("./gen/data-preparation/temp/transform_distributors.RData")

# load data associated with releases
load("./gen/data-preparation/temp/transform_releases.RData")

# load data associated with reviews
load("./gen/data-preparation/temp/transform_reviews.RData")

# change original data set
originals_df <- originals_df %>%
  select(id, original) %>%
  distinct(id, .keep_all = TRUE)

# add original to the data set
reviews_df <- left_join(reviews_df, originals_df, by="id")

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

# remove those titles that are in production
reviews_df <- reviews_df[!(reviews_df$exclusive == 0 & reviews_df$original == 1),]

# add releasing and simultaneous dummy to the data set
reviews_df$releasing <- 0
reviews_df$simultaneous <- 0
reviews_df$duration <- 0

for (i in 1:nrow(reviews_df)){
  print(i)
  for (j in 1:nrow(releases_df)){
    
    # check if similar ids
    if (reviews_df$id[i] == releases_df$imdb_id[j]){
      # count the difference between release date and review written
      duration <- reviews_df$review_data[i] - releases_df$release_data
      reviews_df$duration[i] <- duration
      
      # check whether review has been written in same week
      if (reviews_df$review_data[i] >= releases_df$release_data[j] & reviews_df$review_data[i] < releases_df$release_data[j] + 7 & !is.na(reviews_df$review_data[i]) & !is.na(releases_df$release_data[j])){
        reviews_df$releasing[i] <- 1
        #transfer value simultaneous from releases to reviews
        reviews_df$simultaneous[i] <- releases_df$simultaneous[j]
      }
    }
  }
}

# create directory
dir.create("./gen/data-preparation/output")

# save merged data
save(reviews_df,file="./gen/data-preparation/output/reviews.RData")
