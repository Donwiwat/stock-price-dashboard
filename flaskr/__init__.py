import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
import pandas as pd

from flaskr.utils.tickerHandler import get_ticker
from flaskr.utils.apiHandler import retrieve_financials, retrieve_balance_sheet, retrieve_cashflow


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/')
    def index():
        tickers =sorted(list(get_ticker()))
        return render_template('index.html', tickers=tickers)

    # a simple page that says hello
    @app.route('/ticker_list')
    def ticker_list():
        ticker_data = get_ticker()
        return  jsonify(list(ticker_data))
    
    @app.route('/ticker_redirect')
    def ticker_redirect():
        selected = request.args.get('ticker')
        return redirect(url_for('ticker_detail', symbol=selected))
    
    @app.route('/search_tickers')
    def search_tickers():
        query = request.args.get('q', '').upper()
        matches = [ticker for ticker in get_ticker() if query in ticker]
        return jsonify(matches)
    
    @app.route('/ticker/<symbol>')
    def ticker_detail(symbol):
        data = retreive_financials(symbol)
        if data.empty:
            return jsonify({"error": "No data found"}), 404
        
        table_html = data.to_html(classes="table table-bordered", border=0)
        return render_template('ticker_detail.html', symbol=symbol, table_html=table_html)
    
    
    @app.route('/api/ticker_data/<symbol>/<data_type>')
    def api_ticker_data(symbol, data_type):
        print(f"Fetching data for {symbol} with data type {data_type}")
        df = None
        if data_type == "financials":
            df = retrieve_financials(symbol)  
        elif data_type == "balance_sheet":
            df = retrieve_balance_sheet(symbol) 
        elif data_type == "cashflow":
            df = retrieve_cashflow(symbol)  
        
        if df is None or df.empty:
            return "No data found", 404
        
        # คืนค่าผลลัพธ์ในรูปแบบ HTML (table)
        return df.to_html(classes="table table-bordered", border=0)
    
    return app