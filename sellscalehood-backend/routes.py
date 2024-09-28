from flask import Blueprint, request, jsonify
from models import db, Watchlist, Favorite
from utils import get_user_id_from_token

routes_blueprint = Blueprint('routes', __name__)

# Add a stock to watchlist
@routes_blueprint.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    try:
        user_id = get_user_id_from_token()
        data = request.get_json()
        ticker = data.get('ticker')

        watchlist_entry = Watchlist(user_id=user_id, ticker=ticker)
        db.session.add(watchlist_entry)
        db.session.commit()

        return jsonify({'message': 'Stock added to watchlist'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500    

# View watchlist of the user
@routes_blueprint.route('/watchlist', methods=['GET'])
def view_watchlist():
    try:
        user_id = get_user_id_from_token()
        watchlist = Watchlist.query.filter_by(user_id=user_id).all()
        return jsonify([entry.to_dict() for entry in watchlist]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Mark favorite stock
@routes_blueprint.route('/favorite_stock', methods=['POST'])
def favorite_stock():
    try:
        user_id = get_user_id_from_token()
        data = request.get_json()
        ticker = data.get('ticker')

        favorite_entry = Favorite(user_id=user_id, ticker=ticker)
        db.session.add(favorite_entry)
        db.session.commit()

        return jsonify({'message': 'Stock marked as favorite'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#View favorite stocks of the user
@routes_blueprint.route('/favorites', methods=['GET'])
def view_favorites():
    try:
        user_id = get_user_id_from_token()
        favorites = Favorite.query.filter_by(user_id=user_id).all()

        return jsonify([entry.to_dict() for entry in favorites]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
