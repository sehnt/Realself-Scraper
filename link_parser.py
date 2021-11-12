from html.parser import HTMLParser
import request_sel

class LinkParser(HTMLParser):
    def __init__(self):
        super(LinkParser, self).__init__()
        self.text = ""
        self.link_list = []
        self.link_str = "color_midnight__E6fyY text-decoration_none__2IlxP"
        
        self.url = ""
        self.request = None
    
    def set_url(self, url):
        self.url = url;
        self.request = request_sel.Request(url)

    def handle_starttag(self, tag, attrs):
        if (tag == 'a'):
            if (len(attrs) == 2) and (attrs[0][0] == "href"):
                if("/review/" in attrs[0][1]):
                    self.link_list.append("https://www.realself.com" + attrs[0][1])

    def get_data(self) -> None:
        self.text = self.request.get_data()

    def get_test(self) -> None:
        self.text = self.request.test_data()

    def get_text(self) -> str:
        return self.text
        
    def get_links(self) -> list:
        self.feed(self.text)
        return self.link_list

    
