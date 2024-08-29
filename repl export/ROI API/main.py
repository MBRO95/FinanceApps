import argparse
import pandas as pd
from re import sub
### Salary ###
# https://www.bls.gov/news.release/pdf/wkyeng.pdf
# https://1gyhoq479ufd3yna29x7ubjn-wpengine.netdna-ssl.com/wp-content/uploads/The-Economic-Value-of-College-Majors-Full-Report-web-FINAL.pdf
# http://online.wsj.com/public/resources/documents/info-Degrees_that_Pay_you_Back-sort.html
# http://online.wsj.com/public/resources/documents/info-Salaries_for_Colleges_by_Type-sort.html
# https://www.kaggle.com/wsj/college-salaries/home
# https://www.visualcapitalist.com/visualizing-salaries-college-degrees/
median_hs_grad_salary_start = 38428
median_college_grad_salary_start = 70200
# https://www.thebalance.com/u-s-inflation-rate-history-by-year-and-forecast-3306093
average_annual_inflation_rate = .018

### College Cost ###
# 1 - https://www.valuepenguin.com/student-loans/average-cost-of-college
# 2 - https://www.studentdebtrelief.us/news/average-cost-of-college-2018/
# 3 - https://www.collegedata.com/en/pay-your-way/college-sticker-shock/how-much-does-college-cost/whats-the-price-tag-for-a-college-education/
# Private
median_private_college_cost = 46950  # 2 & # 3
average_private_college_cost_increase_rate = .024  # 2
# Public
median_in_state_public_college_cost = 25290  # 1
median_out_state_public_college_cost = 40940  # 1
average_public_college_cost_increase_rate = .032  # 2


def calculate_roi(request):
    # request details
    major = request['degree']
    college = request['college']
    in_state = request['isInState']
    scholarships = float(request['scholarships'])
    repayment_rate = float(request['repayment'])/100
    age = int(request['age'])
    college_known = True if college != None else False
    major_known = True if major != None else False

    # working variables
    college_tuition = None
    median_college_earnings = None
    major_earnings_start = None
    major_earnings_mid = None
    college_type = None

    if (college_known):
        data = pd.read_csv("scorecard_data.csv")
        college_data = data.loc[data['School Name'] == college]
        median_college_earnings = float(college_data['Median Earnings'])
        if (in_state == True):
            college_tuition = float(college_data['Tuition_In'])
        else:
            college_tuition = float(college_data['Tuition_Out'])
        college_type = college_data['College_Type'].values.tolist()[0]
    else:
        college_type = 'Unknown'
        college_tuition = (
            median_in_state_public_college_cost + median_out_state_public_college_cost + median_private_college_cost)/3

    if (major_known):
        data = pd.read_csv("degrees_that_pay_back_WSJ.csv")
        major_data = data.loc[data['major'] == major]
        major_earnings_start = float(46000)#float(major_data['median_starting'])
        major_earnings_mid = float(77100)#float(major_data['median_mid'])

    college_grad_earnings = None
    if (college_known and major_known):
        college_grad_earnings = calculate_earnings(
            age+4, major_earnings_start, major_earnings_mid)
    elif (college_known and not major_known):
        college_grad_earnings = calculate_earnings(
            age+4, median_college_earnings, None)
    else:  # covers college_known == 'no' and major_known == 'no'
        college_grad_earnings = calculate_earnings(
            age+4, median_college_grad_salary_start, None)

    college_cost = calculate_college_cost(college_tuition, college_type)
    college_cost_with_scholarships = []
    for cost in college_cost[0]:
      college_cost_with_scholarships.append(cost + scholarships)
    post_college_principle = sum(college_cost_with_scholarships)
    net_college_grad_earnings = college_grad_earnings[1][-1] - post_college_principle
    hs_grad_earnings = calculate_hs_earnings(age)
    college_grad_earnings_cum = [0, 0, 0, 0] + college_grad_earnings[1]
    college_grad_earnings = [0, 0, 0, 0] + college_grad_earnings[0]

    college_grad_repayment = calculate_repayment_plan(
        post_college_principle, repayment_rate, college_grad_earnings, college_cost_with_scholarships)

    response = {
        'hs_earnings': hs_grad_earnings[0],
        'hs_earnings_cum': hs_grad_earnings[1],
        'net_hs_lifetime_earnings': hs_grad_earnings[1][-1],
        'college_earnings': college_grad_earnings,
        'college_earnings_cum': college_grad_earnings_cum,
        'net_college_lifetime_earnings': net_college_grad_earnings,
        'repayment_plan': college_grad_repayment,
        'net_college_cost': post_college_principle,
        'roi': round(net_college_grad_earnings / post_college_principle*-1)
    }
    return response


def calculate_hs_earnings(age):
    return calculate_earnings(age, median_hs_grad_salary_start, None)


def calculate_repayment_plan(net_cost, rate, salary_yoy, cost_yoy):
    repayment_yoy = []
    cost = net_cost
    cost_index = 0
    for salary in salary_yoy:
        if (salary == 0):
            if (cost_index == 0):
                repayment_yoy.append(cost_yoy[cost_index])
            else:
                repayment_yoy.append(
                    repayment_yoy[cost_index-1] + cost_yoy[cost_index])
            cost_index += 1
            continue
        if(cost <= 0):
            payment = salary * rate
            if((cost + payment) > 0):
                payment = abs(cost)
            cost += payment
            repayment_yoy.append(round(cost, 2))
    return repayment_yoy


def calculate_college_cost(tuition, college_type):
    year_by_year_cost = [tuition/-1]
    if (college_type == 'Private'):
        for x in range(3):
            year_by_year_cost.append(round(year_by_year_cost[x] +
                                           year_by_year_cost[x] * average_private_college_cost_increase_rate, 2))
    elif (college_type == 'Unknown'):
        for x in range(3):
            year_by_year_cost.append(round(year_by_year_cost[x] +
                                           year_by_year_cost[x] * ((average_private_college_cost_increase_rate + average_public_college_cost_increase_rate)/2), 2))
    else:
        for x in range(3):
            year_by_year_cost.append(round(year_by_year_cost[x] +
                                           year_by_year_cost[x] * average_public_college_cost_increase_rate, 2))
    total_cost = round(sum(year_by_year_cost), 2)
    return(year_by_year_cost, total_cost)

# "...men’s incomes also stall about 10 to 20 years before retirement: “The pay growth leveling off there really just shows that you hit a certain ceiling in your career that is very hard to overcome.”" - PayScale’s chief economist Katie Bardaro https://www.cnbc.com/2018/11/02/the-age-at-which-youll-earn-the-most-money-in-your-career.html
# Using 15 years as the stalling period
# Assuming promotion every two years


def calculate_earnings(age, initial_salary, mid_career_salary):
    working_years = 65-age
    initial_salary = (0, initial_salary)
    if (mid_career_salary == None):
        mid_career_salary = (working_years/2, initial_salary[1] * ((
            1.0+average_annual_inflation_rate) ** float(working_years/2)))
    else:
        mid_career_salary = (working_years/2, mid_career_salary)
    year_by_year_earnings = []
    year_by_year_cumulative_earnings = []
    salary_delta = mid_career_salary[1] - initial_salary[1]
    logarithmic_growth_rate = salary_delta / (mid_career_salary[0] ** (1.0/3))
    exponential_growth_rate = (
        mid_career_salary[1] / initial_salary[1]) ** (1.0/(working_years/2))
    for x in range(working_years):
        current_year_salary = None
        if (x > (mid_career_salary[0])):
            current_year_salary = logarithmic_growth_rate * \
                (x ** (1.0/3)) + initial_salary[1]
        else:
            current_year_salary = initial_salary[1] * \
                ((exponential_growth_rate) ** x)
        year_by_year_earnings.append(round(current_year_salary, 2))
        if (x == 0):
            year_by_year_cumulative_earnings.append(round(current_year_salary, 2))
        else:
            year_by_year_cumulative_earnings.append(
                round(year_by_year_cumulative_earnings[x-1] + current_year_salary, 2))
    return (year_by_year_earnings, year_by_year_cumulative_earnings)


if __name__ == '__main__':
    request = {
        'degree': 'Information Technology (IT)',
        'college': 'Harvard University',
        'isInState': False,
        'scholarships': 2500,
        'repayment': 18,
        'age': 18
    }
    out = calculate_roi(request)
    statement = f'''Hey Matt!\n\nBased on the information you provided, we estimate that your degree will cost you {'${:,.2f}'.format(abs(out['net_college_cost']))}. That may sound like a lot, but we're predicting that you'll make a starting salary of {'${:,.2f}'.format(out['college_earnings'][4])}. Even better, half-way through your career we estimate that you'll be making around {'${:,.2f}'.format(out['college_earnings'][23])}.\n\nWhen it comes to making an informed decision about the degree you wish to obtain, it's important to consider your Return on Investment (ROI). We've calculated that for you based on the information you provided us and we have some good news! Knowing that your college should cost {'${:,.2f}'.format(abs(out['net_college_cost']))}, we're happy to tell you that your degree will pay you back over {out['roi']}x what it cost.\n\nWe project that your lifetime earnings between now and retirement will be right around {'${:,.2f}'.format(out['net_college_lifetime_earnings'])}. That's a {str(out['roi']) + '00%'} ROI!\n'''
    print(statement)
    print(out)

