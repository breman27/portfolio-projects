from datetime import date
import pandas as pd

class MortgageAmortization:
    def __init__(self, amount, annual_rate, years, state_tax_rate, insurance_rate, down_payment=0, start_date=date(2020, 1, 1)):
        self.amount = float(amount) - float(down_payment)
        if str(annual_rate).endswith('%'):
            self.annual_rate = float(annual_rate.strip('%')) / 100
        else: 
            self.annual_rate = float(annual_rate)
        if self.annual_rate <= 0:
            raise ValueError("Annual rate must be greater than 0")
        self.years = int(years)
        if str(state_tax_rate).endswith('%'):
            self.state_tax_rate = float(state_tax_rate.strip('%')) / 100
        else:
            self.state_tax_rate = float(state_tax_rate)
        if str(insurance_rate).endswith('%'):
            self.insurance_rate = float(insurance_rate.strip('%')) / 100
        else:
            self.insurance_rate = float(insurance_rate)
        if str(down_payment).endswith('%'):
            self.down_payment = float(down_payment.strip('%')) / 100 * self.amount
        else:
            self.down_payment = float(down_payment)
        self.monthly_rate = self.annual_rate / 12
        self.months = self.years * 12
        self.monthly_tax = self.amount * self.state_tax_rate / 12
        self.monthly_insurance = self.amount * self.insurance_rate / 12
        self.principal_and_interest_amount = self.amount - self.monthly_tax - self.monthly_insurance
        self.monthly_payment = (self.principal_and_interest_amount * self.monthly_rate / (1 - (1 + self.monthly_rate) ** -self.months)) + self.monthly_tax + self.monthly_insurance
        self.start_date = start_date

    def amortization_schedule(self):
        # Initialize list to store monthly information
        monthly_info = []

        # Calculate monthly information
        balance = self.amount
        for _ in range(self.months):
            interest = balance * self.monthly_rate
            principal = self.monthly_payment - interest - self.monthly_tax - self.monthly_insurance
            balance -= principal
            if balance < 0:
                principal += balance
                balance = 0
            monthly_info.append([round(interest, 2), round(principal, 2), round(balance, 2)])

        df = pd.DataFrame(monthly_info, columns=['Interest', 'Principal', 'Balance'])

        df['Cumulative Principal'] = df['Principal'].cumsum()
        df['Cumulative Interest'] = df['Interest'].cumsum()

        return df