import csv
import random

file = open('accupass_output.csv')
reader = csv.reader(file)
data_list = list(reader)
file.close()


def random_recommend_activity():
    activity = random.choice(data_list)
    return activity
