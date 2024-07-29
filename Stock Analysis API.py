from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import pandas as pd

app = Flask(__name__)
CORS(app)

API_KEY = 'your_api_key'  # Replace with your Alpha Vantage API key
BASE_URL = 'https://www.alphavantage.co/query'

@app.route('/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    daily_params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': API_KEY
    }

    weekly_params = {
        'function': 'TIME_SERIES_WEEKLY',
        'symbol': symbol,
        'apikey': API_KEY
    }

    try:
        daily_response = requests.get(BASE_URL, params=daily_params)
        weekly_response = requests.get(BASE_URL, params=weekly_params)

        if daily_response.status_code != 200:
            return jsonify({'error': f'Daily API Error: {daily_response.status_code}'}), 500
        if weekly_response.status_code != 200:
            return jsonify({'error': f'Weekly API Error: {weekly_response.status_code}'}), 500

        daily_data = daily_response.json()
        weekly_data = weekly_response.json()

        if 'Time Series (Daily)' in daily_data:
            daily_ts_data = daily_data['Time Series (Daily)']
            df_daily = pd.DataFrame(daily_ts_data).T  # Transpose to have dates as index
            df_daily.index = pd.to_datetime(df_daily.index)  # Convert index to datetime

            df_daily['10-day Moving Avg'] = df_daily['4. close'].rolling(window=10).mean()
            df_daily['50-day Moving Avg'] = df_daily['4. close'].rolling(window=50).mean()

            df_daily['Daily Return'] = df_daily['4. close'].astype(float).pct_change()
            volatility = df_daily['Daily Return'].std()

            latest_daily = df_daily.iloc[0].to_dict()

        else:
            return jsonify({'error': 'Daily Data not found for symbol'}), 404

        if 'Weekly Time Series' in weekly_data:
            weekly_ts_data = weekly_data['Weekly Time Series']
            df_weekly = pd.DataFrame(weekly_ts_data).T  # Transpose to have dates as index
            df_weekly.index = pd.to_datetime(df_weekly.index)  # Convert index to datetime

            df_weekly['10-week Moving Avg'] = df_weekly['4. close'].rolling(window=10).mean()
            df_weekly['50-week Moving Avg'] = df_weekly['4. close'].rolling(window=50).mean()

            latest_weekly = df_weekly.iloc[0].to_dict()

        else:
            return jsonify({'error': 'Weekly Data not found for symbol'}), 404

        return jsonify({
            'symbol': symbol,
            'daily_data': {
                'latest': latest_daily,
                'moving_averages': {
                    '10-day': df_daily['10-day Moving Avg'].tolist(),
                    '50-day': df_daily['50-day Moving Avg'].tolist()
                },
                'volatility': volatility
            },
            'weekly_data': {
                'latest': latest_weekly,
                'moving_averages': {
                    '10-week': df_weekly['10-week Moving Avg'].tolist(),
                    '50-week': df_weekly['50-week Moving Avg'].tolist()
                }
            }
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
