from flask import Flask, render_template, request
from investments import MortgageCalculator
from mortgage_helper import MortgageAmortization
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import NumeralTickFormatter
from bokeh.embed import components
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.models.tools import HoverTool
import pandas as pd
from pandas.tseries.offsets import DateOffset

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/monthly_mortgage', methods=['GET', 'POST'])
def monthly_mortgage():
    form_data = {'amount': '', 'annual_rate': '', 'years': '', 'down_payment': ''}
    result = None
    if request.method == 'POST':
        try:
            # Get data from form
            form_data['amount'] = request.form.get('amount')
            form_data['annual_rate'] = request.form.get('annual_rate')
            form_data['years'] = request.form.get('years')
            form_data['down_payment'] = request.form.get('down_payment')

            # Create an instance of your class and call your method
            instance = MortgageCalculator(form_data['amount'], form_data['annual_rate'], form_data['years'], form_data['down_payment'])
            result = instance.monthly_payment()
        except ValueError:
            result = "Invalid input"

    # Render the form
    return render_template('monthly_payment.html', form_data=form_data, result=result)

@app.route('/amortization_schedule', methods=['GET', 'POST'])
def amortization_schedule():
    form_data = {'amount': '', 'annual_rate': '', 'years': '', 'down_payment': '', 'state_tax_rate': '', 'insurance_rate': ''}
    amortization_schedule, plot_script, plot_div = None, None, None

    if request.method == 'POST':
        try:
            # Get data from form
            form_data['loan_amount_input'] = request.form.get('loan_amount_input')
            form_data['interest_rate_input'] = request.form.get('interest_rate_input')
            form_data['loan_term_input'] = request.form.get('loan_term_input')
            form_data['down_payment_input'] = request.form.get('down_payment_input')
            form_data['tax_rate_input'] = request.form.get('tax_rate_input')
            form_data['insurance_rate_input'] = request.form.get('insurance_rate_input')
            form_data['start_date_input'] = request.form.get('start_date_input')

            # Create an instance of your class and call your method
            instance = MortgageAmortization(form_data['loan_amount_input'], form_data['interest_rate_input'], form_data['loan_term_input'], form_data['tax_rate_input'], form_data['insurance_rate_input'], form_data['down_payment_input'], form_data['start_date_input'])
            amortization_schedule = instance.amortization_schedule()

            start_date = pd.to_datetime(form_data['start_date_input'])
            amortization_schedule['Month'] = [start_date + DateOffset(months=i) for i in amortization_schedule.index]

            source = ColumnDataSource(amortization_schedule)

            p = figure(x_axis_type='datetime', x_range=(start_date, start_date + DateOffset(months=amortization_schedule.shape[0])), plot_width=800, plot_height=500, title='Amortization Schedule')
            line1 = p.line('Month', 'Cumulative Principal', source=source, color='blue', legend_label='Cumulative Principal', line_width=2)
            line2 = p.line('Month', 'Cumulative Interest', source=source, color='green', legend_label='Cumulative Interest', line_width=2)
            p.line('Month', 'Balance', source=source, color='red', legend_label='Remaining Balance', line_width=2)
            p.yaxis.formatter = NumeralTickFormatter(format="$0,0")

            invisible_line = p.line('Month', 'Balance', source=source, color='red', alpha=0)
            p.add_tools(HoverTool(renderers=[invisible_line, line1, line2], 
                                  tooltips=[
                                      ('Month', '@Month{%F}'), 
                                      ('Remaining Balance', '$@Balance{0,0}'), 
                                      ('Total Principal', '$@{Cumulative Principal}{0,0}'),
                                      ('Total Interest', '$@{Cumulative Interest}{0,0}')
                                      ], 
                                      formatters={'@Month': 'datetime'}, 
                                      mode='vline'))
            
            plot_script, plot_div = components(p)
            
        except ValueError:
            amortization_schedule = "Invalid input"

    # Render the results in a template
    return render_template('amortization_schedule.html', form_data=form_data, amortization_schedule=amortization_schedule, plot_script=plot_script, plot_div=plot_div)

@app.route('/total_cost', methods=['GET', 'POST'])
def total_cost():
    form_data = {'amount': '', 'annual_rate': '', 'years': '', 'down_payment': '', 'state_tax_rate': '', 'insurance_rate': ''}
    total_cost = None
    breakdown = None
    if request.method == 'POST':
        try:
            # Get data from form
            form_data['amount'] = request.form.get('amount')
            form_data['annual_rate'] = request.form.get('annual_rate')
            form_data['years'] = request.form.get('years')
            form_data['down_payment'] = request.form.get('down_payment')
            form_data['state_tax_rate'] = request.form.get('state_tax_rate')
            form_data['insurance_rate'] = request.form.get('insurance_rate')

            # Create an instance of your class and call your method
            instance = MortgageCalculator(form_data['amount'], form_data['annual_rate'], form_data['years'], form_data['down_payment'])
            total_cost, breakdown = instance.total_cost(form_data['state_tax_rate'], form_data['insurance_rate'])
        except ValueError:
            total_cost = "Invalid input"

    # Render the form
    return render_template('total_mortgage.html', form_data=form_data, total_cost=total_cost, breakdown=breakdown)

if __name__ == '__main__':
    app.run(debug=True)