import pandas as pd

class Degree:

    def __init__(self):
        print("degree initialized")

    def getDegrees(self):
        fields = ["major"]
        degree_df = pd.read_csv('degrees_that_pay_back_WSJ.csv', usecols=fields)
        return degree_df.to_json()

    def getEarnings(self, degree):
        fields = ["major", "median_starting", "median_mid"]
        df = pd.read_csv('degrees_that_pay_back_WSJ.csv', usecols=fields)
        earnings = df.loc[df['major'] == degree]
        return earnings