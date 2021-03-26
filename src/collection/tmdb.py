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
    with open('../../data/imdb/content.csv') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
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

    # divide URL in shorter parts
    base_url = "https://api.themoviedb.org/3/" 
    api_key_url = f"?api_key={api_key}" 
    find_url = "find/"
    external_source_url =  "&external_source=imdb_id"

    # for each row in release dates get imdb id
    for row in transform_ids:
        print(row)
        try:
            imdb_id = row['imdb_id']
        # needed as it may break when last line of csv is empty row
        except:
            break

        url = base_url + find_url + imdb_id + api_key_url + external_source_url
        r = requests.get(url)
        responses = r.json() # transform request into json so that you can extract data from it

        # if tv then responses['tv_results'] is a filled list
        if len(responses['tv_results']) != 0:
            tmdb_id = responses['tv_results'][0]['id']
            content_type = 'tv'

        # if movie then responses['movie_results'] is a filled list
        elif len(responses['movie_results']) != 0:
            tmdb_id = responses['movie_results'][0]['id'] 
            content_type = 'movie'
        
        # extend every row of transform_id with tmdb id and content type
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
            Note that the API request depends on whether the content
            type is movie or tv show. Hence, content type needs to be
            filtered before requesting to API. Movies only have one
            release date. TV have release dates based on the episode
            number of a certain season. Hence, release dates for TV shows
            are stored in a list of dictionaries, consisting of sesason
            number, episode number and release date.
    ''' 
    base_url = "https://api.themoviedb.org/3/" 
    api_key_url = f"?api_key={api_key}" 
    
    for row in transform_ids:

        release_data = []

        if row['content_type'] == 'movie':
            movie_url = 'movie/'
            movie_id = str(row['tmdb_id'])

            # print id to show in terminal that code is running
            print(movie_id)

            url = base_url + movie_url + movie_id + api_key_url
            r = requests.get(url)
            responses = r.json() # makes it into a dictionary

            release_date = responses['release_date']

            # extend row of transform id with release date
            row.update({'release_date': release_date})

        else: 
            tv_url =  'tv/'
            tv_id = str(row['tmdb_id'])

            # print id to show in terminal that code is running
            print(tv_id)

            url = base_url + tv_url + tv_id + api_key_url
            r = requests.get(url)
            responses = r.json() 

            season_number = responses['number_of_seasons']

            # get a list of all season numbers subsequentially
            season_list = []
            for i in range(season_number): 
                season_list.append(i+1)

            # for each season get the episode data
            for season_item in season_list:
                season_url = '/season/'
                season_number = str(season_item)
                url = base_url + tv_url + tv_id + season_url + season_number + api_key_url
                r = requests.get(url)
                responses = r.json()

                # if api request is successful, key should be episodes
                if "episodes" in responses:
                    episodes_data = responses['episodes'] 
                # otherwise episodes should not be a key, and request success is false
                else:
                    continue

                # for each episode in episodes data, get the episode number and air date
                for episode_item in episodes_data:
                    episode_number = episode_item['episode_number']
                    air_date = episode_item['air_date']

                    release_data.append({'season_number': season_number,
                                        'episode_number': episode_number,
                                        'air_date': air_date})

            # extend row of transform id with release date
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
        # for row in release_dates
        for row in release_dates:
            # if movie
            if row['content_type'] == 'movie':
                writer.writerow([row['imdb_id'], row['tmdb_id'], row['release_date'], 'NA', 'NA'])
            # if tv
            else:
                # for key in the dictionary release date
                for item in row['release_date']:
                    writer.writerow([row['imdb_id'], row['tmdb_id'], item['air_date'], item['season_number'], item['episode_number']])
    print("done!")
    
    return

make_releases_csv(release_dates)