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

# Function to integrate performer type into ROI calculation
def get_performance(tier):
  tiers = {
      'low' : 'p10',
      'mid-low' : 'p25',
      'mid' : 'mid',
      'mid-high' : 'p75',
      'high' : 'p90'
  }
  return tiers.get(tier, "Invalid tier")

# Main API function to calculate ROI
def calculate_roi(request):
    # request details
    major = request['degree']
    performer = request['performer']
    college = request['college']
    in_state = request['isInState']
    principle = float(request['principle'])
    repayment_rate = float(request['repayment'])/100
    age = int(request['age'])
    college_known = True if college != None else False
    major_known = True if major != None else False
    print(major)
    print(major_known)

    # working variables
    college_tuition = None
    college_type = None
    college_earnings = {}
    major_earnings = {}

    if (college_known):
        data = pd.read_csv("scorecard_data.csv")
        college_data = data.loc[data['School Name'] == college]
        college_earnings = {
        'p10' : float(college_data['10th Percentile Earnings'].iloc[0]),
        'p25' : float(college_data['25th Percentile Earnings'].iloc[0]),
        'mid' : float(college_data['Median Earnings'].iloc[0]),
        'p75' : float(college_data['75th Percentile Earnings'].iloc[0]),
        'p90' : float(college_data['90th Percentile Earnings'].iloc[0])
        }
        if (in_state == True):
            college_tuition = float(college_data['Tuition_In'].iloc[0])
        else:
            college_tuition = float(college_data['Tuition_Out'].iloc[0])
        college_type = college_data['College_Type'].values.tolist()[0]
    else:
        college_type = 'Unknown'
        college_tuition = (
            median_in_state_public_college_cost + median_out_state_public_college_cost + median_private_college_cost)/3

    if (major_known):
        data = pd.read_csv("degrees_that_pay_back_WSJ.csv")
        major_data = data.loc[data['major'] == major]
      # Ratio represents factor difference between starting career median and halfway career median
        ratio = float(major_data['median_starting'].iloc[0])/float(major_data['median_mid'].iloc[0])
        major_earnings = {
          'sp10' : float(major_data['10p_mid'].iloc[0])*ratio,
          'sp25' : float(major_data['25p_mid'].iloc[0])*ratio,
          'smid' : float(major_data['median_starting'].iloc[0]),
          'sp75' : float(major_data['75p_mid'].iloc[0])*ratio,
          'sp90' : float(major_data['90p_mid'].iloc[0])*ratio,
          'mp10' : float(major_data['10p_mid'].iloc[0]),
          'mp25' : float(major_data['25p_mid'].iloc[0]),
          'mmid' : float(major_data['median_mid'].iloc[0]),
          'mp75' : float(major_data['75p_mid'].iloc[0]),
          'mp90' : float(major_data['90p_mid'].iloc[0])
        }
        print(major_earnings['smid'])

    # Composite earnigns data calculated by multiplying the ratio of (median_specific_college_earnings/median_general_college_earnings) by the degree-specific starting AND mid-career salaries
    college_grad_earnings = None
    if (college_known and major_known):
        perf = get_performance(performer)
        ratio = 1
        if(college_earnings['mid'] > median_college_grad_salary_start):
          ratio = college_earnings['mid'] / median_college_grad_salary_start
        print(median_college_grad_salary_start)
        print(ratio)
        perf_earnings_start = major_earnings[f'''{'s'+perf}'''] * ratio
        perf_earnings_mid = major_earnings[f'''{'m'+perf}'''] * ratio
        print(perf_earnings_start, perf_earnings_mid)
        college_grad_earnings = calculate_earnings(
            age+4, perf_earnings_start, perf_earnings_mid)
    elif (college_known and not major_known):
        perf = get_performance(performer)
        perf_earnings_start = college_earnings[f'''{perf}''']
        college_grad_earnings = calculate_earnings(
            age+4, perf_earnings_start, None)
    # Expand to recommend top 3 colleges for major by highest salary
    # Pure degree data driving
    elif (major_known and not college_known):
        perf = get_performance(performer)
        perf_earnings_start = major_earnings[f'''{'s'+perf}''']
        perf_earnings_mid = major_earnings[f'''{'m'+perf}''']
        college_grad_earnings = calculate_earnings(
            age+4, perf_earnings_start, perf_earnings_mid)
    else:  # covers college_known == 'no' and major_known == 'no'
        college_grad_earnings = calculate_earnings(
            age+4, median_college_grad_salary_start, None)
    
    college_cost = calculate_college_cost(college_tuition, college_type)
    post_college_principle = college_cost[1] + principle
    net_college_grad_earnings = college_grad_earnings[1][-1] - \
        post_college_principle
    hs_grad_earnings = calculate_hs_earnings(age)
    college_grad_earnings_cum = [0, 0, 0, 0] + college_grad_earnings[1]
    college_grad_earnings = [0, 0, 0, 0] + college_grad_earnings[0]
    
    college_grad_repayment = calculate_repayment_plan(
        post_college_principle, repayment_rate, college_grad_earnings, college_cost[0])
    
    response = {
        'hs_earnings': hs_grad_earnings[0],
        'hs_earnings_cum': hs_grad_earnings[1],
        'net_hs_lifetime_earnings': hs_grad_earnings[1][-1],
        'college_earnings': college_grad_earnings,
        'college_earnings_cum': college_grad_earnings_cum,
        'net_college_lifetime_earnings': net_college_grad_earnings,
        'repayment_plan': college_grad_repayment,
        'net_college_cost': post_college_principle,
        'roi': round(net_college_grad_earnings / post_college_principle*-1, 2)
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
        # If college AND major are unknown, performer level is not a visible field
        'performer': 'mid-high',
        # Set to 'None' if not known
        'degree': 'Computer Engineering',
        # Set to 'None' if not known
        'college': 'Champlain College',
        'isInState': False,
        'principle': 0,
        'repayment': 18,
        'age': 18
    }
    out = calculate_roi(request)
    print("Debt Repayment Timeline: " + str(out['repayment_plan']))
    statement = f'''Hey Matt!\n\nBased on the information you provided, we estimate that your degree will cost you {'${:,.2f}'.format(abs(out['net_college_cost']))}. That may sound like a lot, but we're predicting that you'll make a starting salary of {'${:,.2f}'.format(out['college_earnings'][4])}. Even better, half-way through your career we estimate that you'll be making around {'${:,.2f}'.format(out['college_earnings'][23])}.\n\nWhen it comes to making an informed decision about the degree you wish to obtain, it's important to consider your Return on Investment (ROI). We've calculated that for you based on the information you provided us and we have some good news! Knowing that your college should cost {'${:,.2f}'.format(abs(out['net_college_cost']))}, we're happy to tell you that your degree will pay you back over {str(round(out['roi']))+'00%'}.\n\nBased on your yearly salary allocation of {request['repayment']}% towards the repayment of your college debt, you'll be debt-free by age {out['repayment_plan'].index(0.0) + request['age']}.\n\nWe project that your lifetime earnings between now and retirement will be right around {'${:,.2f}'.format(out['net_college_lifetime_earnings'])}. That's a {str(round(out['roi'])) + 'x'} ROI!\n'''
    print('\n' + statement)