from flask import Flask, request, jsonify
import data

app = Flask(__name__)
SQLITE_URI = 'sqlite:///data/flights.sqlite3'
data_manager = data.FlightData(SQLITE_URI)


def convert_row_to_dict(row):
    return dict(row)


@app.route('/')
def home():
    return "Welcome to the Flights API!"


@app.route('/flight/<int:flight_id>', methods=['GET'])
def get_flight_by_id(flight_id):
    result = data_manager.get_flight_by_id(flight_id)
    result_dict = [convert_row_to_dict(row) for row in result]
    return jsonify(result_dict)


@app.route('/flights/date', methods=['GET'])
def get_flights_by_date():
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')
    if not all([day, month, year]):
        return jsonify({"error": "Missing required query parameters: day, month, year"}), 400
    result = data_manager.get_flights_by_date(int(day), int(month), int(year))
    result_dict = [convert_row_to_dict(row) for row in result]
    return jsonify(result_dict)


@app.route('/delayed_flights/airline', methods=['GET'])
def get_delayed_flights_by_airline():
    airline = request.args.get('airline')
    if not airline:
        return jsonify({"error": "Missing required query parameter: airline"}), 400
    result = data_manager.get_delayed_flights_by_airline(airline)
    result_dict = [convert_row_to_dict(row) for row in result]
    return jsonify(result_dict)


@app.route('/delayed_flights/airport', methods=['GET'])
def get_delayed_flights_by_airport():
    airport = request.args.get('airport')
    if not airport:
        return jsonify({"error": "Missing required query parameter: airport"}), 400
    result = data_manager.get_delayed_flights_by_airport(airport)
    result_dict = [convert_row_to_dict(row) for row in result]
    return jsonify(result_dict)


if __name__ == '__main__':
    app.run(port=5001, debug=True)