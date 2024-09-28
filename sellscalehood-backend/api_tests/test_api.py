import requests

# Define the base URL of the API
BASE_URL = "http://127.0.0.1:5000"

# Utility function to print the response neatly
def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except ValueError:
        print("No JSON response or invalid JSON format.")
    print("-" * 50)

# Test 1: Register a new user
def test_register_user(username, password):
    url = f"{BASE_URL}/auth/register"  # /auth/register
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    print("Test: Register User")
    print_response(response)

# Test 2: Log in a user
def test_login_user(username, password):
    url = f"{BASE_URL}/auth/login"  # /auth/login
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    print("Test: Log In User")
    print_response(response)
    if response.status_code == 200:
        return response.json().get("token")  # Return the JWT token if login is successful
    return None

# Test 3: Buy stock (updated URL prefix for stock)
def test_buy_stock(token, ticker, quantity):
    url = f"{BASE_URL}/stock/buy_stock"  # Now in stock blueprint
    headers = {"Authorization": f"Bearer {token}"}
    data = {"ticker": ticker, "quantity": quantity}
    response = requests.post(url, json=data, headers=headers)
    print("Test: Buy Stock")
    print_response(response)

# Test 4: View portfolio (moved to portfolio blueprint)
def test_view_portfolio(token):
    url = f"{BASE_URL}/portfolio/portfolio"  # Now in portfolio blueprint
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Test: View Portfolio")
    print_response(response)

# Test 5: Sell stock (updated URL prefix for stock)
def test_sell_stock(token, ticker, quantity):
    url = f"{BASE_URL}/stock/sell_stock"  # Now in stock blueprint
    headers = {"Authorization": f"Bearer {token}"}
    data = {"ticker": ticker, "quantity": quantity}
    response = requests.post(url, json=data, headers=headers)
    print("Test: Sell Stock")
    print_response(response)

# Test 6: Add to watchlist (moved to routes)
def test_add_to_watchlist(token, ticker):
    url = f"{BASE_URL}/add_to_watchlist"  # Still in main routes
    headers = {"Authorization": f"Bearer {token}"}
    data = {"ticker": ticker}
    response = requests.post(url, json=data, headers=headers)
    print("Test: Add to Watchlist")
    print_response(response)

# Test 7: View watchlist (moved to routes)
def test_view_watchlist(token):
    url = f"{BASE_URL}/watchlist"  # Still in main routes
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Test: View Watchlist")
    print_response(response)

# Test 8: Schedule an order (moved to portfolio blueprint)
def test_schedule_order(token, ticker, quantity, action, execution_time):
    url = f"{BASE_URL}/portfolio/schedule_order"  # Now in portfolio blueprint
    headers = {"Authorization": f"Bearer {token}"}
    data = {"ticker": ticker, "quantity": quantity, "action": action, "execution_time": execution_time}
    response = requests.post(url, json=data, headers=headers)
    print("Test: Schedule Order")
    print_response(response)

# Test 9: View scheduled orders (moved to portfolio blueprint)
def test_view_scheduled_orders(token):
    url = f"{BASE_URL}/portfolio/scheduled_orders"  # Now in portfolio blueprint
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Test: View Scheduled Orders")
    print_response(response)

# Additional Tests
def test_query_stock(token, ticker):
    url = f"{BASE_URL}/stock/query_stock"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"ticker": ticker}
    response = requests.get(url, headers=headers, params=params)
    print("Test: Query Stock Information")
    print_response(response)

def test_stock_history(token, ticker, period='1mo', interval='1d'):
    url = f"{BASE_URL}/stock/stock_history"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"ticker": ticker, "period": period, "interval": interval}
    response = requests.get(url, headers=headers, params=params)
    print("Test: View Stock History")
    print_response(response)

def test_favorite_stock(token, ticker):
    url = f"{BASE_URL}/favorite_stock"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"ticker": ticker}
    response = requests.post(url, json=data, headers=headers)
    print("Test: Mark Stock as Favorite")
    print_response(response)

def test_view_favorites(token):
    url = f"{BASE_URL}/favorites"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Test: View Favorites")
    print_response(response)

def test_market_summary(token):
    url = f"{BASE_URL}/stock/market_summary"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Test: Market Summary")
    print_response(response)

def test_portfolio_stats(token):
    url = f"{BASE_URL}/portfolio/portfolio_stats"  # Now in portfolio blueprint
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Test: Portfolio Stats")
    print_response(response)

def test_transaction_history(token):
    url = f"{BASE_URL}/portfolio/transaction_history"  # Now in portfolio blueprint
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Test: Transaction History")
    print_response(response)


# Execute tests
if __name__ == "__main__":
    # Test credentials
    username = "testuser1"
    password = "testpass1"
    execution_time = "2024-09-28 10:00:00"

    # Test user registration
    test_register_user(username, password)

    # Test user login and get the JWT token
    token = test_login_user(username, password)
    if token:
        # Existing tests...
        test_buy_stock(token, "AAPL", 10)
        test_view_portfolio(token)
        test_sell_stock(token, "AAPL", 5)
        test_add_to_watchlist(token, "AAPL")
        test_view_watchlist(token)
        test_schedule_order(token, "AAPL", 10, "buy", execution_time)
        test_view_scheduled_orders(token)
        test_query_stock(token, "AAPL")
        test_stock_history(token, "AAPL")
        test_favorite_stock(token, "AAPL")
        test_view_favorites(token)
        test_market_summary(token)
        test_portfolio_stats(token)
        test_transaction_history(token)
    else:
        print("Failed to log in; tests for authenticated routes cannot be run.")
