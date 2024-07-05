import requests
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

def insert_data(city, timestamp, aqi):
    connection = get_connection()
    cursor = connection.cursor()
    insert_statement = f"""
        INSERT INTO de10_kk_project.air_quality (city, timestamp, aqi)
        VALUES ('{city}', '{timestamp}', {aqi});
    """
    cursor.execute(insert_statement)
    connection.commit()
    cursor.close()
    connection.close()

cities = [
    "Beijing", "Delhi", "New York", "London", "Tokyo",
    "Los Angeles", "Paris", "Berlin", "Moscow", "Sydney",
    "Mexico City", "Rio de Janeiro", "Cairo", "Mumbai",
    "Bangkok", "Jakarta", "Seoul", "Hong Kong", "Dubai",
    "Singapore", "Nairobi", "Cape Town", "Lagos", "Accra",
    "Addis Ababa", "Johannesburg", "Casablanca", "Dakar",
    "Abidjan", "Dar es Salaam"
]

token = "16e95c6c33eef01951b60b4f2c3ab37da1720e0e"  # Replace with your WAQI API token

for city in cities:
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    response = requests.get(url).json()

    if 'data' in response and 'aqi' in response['data']:
        aqi = response['data']['aqi']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_data(city, timestamp, aqi)

