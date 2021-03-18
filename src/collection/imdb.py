# packages needed
from bs4 import BeautifulSoup
from time import sleep
import requests
import csv 
import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


# seeds that start at the base of distributor content
distributor_base_urls = {
    "Netflix":"https://www.imdb.com/search/title/?companies=co0144901"}

def generate_page_urls(base_url, num_pages):

    ''' Collects all pages needed to navigate to all content connected
        to the base_url.
        
        Args: 
            base_url: IMDb url linked to a streaming service. String.
            num_pages: Number of how many pages it should collect. Integer.

        Returns:
            List of page urls in order to navigate through the website
            which has all hits on the distributor base url. Full page
            urls consists of a base urls and counter that corresponds 
            to moving towards the next page. 
    '''

    page_urls = []

    counter_content = 10001
    for counter in range(1,num_pages+1):

        #make sure that is alphabetically sorted, ascending, per 250 items
        sort_alpha = "&sort=alpha,asc"
        start_at = "&start=" + str(counter_content)
        count = "&count=250"

        #assemble full url
        full_url = base_url + sort_alpha + start_at + count
        page_urls.append(full_url)

        #make sure that next page shows next 250 content
        counter_content += 250

        sleep(2)

    return page_urls

page_urls = generate_page_urls(distributor_base_urls["Netflix"],5)
print(page_urls)

def extract_content_urls(page_urls):

    ''' Generates from each distributor-linked search results the page
        URLs of the content linked to those distributors.
        
        Args:
            page_urls: Outcome of generate_page_urls(base_url, num_pages)
        
        Returns:
            List of dictionaries consisting of content id, content url
            and content title. Content url navigates to content-specfic
            homepage. Content id equals the IMDB id.
    '''

    content_urls = []

    for page_url in page_urls:
        request = requests.get(page_url)
        soup = BeautifulSoup(request.text, "html.parser")
        all_content = soup.find_all(class_="lister-item-header")

        for content in all_content:
            content_title = content.find("a").get_text()
            content_url = "https://www.imdb.com" + content.find("a").attrs["href"]
            content_id = content_url.split("/")[4]

            if not any(d["id"] == content_id for d in content_urls):
                content_urls.append({"id": content_id,
                                    "title": content_title,
                                    "url": content_url})
            else:
                continue

        sleep(2)
        
        # know how many items have been added to dictionary per page url
        print(len(content_urls))

    return content_urls

content_urls = extract_content_urls(page_urls)

def extract_content_data(content_urls):

    ''' Collect content-specific info from content links collected
    
        Args:
            content_urls: Outcome of extract_content_urls(page_urls)
        
        Returns:
            List of dictionaries consisting of the IMDB id, the title,
            the country it is associated wtih, the duration of a single
            instance of the show (movie or episode), a list of genres,
            and the stars associated with the content.
    '''
    content = []

    for content_url in content_urls:
        url = content_url["url"]
        print(url)
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")

        # set duration to empty
        duration = ""

        # check whether duration exists
        find_duration = soup.find(class_="title_wrapper").find("time")
        if find_duration:
            duration = find_duration.get_text().replace("\n","").replace(" ","")
        
        # set country to empty
        country = ""
        
        # check whether movie details exists
        find_details = soup.find(id="titleDetails")
        if find_details: 

            # check whether country exists
            find_country = find_details.find_all("a")
            if find_country:
                if len(find_country) > 2:
                    country_data = find_country[2]
                    if country_data:
                        country = country_data.get_text()
        
        # if movie details not exist
        else:
            print(f'This {url} is in production')
            continue
        
        # set genres to empty list
        genres = []

        # check whether genres exist
        find_genres = soup.find_all(class_="see-more inline canwrap")
        if find_genres: 
            if len(find_genres) > 1: 
                genre_data = find_genres[1]
            else:
                genre_data = find_genres[0]
            genre_list = genre_data.find_all("a")
            for genre_item in genre_list:
                genre = genre_item.get_text().replace(" ","")
                genres.append(genre)

        # set starts to empty list
        stars = []

        # check whether stars exists
        find_stars = soup.find(class_="credit_summary_item")
        if find_stars:
            stars_list = find_stars.find_all("a")
            for stars_item in stars_list:
                star = stars_item.get_text()
                if star == "See full cast & crew": 
                    continue
                else:
                    stars.append(star)

        content.append({"id": content_url["id"],
                        "title": content_url["title"],
                        "duration": duration,
                        "country": country,
                        "stars": stars,
                        "genres": genres})

        sleep(2)

    return content

#content = extract_content_data(content_urls)

def make_content_csv(content):

    ''' Transforms the content list of dictionaries in a CSV.

        Args:
            content: Output of extract_content_data(content_urls)

        Returns:
            CSV file consisting of IMDB id, title, duration, country,
            stars and genres. The CSV file is stored in ../data/imdb/
            directory.
    ''' 
    # make sure right directory has been set
    print(os.getcwd())
    # this ensures that all following functions are in this directory
    os.chdir('../../')

    # check whether file location exists
    dirname = "data/imdb"
    try:
        os.makedirs(dirname)
        print("Directory has been created")
    except FileExistsError:
        print("Directory already exists") 

    if os.path.isfile("data/imdb/content.csv") == False:
        with open("data/imdb/content.csv", "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["id", "title",
                             "duration", "country",
                             "stars", "genres"])
       
    with open("data/imdb/content.csv", "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for row in content:
            writer.writerow([row['id'], row['title'], row['duration'], row['country'], row['stars'], row['genres']])
    print("done!")

    return 

#make_content_csv(content)

def extract_company_data(content_urls):

    ''' Collects producer and distributor information listed on each
        content title's IMDb website.

        Args:
            content_urls: Output of extract_content_urls(page_urls)

        Returns:
            List of dictionaries consisting of companies associated 
            with the IMDB id. Retrieve all producers and distributors
            listed on imdb.com/title/company_credits. Producers are 
            within a list, whereas distributors is a list of dictionaries, 
            specifying name, year, country and type (TV, SVOD, Cinema).
            Besides it extracts the start year and end year of each 
            distributor. "2019-" is transformed in "start year: 2019", 
            "end year: 2021".
    '''
    company_credits = []

    # access all individual content_urls
    for content in content_urls:

        company_credits_url = content["url"] + "companycredits"
        request = requests.get(company_credits_url)
        soup = BeautifulSoup(request.text, "html.parser")

        # id of each content extracted from content_urls
        content_id = content["id"]
        print(content_id)

        # create list for production companies for content
        production_companies = []
        find_production = soup.find(id="production")
        
        # check whether production companies are available
        if find_production:
            
            # "ul" contains producer items after find_production
            production_list = find_production.find_next("ul").find_all("a")
            
            for production_item in production_list:
                production_companies.append(production_item.get_text())

        else:
            print(f"No producers found for {content_id}")

        # create list for distributor companies for content
        distributors = []
        find_distributor = soup.find(id="distributors")
        
        # check whether distributor companies are available
        if find_distributor:

            # "ul" constains distributor items after find_distributor
            distributor_list = find_distributor.find_next("ul").find_all("li")
            
            for distributor_item in distributor_list:
                distributor_name = distributor_item.find("a").get_text()
                length_name = len(distributor_name)
                
                # distributor_info needs to be cleaned to extract year, country and type(s)
                distributor_info = distributor_item.get_text()[length_name:]
                
                # check whether first item in distributor_info is year
                distributor_year = ""
                first_item = distributor_info.split('(')[1]
                
                for character in first_item:
                    if character.isdigit() or character == "-":
                        distributor_year = distributor_year + character

                if len(distributor_year) <= 3:
                    distributor_year = ""
                
                # if distributor year is specified, then country is second in list, followed by types
                if distributor_year:
                    distributor_country = distributor_info.split(distributor_year[-4:])[1].split("(")[1].replace(")","")
                    distributor_types = distributor_info.split(distributor_year[-4:])[1].split("(")[2:]

                # if distributor year is not specified, then country first in list followed by types
                else:
                    distributor_country = distributor_info.split("(")[1].replace(")","")
                    distributor_types = distributor_info.split("(")[2:]              
                
                # distributor types be cleaned in order to be list item
                distributor_types_cleaned = []  

                for distributor_type in distributor_types:
                    distributor_types_cleaned.append(distributor_type.replace(")","").replace("\n","").replace(" ",""))

                # determine start and end year
                if len(distributor_year) == 4:
                    start_year = distributor_year
                    end_year = distributor_year
                elif len(distributor_year) == 5:
                    start_year = distributor_year[:4]
                    end_year = 2021 # this is hard coded, what works for data analysis, current distributor
                elif len(distributor_year) == 9:
                    start_year = distributor_year[:4]
                    end_year = distributor_year[-4:]
                
                # append all distributor data in a list of dictionaries
                distributors.append({"name": distributor_name,
                                    "start_year": start_year,
                                    "end_year": end_year,
                                    "country": distributor_country,
                                    "type": distributor_types_cleaned})

        else:
            print(f"No distributor found for {content_id}")

        # append company credits data in a list of dictionaries
        company_credits.append({"id": content_id,
                                "producers":production_companies,
                                "distributors":distributors})
                                
        sleep(2)
       
    return company_credits

company_credits = extract_company_data(content_urls)

def make_producers_csv(company_credits):

    ''' Creates CSV file of producer information per IMDB id
    
        Args:
            company_credits: Output of extract_company_data(content_urls)
    
        Returns:
            CSV file consisting of IMDB id and list of producers. CSV is
            stored in ../data/imdb/ directory
    ''' 
   # make sure right directory has been set
    print(os.getcwd())
    
    # check whether file location exists
    dirname = "data/imdb"
    try:
        os.makedirs(dirname)
        print("Directory has been created")
    except FileExistsError:
        print("Directory already exists") 

    if os.path.isfile("data/imdb/producers.csv") == False:
        with open("data/imdb/producers.csv", "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["id", "producer"])
       
    with open("data/imdb/producers.csv", "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for credit in company_credits:
            # currently producers is set to a list, so each instance is a id
            # this is to iterate over each row, and then question whether 
            # producer e.g. "Netflix" is in list and then say it is Netflix Original
            writer.writerow([credit['id'], credit['producers']])
    print("done!")

    return 

make_producers_csv(company_credits)

def make_distributor_csv(company_credits):

    ''' Make a csv file to get information of each distributor involved 
        with each IMDb ID.
    
        Args:
            company_credits: Output of extract_company_data(content_urls)

        Returns:
            CSV file consisting of id of content, distributor, start year,
            distributor end year, distributor country and distributor type.
            IMDb id can have multiple entries based on number distributors 
            there are for each id. For example, tt7078180 has 5 distributors, 
            hence this id has 5 entries.
    ''' 
   # make sure right directory has been set
    print(os.getcwd())
    
    # check whether file location exists
    dirname = "data/imdb"
    try:
        os.makedirs(dirname)
        print("Directory has been created")
    except FileExistsError:
        print("Directory already exists") 

    if os.path.isfile("data/imdb/distributors.csv") == False:
        with open("data/imdb/distributors.csv", "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["id", "distributor_name",
                             "distributor_type", "distributor_country",
                             "distributor_start_year", "distributor_end_year"])
       
    with open("data/imdb/distributors.csv", "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for credit in company_credits:
            for distributor in credit["distributors"]:
                writer.writerow([credit['id'], distributor['name'], distributor['type'], distributor['country'], distributor['start_year'], distributor['end_year']])
    print("done!")

    return 

make_distributor_csv(company_credits)

def extract_review_data(content_urls):

    ''' Collects review date and review rating of all content
        
        Args:
            content_urls: Output of extract_content_urls(page_urls)

        Returns:
            List of dictionaries consisting of IMDB id, review date,
            and review rating. Review dates are stored in a list in order
            to compute the volume of the reviews and aggregate these in a
            weekly overview to find the rate at which popularity decreases
    '''

    driver = webdriver.Chrome()

    review_data = []

    for content in content_urls:
        
        content_id = content["id"]
        print(content_id)
        # reviews that are sorted by submission date
        reviews_url = content["url"] + "reviews" + "/?sort=submissionDate&dir=desc&rating"
        
        driver.get(reviews_url)

        request = driver.page_source.encode("utf-8")
        soup = BeautifulSoup(request, "html.parser")

        # click on all load more buttons
        while True:
            # check whether there is a button
            try:
                button_data = driver.find_elements_by_class_name("ipl-load-more__button")
                button = button_data[0]
            except IndexError:
                break
            # check whether there is a clickable button
            try:
                button.click()
            except WebDriverException:
                break
            
            request = driver.page_source.encode("utf-8")
            soup = BeautifulSoup(request, "html.parser")

            # sleep when clicked on button
            sleep(1)    
    
        review_container = soup.find_all(class_="lister-item mode-detail imdb-user-review collapsable")
        
        for review_item in review_container:
            review_date = review_item.find(class_ = "review-date").get_text()
            review_rating_data = review_item.find(class_="rating-other-user-rating")
            if review_rating_data:
                review_rating = review_rating_data.text.strip()
            else:
                review_rating = ""
            
            review_data.append({"id": content_id,  
                                "date": review_date,
                                "rating": review_rating})
    return review_data

review_data = extract_review_data(content_urls)

def make_reviews_csv(review_data):

    ''' Creates CSV file of reviews per IMDb id
    
        Args:
            review_data: Output of extract_review_data(content_urls)
    
        Returns:
            CSV file consisting of IMDb id, review data and review rating.
            Each IMDb id may have several entries depending on the number
            of reviews that IMDb id has. CSV is stored in ../data/imdb/ 
            directory
    ''' 
    # make sure right directory has been set
    print(os.getcwd())

    # check whether file location exists
    dirname = "data/imdb"
    try:
        os.makedirs(dirname)
        print("Directory has been created")
    except FileExistsError:
        print("Directory already exists") 

    if os.path.isfile("data/imdb/reviews.csv") == False:
        with open("data/imdb/reviews.csv", "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["id", "review_data", "review_rating"])
       
    with open("data/imdb/reviews.csv", "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        for review in review_data:
            print(review)
            writer.writerow([review['id'], review['date'], review['rating']])
    print("done!")

    return 

make_reviews_csv(review_data)