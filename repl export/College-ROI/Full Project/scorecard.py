import pandas as pd

class Scorecard:

    def __init__(self):
        print("scorecard initialized")

    def getColleges(self):
        fields = ["School Name", "State"]
        college_df = pd.read_csv('scorecard_data.csv', usecols=fields)
        return college_df.to_json()

    def getState(self, college):
        fields = ["School Name", "State"]
        df = pd.read_csv('scorecard_data.csv', usecols=fields)
        state = df.loc[df['School Name'] == college]
        return state['State'].to_json()

    def getCollegesByState(self, state):
        fields = ["School Name", "State"]
        college_df = pd.read_csv('scorecard_data.csv', usecols=fields)
        collegeInState = college_df.loc[college_df['State'] == state]
        return collegeInState["School Name"].to_json()

    def getInStateTuition(self, school):
        fields = ["School Name", "Tuition_In"]
        tuition_df = pd.read_csv('scorecard_data.csv', usecols=fields)
        tuition = tuition_df.loc[tuition_df['School Name'] == school]
        return tuition["Tuition_In"]

    def getOutStateTuition(self, school):
        fields = ["School Name", "Tuition_Out"]
        tuition_df = pd.read_csv('scorecard_data.csv', usecols=fields)
        tuition = tuition_df.loc[tuition_df['School Name'] == school]
        return tuition["Tuition_Out"]

    def getCollegeType(self, school):
        fields = ["School Name", "College_Type"]
        df = pd.read_csv('scorecard_data.csv', usecols = fields)
        collegeType = df.loc[df['School Name'] == school]
        return collegeType["College_Type"]

    def getMedianCollegeEarnings(self, school):
        fields = ['School Name', "Median Earnings"]
        df = pd.read_csv('scorecard_data.csv', usecols = fields)
        median = df.loc[df['School Name'] == school]
        return median['Median Earnings']