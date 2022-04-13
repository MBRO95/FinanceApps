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
# 1 - https://www.communitycollegereview.com/avg-tuition-stats/national-data
# 2 - https://www.valuepenguin.com/student-loans/average-cost-of-college
# 3 - https://ccrc.tc.columbia.edu/Community-College-FAQs.html
# 4 - https://www.studentdebtrelief.us/news/average-cost-of-college-2018/
# 5 - https://www.collegedata.com/en/pay-your-way/college-sticker-shock/how-much-does-college-cost/whats-the-price-tag-for-a-college-education/
# 6 - https://www.huffpost.com/entry/more-community-colleges-are-offering-bachelors-degrees_b_5ae1de02e4b0d538c22dfbfe
# Private
median_private_college_tuition = 34740  # 4 & #5
median_private_college_room_board = 12210  # 5
median_private_college_cost = 46950  # 4 & #5
median_private_community_college_cost_2_year = 15480  # 1
average_private_college_cost_increase_rate = .024  # 4
# Public
# In-state
median_in_state_public_college_tuition = 9970  # 5
median_in_state_public_college_room_board = 10800  # 5
median_in_state_public_college_cost = 25290  # 2
median_in_state_public_community_college_cost_2_year = 4828  # 1
median_in_state_public_community_college_cost_4_year = 10230  # 3
# Out-state
median_out_state_public_college_tuition = 25620  # 5
median_out_state_public_college_room_board = 10800  # 5
median_out_state_public_college_cost = 40940  # 2
median_out_state_public_community_college_cost_2_year = 8587  # 1
median_out_state_public_community_college_cost_4_year = 25620  # 2 & #5
# Community
community_college_4yr_degree_states = ['WA', 'CA', 'NV', 'UT', 'CO', 'NM',
                                       'TX', 'OK', 'ND', 'WI', 'MI', 'IN', 'WV', 'NY', 'VT', 'DE', 'GA', 'FL']  # 6
average_public_college_cost_increase_rate = .032  # 4

'''
degree_types = ['1) Associates', '2) Bachelors', '3) Graduate']
major_types = ['1) Agriculture and Natural Resources', '2) Architecture and Engineering', '3) Arts', '4) Biology and Life Sciences', '5) Business', '6) Communications and Journalism', '7) Computers, Statistics, and Mathematics',
               '8) Education', '9) Health', '10) Humanities and Liberal Arts', '11) Industrial Arts, Consumer Services, and Recreation', '12) Law and Public Policy', '13) Physical Sciences', '14) Psychology and Social Work', '15) Social Sciences']
'''
def calculate_roi(request):
  # request details
  major = request['degree']
  college = request['college']
  in_state = request['isInState']
  principle = float(request['principle'])
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
    data = pd.read_csv("./ROI/scorecard_data.csv")
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
    data = pd.read_csv("./ROI/degree_to_earnings_census.csv")
    major_data = data.loc[data['major'] == major]
    major_earnings_start = float(major_data['median_starting'])
    major_earnings_mid = float(major_data['median_mid'])

  college_grad_earnings = None
  if (college_known and major_known):
      college_grad_earnings = calculate_earnings(age+4, major_earnings_start, major_earnings_mid)
  elif (college_known and not major_known):
      college_grad_earnings = calculate_earnings(age+4, median_college_earnings, None)
  else: # covers college_known == 'no' and major_known == 'no'
      college_grad_earnings = calculate_earnings(age+4, median_college_grad_salary_start, None)

  post_college_principle = calculate_college_cost(college_tuition, college_type)[1] + principle
  net_college_grad_earnings = college_grad_earnings[1] - post_college_principle
  hs_grad_earnings = calculate_hs_earnings(age)
  college_grad_earnings = [0,0,0,0] + college_grad_earnings[0]
  
  college_grad_repayment = calculate_repayment_plan(post_college_principle, repayment_rate, college_grad_earnings)
  
  response = {
    'hs_earnings' : hs_grad_earnings,
    'grad_earnings' : college_grad_earnings,
    'repayment_plan' : college_grad_repayment,
    'net_college_cost' : post_college_principle,
    'net_lifetime_earnings' : net_college_grad_earnings,
    'roi' : round(net_college_grad_earnings / post_college_principle*-1, 2)
  }
  return response

def calculate_hs_earnings(age):
  return calculate_earnings(age, median_hs_grad_salary_start, None)

def calculate_repayment_plan(net_cost, rate, salary_yoy):
  repayment_yoy = []
  cost = net_cost
  for salary in salary_yoy:
    if(cost <= 0):
      payment = salary * rate
      if((cost + payment) > 0):
        payment = abs(cost)
      cost += payment
      repayment_yoy.append(round(cost, 2))
  return repayment_yoy


def chatbot():
    # working variables
    college_tuition = None
    median_college_earnings = None
    major_earnings_start = None
    major_earnings_mid = None
    college_type = None

    name = input("Hey There! What's your name: ")
    print(f'''\nHey {name}, let's get some more info from you...''')
    age = input(f'''How old are you {name}: ''')
    state = input(f'''{age} years young!\n\nWhat state do you live in (i.e. PA): ''')
    college_known = input(
        f'''\n{name}, do you know what college you'd like to go to (yes or no): ''')
    college = ''
    if college_known == 'yes':
        # CollegeScoreCard Dataset
        data = pd.read_csv(
            "./ROI/scorecard_data.csv")
        college_list = data['School Name'].values.tolist()
        print("\nHere's a list of colleges: \n")
        while True:
            try:
                colleges = []
                for place in college_list:
                    colleges.append(str(college_list.index(place)+1) +
                                    ") " + str(place))
                print(f'''\n{print_table(colleges,3,60)}\n''')
                college = int(
                    input(f'''\n{name}, enter the code of the college you would like to go to: '''))
            except ValueError:
                print(
                    f'''\nSorry, please enter the number of the college you'd like. Valid input is 1-{len(college_list)}''')
                continue
            else:
                break
        college_data = data.iloc[college-1]
        median_college_earnings = float(college_data['Median Earnings'])
        print(
            f'''\nAwesome, {name}!\nDid you know that {college_data['School Name']} is known for {college_data['Highest Degree Awarded']} degrees? Cool stuff!''')
        if (college_data['State'] == state):
            print(
                f'''You're staying in-state.''')
            print(
                f'''Looks like your tuition will cost {'${:,.2f}'.format(college_data['Tuition_In'])} annually.''')
            college_tuition = float(college_data['Tuition_In'])
        else:
            print(
                f'''You chose an out-of-state school.''')
            print(
                f'''Looks like your tuition will cost {'${:,.2f}'.format(college_data['Tuition_Out'])} annually.''')
            college_tuition = float(college_data['Tuition_Out'])
        college_type = college_data['College_Type']
    else:
        college_type = 'Unknown'
        college_tuition = (
            median_in_state_public_college_cost + median_out_state_public_college_cost + median_private_college_cost)/3
        print(
            f'''That's perfectly fine, {name}!''')
    major_known = input(f'''\n{name}, do you know what you want to study (yes or no): ''')
    major = None
    if major_known == 'yes':
        # WSJ Degree's that pay you back dataset
        # data = pd.read_csv("/Users/MMAY/Downloads/College ROI/degrees-that-pay-back.csv")
        # Census Earnings dataset
        data = pd.read_csv(
            "./ROI/degree_to_earnings_census.csv")
        major_types = data['major'].values.tolist()
        print("\nHere's a list of majors: \n")
        while True:
            try:
                majors = []
                for major in major_types:
                    majors.append(str(major_types.index(major)+1) +
                                  ") " + str(major))
                print(f'''\n{print_table(majors,3,60)}''')
                major = int(
                    input(f'''{name}, enter the code of the degree you would like to pursue: '''))
            except ValueError:
                print(
                    f'''Sorry, please enter the number of the degree you'd like. Valid input is 1-{len(major_types)}\n''')
                continue
            else:
                break
        major_data = data.iloc[major-1]
        major_earnings_start = float(major_data['median_starting'])
        major_earnings_mid = float(major_data['median_mid'])
        #calculate_earnings(age, start, mid)
    else:
        print('No Worries!\n')

    # same as college_known == 'no' and major_known == 'yes'
    if (college_known == 'yes' and major_known == 'yes'):
        return (calculate_college_cost(college_tuition, college_type), calculate_earnings(age, major_earnings_start, major_earnings_mid))
    elif (college_known == 'yes' and major_known == 'no'):
        return (calculate_college_cost(college_tuition, college_type), calculate_earnings(age, median_college_earnings, None))
    else:  # covers college_known == 'no' and major_known == 'no'
        return (calculate_college_cost(college_tuition, college_type), calculate_earnings(age, median_college_grad_salary_start, None))


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
    return(year_by_year_cost, abs(total_cost))


def print_table(data, cols, wide):
    '''Prints formatted data on columns of given width.'''
    n, r = divmod(len(data), cols)
    pat = '{{:{}}}'.format(wide)
    line = '\n'.join(pat * cols for _ in range(n))
    last_line = pat * r
    print(line.format(*data))
    print(last_line.format(*data[n*cols:]))

# "...men’s incomes also stall about 10 to 20 years before retirement: “The pay growth leveling off there really just shows that you hit a certain ceiling in your career that is very hard to overcome.”" - PayScale’s chief economist Katie Bardaro https://www.cnbc.com/2018/11/02/the-age-at-which-youll-earn-the-most-money-in-your-career.html
# Using 15 years as the stalling period
# Assuming promotion every two years


def calculate_earnings(age, initial_salary, mid_career_salary):
    working_years = 65-int(age)
    initial_salary = (0, initial_salary)
    if (mid_career_salary == None):
        mid_career_salary = (working_years/2, initial_salary[1] * (
            1.0+average_annual_inflation_rate) ** float(working_years/2))
    else:
        mid_career_salary = (working_years/2, mid_career_salary)

    # average_annual_salary_increase = ((initial_salary + mid_career_salary)/2)/(working_years/2)/mid_career_salary
    # print(average_annual_salary_increase)
    year_by_year_earnings = []
    lifetime_earnings = 0
    salary_delta = mid_career_salary[1] - initial_salary[1]
    logarithmic_growth_rate = salary_delta / (mid_career_salary[0] ** (1.0/3))
    exponential_growth_rate = (
        mid_career_salary[1] / initial_salary[1]) ** (1.0/working_years)
    print('\n')
    for x in range(working_years):
        current_year_salary = None
        if (x >= (mid_career_salary[0])):
            current_year_salary = logarithmic_growth_rate * \
                (x ** (1.0/3)) + initial_salary[1]
        else:
            current_year_salary = initial_salary[1] * \
                ((exponential_growth_rate) ** x)
        year_by_year_earnings.append(round(current_year_salary, 2))
        lifetime_earnings += current_year_salary
    return (year_by_year_earnings, round(lifetime_earnings, 2))


if __name__ == '__main__':
    '''parser = argparse.ArgumentParser(description = 'Say hello')
    parser.add_argument('name')
    parser.add_argument('college', help='')
    args = parser.parse_args()
    main(args.name)'''
  
    '''request = {
      'degree' : 'Nuclear engineering',
      'college' : 'Harvard University',
      'isInState' : True,
      'principle' : 25000,
      'repayment' : 18,
      'age' : 23
    }
    calculate_roi(request)'''
    
    data = chatbot()
    
    print(f'''\nWith lifetime earnings of {'${:,.2f}'.format(data[1][1])} and total college cost of {'${:,.2f}'.format(data[0][1])}, the ROI of your college degree is {round(data[1][1]/data[0][1])}x or {round(data[1][1]/data[0][1])}00%''')