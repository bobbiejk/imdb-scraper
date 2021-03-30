# packages needed
require(dplyr)
require(purrr)
require(stringr)

exclusivity <- function(csv_file = "./gen/data-preparation/input/distributors.csv"){
  
  #' Creates dummy variable indicating the exclusivity
  #' of a title. Exclusivity is specified when during 
  #' that year there is only one distributor.
  #' 
  #' @param csv_file Output of data collection of distributors
  
  # import dataset
  distributors <- read.csv(csv_file, sep=",")
  
  # remove rows that include NA as this rows cannot provide information on exclusivity
  distributors <- distributors %>%
    na.omit()
  
  # clean data from faulty observation
  distributors <- distributors[!(distributors$id == "tt4908644" & distributors$distributor_country == "Chile "),]
  
  # get unique_ids from dataset
  unique_ids = c()
  for (id in distributors$id){
    if (!(id %in% unique_ids)){
      unique_ids[[length(unique_ids)+1]] <- id
    }
  }
  # make a dataset to store exclusivity per year per IMDB id 
  exclusive_df = data.frame()
  
  # create column names
  exclusive_names <- c("id", "year")
  for (exclusive_name in exclusive_names){
    exclusive_df[,exclusive_name] <- as.character()
  } 
  # put all unique IMDb id in data frame with all years in single rows
  for (unique_id in unique_ids){
    start_year <- 2022
    end_year <- 2000
    
    for (row in 1:nrow(distributors)){
      if (distributors$id[row] == unique_id){
        
        start_year_row <- as.numeric(str_replace(distributors$distributor_start_year[row], "-", ""))
        print(start_year_row)
        end_year_row <- distributors$distributor_end_year[row]
        
        if (start_year_row < start_year){
          start_year <- start_year_row
        }
        if (end_year_row > end_year){
          end_year <- end_year_row
        }
      }
    }
    sequence <- seq(start_year, end_year, by = 1)
    for (year in sequence){
      exclusive_df[nrow(exclusive_df)+1, ] <- list(unique_id, year)
    }
  }
  # append distributors per year for certain id
  for (row_df in 1:nrow(exclusive_df)){
    
    # set list empty for year for certain id
    distributor_list = list()
    
    for (row in 1:nrow(distributors)){

      if (exclusive_df$id[row_df] == distributors$id[row]){
        
        start_year_row <- as.numeric(str_replace(distributors$distributor_start_year[row], "-", ""))
        end_year_row <- distributors$distributor_end_year[row]
        year <- exclusive_df$year[row_df]
        
        if (between(year, start_year_row , end_year_row) == TRUE){
          distributor <- distributors$distributor_name[row]
          
          if (!(distributor %in% distributor_list)){
            distributor_list[[length(distributor_list)+1]] <- distributor
          }
        }
      }
    }
    # check whether the distributor list has items in it
    if (length(distributor_list) == 0){
      exclusive_df$distributors[row_df] <- ""
      exclusive_df$exclusive[row_df] <- 0
    }
    else{
      # indicate exclusivity when there is one distributor and that distributor is Netflix
      exclusive <- if (length(distributor_list) == 1 & grepl("Netflix", distributor_list)) 1 else 0 
      
      # need to transpose list in order to fit in data frame
      distributor_t <- transpose(distributor_list)
      
      # add variables to data frame
      exclusive_df$distributors[row_df] <- distributor_t
      exclusive_df$exclusive[row_df] <- exclusive 
    }
  }
  return(exclusive_df)
}
exclusive_df <- exclusivity()

# create directory
dir.create("./gen/data-preparation/temp")

# save transformed data
save(exclusive_df, file= "./gen/data-preparation/temp/transform_distributors.RData")