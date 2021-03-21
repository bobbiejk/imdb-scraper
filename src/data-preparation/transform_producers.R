originals <- function(csv_file = "./gen/data-preparation/input/producers.csv"){
  
  #' Creates dummy variable whether the show is original.
  #' Orginality is specified when a streaming service
  #' specified in the list streaming_services is found in
  #' the producers list
  #' 
  #' @param csv_file Output of data collection of producers
  
  # import dataset
  producers <- read.csv(csv_file, sep=",")
  
  # in this data set, the only streaming service of interest is Netflix
  streaming_services <- c("Netflix")
  
  # hence the column original stands for Netflix original
  producers$original <- NA
  
  # check whether streaming service is in list of producers
  for (row in 1:nrow(producers)){
    for (streaming_service in streaming_services){
      if (grepl(streaming_service, producers[row,2]) == 1){ 
        producers[row,original] <- 1 
      }
      else{
        producers[row, original] <- 0
      }
    }
  }
  return(producers)
}

# get originals
originals_df  <- originals()

# create directory
dir.create("./gen/data-preparation/temp")

# save transformed data
save(originals_df, file= "./gen/data-preparation/temp/transform_producers.RData")
