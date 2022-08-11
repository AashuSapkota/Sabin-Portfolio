import csv
import os
from .models import CountryList
 


def load_data():
    try:
        file = open("E:/broadcast_platform/broadcast_platform/users/country_data.csv")
        # file.read()
    except Exception as e:
        print('Excepton:', e)
    read_file = csv.reader(file)

    count = 1

    for record in read_file:
        if count == 1:
            print('hello')
            pass
        else:
            print(record)
            CountryList.objects.create(country_name=record[0], country_code=record[1])
        count += 1


# load_data()