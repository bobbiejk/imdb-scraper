originals <- function(){

  # import dataset
  producers <- read.csv("./gen/data-preparation/input/producers.csv", sep=";")
  
  # create data frame colnames
  streaming_services <- c("Netflix", "Disney+", "Medialand")
  producers[,streaming_services] <- NA
  
  # check whether streaming service is in list of producers
  for (row in 1:nrow(producers)){
    for (streaming_service in streaming_services){
      if (grepl(streaming_service, producers[row,2]) == 1){ 
        producers[row,streaming_service] <- 1 
      }
      else{
        producers[row, streaming_service] <- 0
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
