import visit
import time
import requests
from get_links import grab_links
from pathlib import Path

# Change this to the folder where you
# want the data to be stored
BASE_PATH = Path("C:/Users/Steve/Desktop/Realself")

# This is the name of the procedure being
# scraped used in realself.com's links
PROCEDURE = "tummy-tuck"


# Uncomment sections as needed. You probably
# only want one uncommented at a time
if __name__ == "__main__":

    # Downloads the webpages containing
    # the links for each review and parses
    # out the review links.
    # grab_links(url, delay, num_pages, PROCEDURE)
    # delay is minimum seconds between each set of requests
    # grab_links will visit links [0, num_pages]
    url = "https://www.realself.com/reviews/" + PROCEDURE + "?sort=3&page="
    grab_links(url, 5, 4215, PROCEDURE)


    # Visits every link in BASE_PATH/PROCEDURE/links.txt and downloads
    # the review page's HTML.
##    visit.visit_links(PROCEDURE, 5)


    # Parses the downloaded html .txt file for every link
    # in links.txt. It goes until it reaches a webpage that didn't
    # get downloaded and throws an exception because
    # the .txt file doesn't exist.
##    visit.parse_reviews(PROCEDURE)

