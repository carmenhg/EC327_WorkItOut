from __future__ import print_function
import os, sys  # lower level functions and file management
import numpy as np  # array operations
from PIL import Image  # manage profile and project images
from datetime import date, datetime, timedelta  # date and time datatypes
import flask  # web development
import random  # random interest generation

profileSize1 = (180, 180)  # profile image is 180x180 or 360x360
profileSize2 = (360, 360)


topics = [
    "Science",
    "Math",
    "Engineering",
    "Arts",
    "Business",
    "English",
    "Biology/Medical",
    "Research",
    "Manufacture"
]
numTopics = len(topics)  # can be any interests - number of tags we will use


def calculateAge(birthday):
    today = date.today()
    age = (
        today.year
        - birthday.year
        - ((today.month, today.day) < (birthday.month, birthday.day))
    )
    return age


class User:
    def __init__(
        self,
        name,
        username,
        birthday,
        profile_picture=None,
        age=None,
        interests=None,
        mentor=None,
        mentee=None,
    ):
        self.name = name  # real name
        self.username = username  # username
        self.birthday = birthday.date()  # datetime object
        self.profile_picture = profile_picture
        self.age = calculateAge(birthday)  # age in years
        self.interests = np.zeros(shape=(1, numTopics), dtype=bool)
        self.user_matches = []
        self.mentor = False
        self.mentee = False

    def ChangeName(self, new_name):
        self.name = new_name

    def ChangeUsername(self, new_username):
        self.username = new_username

    def ChangeBirthday(self, new_birthday):
        self.name = new_birthday

    def ChangeProfilePicture(self, new_profile_picture):
        self.profile_picture = new_profile_picture

    def GenerateInterests(
        self,
    ):  # generates random true false array with equal likelihood
        self.interests = np.random.choice(
            a=[False, True], size=(1, numTopics), p=[0.5, 0.5]
        )


if __name__ == "__main__":
    # TODO Add profile picture cropping
    # try:
    #     # img = Image.open("baby-yoda.jpg")
    #     # width, height = img.size
    #     # img.show()
    # except IOError:
    #     print("Error image could not be loaded")
    #     pass

    users = [
        User("Mrinal Ghosh", "ghoshm", datetime(1998, 1, 6)),
        User("Lana Del Rey", "ldr", datetime(1985, 7, 21)),
    ]  # list of users

    users[0].ChangeUsername("mg")
    users[0].GenerateInterests()

    print("User1's name is", users[0].name)
    print("User1's  username is", users[0].username)
    print("User1's birthday is", users[0].birthday)
    print("User1's age is", users[0].age)
    print("User1's interest array is", users[0].interests, "\n")

    print("User2's name is", users[1].name)
    print("User2's  username is", users[1].username)
    print("User2's birthday is", users[1].birthday)
    print("User2's age is", users[1].age)
