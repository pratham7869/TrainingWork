import json
import pandas as pd

# I have copied the data from assignment pdf and paste it in training.json file ....
"""
{
  "name": "Python Training",
  "date": "April 19, 2024",
  "completed": "True",
  "instructor": {
   "name": "XYZ",
   "website": "http://pqr.com/"
  },
  "participants": [
    {
      "name": "Participant 1",
      "email": "email1@example.com"
    },
    {
      "name": "Participant 2",
      "email": "email2@example.com"
    }
  ]
}
"""


class Training:
    def __init__(self, name, date, completed, instructor, participants):
        self.name = name
        self.date = date
        self.completed = completed
        self.instructor = instructor
        self.participants = participants


class Instructor:
    def __init__(self, iname, website):
        self.iname = iname
        self.website = website


class Participant:
    def __init__(self, pname, email):
        self.pname = pname
        self.email = email


file = open("training.json", 'r')
data = json.load(file)
print(data)

name = data["name"]
date = data["date"]
if data["completed"] == "True":
    completed = True
else:
    completed = False

instructor = data["instructor"]
iname = instructor["name"]
website = instructor["website"]

participants = data["participants"]
participants_list = []

for participant in participants:
    p = Participant(participant["name"],participant["email"])
    participants_list.append(p)


print(name)
print(type(name))
print(date)
print(type(date))
print(completed)
print(type(completed))
print(instructor)
print(type(instructor))
print(iname)
print(type(iname))
print(website)
print(type(website))
print(participants_list)
print(type(participants_list))

for Participant in participants_list:
    print(Participant.pname)
    print(Participant.email)



