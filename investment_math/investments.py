import math
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_tax_rates():
    url = "https://www.rocketmortgage.com/learn/property-taxes-by-state"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')  # Find the first table on the page

    df = pd.read_html(str(table), header=0)[0]  # Convert the table to a dataframe

    # Create a dictionary of tax rates by state
    tax_rates = {row['State']: row['Real Estate Tax Rate'] for _, row in df.iterrows()}

    return tax_rates

def scrape_insurance_rates():
    url = 'https://www.bankrate.com/insurance/homeowners-insurance/homeowners-insurance-cost/#cost-by-state'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')  # Find the first table on the page

    df = pd.read_html(str(table))[0]  # Convert the table to a dataframe
    
    # Remove the string and extract only the dollar amount from the "Average monthly premium" column
    df['Average annual premium'] = df['Average annual premium'].str.extract('(\d+\.?\d*)').astype(float)
    
    # Create a dictionary of insurance rates by state
    insurance_rates = {row['State']: row['Average annual premium'] / 250000 for _, row in df.iterrows()}

    return insurance_rates

def refinancing_break_even(old_monthly_payment, new_monthly_payment, refinancing_cost):
    savings_per_month = old_monthly_payment - new_monthly_payment
    break_even_in_months = refinancing_cost / savings_per_month
    return break_even_in_months

def invest(amount, rate, time):
    print("principal amount: ${}".format(amount))
    print("annual rate of return: {}".format(rate))
    for t in range(1, time + 1):
        amount = amount * (1 + rate)
        print("year {}: ${}".format(t, amount))
    print()

def mortgage_payoff(amount, annual_rate, monthly_payment, down_payment=0):
    amount -= down_payment  # Subtract the down payment from the loan amount
    monthly_rate = annual_rate / 12

    if monthly_payment <= amount * monthly_rate:
        return "Infinite. Monthly payment is less than the interest."

    months = -math.log(1 - monthly_rate * amount / monthly_payment) / math.log(1 + monthly_rate)
    months = math.ceil(months)  # Round up to the nearest month

    total_paid = monthly_payment * months
    total_interest = total_paid - amount

    years = months // 12
    remaining_months = months % 12

    # Initialize list to store monthly information
    monthly_info = []

    # Calculate monthly information
    balance = amount
    for _ in range(months):
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        balance -= principal
        monthly_info.append([round(interest, 2), round(principal, 2), round(balance, 2)])

    return years, remaining_months, round(total_paid, 2), round(total_interest, 2), monthly_info

def pretty_print_mortgage(years, months, total_paid, total_interest):
    print("Total paid: ${}".format(round(total_paid, 2)))
    print("Total interest paid: ${}".format(round(total_interest, 2)))
    print("Time to pay off: {} years, {} months".format(years, months)) 

def refinance(amount, annual_rate, updated_rate, years, state_tax_rate, insurance_rate, down_payment=0):
    state_tax_rate = float(state_tax_rate.strip('%')) / 100 
    amount -= down_payment  # Subtract the down payment from the loan amount
    monthly_rate = annual_rate / 12
    updated_monthly_rate = updated_rate / 12
    months = years * 12

    monthly_tax = amount * state_tax_rate / 12
    monthly_insurance = amount * insurance_rate / 12
    monthly_payment = (amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)) + monthly_tax + monthly_insurance

    # Initialize list to store monthly information
    monthly_info = []

    # Calculate monthly information
    balance = amount
    for _ in range(months):
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        balance -= principal
        if balance <= 0:
            break
        monthly_info.append([round(interest, 2), round(principal, 2), round(balance, 2)])

    total_interest = sum(month[0] for month in monthly_info)
    total_paid = total_interest + amount

    # Calculate the new monthly payment
    new_monthly_payment = (amount * updated_monthly_rate / (1 - (1 + updated_monthly_rate) ** -months)) + monthly_tax + monthly_insurance

    # Initialize list to store monthly information
    new_monthly_info = []

    # Calculate monthly information
    balance = amount
    for _ in range(months):
        interest = balance * updated_monthly_rate
        principal = new_monthly_payment - interest
        balance -= principal
        if balance <= 0:
            break
        new_monthly_info.append([round(interest, 2), round(principal, 2), round(balance, 2)])

    new_total_interest = sum(month[0] for month in new_monthly_info)
    new_total_paid = new_total_interest + amount

    return total_paid, new_total_paid

def prepayment_scenario(amount, annual_rate, insurance_rate, state_tax_rate, monthly_payment, down_payment=0, additional_payment=0):
    state_tax_rate = float(state_tax_rate.strip('%')) / 100 
    if str(down_payment).endswith('%'):
        down_payment = float(down_payment.strip('%')) / 100 * amount

    amount -= down_payment  # Subtract the down payment from the loan amount
    monthly_rate = annual_rate / 12

    remaining_balance = amount
    total_paid = 0
    month = 0

    monthly_payment -= amount * state_tax_rate / 12
    monthly_payment -= amount * insurance_rate / 12

    while remaining_balance > 0:
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment + additional_payment
        remaining_balance -= principal_payment
        total_paid += principal_payment + interest_payment  # Add the principal and interest to the total paid
        month += 1

    return total_paid, month

class MortgageCalculator:
    def __init__(self, amount, annual_rate, years, down_payment=0):
        if not amount or not annual_rate or not years:
            raise ValueError("Amount, annual rate, and years must not be empty")

        self.amount = float(amount)
        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0")

        if str(annual_rate).endswith('%'):
            self.annual_rate = float(annual_rate.strip('%')) / 100
        else: 
            self.annual_rate = float(annual_rate)
        if self.annual_rate <= 0:
            raise ValueError("Annual rate must be greater than 0")

        self.years = int(years)
        if self.years <= 0:
            raise ValueError("Years must be greater than 0")

        if str(down_payment).endswith('%'):
            self.down_payment = float(down_payment.strip('%')) / 100 * self.amount
        else:
            self.down_payment = float(down_payment)
        if self.down_payment < 0:
            raise ValueError("Down payment must not be negative")

    def monthly_payment(self):
        if self.amount <= 0 or self.annual_rate <= 0 or self.years <= 0 or self.down_payment < 0:
            return "Invalid input"

        self.amount -= self.down_payment  # Subtract the down payment from the loan amount

        if self.years == 0:
            return round(self.amount, 2)

        monthly_rate = self.annual_rate / 12
        months = self.years * 12

        if self.annual_rate == 0:
            return round(self.amount / months, 2)

        monthly_payment = (self.amount * monthly_rate / (1 - (1 + monthly_rate) ** -months))

        return f"${monthly_payment:,.2f}"
    
    def total_cost(self, state_tax_rate, insurance_rate):
        state_tax_rate = float(state_tax_rate.strip('%')) / 100 
        insurance_rate = float(insurance_rate.strip('%')) / 100 

        self.amount -= self.down_payment  # Subtract the down payment from the loan amount
        monthly_rate = self.annual_rate / 12
        months = self.years * 12

        monthly_tax = self.amount * state_tax_rate / 12
        monthly_insurance = self.amount * insurance_rate / 12
        monthly_payment = self.amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)
        total_monthly_payment = monthly_payment + monthly_tax + monthly_insurance

        # Initialize variables to store total amounts
        total_interest = 0
        total_principal = 0
        total_tax = 0
        total_insurance = 0

        # Calculate monthly information
        balance = self.amount
        for _ in range(months):
            interest = balance * monthly_rate
            principal = total_monthly_payment - interest - monthly_tax - monthly_insurance
            balance -= principal
            total_interest += interest
            total_principal += principal
            total_tax += monthly_tax
            total_insurance += monthly_insurance
            if balance <= 0:
                break

        total_cost = total_principal + total_interest + total_tax + total_insurance + self.down_payment
        breakdown = {'principal': f"{total_principal:,.2f}", 'interest': f"{total_interest:,.2f}", 'tax': f"{total_tax:,.2f}", 'insurance': f"{total_insurance:,.2f}", 'down_payment': f"{self.down_payment:,.2f}"}

        return f"{total_cost:,.2f}", breakdown