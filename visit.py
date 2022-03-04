from review import Review, Comment
from review_parser import ReviewParser
import time
from pathlib import Path
from multiprocessing.dummy import Pool as ThreadPool
import main

HTML_THREAD_COUNT = 7

def unique_id(link):
    unique_id = link[link.find("/review/") + 8:]
    return unique_id.replace("/", "-")

def store_review(review, path) -> None:
    url = review.get_url()
    file = open((path / "reviews") / (unique_id(url) + ".txt"), "w", errors="ignore")
    file.write(str(review))
    file.close()

def store_html(url, text, path) -> None:
    file = open((path / "webpages") / (unique_id(url) + ".txt"), "w", errors="ignore")
    file.write(text)
    file.close()

def visit(args: []):
    link = args[0]
    directory = Path(args[1])

    link = link.strip()
    html_path = (directory / "webpages") / (unique_id(link) + ".txt")
    reviewParser = ReviewParser()
    reviewParser.set_url(link)

    if not (Path(html_path).is_file()) :
        reviewParser.get_data()
        store_html(link, reviewParser.get_text(), directory)


def visit_links(procedure, thread_count):
    directory = (main.BASE_PATH / 'data') / Path(procedure)
    (directory / "webpages").mkdir(parents=True, exist_ok=True)
        
    links_file = open(directory / "links.txt", 'r', encoding='utf-8')

    thread_groups = []
    temp_group = []

    for link in links_file.readlines():
        link = link.strip()
        html_path = (directory / "webpages") / (unique_id(link) + ".txt")
        if not html_path.is_file():
            if len(temp_group) < thread_count:
                temp_group.append([link, directory])
            else:
                thread_groups.append(temp_group)
                temp_group = []
                temp_group.append([link, directory])
    if len(temp_group) != 0:
        thread_groups.append(temp_group)
    
    for group in thread_groups:
        start = time.time()
        pool = ThreadPool(thread_count)
        pool.map(visit, group)

        while(time.time() < start + 5):
            pass
  
    links_file.close() 



def parse_reviews(procedure, thread_count):
    directory = (main.BASE_PATH / 'data') / procedure
    links_file = open(directory / "links.txt", 'r', encoding = "utf-8")

    
    failed_links = []

    thread_groups = []
    temp_group = []

    for link in links_file.readlines():
        link = link.strip()
        html_path = (directory / "webpages") / (unique_id(link) + ".txt")
        
        if len(temp_group) < thread_count:
            if html_path.is_file():
                temp_group.append([link, directory, failed_links])
        else:
            thread_groups.append(temp_group)

            temp_group = []
            temp_group.append([link, directory, failed_links])
    
    for group in thread_groups:
        pool = ThreadPool(thread_count)
        output = pool.map(parse_review, group)
        
    print(failed_links)
    return failed_links

def parse_review(args: []) -> [str]:
    link = args[0]
    directory = Path(args[1])
    failed_links = args[2]


    parser = ReviewParser()
    parser.set_url(link)
    (directory / "reviews").mkdir(parents=True, exist_ok=True)
    html_path = (directory / "webpages") / (unique_id(link) + '.txt')
    review_path = (directory / "reviews") / (unique_id(link) + '.txt')
    
    
    if not review_path.is_file():
        review_file = open(html_path, "r", errors="ignore")
        parser.process_data(review_file.read())
        review_file.close()
        
        review = parser.get_review()

        if (len(review.get_comments()) == 0):
            print(link)
            failed_links.append(link)

        for comment in review.get_comments():
            if (comment.get_date() == ""):
                print("bad date")
                failed_links.append(link)

        if link not in failed_links:
            store_review(review, directory)
