# Stock Analysis API

This project is a RESTful API for retrieving and analyzing stock data using Flask. The API fetches daily and weekly stock data from the Alpha Vantage API, calculates moving averages and volatility, and provides these metrics in a JSON format.

## Features
- **Retrieve stock data**: Fetch daily and weekly stock data for a given symbol.
- **Calculate moving averages**: Compute 10-day, 50-day, 10-week, and 50-week moving averages.
- **Calculate volatility**: Compute daily return volatility.
- **Cross-Origin Resource Sharing (CORS)**: Enable interaction with the API from different domains.

## Endpoints
### Get Stock Data
- **URL**: `/stock/<symbol>`
- **Method**: `GET`
- **Response**: JSON object with the latest daily and weekly stock data, moving averages, and volatility.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/waqi786/stock-analysis-api.git
   cd stock-analysis-api

2. Create and activate a virtual environment:
   
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required dependencies:

   pip install -r requirements.txt

4. Set up your Alpha Vantage API key:
Replace your_api_key in the API_KEY variable with your Alpha Vantage API key.

5. Run the application:

   flask run

**Dependencies**:

Flask
Flask-CORS
requests
pandas

Install the dependencies using the command:

   pip install flask flask-cors requests pandas

**Usage**

Example Request to Get Stock Data

    curl -X GET http://127.0.0.1:5000/stock/AAPL

**Contribution**

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

Developed by Waqar Ali.


### Short Description

A Flask-based RESTful API to fetch and analyze stock data, calculating moving averages and volatility using data from Alpha Vantage.

**Uploaded Date:**

7/28/2024
