from flask import Flask, jsonify, request, Response
from kafka import KafkaConsumer
import pandas as pd
import json
import six
import sys
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

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
