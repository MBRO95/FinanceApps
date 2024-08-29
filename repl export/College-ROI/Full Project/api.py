from scorecard import Scorecard
from calculator import Calculator
from degree import Degree
from user import User
import json

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

user = User()
d = Degree()

@app.route("/colleges")
def getColleges():
    score = Scorecard()   
    return score.getColleges()

@app.route("/colleges/<state>")
def getCollegesByState(state):
    score = Scorecard()
    return score.getCollegesByState(state)

@app.route("/colleges/<college>")
def getStateOfCollege(college): 
    score = Scorecard()
    return score.getState(college)

@app.route("/colleges", methods=['POST'])
def setCollege():
    college = request.get_json(force=True)
    user.setCollege(college['college'])
    user.save()
    return jsonify({'status': 'success'})

@app.route("/degrees")
def getDegrees():
    degree = Degree()
    return degree.getDegrees()

@app.route("/degrees", methods=['POST'])
def setDegree():
    degree = request.get_json(force=True)
    user.setDegree(degree['degree'])
    user.save()
    return jsonify({'status': 'success'})

@app.route("/age", methods=['POST'])
def setAge():
    age = request.get_json(force=True)
    user.setAge(age['age'])
    user.save()
    return jsonify({'status': 'success'})

@app.route("/user")
def getUser():
    return jsonify({'college': user.college, 'degree': user.degree})

@app.route("/user", methods=['POST'])
def setUser():
    name = request.get_json(force=True)
    print(name['name'])
    user.setName(name['name'])
    user.save()
    return jsonify({'status': 'success'})

@app.route("/tuition", methods=['POST'])
def setTuitionFlag():
    isInState = request.get_json(force=True)
    user.setInStateBool(isInState['isInState'])
    user.save()
    return jsonify({'status':'success'})

@app.route("/principle", methods=['POST'])
def setPrinciple():
    principle = request.get_json(force=True)
    user.setPrinciple(principle['principle'])
    user.save()
    return jsonify({'status':'success'})

@app.route("/repayment", methods=['POST'])
def setRepayment():
    repayment = request.get_json(force=True)
    user.setRepayment(repayment['repayment']/100.0)
    user.save()
    getEarnings()
    return jsonify({'status': 'success'})

@app.route("/chartdata")
def getEarnings():
    calc = Calculator(user)
    data = calc.getChartData()
    yearly_earnings = data[0]
    cumulative_earnings = data[1]
    hs_earnings = data[2]
    cumulative_hs = data[3]
    repayment = data[4]
    total_cost = data[5]
    starting_salary = data[6]
    mid_salary = data[7]

    college = user.college
    degree = user.degree
    name = user.name
    age = user.age
    repayment_percent = user.repayment

    return jsonify({
        'yearly_earnings': yearly_earnings,
        'cumulative_earnings': cumulative_earnings,
        'hs_earnings': hs_earnings,
        'cumulative_hs': cumulative_hs,
        'repayment': repayment,
        'college': college,
        'degree': degree,
        'name': name,
        'age': age,
        'repayment_percent': repayment_percent * 100,
        'total_cost': total_cost,
        'starting_salary': starting_salary,
        'mid_salary': mid_salary
    })
