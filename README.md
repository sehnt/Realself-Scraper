# Realself-Scraper
Scraper to extract reviews from the website www.realself.com. Built as a contribution to a social media analysis medical study.

Isn't the most user friendly, you have to modify some of the .py files for full functionality:

In main.py, **you need to change BASE_PATH** to the directory you are storing the code in. You can also comment / uncommment certain groups of functions to enable / disable certain functionality. I strongly recommend only running one set of functions at a time for simplicity. Change PROCEDURE to specify which procedure from www.realself.com you want to scrape.

In visit.py and get_links.py, you can specify the number of threads that will be run at once. HTML_THREAD_COUNT specifies the number of browsers opened at once and should be kept relatively low. PARSE_THREAD_COUNT specifies the number of threads for parsing the already downloaded reviews. This does not connect with the internet and can be increased based on CPU.
