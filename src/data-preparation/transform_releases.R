#packages needed
require(dplyr)
require(tidyquant)

momentum <- function(csv_file = "./gen/data-preparation/input/releases.csv"){
  
  # import release dates csv
  releases <- read.csv(csv_file, sep = ";")
  
  # set release data as dates
  releases$release_data <- as.Date(releases$release_date, "%Y-%m-%d"))
  
  # create dummy whether whole season is dropped simultaneously
  releases <- releases %>%
    group_by(tmdb_id, season_number) %>%
    mutate(simultaneous = ifelse(n_distinct(release_date) == 1, 1,0))
  
  # merge release with popularity
  merged_df <- merge(popularity_df, releases, by.x = "id", by.y = "imdb_id")
  
  # check whether review date is written within 7 days 
  momentum_df <- merged_df %>%
    group_by(tmdb_id) %>%
    mutate(momentum = ifelse(review_data >= release_date & review_data < release_date + 7, 1, 0))
  
  return(momentum_df)
}

momentum_df <- momentum()

# create directory
dir.create("./gen/data-preparation/temp")

# save transformed data
save(popularity_df, file= "./gen/data-preparation/temp/transform_releases.RData")
