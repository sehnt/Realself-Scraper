class Review():
    comments = []
    def __init__(self, url):
        self.url = url
        self.cost = 0
        self.date = ""
        self.rating = ""
        self.title = ""
        self.comments = []
        self.sep = ":::"
        self.line_sep = "----------\n"
        self.name = "";
        self.help_count = 0
        self.pic_count = 0

    def read_review(self, text):
        lines = text.splitlines(True)
        first_line = lines[0].strip().split(self.sep)

        self.set_name(first_line[0])
        self.set_cost(first_line[1])
        self.set_date(first_line[2])
        self.set_rating(first_line[3])
        self.set_title(first_line[4])
        self.pic_count = int(first_line[5])
        self.help_count = int(first_line[6])

        idx = 1
        temp_comment = Comment()
        while idx < len(lines):
            if lines[idx] == self.line_sep:
                if temp_comment.get_date() != "":
                    self.add_comment(temp_comment)

                temp_comment = Comment()
                    
                # Line separator should always have at least 3 lines below it
                temp_comment.set_title(lines[idx+1].strip())
                temp_comment.set_date(lines[idx+2].strip())
                idx += 2
            elif (lines[idx].strip() == ""):
                pass
            elif temp_comment.get_date() != "":
                temp_comment.add_text(lines[idx])
            idx += 1
            
        if temp_comment.get_date() != "":
                    self.add_comment(temp_comment)

            

    def set_cost(self, cost):
        self.cost = cost

    def set_date(self, date):
        self.date = date

    def set_rating(self, rating):
        self.rating = rating

    def set_title(self, title):
        self.title = title

    def set_name(self, name):
        self.name = name;

    def get_name(self):
        return self.name;

    def get_cost(self):
        return self.cost

    def get_date(self):
        return self.date

    def get_rating(self):
        return self.rating

    def get_title(self):
        return self.title

    def add_comment(self, comment):
        self.comments.append(comment)

    def get_comments(self) -> list:
        return self.comments

    def get_url(self) -> str:
        return self.url

    def __str__(self) -> str:

        ret = str(self.get_name())
        ret += self.sep + str(self.get_cost())
        ret += self.sep + str(self.get_date())
        ret += self.sep + str(self.get_rating())
        ret += self.sep + str(self.get_title())
        ret += self.sep + str(self.pic_count)
        ret += self.sep + str(self.help_count)
        ret += "\n"

        for comment in self.get_comments():
            ret += self.line_sep
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

    def add_text(self, text):
        self.text += text

    def get_title(self):
        return self.title

    def get_date(self):
        return self.date

    def get_text(self):
        return self.text
