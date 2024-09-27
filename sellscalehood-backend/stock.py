from flask import Blueprint, request, jsonify
import yfinance as yf
from utils import get_user_id_from_token
from models import db, Portfolio

stock_blueprint = Blueprint('stock', __name__)

#Query stock information
@stock_blueprint.route('/query_stock', methods=['GET'])
def query_stock():
    try:
        ticker = request.args.get('ticker')
        if not ticker:
            return jsonify({'error': 'Ticker symbol is required'}), 400

        stock = yf.Ticker(ticker)
        stock_info = stock.info
        return jsonify(stock_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Buy stock
@stock_blueprint.route('/buy_stock', methods=['POST'])
def buy_stock():
    try:
        user_id = get_user_id_from_token()
        data = request.get_json()
        ticker = data.get('ticker')
        quantity = data.get('quantity')

        if not ticker or not quantity:
            return jsonify({'error': 'Ticker and quantity are required'}), 400

        portfolio_entry = Portfolio(user_id=user_id, ticker=ticker, quantity=quantity, action='buy')
        db.session.add(portfolio_entry)
        db.session.commit()

        return jsonify({'message': 'Stock bought successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#Sell stock
@stock_blueprint.route('/sell_stock', methods=['POST'])
def sell_stock():
    try:
        user_id = get_user_id_from_token()
        data = request.get_json()
        ticker = data.get('ticker')
        quantity = data.get('quantity')

        if not ticker or not quantity:
            return jsonify({'error': 'Ticker and quantity are required'}), 400

        portfolio_entry = Portfolio(user_id=user_id, ticker=ticker, quantity=quantity, action='sell')
        db.session.add(portfolio_entry)
        db.session.commit()

        return jsonify({'message': 'Stock sold successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Stock history
@stock_blueprint.route('/stock_history', methods=['GET'])
def stock_history():
    try:
        ticker = request.args.get('ticker')
        period = request.args.get('period', '1mo')  
        interval = request.args.get('interval', '1d')
        stock = yf.Ticker(ticker)
        history = stock.history(period=period, interval=interval)
        history = history.reset_index()
        history['Date'] = history['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        data = history.to_dict(orient='records')

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Market summary
@stock_blueprint.route('/market_summary', methods=['GET'])
def market_summary():
    try:
        sp500 = yf.Ticker('^GSPC').info
        nasdaq = yf.Ticker('^IXIC').info
        dowjones = yf.Ticker('^DJI').info

        return jsonify({
            'sp500': sp500,
            'nasdaq': nasdaq,
            'dowjones': dowjones
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
