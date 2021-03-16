# packages needed
import requests
import json
import os.path
import csv
import os

api_key = os.environ['TMDB_API']

def extract_content_data(): 
    
    ''' Set content csv to list of dictionaries to use in following functions
    
        Returns:
            List of dictionaries consisting of IMDb ID
    ''' 
    # opened csv file
    with open('data/imdb/content.csv') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            content_data = list(reader)

    return content_data

content_data = extract_content_data()

def transform_imdb_in_tmdb(content_data):

    ''' Transforms IMDb ID to TMDb ID and extracts content type

        Args:
            content_data: Output of extract_content_csv()

        Returns:
            List of dictionaries consisting of IMDb ID, TMDb ID
            and content type
    ''' 

    # create empty list of dictionaries
    transform_ids = []   

    # for each row check the imdb_id
    for row in content_data:
        imdb_id = row['id']
        transform_ids.append({'imdb_id':imdb_id})
                                # { KEY : VALUE}
                                # COLUMN NAME

    base_url = "https://api.themoviedb.org/3/" 
    api_key_url = f"?api_key={api_key}" 
    find_url = "find/"
    external_source_url =  "&external_source=imdb_id"

    # for each row in release dates get imdb id
    for row in transform_ids:
        try:
            imdb_id = row['imdb_id']
        except:
            break

        url = base_url + find_url + imdb_id + api_key_url + external_source_url
        r = requests.get(url)
        responses = r.json() # transform request into json so that you can extract data from it

        # if tv
        if len(responses['tv_results']) != 0:
            tmdb_id = responses['tv_results'][0]['id']
            content_type = 'tv'

        # if movie
        if len(responses['movie_results']) != 0:
            tmdb_id = responses['movie_results'][0]['id'] 
            content_type = 'movie'
        
        row.update({'tmdb_id': tmdb_id,
                    'content_type': content_type})
    
    return transform_ids

transform_ids = transform_imdb_in_tmdb(content_data)

def extract_releases_data(transform_ids):
    
    ''' Get release dates information from API of TMDb
    
        Args:
            transform_ids: Output of transform_imdb_to_tmdb()

        Returns:
            List of dictionaries consisting of IMDb ID, TMDB ID,
            release dates, episode numbers and season numbers. 
            Episode numbers and season numbers are only available
            for TV. Only TV returns for release dates an additional
            list of dictionaries consisting of all release dates
            per episode.
    ''' 
    base_url = "https://api.themoviedb.org/3/" 
    api_key_url = f"?api_key={api_key}" 
    
    for row in transform_ids:

        release_data = []

        if row['content_type'] == 'movie':
            # https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<api_key>>
            movie_url = 'movie/'
            movie_id = str(row['tmdb_id'])
            url = base_url + movie_url + movie_id + api_key_url
            r = requests.get(url)
            responses = r.json() # makes it into a dictionary

            release_date = responses['release_date']

            row.update({'release_date': release_date})

        else:
            # https://api.themoviedb.org/3/tv/{tv_id}?api_key=<<api_key>> 
            tv_url =  'tv/'
            tv_id = str(row['tmdb_id'])
            url = base_url + tv_url + tv_id + api_key_url
            r = requests.get(url)
            responses = r.json() 

            season_number = responses['number_of_seasons']

            season_list = []
            for i in range(season_number): 
                season_list.append(i+1)

            for season_item in season_list:
                # https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}?api_key=<<api_key>>
                season_url = '/season/'
                season_number = str(season_item)
                url = base_url + tv_url + tv_id + season_url + season_number + api_key_url
                r = requests.get(url)
                responses = r.json()

                episodes_data = responses['episodes'] # list of dictionaries

                for episode_item in episodes_data:
                    episode_number = episode_item['episode_number']
                    air_date = episode_item['air_date']

                    release_data.append({'season_number': season_number,
                                        'episode_number': episode_number,
                                        'air_date': air_date})

            row.update({'release_date': release_data})

    return transform_ids

release_dates = extract_releases_data(transform_ids)

def make_releases_csv(release_dates):

    ''' Make a csv file to get information of release dates.
    
        Args:
            release_dates: Output of extract_releases_data()

        Returns:
            CSV file consisting of IMDb ID, TMDb ID, release dates,
            season number, episode number. If it is a movie type,
            then episode and season number are depicted as 'NA'
    ''' 
    dirname = "data/tmdb"
    try:
        os.makedirs(dirname)
        print("Directory has been created")
    except FileExistsError:
        print("Directory already exists") 

    # if path does not exists that means that csv file needs to be made
    if os.path.isfile("data/tmdb/release_dates.csv") == False:
            # hence column names need to be specified
            with open("data/tmdb/release_dates.csv", "a", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=";")
                writer.writerow(["imdb_id", "tmdb_id", 'release_date', 'season_number', 'episode_number'])

    # insert values in csv file   
    with open("data/tmdb/release_dates.csv", "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for id_item in release_dates:
            # if movie
            if id_item['content_type'] == 'movie':
                writer.writerow([id_item['imdb_id'], id_item['tmdb_id'], id_item['release_date'], 'NA', 'NA'])
            # if tv
            else:
                for episode_id in id_item['release_date']:
                    writer.writerow([id_item['imdb_id'], id_item['tmdb_id'], episode_id['air_date'], episode_id['season_number'], episode_id['episode_number']])
    print("done!")
    
    return

make_releases_csv(release_dates)





# with open -> a to append, w to write, and r to read




#for
#if
#list.append
#dict.update  

# RELEASE DATES DICTIONARY
# # TMDB, IMDB, CONTENT TYPE, RELEASE DATA

# RELEASE DATA DICTIONARY
# # SEASON NUMBER, EPISODE NUMBER, AIR DATE







            





        


# LIST OF DICTIONARIES -> DICTIONIARY -> KEY:VALUE -> [KEY] -> VALUE
# RELEASE_DATES -> ROW -> IMDB: ####, TMDB: ###, CONTENT_TYPE: MOVIE OF TV -> [IMDB_ID] -> #####
# A LIST SHOULD ALWAYS BE LOOPED TO EXTRACT ELEMENTS -> release_dates is a list of dictionaries, dat betekent dat elk element van de lijst een dictionary is
# WHAT ARE THE ELEMENTS OF A LIST OF DICTIONARIES, ALL INVIDIUAL DICTIONARIES -> release_dates is elke row a dictionary
# TO GET THE VALUE OF A KEY OF A DICTIONARY, BENOEM JE DE DICTIONARY -> ROW['KEY'] -> VALUE

## YOU END UP WITH AN TMDB ID
## NEED TO GET CONTENT TYPE

## DO I GET TV_RESULTS OR MOVIE_RESULTS. if len(responses['tv_results']) == 0, then content_type = movie

### Look up release data for movies
# def release_date(tmdb_ids):
# if content type is movie:
# then get release date
# get origin country

## DISCOVER API > MOVIES > DETAILS


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
