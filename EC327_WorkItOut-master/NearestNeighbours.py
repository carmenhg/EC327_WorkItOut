from __future__ import print_function
import user_class
from datetime import datetime
import numpy as np
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from testing import db, login_manager, app
from flask_login import UserMixin
from testing.models import User, Post

"""
function to match users with the k nearest neighbours in terms of interests
"""


class Match:
    def __init__(self):
        self.mse = []
        self.name = []

    def appendMatch(self, mse, name):
        self.mse.append(mse)
        self.name.append(name)

    def sortByMse():
        mse, name = (list(t) for t in zip(*sorted(zip(mse, name))))
        return mse, name


# relative interest in other topics based on liking Science
scienceCorrelation = [1, 0.5, 0.85, 0, 0.15]
mathCorrelation = [0.5, 1, 0.5, 0, 0]
engineeringCorrelation = [0.75, 0.75, 1, 0.25, 0.25]
artCorrelation = [0.1, 0, 0.3, 1, 0.25]
businessCorrelation = [0, 0, 0.4, 0.1, 1]

biasedCorrelation = np.array(
    [
        scienceCorrelation,
        mathCorrelation,
        engineeringCorrelation,
        artCorrelation,
        businessCorrelation,
    ]
)

unbiasedCorrelation = np.identity(user_class.numTopics)

# make boolean array from string of numbers
def makeBoolArray(numstr):
    bool_array = np.zeros(shape=(1,user_class.numTopics),dtype=bool)
    for num in numstr:
        bool_array[0,int(num)]=True
    return bool_array

def returnMatches(numstr):
    bool_array = makeBoolArray(numstr)
    posts = Post.query.all()
    users = User.query.all()
    print(posts)
    print(users)

k = 2  # number of matches desired for suggestions

if __name__ == "__main__":
    users = [
        user_class.User("Person A", "a", datetime(1998, 1, 6)),
        user_class.User("Person B", "b", datetime(1985, 7, 21)),
        user_class.User("Person C", "c", datetime(1925, 1, 11)),
        user_class.User("Person D", "d", datetime(2001, 2, 5)),
        user_class.User("Person E", "e", datetime(1995, 9, 30)),
        user_class.User("Person F", "f", datetime(2012, 7, 13)),
    ]

    print("Topics of interest are", user_class.topics, "\n")
    for user in users:
        user.GenerateInterests()  # randomly generate interest in topics
        print(
            user.name,
            "has interest mat",
            np.ma.masked_array(user_class.topics, mask=user.interests),
        )
    # Mean square error
    def mse(user_interest, comp_interest, biased=True):
        if biased:
            return np.sum(np.dot((user_interest.T or comp_interest), biasedCorrelation))
        else:
            return np.sum(
                np.dot((user_interest == comp_interest.T), unbiasedCorrelation)
            )

    for user in users:
        for user_T in users:
            if user is not user_T:
                # printing users difference value with each other - used for testing
                # print(
                # user.name + "'s MSE relative to",
                # user_T.name,
                # "is",
                # mse(user.interests, user_T.interests),
                # )

                user.user_matches.append(
                    [mse(user.interests, user_T.interests, biased=False), user_T.name]
                )  # append matches to each user.user_matches
        user.user_matches = np.array(
            user.user_matches
        )  # turn into numpy array for matrix operations

    if False: # comment out print for testing
        for user in users:
            print(
                user.name, "has most in common with \n", user.user_matches
            )  # listing users with unsorted matches

            print(
                user.name,
                "has ranked matches \n",
                user.user_matches[np.argsort(user.user_matches[:, 0])],
            ) # listing sorted matches

    returnMatches("123")