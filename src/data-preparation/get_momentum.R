require(dplyr)

momentum <- function(){
  
  #' Creates dummy variable which shows what the momentum is.
  #' Momentum is identified when release date and the review data
  #' are at least 7 days in between. 
  
  # add datasets to transfrm
  popularity_df <- load("./gen/data-preparation/temp/transform_reviews.RData")
  simultaneous_df <- load("./gen/data-preparation/temp/transform_releases.RData")
  
  # add a column in order to account for momentum
  popularity_df$momentum <- 0
  
  # skip na from analysis as not useful
  popularity_df <- popularity_df %>%
    na.omit(review_date)
  
  simultaneous_df <- simultaneous_df %>%
    na.omit(release_date)
  
  # iterate over each row in popularity_df and releases
  for (i in 1:nrow(popularity_df)){
    for (j in 1:nrow(simultaneous_df)){
      # when the ids are equal, then check for that release date of that episode
      # in order to find whether the review date has been written within a week
      if (popularity_df$id[i] == simultaneous_df$imdb_id[j]){
        if(popularity_df$review_data[i] >= simultaneous_df$release_date[j] & popularity_df$review_data[i] < simultaneous_df$release_date[j] + 7){
          popularity_df$momentum[i] <- 1
        }
      }
    }
  }
  return(popularity_df)
}

momentum_df <- momentum()

# create directory
dir.create("./gen/data-preparation/output")

# save transformed data
save(momentum_df, file= "./gen/data-preparation/output/momentum.RData")