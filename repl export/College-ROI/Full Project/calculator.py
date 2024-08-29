import pandas as pd
from degree import Degree
from scorecard import Scorecard
import json
from user import User
import statistics
import math

class Calculator:

    def __init__(self, user, repayment=.2):
        print("initialized calculator")
        df = pd.read_csv('userdata.csv')

        self.degree = df['degree'][0] if (not hasattr(user, 'degree')) else  user.degree
        self.age = df['age'][0] if (not hasattr(user, 'age')) else user.age
        self.college = df['college'][0] if (not hasattr(user, 'college')) else user.college
        self.inStateFlag = df['inStateFlag'][0] if (not hasattr(user, 'inStateFlag')) else user.inStateFlag
        self.scholarships = df['principle'][0] if (not hasattr(user, 'principle')) else user.principle
        self.repayment = df['repayment'][0] if (not hasattr(user, 'repayment')) else user.repayment
        print(self.repayment)

        self.s = Scorecard()
        self.d = Degree()
        median_in_state_public_tuition = 25290
        median_out_state_public_tuition = 40940
        median_private_tuition = 46950

        self.defaultTuition = round(statistics.mean([median_in_state_public_tuition, median_out_state_public_tuition, median_private_tuition]), 2)

    def getChartData(self):
        earnings = self.getEarnings()
        hs_earnings = self.calculate_hs_earnings()
        return (
            json.dumps(earnings[0]),
            json.dumps(earnings[1]),
            json.dumps(hs_earnings[0]),
            json.dumps(hs_earnings[1]),
            json.dumps(self.getRepaymentPlan()),
            json.dumps(self.totalCollegeCost),
            json.dumps(self.starting_salary),
            json.dumps(self.mid_salary)
        )

    def getEarnings(self):

        if(isinstance(self.degree, str) and self.degree != ''):
            earnings = self.d.getEarnings(self.degree)
            self.starting_salary = earnings['median_starting'].values[0]
            self.mid_salary = earnings['median_mid'].values[0]
            self.wages = self.calculate_wages((self.age + 4), earnings['median_starting'].values[0], earnings['median_mid'].values[0])
        else:
            earnings = self.s.getMedianCollegeEarnings(self.college)
            earnings = earnings.values[0]
            self.starting_salary = earnings.astype(float)
            self.mid_salary = ''
            self.wages = self.calculate_wages((self.age + 4), earnings, 0)
   
        padded_wage_zero = [0, 0, 0, 0] + self.wages[0]
        padded_wage_one = [0, 0, 0, 0] + self.wages[1]

        return (padded_wage_zero, padded_wage_one)

    def getRepaymentPlan(self):
        college_cost = self.calculate_college_cost()
        college_cost_with_scholarships = []
      
        for cost in college_cost[0]:
            college_cost_with_scholarships.append(cost + self.scholarships)
        post_college_principle = sum(college_cost_with_scholarships)

        col_salary = [0, 0, 0, 0] + self.wages[0]

        return self.calculate_repayment_plan(post_college_principle, self.repayment, col_salary, college_cost_with_scholarships)

    def calculate_hs_earnings(self):
        median_hs_grad_salary = 38428
        hs_salary = self.calculate_wages(self.age, median_hs_grad_salary, 0)
        return hs_salary

    def calculate_college_cost(self):
       
        total_cost = 0
        avg_private_inc_rate = .024
        avg_public_inc_rate = .032

        if(self.college != ''):
            college_type = self.s.getCollegeType(self.college).values[0]
            if(not math.isnan(self.inStateFlag)):
                tuition = self.s.getInStateTuition(self.college).values[0]
            else: 
                tuition = self.s.getOutStateTuition(self.college).values[0]
        else: 
            college_type = ''
            tuition = self.defaultTuition
        
        total_cost -= tuition
        yearly_cost = [total_cost]

        if(college_type == 'Private'):
            for x in range(3):
                yearly_cost.append(round(yearly_cost[x] + yearly_cost[x] * avg_private_inc_rate, 2))
        elif(college_type == 'Public'):
            for x in range(3):
                yearly_cost.append(round(yearly_cost[x] + yearly_cost[x] * avg_public_inc_rate, 2))
        else: 
            for x in range(3):
                yearly_cost.append(round(yearly_cost[x] + yearly_cost[x] * (avg_public_inc_rate + avg_private_inc_rate)/2, 2))

        self.yearlyCollegeCosts = yearly_cost
        self.totalCollegeCost = sum(yearly_cost)
        return (yearly_cost, sum(yearly_cost))

    def calculate_repayment_plan(self, net_cost, rate, salary_yoy, cost_yoy):
        repayment_yoy = []
        cost = net_cost
        cost_index = 0

        for salary in salary_yoy:

            if (salary == 0):
                if (cost_index == 0):
                    repayment_yoy.append(cost_yoy[cost_index])
                else:
                    repayment_yoy.append(repayment_yoy[cost_index-1] + cost_yoy[cost_index])
                cost_index += 1
                continue
            if(cost <= 0):
                payment = salary * rate
                if((cost + payment) > 0):
                    payment = abs(cost)
                cost += payment
                repayment_yoy.append(round(cost, 2))

        return repayment_yoy
    
    def calculate_wages(self, age, initial_salary, mid_career_salary):
        avg_ann_inflation_rate = .018

        working_years = 65 - age

        if (mid_career_salary == 0):
            mid_career_salary = initial_salary * (1.0 + avg_ann_inflation_rate) ** float(working_years / 2)
        
        year_by_year_earnings = [] 
        year_by_year_cumulative = [] 
        
        lifetime_earnings = 0

        salary_delta = mid_career_salary - initial_salary
        log_growth_rate = salary_delta / ((working_years/2) ** (1.0/3))
        exp_growth_rate = (mid_career_salary / initial_salary) ** (1.0/(working_years/2))

        for x in range(working_years):
            current_year_salary = 0
            if(x > (working_years/2)):
                current_year_salary = log_growth_rate * (x ** (1.0/3)) + initial_salary
            else:
                current_year_salary = initial_salary * (exp_growth_rate ** x)

            year_by_year_earnings.append(round(current_year_salary, 2))
            
            if(x == 0):
                year_by_year_cumulative.append(round(current_year_salary, 2))
            else:
                year_by_year_cumulative.append(round(year_by_year_cumulative[x-1] + current_year_salary, 2))

        return (year_by_year_earnings, year_by_year_cumulative)

# u = User()
# c = Calculator(u)
# c.getChartData()