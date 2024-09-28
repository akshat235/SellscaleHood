from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Portfolio, ScheduledOrder
from utils import get_user_id_from_token
import yfinance as yf

portfolio_blueprint = Blueprint('portfolio', __name__)

#View portfolio
@portfolio_blueprint.route('/portfolio', methods=['GET'])
def view_portfolio():
    try:
        user_id = get_user_id_from_token()
        portfolio = Portfolio.query.filter_by(user_id=user_id).all()
        return jsonify([entry.to_dict() for entry in portfolio]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Portfolio stats
@portfolio_blueprint.route('/portfolio_stats', methods=['GET'])
def portfolio_stats():
    try:
        user_id = get_user_id_from_token()
        portfolio = Portfolio.query.filter_by(user_id=user_id).all()
        total_invested = sum([
            entry.quantity * yf.Ticker(entry.ticker).history(period='1d')['Close'].iloc[-1]
            for entry in portfolio
        ])
        current_value = sum([
            entry.quantity * yf.Ticker(entry.ticker).fast_info['lastPrice']
            for entry in portfolio
        ])
        return jsonify({
            'total_invested': total_invested,
            'current_value': current_value,
            'profit_loss': current_value - total_invested
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Transaction history
@portfolio_blueprint.route('/transaction_history', methods=['GET'])
def transaction_history():
    try:
        user_id = get_user_id_from_token()
        history = Portfolio.query.filter_by(user_id=user_id).all()
        return jsonify([entry.to_dict() for entry in history]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Schedule an order
@portfolio_blueprint.route('/schedule_order', methods=['POST'])
def schedule_order():
    try:
        user_id = get_user_id_from_token()
        data = request.get_json()
        ticker = data.get('ticker')
        quantity = data.get('quantity')
        action = data.get('action') 
        execution_time = data.get('execution_time')  

        scheduled_order = ScheduledOrder(
            user_id=user_id,
            ticker=ticker,
            quantity=quantity,
            action=action,
            execution_time=datetime.strptime(execution_time, '%Y-%m-%d %H:%M:%S')
        )
        db.session.add(scheduled_order)
        db.session.commit()

        return jsonify({'message': 'Order scheduled successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# View scheduled orders
@portfolio_blueprint.route('/scheduled_orders', methods=['GET'])
def view_scheduled_orders():
    try:
        user_id = get_user_id_from_token()
        orders = ScheduledOrder.query.filter_by(user_id=user_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
