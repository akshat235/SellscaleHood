from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
from models import db, ScheduledOrder, Portfolio  # Import models
import yfinance as yf

# This function will be executed periodically by the scheduler
def execute_scheduled_orders():
    from app import app  

    with app.app_context():  
        now = datetime.now(timezone.utc)

        # Fetch pending scheduled orders 
        pending_orders = ScheduledOrder.query.filter(
            ScheduledOrder.execution_time <= now,
            ScheduledOrder.status == 'pending'
        ).all()

        for order in pending_orders:
            stock = yf.Ticker(order.ticker)
            current_price = stock.info['regularMarketPrice']

            # Execute the buy action if the price is less than or equal to the target
            if order.action == 'buy' and current_price <= order.target_price:
                portfolio_entry = Portfolio(
                    user_id=order.user_id,
                    ticker=order.ticker,
                    quantity=order.quantity,
                    action='buy'
                )
                db.session.add(portfolio_entry)
                order.status = 'executed'
            
            # Execute the sell action if the price is greater than or equal to the target
            elif order.action == 'sell' and current_price >= order.target_price:
                portfolio_entry = Portfolio(
                    user_id=order.user_id,
                    ticker=order.ticker,
                    quantity=order.quantity,
                    action='sell'
                )
                db.session.add(portfolio_entry)
                order.status = 'executed'

            # Commit the changes to the database
            db.session.commit()


# Function to start the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()

    # Add the job to be executed every 60 seconds
    scheduler.add_job(func=execute_scheduled_orders, trigger="interval", seconds=60)  # Runs every 60 seconds

    scheduler.start()  # Start the scheduler
