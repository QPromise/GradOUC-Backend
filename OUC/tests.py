#!/usr/bin/python3
# _*_coding:utf-8 _*_
# 第五次
import pandas as pd
# img2
def calculate_common(dataset, column):
    items_count = dataset[column].value_counts()
    max_ele = items_count.idxmax()
    max_count = items_count.max()
    return (max_ele, max_count)
res = calculate_common(pd.DataFrame({'ID': [1, 2, 3, 4, 5, 6, 7], 're': ['a', 'a', 'b', 'c', 'd', 'd', 'e']}), 're')
print(res)
# img4
import numpy as np
def split_dataset(dataset, n_split=3):
    shuffled = dataset.sample(frac=1, replace=False)
    result = np.array_split(shuffled, n_split)
    return result
print(split_dataset(pd.DataFrame({'ID': [1, 2, 3, 4, 5, 6, 7], 're': ['a', 'a', 'b', 'c', 'd', 'd', 'e']}), 2))

# img5
humans_random = True

most_common = 2

proportion_unique = 20
exit()
# 第四次 2 hour
# img1
import pandas as pd
data = pd.read_csv("https://raw.githubusercontent.com/fivethirtyeight/data/master/voter-registration/new-voter-registrations.csv")
df = pd.DataFrame(data)
# img2
df.shape
df.columns
# img3
df.head()
df["Year"].unique()
len(df["Year"].unique())
df["Year"].value_counts()
df["New registered voters"].sum()
# img4
def get_most_common(df, column_name=None):
    if column_name is None:
        return None
    data_counts = df[column_name].value_counts()
    max_val_idx, max_val = data_counts.idxmax(), data_counts.max()
    return max_val_idx, max_val
# img5
def test_get_most_common():
    return get_most_common(pd.DataFrame([]))
# img6
import pandas as pd
import numpy as np
import random
# img7
my_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# img8
def row_sums(np_array):
    res = []
    for i in range(len(np_array)):
        res.append(np.sum(np_array[i]))
    return res
# img9
def array_min(np_array):
    min_val = np.min(np_array)
    out = np.where(np_array == min_val)
    return out
# img10
csv_data = pd.read_csv("data/random_guess.csv")
df = pd.DataFrame(csv_data)
# img11
def calculate_unique(data, variable):
    num_unique = len(data[variable].unique())
    num_total = data.size
    return num_unique, num_total, num_unique / num_total
# img12
def select_sample(dataset, n):
    out = dataset.sample(n, replace=False)
    return out
exit()
# 第三次
my_list = ['Python', "is", "so", "fun"]
# 0:18min
joined_string = "*".join(my_list)
print(joined_string)
statement = "UCLA asdasdasdsad"
statement = statement.replace("UCLA", "UCSD")
print(statement)
excessive = "dasdasd!!!dadsd   !!! dadsdasds!!!"
fixed = excessive.replace("!", "")
print(fixed)
too_much = "i, think tha@t !!!...may be>> the!!"
import string
for ele in too_much:
    if ele in string.punctuation:
        too_much = too_much.replace(ele, "")
print(too_much)
# img1
def sort_keys(dictionary, reverse_it=False):
    keys = dictionary.keys()
    sorted_keys = sorted(keys, reverse=reverse_it)
    return sorted_keys
res = sort_keys({"B": 2, "A": 1}, True)
print(res)
# img2
def list_powers(collection, power=2):
    power_list = []
    for ele in collection:
        power_list.append(ele ** power)
    return power_list
print(list_powers((2, 6)))
# img4
def add_lists(list1, list2):
    output = []
    for ele1, ele2 in zip(list1, list2):
        output.append(ele1 + ele2)
    return output
print(add_lists([1, 2], [1, 3]))
# img5
def check_bounds(position, size):
    for ele in position:
        if ele < 0 or ele >= size:
            return False
    return True
print(check_bounds([0, 4], 5))
# img6
class OfficeHours(object):
    course = "COGS 18"
    def __init__(self, name, day, time, place):
        self.name = name
        self.day = day
        self.time = time
        self.place = place

    def check(self):
        return "%s's office hours are on %s at %s on %s." % (self.name, self.day, self.time, self.place)
test = OfficeHours("Bob", "Sunday", "9:00", "Zoom")
print(test.check())
# img7
all_office_hours = [OfficeHours("Harshita", "Monday", "7:00", "Zoom"), OfficeHours("Juan", "Monday", "5:00", "Zoom"),
                    OfficeHours("Wendi", "Tuesday", "6:00", "Zoom"), OfficeHours("Carson", "Wednesday", "9:00", "Zoom"),
                    OfficeHours("Dr. Bardolph", "Wednesday", "2:00", "Zoom"), OfficeHours("David", "Thursday", "2:00", "Zoom"),
                    OfficeHours("Siu", "Friday", "1:00", "Zoom"), OfficeHours("Ryan", "Friday", "2:00", "Zoom")]

# img8
def check_all():
    for office in all_office_hours:
        print(office.check())
check_all()
# img9
class CarInvetory(object):
    def __init__(self):
        self.n_cars = 0
        self.cars = []

    def add_car(self, manufacturer, model, year, mpg):
        self.cars.append({"manufacturer": manufacturer, "model": model, "year": year, "mpg": mpg})
        self.n_cars += 1

    def compare(self, attribute, direction="highest"):
        if direction == "highest":
            highest = self.cars[0]
            for i in range(1, len(self.cars)):
                if self.cars[i][attribute] > highest[attribute]:
                    highest = self.cars[i]
            output = highest
        elif direction == "lowest":
            lowest = self.cars[0]
            for i in range(1, len(self.cars)):
                if self.cars[i][attribute] < lowest[attribute]:
                    lowest = self.cars[i]
            output = lowest
        return output
test = CarInvetory()
test.add_car("Toyota", "Prius", 2012, 36)
print(test.n_cars, test.cars)
test.add_car("BMW", "M3", 2017, 27)
print(test.compare('year', 'lowest'))

# img10
# highest_mpg = inventory.compare('mpg')['manufacturer']
# oldest_car = inventory.compare('year', 'lowest')['model']

# img 11
import random
def add_lists(list1, list2):
    output = []
    for ele1, ele2 in zip(list1, list2):
        output.append(ele1 + ele2)
    return output

def check_bounds(position, size):
    for ele in position:
        if ele < 0 or ele >= size:
            return False
    return True

class WanderBot(object):
    def __init__(self, character="8982"):
        self.character = character
        self.position = [0, 0]
        self.moves = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.grid_size = None

    def wander(self):
        has_new_pos = False
        while not has_new_pos:
            move = random.choice(self.moves)
            new_pos = add_lists(move, self.position)
            has_new_pos = check_bounds(new_pos, self.grid_size)
        return new_pos

    def move(self):
        self.position = self.wander()
bot = WanderBot()
bot.grid_size = 3
print(bot.wander())
bot.move()
print(bot.position)

# img13
bots_list = [WanderBot("1078"), WanderBot("1127"), WanderBot("1279")]
print(bots_list[0].character)

# img 14
grid_n = 15
iter_n = 25
play_board(bots_list, grid_n, iter_n)
exit()
# 第二次 一小时
# img1
honor_code = True

# img2
grocery = ["celery", "prea", "lemod", "peas", "udon", "romain"]
out_a = [grocery[i] for i in range(len(grocery)) if i % 2 == 1]
out_b = grocery[-3]
out_c = [True if 'n' in grocery[i] else False for i in range(len(grocery))]
print(out_a)
print(out_b)
print(out_c)
# img3
message = "date"
secret_message = ""
count = 0
new_message = ""
for i in range(len(message)):
    count += 1
    if count == 3:
       count = 0
       secret_message += message[i]
    else:
        new_message += message[i]
message = new_message
secret_message += message[::-1]
print(secret_message)

has_pictures_dict = {"dasdas": True, "sss": False}
# img4
illustrated_books = []
unillustrated_books = []
for k in has_pictures_dict:
    if has_pictures_dict[k]:
        illustrated_books.append(k)
    else:
        unillustrated_books.append(k)
print(illustrated_books, unillustrated_books)

page_count = [210, 211]
has_pictures_dict = {"dasdas": True, "sss": False}
# img5
book_titles = []
book_pages = {}
for k in has_pictures_dict:
    book_titles.append(k)
for i in range(len(book_titles)):
    book_pages[book_titles[i]] = page_count[i]
print(book_titles, book_pages)

# img6
# joke_random = court_jester_jokes()
# joke_nonrandom = court_jester_jokes(False)

# img7
def encrypt_message(input_message):
    encrypted_message = ""
    count = 0
    new_message = ""
    for i in range(len(input_message)):
        count += 1
        if count == 3:
            count = 0
            encrypted_message += input_message[i]
        else:
            new_message += input_message[i]
    message = new_message
    encrypted_message += message[::-1]
    return encrypted_message
# img8
def list_books(input_dict, illustrated=True):
    illustrated_books = []
    unillustrated_books = []
    for k in input_dict:
        if input_dict[k]:
            illustrated_books.append(k)
        else:
            unillustrated_books.append(k)
    if illustrated:
        return illustrated_books
    else:
        return unillustrated_books
# img9
def new_encrypt(input_string):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    reverse_alpha = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    output_string = ""
    for char in input_string:
        if char.upper() in alpha:
            position = alpha.find(char.upper())
            output_string += reverse_alpha[position]
        else:
            output_string = None
            break
    return output_string

zodiac_signs = {"dragn": [1998, 1970, 1985, 2001, 1111]}
# img10
class NewYear(object):
    def __init__(self, year):
        self.year = year
        self.zodiac_signs = zodiac_signs

    def return_sign(self):
        for k in self.zodiac_signs:
            if self.year in self.zodiac_signs[k]:
                return "You were born in the year of the %s" % k
print(NewYear(1998).return_sign())

# img11
class PresidentsDay(object):
    def __init__(self, when="Third Monday in February", has_school=False):
        self.when = when
        self.has_school = has_school

    def sleep_in(self):
        if not self.has_school:
            return "Go ahead and sleep in!"
        else:
            return "Get up! It's time for class"
print(PresidentsDay.sleep_in)
def find_max(random_list):
    list_max = 0
    for x in random_list:
        if x > list_max:
            list_max = x
    return list_max


list_max = find_max([1, 7, 5])
print(list_max)

# 第一次 俩小时
# answer 2
def square_all(collection):
    res = []
    for element in collection:
        res.append(element ** 2)
    return res


print(square_all((2, 5)))
print(square_all([1, 2]))
# answer3
def summation(num1, num2):
    return num1 + num2

def subtraction(num1, num2):
    return num1 - num2

def multiplication(num1, num2):
    return num1 * num2

def division(num1, num2):
    return num1 / num2
# answer4
def squared(num):
    return num ** 2

def square_root(num):
    return num ** 0.5
# answer5
cal_a = summation(squared(3), square_root(81))
cal_b = subtraction(division(12, 2), multiplication(2, 4))
cal_c = multiplication(square_root(25), summation(7, 9))
cal_d = division(squared(6), square_root(36))

# answer6
def is_even(value):
    return value % 2 == 0
def is_postive(value):
    return value > 0
print(is_even(2), is_postive(1))
print(cal_a, cal_b, cal_c, cal_d)
print(square_root(144))
print(division(1, 0.5))

# answer7
def make_new_list(data_list):
    output = []
    for i in data_list:
        if is_even(i) and is_postive(i):
            output.append(1)
        elif not is_even(i) and not is_postive(i):
            output.append(-1)
        else:
            output.append(0)
    return output
print(make_new_list([-1, 20, -100, -40, 33, 97, -101, 45, -79, 96]))
# answer8
algo_q_a = "computer"
algo_q_b = "human"
algo_q_c = "human"
algo_q_d = "computer"
# answer9
def is_question(input_string):
    output = False
    for letter in input_string:
        if letter == "?":
            output = True
    return output

# answer10
# answer11
import string
def remove_punctuation(input_string):
    out_string = ""
    for letter in input_string:
        if letter not in string.punctuation:
            out_string += letter
    return out_string


def prepare_text(input_string):
    temp_string = input_string.lower()
    temp_string = remove_punctuation(temp_string)
    out_list = temp_string.split()
    return out_list
print(prepare_text("Hey! It's professor Ellis!"))


# answer12
def respond_echo(input_string, number_of_echoes, spacer):
    if input_string is not None:
        echo_output = input_string
        echo_output = (echo_output + spacer) * number_of_echoes
    else:
        echo_output = None
    return echo_output
print(respond_echo("bark", 2, "-"))


# answer13
import random
def selector(input_list, check_list, return_list):
    output = None
    for ele in input_list:
        if ele in check_list:
            output = random.choice(return_list)
            break
    return output
print(selector(["in", "word"], ["wrd"], ["future"]))

# answer14
def string_concatenator(string1, string2, separator):
    output = "%s%s%s" % (string1, separator, string2)
    return output
# answer15
def list_to_string(input_list, separator):
    output = input_list[0]
    for i in range(1, len(input_list)):
        output = "%s%s%s" % (output, separator, input_list[i])
    return output
print(list_to_string(["this", "is", "fun"], " ,"))
print(string_concatenator("hello", "world", "   "))
# answer16
def end_chat(input_list):
    output = False
    for ele in input_list:
        if ele == "quit":
            output = True
            break
    return output

print(end_chat(["A", "s", "qit"]))
print(is_question("what"))
exit()




















import time
import json
import bs4
import os
from bs4 import  BeautifulSoup

print(os.listdir("../OUC/static/exam_json/"))
cur = int(time.time())
end = 1610606871
print((end - cur) // (3600 * 24))
expire_time = time.strptime("2021-01-20 15:32:08", "%Y-%m-%d %H:%M:%S")
expire_time = int(time.mktime(expire_time))
print(2020 in range(2020, 2020))
print(",".join(list(map(str, ["计算机科学"]))))
print("http://grad.ouc.edu.cn/"[:-1])
a = ["自然辩证法", "中特", "英语"]
b = ["中特", "maogai", "自然辩证法"]
print(list(set(a).intersection(set(b))))
string = "[{'name': '自然辩证法概论', 'type': '公共课', 'credit': 1.0, 'score': 88.0, 'selected': True, 'disabled': False}, {'name': '中国特色社会主义理论与实践研究', 'type': '公共课', 'credit': 2.0, 'score': 94.0, 'selected': True, 'disabled': False}, {'name': '专业学位研究生外国语', 'type': '公共课', 'credit': 3.0, 'score': '免修', 'selected': False, 'disabled': True}, {'name': '工程伦理', 'type': '公共课', 'credit': 1.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '学术道德与规范', 'type': '公共课', 'credit': 1.0, 'score': 98.0, 'selected': True, 'disabled': False}, {'name': '论文写作指导', 'type': '公共课', 'credit': 2.0, 'score': 91.0, 'selected': True, 'disabled': False}, {'name': '机器学习Ⅰ', 'type': '基础课', 'credit': 3.0, 'score': 89.0, 'selected': True, 'disabled': False}, {'name': '多媒体技术', 'type': '基础课', 'credit': 3.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '三维计算机图形学', 'type': '专业课', 'credit': 3.0, 'score': 97.0, 'selected': True, 'disabled': False}, {'name': '图像处理与模式识别', 'type': '专业课', 'credit': 3.0, 'score': 91.5, 'selected': True, 'disabled': False}, {'name': '云计算', 'type': '其他课程', 'credit': 3.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '多核处理与GPU计算', 'type': '其他课程', 'credit': 3.0, 'score': 99.0, 'selected': True, 'disabled': False}, {'name': '实践训练', 'type': '培养环节', 'credit': 6.0, 'score': '未选', 'selected': False, 'disabled': True}, {'name': '开题审核', 'type': '培养环节', 'credit': 0.0, 'score': '未选', 'selected': False, 'disabled': True}]"
json_str = json.dumps(string, ensure_ascii=False)
print(type(json_str))
print(json_str[0])
string = "[{'name': '自然辩证法概论', 'type': '公共课', 'credit': 1.0, 'score': 88.0, 'selected': True, 'disabled': False}, {'name': '中国特色社会主义理论与实践研究', 'type': '公共课', 'credit': 2.0, 'score': 94.0, 'selected': True, 'disabled': False}, {'name': '专业学位研究生外国语', 'type': '公共课', 'credit': 3.0, 'score': '免修', 'selected': False, 'disabled': True}, {'name': '工程伦理', 'type': '公共课', 'credit': 1.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '学术道德与规范', 'type': '公共课', 'credit': 1.0, 'score': 98.0, 'selected': True, 'disabled': False}, {'name': '论文写作指导', 'type': '公共课', 'credit': 2.0, 'score': 91.0, 'selected': True, 'disabled': False}, {'name': '机器学习Ⅰ', 'type': '基础课', 'credit': 3.0, 'score': 89.0, 'selected': True, 'disabled': False}, {'name': '多媒体技术', 'type': '基础课', 'credit': 3.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '三维计算机图形学', 'type': '专业课', 'credit': 3.0, 'score': 97.0, 'selected': True, 'disabled': False}, {'name': '图像处理与模式识别', 'type': '专业课', 'credit': 3.0, 'score': 91.5, 'selected': True, 'disabled': False}, {'name': '云计算', 'type': '其他课程', 'credit': 3.0, 'score': '未出', 'selected': False, 'disabled': True}, {'name': '多核处理与GPU计算', 'type': '其他课程', 'credit': 3.0, 'score': 99.0, 'selected': True, 'disabled': False}, {'name': '实践训练', 'type': '培养环节', 'credit': 6.0, 'score': '未选', 'selected': False, 'disabled': True}, {'name': '开题审核', 'type': '培养环节', 'credit': 0.0, 'score': '未选', 'selected': False, 'disabled': True}]"
json_str = eval(string)
print(type(json_str))
# print(begin_day)
#
# import requests
# s = requests.session()
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
#         'Connection': 'close'
#     }
# url = "http://www.baidu.com/"
# s.keep_alive = False
# s.proxies = {
#                 "http": "182.34.27.148:9999"
#              }
# r = s.get(url, headers=headers)
# profile_soup = BeautifulSoup(r.text, 'lxml')
# print(profile_soup)
# print(r.status_code)  # 如果代理可用则正常访问，不可用报以上错误