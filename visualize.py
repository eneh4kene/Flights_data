import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text

# Database connection
SQLITE_URI = 'sqlite:///data/flights.sqlite3'
engine = create_engine(SQLITE_URI)


def percentage_delayed_flights_per_airline():
    query = '''
    SELECT airlines.airline AS Airline, 
           COUNT(CASE WHEN flights.departure_delay >= 20 THEN 1 END) * 1.0 / COUNT(*) * 100 AS DelayedPercentage
    FROM flights
    JOIN airlines ON flights.airline = airlines.id
    GROUP BY airlines.airline
    ORDER BY DelayedPercentage DESC;
    '''
    with engine.connect() as connection:
        result = connection.execute(text(query))
        data = result.fetchall()
        df = pd.DataFrame(data, columns=['Airline', 'DelayedPercentage'])

    plt.figure(figsize=(12, 8))
    sns.barplot(x='DelayedPercentage', y='Airline', data=df, palette='viridis')
    plt.title('Percentage of Delayed Flights per Airline')
    plt.xlabel('Percentage of Delayed Flights')
    plt.ylabel('Airline')
    plt.show()

# Add more functions for other visualizations as needed
