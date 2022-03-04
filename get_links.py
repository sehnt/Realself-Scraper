from link_parser import LinkParser
import time
from pathlib import Path
import main
from multiprocessing.dummy import Pool as ThreadPool

HTML_THREAD_COUNT = 7

def store_html(page_num, text, path):
    file = open((path / "link_pages") / (str(page_num) + ".txt"), "w", errors="ignore")
    file.write(text)
    file.close()

def grab_links(base_url, num_pages, procedure) -> None:
    directory = (main.BASE_PATH / 'data') /  procedure
    directory.mkdir(parents=True, exist_ok=True)
    
    (directory / "link_pages").mkdir(parents=True, exist_ok=True)
    

    thread_groups = []
    temp_group = []

    for page_num in range(0, num_pages+2):
        if not (((directory / "link_pages") / (str(page_num) + ".txt")).is_file()):
            link = base_url + str(page_num)

            if len(temp_group) < HTML_THREAD_COUNT:
                temp_group.append([link, page_num, procedure])
            else:
                thread_groups.append(temp_group)
                temp_group = []
                temp_group.append([link, page_num, procedure])
    if len(temp_group) != 0:
        thread_groups.append(temp_group)

    for group in thread_groups:
        start = time.time()
        pool = ThreadPool(len(group))
        pool.map(grab_link, group)


        while(time.time() < start + 5):
            pass
        

def grab_link(args: []):
    link = args[0]
    page_num = args[1]
    procedure = args[2]
    directory = (main.BASE_PATH / 'data') / procedure
    
    parser = LinkParser()
    parser.set_url(link)
    parser.get_data()
    links = parser.get_links()
    update_links(links, procedure)
    store_html(page_num, parser.get_text(), directory)

    
def update_links(links, procedure) -> None:
    links_path = (main.BASE_PATH / 'data') / procedure / "links.txt"
    if not links_path.is_file():
        links_path.touch()
        
    unique_links = set()
    file = open(((main.BASE_PATH / 'data') / procedure) / "links.txt", "r+", encoding="utf-8")
    for line in file.readlines():
        unique_links.add(line.strip())

    for link in links:
        if link not in unique_links:
            unique_links.add(link)
            file.write(link + "\n")
