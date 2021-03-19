#packages needed
require(dplyr)
require(tidyquant)

popularity <- function(csv_file = "./gen/data-preparation/input/reviews.csv"){
  
  # import reviews csv
  reviews <- read.csv(csv_file, sep=";")
  
  # set review date to actual date
  reviews$review_data <- as.Date(reviews$review_data, "%d %B %Y")
  
  # review count column
  reviews$review_count <- 1
  
  # get first number in rating
  reviews$review_rating_num <- as.numeric(gsub("/.*", "", reviews$review_rating))
  
  # aggegrate count weekly
  reviews_count_agg <- reviews %>%
    group_by(id) %>%
    tq_transmute(select = review_count,
                 mutate_fun = apply.weekly,
                 FUN = sum,
                 col_rename = "review_count_weekly")
  
  # aggregate rating weekly
  reviews_rating_agg <- reviews %>%
    group_by(id) %>%
    tq_transmute(select = review_rating_num,
                 mutate_fun = apply.weekly,
                 FUN = mean,
                 col_rename = "review_rating_weekly")
  
  # merge the weekly count and the weekly rating
  reviews_merge <- merge(reviews_count_agg, reviews_rating_agg)
  
  # round review rating to 1 decimal
  reviews_merge$review_rating_weekly <- round(reviews_merge$review_rating_weekly, digits = 1)
  
  return(reviews_merge)
}
popularity_df <- popularity()

# create directory
dir.create("./gen/data-preparation/temp")

# save transformed data
save(popularity_df, file= "./gen/data-preparation/temp/transform_reviews.RData")

