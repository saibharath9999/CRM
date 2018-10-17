import os
from random import *
from faker import Faker
fake=Faker()

first = fake.first_name()
last = fake.last_name()
print(first + "_"+last)