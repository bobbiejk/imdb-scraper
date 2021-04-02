# get the urls
url_dist = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRtJDK6qqMuBnlS2Wh7cPLzqOrcsk_k8WHZiCIFOtWxfwAnJLENL9o7LzvgypPKy72Yu1R8w1hmwHZu/pub?gid=1803318986&single=true&output=csv"
url_prod = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQcUNhaApQbcn_EpG5o4gS2GIXw8qY2UYQ9Yf6vU-fewPMVHc8wd7_4hKrS1R-7qxN6rXmaOqb9Hn1W/pub?gid=852962914&single=true&output=csv"
url_cont ="https://docs.google.com/spreadsheets/d/e/2PACX-1vSr6Zp-qQ2BBqz5pPoz1Ab1BatnNEvwU4Abm3IJeC1r2lH3okpGXoKMafSWJnkmlMpHkHRteborPfdp/pub?gid=1977069416&single=true&output=csv"
url_rev = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLP4F-17eP4WSjLDJI3kSOzSPWNxvi1CVLq8to32ksFBm1AhTb6ex-cMfVHpakJDDcQFr-XzczEsnn/pub?gid=1374568034&single=true&output=csv"
url_rel = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRSJiLcXeO6TXbZv_OL-MKiUNLJtLkLxZjigcogtT8zrlwu5pwLrFwG9kNRSm1x5eN5T21qhX3xm5KI/pub?gid=1677454268&single=true&output=csv"

# read csv from website
distributors <- read.csv(url(url_dist))
producers <- read.csv(url(url_prod))
content <- read.csv(url(url_cont))
reviews <- read.csv(url(url_rev))
releases <- read.csv(url(url_rel), sep = ";")

# create directory
dir.create("data")
dir.create("data/imdb")
dir.create("data/tmdb")

# write to data map
write.csv(distributors, "./data/imdb/distributors.csv")
write.csv(distributors, "./data/imdb/producers.csv")
write.csv(distributors, "./data/imdb/content.csv")
write.csv(distributors, "./data/imdb/reviews.csv")
write.csv(distributors, "./data/tmdb/releases.csv")

