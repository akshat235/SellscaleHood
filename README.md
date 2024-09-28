### 2. **Backend `README.md`**

This will focus on setting up and running the Flask-based backend of the project.

```markdown
# SellScaleHood Backend

This is the backend of **SellScaleHood**, a stock trading web application powered by **Flask** with **PostgreSQL** or **MySQL** as the database.

## Tech Stack

- **Flask** (Python web framework)
- **SQLAlchemy** (ORM for database management)
- **YFinance API** (For stock data querying)
- **SQLlite** (Database)

## Prerequisites

- **Python** (v3.x)
- **PostgreSQL** or **MySQL** (for database)
- **pip** (Python package installer)

## Setup

1. Clone the backend repository:

    ```bash
    git clone https://github.com/akshat235/sellscalehood.git
    cd sellscalehood-backend
    ```

2. Create a Python virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
   - For **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - For **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    !!! Check for any additional requirements and isntall them using pip.

5.  using terminal cd into the project adn run 
    ```bash
    python app.py
    ```

   The backend server will be running at `http://127.0.0.1:5000`.



## Available Scripts

- `flask run`: Start the Flask development server.
- `flask db upgrade`: Apply the latest database migrations.
- `pytest`: Run tests for the backend.


