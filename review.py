class Review():
    comments = []
    def __init__(self, url):
        self.url = url
        self.cost = 0
        self.date = ""
        self.rating = ""
        self.comments = []

    def set_cost(self, cost):
        self.cost = cost

    def set_date(self, date):
        self.date = date

    def set_rating(self, rating):
        self.rating = rating

    def get_cost(self):
        return self.cost

    def get_date(self):
        return self.date

    def get_rating(self):
        return self.rating

    def add_comment(self, comment):
        self.comments.append(comment)

    def get_comments(self) -> list:
        return self.comments

    def get_url(self) -> str:
        return self.url

    def __str__(self) -> str:
        sep = ";,;"
        line_sep = "----------\n"
        ret = str(self.get_cost()) + sep + str(self.get_date()) + sep + str(self.get_rating()) + "\n"

        for comment in self.get_comments():
            ret += line_sep
            ret += comment.get_title() + '\n'
            ret += comment.get_date() + '\n'
            ret += comment.get_text() + '\n'
        
        return ret




class Comment():
    def __init__(self, title="", date="", text=""):
        self.title = title
        self.date = date
        self.text = text

    def set_title(self, title):
        self.title = title

    def set_date(self, date):
        self.date = date

    def set_text(self, text):
        self.text += text

    def get_title(self):
        return self.title

    def get_date(self):
        return self.date

    def get_text(self):
        return self.text
