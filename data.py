import csv
import random

file = open('accupass_output.csv')
reader = csv.reader(file)
data_list = list(reader)
data_list.pop(0)
file.close()


def generate_city_dict():
    city_dict = {}

    for row in data_list:
        if row[1] not in city_dict.keys():
            city_dict[row[1]] = [row]
        else:
            city_dict[row[1]].append(row)
    return city_dict


def random_recommend_activity():
    activity = random.choice(data_list)
    return activity
