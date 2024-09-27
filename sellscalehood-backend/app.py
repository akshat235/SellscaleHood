from flask import Flask
from models import db
from scheduler import start_scheduler
from auth import auth_blueprint
from stock import stock_blueprint
from portfolio import portfolio_blueprint
from routes import routes_blueprint

app = Flask(__name__)

# Set app configuration
app.config['SECRET_KEY'] = 'sellscale@akshat235'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(stock_blueprint, url_prefix='/stock')
app.register_blueprint(portfolio_blueprint, url_prefix='/portfolio')
app.register_blueprint(routes_blueprint, url_prefix='/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
        start_scheduler()  # Start scheduler
    app.run(debug=True)
