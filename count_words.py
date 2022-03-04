from review import Review
import main
import visit
##from collections import defaultdict
import ast
from dateutil import parser

PARSE_THREAD_COUNT = 10

WORTH_IT = 0
NOT_SURE = 1
NOT_WORTH_IT = 2
BLANK = 3

def count_words(procedure, separator):
    directory = (main.BASE_PATH / 'data') / procedure
    links_file = open(directory / "links.txt", 'r', encoding = "utf-8")
    word_path = (directory / "unique_words.txt")

    dict_path = (directory / "unique_words_dict.txt")
    combined_path = (directory / "combined.txt")

    with open(combined_path, 'w+') as file:
        file.truncate(0)

    words_by_rating = [0]*4
    for idx in range(0, 4):
        words_by_rating[idx] = dict()

    rating_to_idx = {'Worth It': WORTH_IT, 'Not Sure': NOT_SURE, 'Not Worth It': NOT_WORTH_IT, '': BLANK}

    earliest = parser.parse("Jan 1 2022")

    for link in links_file.readlines():
        link = link.strip()
        review_path = (directory / "reviews") / (visit.unique_id(link) + '.txt')

        if review_path.is_file():
            review = Review("")
            text = ""
            with open(review_path, "r") as file:
                text = file.read()

            review.read_review(text)

            comments = review.get_comments()

            text = review.get_title() + "\n"
            for comment in comments:
                text += comment.get_text() + "\n"
                text += comment.get_title()+ "\n"

                date_str = comment.get_date()
                date = parser.parse(date_str)
                if date < earliest:
                    
                     earliest = date

            unique_words = set()

            text = text.lower()
                
            text = text.replace('~', ' ')
            text = text.replace('!', ' ')
            text = text.replace('.', ' ')
            text = text.replace(',', ' ')
            text = text.replace('?', ' ')
            text = text.replace('(', ' ')
            text = text.replace(')', ' ')
            text = text.replace('-', ' ')
            text = text.replace('+', ' ')
            text = text.replace('=', ' ')
            text = text.replace(':', ' ')
            text = text.replace(';', ' ')
            text = text.replace('*', ' ')
            text = text.replace("'", ' ')
            text = text.replace("\n", ' ')
            text = text.replace('”', ' ')
            text = text.replace('"', ' ')
            text = text.replace('“', ' ')
            text = text.replace('\\', ' ')
            text = text.replace('‘', '')
            text = text.replace('’', '')
            text = text.replace('/', ' ')
            text = text.replace('	', ' ')
            text = text.replace(' ', ' ')
            
            line = visit.unique_id(link) + separator
            line += review.get_name() + separator

            first = ""
            
            for comment in review.get_comments():
                date_str = comment.get_date()

                if first == "":
                    if date != "":
                        first = parser.parse(date_str)
                else:
                    if date != "":
                        first = date if date < first else first
                                            
            line += str(first) + separator
            line += review.get_rating() + separator
            line += review.get_cost() + separator
            line += str(review.pic_count) + separator
            if review.pic_count != 0:
                print(review.pic_count, visit.unique_id(link))
            line += str(review.help_count) + separator
            line += text + "\n"

            with open(combined_path, 'a+') as file:
                file.write(line)
                
            all_words = text.split(" ")
            for word in all_words:
                unique_words.add(word)

            for word in unique_words:
                rating_idx = rating_to_idx[review.get_rating()]
                if word not in words_by_rating[rating_idx]:
                    words_by_rating[rating_idx][word] = 1
                else:
                    words_by_rating[rating_idx][word] += 1
            
            with open(dict_path, 'w+') as file:
                file.write(str(words_by_rating))
        else:
            print(review_path)
##            break
    print (earliest)



def words_to_csv(procedure, separator):
    directory = (main.BASE_PATH / 'data') / procedure
    with open((directory / "unique_words_dict.txt"), 'r') as file:
        text = file.read()

    words_by_rating = ast.literal_eval(text)
    with open((directory / "words_csv.txt"), 'a+') as file:
        file.truncate(0)
        
    with open((directory / "words_csv.txt"), 'a+') as file:
        
        for rating in range(len(words_by_rating)):
            for word, count in sorted(words_by_rating[rating].items(), key = lambda item: item[1], reverse=True):
                line = ""
                if rating == WORTH_IT:
                    line += "Worth It" + separator
                elif rating == NOT_SURE:
                    line += "Not Sure" + separator
                elif rating == NOT_WORTH_IT:
                    line += "Not Worth It" + separator
                elif rating == BLANK:
                    line += "Blank" + separator
                else:
                    line += "ERROR" + separator

                # Word
                line += word + separator

                # Count of this word
                line += str(count)

                line += '\n'
                
                file.write(line)


##if __name__ == '__main__':
##    # Testing
####    count_words('tummy-tuck')
##    words_to_csv('tummy-tuck', '::?::')
