from __future__ import print_function
import User
from datetime import datetime
import numpy as np

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

unbiasedCorrelation = np.identity(User.numTopics)

k = 2  # number of matches desired

if __name__ == "__main__":
    users = [
        User.User("Person A", "a", datetime(1998, 1, 6)),
        User.User("Person B", "b", datetime(1985, 7, 21)),
        User.User("Person C", "c", datetime(1925, 1, 11)),
        User.User("Person D", "d", datetime(2001, 2, 5)),
        User.User("Person E", "e", datetime(1995, 9, 30)),
        User.User("Person F", "f", datetime(2012, 7, 13)),
    ]

    print("Topics of interest are", User.topics, "\n")
    for user in users:
        user.GenerateInterests()  # randomly generate interest in topics
        print(
            user.name,
            "has interest mat",
            np.ma.masked_array(User.topics, mask=user.interests),
        )
    # Mean square error
    def mse(user_interest, comp_interest, biased=True):
        if biased:
            return np.sum(np.dot((user_interest.T or comp_interest), biasedCorrelation))
        else:
            return np.sum(np.dot((user_interest == comp_interest.T), unbiasedCorrelation))

    userMatchSet = []
    for user in users:
        userMatches = []
        # match = 999999
        for user_T in users:
            if user is not user_T:
                # print(
                # user.name + "'s MSE relative to",
                # user_T.name,
                # "is",
                # mse(user.interests, user_T.interests),
                # )
                
                user.user_matches.append([mse(user.interests, user_T.interests, biased=False), user_T.name])
        user.user_matches = np.array(user.user_matches)
                # Match.appendMatch(mse=mse(user.interests, user_T.interests, biased=False), name=user_T.name)

    
        # userMatchSet.append(userMatches)

        #         if mse(user.interests, user_T.interests, biased=True) <= match:
        #             match = mse(user.interests, user_T.interests, biased=True)
        #             temp = user_T.name


    for user in users:
        print(user.name,"has most in common with \n",user.user_matches)
        
        print(user.name,"has ranked matches \n",user.user_matches[np.argsort(user.user_matches[:,0])])
    

    
