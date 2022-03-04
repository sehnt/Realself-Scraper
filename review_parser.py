from html.parser import HTMLParser
import request_sel
from review import Review
from review import Comment

class ReviewParser(HTMLParser):
    review_str = "CroppedText CroppedText--phone CroppedText--4 BodyText BodyText--large"
    main_title_str = "Headline Headline--hero u-semiBold u-textPoppins"
    title_str = "Content-title Headline Headline--legacy Headline--legacy3 Headline--5"
    currency_tag = "rs-currency"
    comment_str = "List Content-byline Byline Byline--bulleted"
    date_str = "Byline-item"
    provider_title = "Headline Headline--3 u-marginExtraSmall"
    provider_date = "Content-byline Byline"
    provider_text = "BodyText BodyText--large user-generated-content"
    name_str = "Link Link--legacySecondary Link--primary"
    pic_str = "!loading"
    helpful_str = "people found this helpful"
    

    def __init__(self):
        super(ReviewParser, self).__init__()
        self.text = ""
        self.last = ""
        self.date_flag = False
        self.temp_comment = Comment()

        self.url = ""
        self.output = None
        self.request = None

    def set_url(self, url):
        self.url = url;
        self.output = Review(url)
        self.request = request_sel.Request(url)

    def get_data(self) -> None:
        self.text = self.request.get_data()

    def process_data(self, data=None) -> None:
        if data is None:
            data = self.text
        self.text = data
        self.feed(self.text)
        if (self.temp_comment.get_date() != ""):
            self.output.add_comment(self.temp_comment)
        self.temp_comment = Comment()

    def get_text(self) -> None:
        return self.text
    
    def handle_starttag(self, tag, attrs):
        if tag == "br":
            pass
        else:
            self.last = ""
            
        if (tag == "h1") and (len(attrs) >= 1) and (attrs[0][0] == "class"):
            if attrs[0][1] == self.main_title_str:
                self.last = self.main_title_str
        if (tag == "a") and (len(attrs) >= 3) and (attrs[2][0] == "class") and (attrs[2][1] == self.name_str):
            self.last = self.name_str
        elif (tag == "div") and (len(attrs) > 2) and (attrs[0][1] == self.pic_str) and ("lazyload" in attrs[1][1]):
            self.output.pic_count += 1
        elif (tag == "div") and (len(attrs) >= 1) and (attrs[0][0] == "class"):
                if attrs[0][1] == self.review_str:
                    self.last = self.review_str
        elif (tag == self.currency_tag):
            if (len(attrs) == 2):
                self.output.set_cost(attrs[0][1])
                self.output.set_date(attrs[1][1])
        elif (tag == "h3"):
            if (len(attrs) >= 1) and (attrs[0][0] == "class"):
                if attrs[0][1] == self.title_str:
                    self.last = self.title_str
                elif attrs[0][1] == self.provider_title:
                    self.last = self.provider_title
        elif (tag == "ul") and (len(attrs) == 1):
            if (attrs[0][0] == "class"):
                if (attrs[0][1] == self.comment_str):
                    self.date_flag = True
                elif (attrs[0][1] == self.provider_date):
                    self.date_flag = True
        elif (tag == "li") and (len(attrs) == 1) and (self.date_flag == True):
            if (attrs[0][0] == "class"):
                if (attrs[0][1] == self.date_str):
                    self.last = self.date_str
                    self.date_flag = False
        elif (tag == "li") and (self.date_flag == True):
            self.last = self.provider_date
            self.date_flag = False
                
        elif (tag == "p") and (len(attrs) == 1) and (attrs[0][0] == "class"):
            if (attrs[0][1] == self.provider_text):
                self.last = self.provider_text

        elif ((tag == "span") and (len(attrs) == 1) and (attrs[0][1] == "likeCount")):
            self.last = self.helpful_str
        
        


    def handle_data(self, data) -> None:
        data = data.strip()

        if self.last == self.main_title_str:
            data = data.replace("\n", " ")
            self.output.set_title(data)
            
            self.last = ""
        elif self.last == self.name_str:
            self.output.set_name(data)
            self.last = ""
        elif self.last == self.title_str:
            if (self.temp_comment.get_date() != ""):
                self.output.add_comment(self.temp_comment)
            self.temp_comment = Comment()
            data = data.replace("\n", " ")
            self.temp_comment.set_title(data)
            self.last = ""
        elif (self.last == self.date_str) or (self.last == self.provider_date):
            self.temp_comment.set_date(data)
            self.last = ""
        elif (self.last == self.review_str) or (self.last == self.provider_text):
            if data != "":
                self.temp_comment.add_text(data + "\n")
        elif (data == "Worth It"):
            self.output.set_rating(data)
        elif (data == "Not Sure"):
            self.output.set_rating(data)
        elif (data == "Not Worth It"):
            self.output.set_rating(data)
        elif (self.last == self.helpful_str):
            self.output.help_count += int(data)
            self.last = ""
        

    def get_review(self) -> Review:
        return self.output
