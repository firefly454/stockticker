# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
import sqlite3
import requests
import numpy as np
from bokeh.plotting import figure, show, output_file, vplot
from bokeh.embed import components
import pandas as pd

# create the application object
app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def home():
    errors = []
    if request.method == "GET":
        return render_template('enter_stock.html')
    else:
        symbol = request.form['symbol']
        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=8L5MpAx2n-9x-tTp5jw4' %symbol
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)
        #r = requests.get(api_url)
        data = raw_data.json()
        df = pd.DataFrame(data['data'])
        df.columns = data['column_names']

        def datetime(x):
            return np.array(x, dtype=np.datetime64)

        p1 = figure(x_axis_type = "datetime")
        p1.title = "Data from Quandl WIKI set"
        p1.grid.grid_line_alpha=0.3
        p1.xaxis.axis_label = 'Date'
        p1.yaxis.axis_label = 'Price'
        #p1.line(datetime(df['Date']), df['Open'], color='#A6CEE3', legend='open')
        if 'open' in request.form:
            p1.line(datetime(df['Date']), df['Open'], color='red', legend='open')
        if 'adjopen' in request.form:
            p1.line(datetime(df['Date']), df['Adj. Open'], color='green', legend='adj. open')
        if 'close' in request.form:
            p1.line(datetime(df['Date']), df['Close'], color='blue', legend='close')
        if 'adjclose' in request.form:
            p1.line(datetime(df['Date']), df['Adj. Close'], color='black', legend='adj. close')
        script, div = components(p1)  
        return render_template('graph.html', symbol=symbol, script=script, div=div)
     
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)