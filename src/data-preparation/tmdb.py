# packages needed
import requests
import json
import os.path

# my credentials
api_key = "cf279383d33a6bd1a247f9292db24121"

base_url = "https://api.themoviedb.org/3/"
api_key_url = f"?api_key={api_key}"

watch_provider_url = "&with_watch_providers="
watch_providers = ["Netflix", "Disney+", "AmazonPrime"]

for watch_provider in watch_providers:
    r = requests.get(f"https://api.themoviedb.org/3/discover/movie/?api_key={api_key}&language=en-US&with_watch_providers=Netflix")
    responses = r.json()

###########
## TO DO ##
###########

def load_content_csv(content = "content.csv"):
    
    ''' Downloads file consisting of all content and their ids.

    Args:
        users: content.csv collected from web scraper collecting content

    Returns: 
        List of dictionaries consisting of IMDb ID, title, duration,
        country, stars and genres. This IMDb is the variable of interest.

    '''
    # make sure right directory has been set
    # needed to be turn off for make file
    print(os.getcwd())
    
    with open (f"data/{content}") as csv_file:
        reader = csv.DictReader(csv_file)
        content_data = list(reader)

    return content_data

content_data = load_content_csv()
print(content_data)

###  Tranform IMDb IDs into TMDb IDs
def transform_imdb_in_tmdb(content_data):

    for imdb_id in content_data["id"]:
        
        print(imdb_id)

        find_url = "find/"
        external_source_url = "&external_source=imdb_id"
        
        url = base_url + find_url + imdb_id + api_key_url + external_source_url
        r = requests.get(url)
        responses = r.json()

        print(responses)

    return

transform_imdb_in_tmdb(content_data)
# for external_id in external_ids:
#   url = base_url + find_url + api_key_url + external_source_url
#   r = requests.get(url)
#   responses = r.json

# check whether there is a release data or first air date
# first air date indicates tv series
# release data indicates movies
# set type of content 
# Output  is list of dictionaries with IMDb, TMDb ID, Content type

### Look up release data for movies
# def release_date(tmdb_ids):
# if content type is movie:
# then get release date
# get origin country


### Look up episode air date for shows
# def air_date(tmdb_ids):
# if content type is tvshow

## from tv api doc
# get origin country
# get producers
# get number of seasons
# get number of episodes per season

## from tv episode api doc
# get air dates per episode







r = requests.get("https://api.themoviedb.org/3/tv/87739?api_key=cf279383d33a6bd1a247f9292db24121")
responses = r.json()

print(responses)




