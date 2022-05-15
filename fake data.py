from faker import Faker
import faker
import datetime
import random
import json
fake = Faker('en_US')
name = []
sem = []
branchList = []
date = {}
Usn = {}
tareekh = []
month = []
saal = []
section = []
attd = ["Absent", "Present"]
usn_year = [18, 19, 20, 21]
usn_Branch = ['CS', 'IS', 'EC', 'EE', 'ME', 'IP', 'CV', 'Mtech', 'MCA']
semester = ['1', '2', '3', '4', '5', '6', '7', '8']

for i in range(1000):
    name.append(fake.name())
count = 0;
while count < 1000:
    usn = ""
    year = str(random.choice(usn_year))
    branch = random.choice(usn_Branch)
    number = str(random.randint(1,120))
    if len(number) == 1:
        number = "00" + number
    elif len(number) == 2:
        number = "0" + number
    else:
        number = number
    usn = "4NI"+year+branch+number
    if usn not in Usn.keys():
        Usn[usn] = 1
        count = count+1
        branchList.append(branch)

    sem.append(random.choice(semester))
    section.append(random.choice(['A', 'B']))
count = 0
while count < 10:
    fake.date_between(start_date='today', end_date='+30y')
    start_date = datetime.date(year=2019, month=8, day=19)
    end_date = datetime.date(year=2022, month=5, day=15)
    data = fake.date_between(start_date=start_date, end_date=end_date)
    if data not in date.keys():
        date[data] = random.choice(attd)
        month.append(data.strftime("%m"))
        saal.append(data.strftime("%Y"))
        tareekh.append(data.strftime("%d/%m/%Y"))
        count = count+1

date_data = []
for i in range(0, 10):
    date_data.append({"date": tareekh[i], "month": month[i], "year": saal[i]})

result = []
USN = []
for key in Usn.keys():
    USN.append(key)
for el in date_data:
    for i in range(0, len(name)):
        result.append({"dates": el['date'],
                       "month": el['month'],
                       'year': el['year'],
                       'attendance': random.choice(['Present', 'Absent']),
                       "name": name[i],
                       "usn": USN[i],
                       "branch": branchList[i],
                       "sem": sem[i],
                       "section": section[i]
                       })
res = json.dumps(result)

try:
    with open("data.json", "w") as file:
        file.write(res)
        file.close()
except Exception as error:
    print(error)
with open("data.json", "r") as file:
    file.read()
    file.close()


