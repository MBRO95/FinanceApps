import csv
import pickle
from scorecard import Scorecard

class User: 

    def __init__(self):
        self.db = {}
        print("User created")
        self.repayment = .2

    def setName(self, name):
        self.name = name
        self.db['name'] = self.name
        print("Name set")

    def getName(self):
        return self.name

    def setAge(self, age):
        self.age = age
        self.db['age'] = self.age
        print("Age set")

    def getAge(self):
        return self.age

    def setCollege(self, college):
        self.college = college
        self.db['college'] = self.college
        print("College set")

    def getCollege(self):
        return self.college
    
    def setInStateBool(self, isInState):
        self.isInState = isInState
        self.db['inStateFlag'] = self.isInState
    
    def getInStateBool(self):
        return self.isInState

    def setDegree(self, degree):
        self.degree = degree
        self.db['degree'] = self.degree
        print("degree set")

    def getDegree(self):
        return self.degree

    def setPrinciple(self, amount):
        self.principle = amount
        self.db['principle'] = self.principle
    
    def getPrinciple(self):
        return self.principle

    def setRepayment(self, amount):
        self.repayment = amount
        self.db['repayment'] = self.repayment

    def getRepayment(self):
        return self.repayment

    def save(self):
        self.b = pickle.dumps(self.db)
        self.store()

    def retrieve(self):
        self.db = pickle.loads(self.b)
        return self.db

    def store(self):
        data = []
        data.append(self.db)
        with open('userdata.csv', 'w') as csvFile:
            fields = ['name', 'age', 'college', 'inStateFlag', 'degree', 'principle', 'repayment']
            writer = csv.DictWriter(csvFile, fieldnames = fields)
            writer.writeheader()
            writer.writerows(data)
        print("Save complete")
        csvFile.close()