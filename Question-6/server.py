from flask import Flask, jsonify, request, Response
import pandas as pd
import json


app = Flask(__name__)

# Load cleaned data (e.g., CSV file or from a database)
cleaned_data = pd.read_csv("weather.csv")

# Endpoint to serve cleaned weather data with optional filters
@app.route('/api/weather', methods=['GET'])
def get_cleaned_data():
    region = request.args.get('location')
    date = request.args.get('last_time')
    data = cleaned_data.copy()
    return jsonify(data.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)
