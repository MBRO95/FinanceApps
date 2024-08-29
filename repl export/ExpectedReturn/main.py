principal = 25000
monthlyContribution = input("Enter Monthly Contribution: $")
print("Monthly Contributions: $%s" % monthlyContribution)
yearlyContribution = int(monthlyContribution) * 12
print("Yearly Contributions: $%d" % yearlyContribution)
annualRate = float(input("Enter Expected Return Rate: "))