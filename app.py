from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import requests
from datetime import datetime  # Import datetime for timestamp

app = Flask(__name__)
CORS(app, resources={r"/track": {"origins": "*"}})  # Explicitly allow all origins for /track route

# MySQL database connection parameters
db_config = {
    "host": "localhost",  # Replace with your MySQL host
    "user": "root",       # Replace with your MySQL user
    "password": "",       # Replace with your MySQL password
    "database": "crm"     # Corrected to your database name
}

# Connect to MySQL database
# def get_db_connection():
#     conn = mysql.connector.connect(**db_config)
#     return conn

# Function to get country and city from IP
@app.route('/')
def get_location():
    try:
        ip_address= request.remote_addr 
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        return data.get("country", "Unknown")
    except Exception as e:
        print(f"Error fetching location: {e}")
        return "Unknown"

# Insert a new row for each tracking event
# def insert_user_tracking(
#     user_id, time_spent, session_duration, event, user_agent, referrer,
#     ip_address, clicks, submissions, scrolls, video_plays, hovers,
#     country, city, screen_resolution, scroll_depth, session_id,
#     timestamp, page_url, device_type, operating_system,
#     browser_info, referring_domain, utm_source, utm_medium,
#     utm_campaign, click_path, error_logs
# ):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Insert new tracking record into user_tracking_2
#     cursor.execute('''
#         INSERT INTO user_tracking_2 (
#             user_id, time_spent, session_duration, event, ip_address,
#             referrer, user_agent, clicks, submissions, scrolls,
#             video_plays, hovers, country, city, screen_resolution,
#             scroll_depth, session_id, timestamp, page_url,
#             device_type, operating_system, browser_info,
#             referring_domain, utm_source, utm_medium,
#             utm_campaign, click_path, error_logs
#         )
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     ''', (
#         user_id, time_spent, session_duration, event, ip_address,
#         referrer, user_agent, clicks, submissions, scrolls,
#         video_plays, hovers, country, city, screen_resolution,
#         scroll_depth, session_id, timestamp, page_url,
#         device_type, operating_system, browser_info,
#         referring_domain, utm_source, utm_medium,
#         utm_campaign, click_path, error_logs
#     ))

#     conn.commit()
#     cursor.close()
#     conn.close()

# Function to track user activity and additional data points
# @app.route('/track', methods=['POST'])
# def track_visitor():
#     # Check for correct content type
#     if request.content_type != 'application/json':
#         return jsonify({"status": "error", "message": "Invalid content type. Expected application/json"}), 415

#     data = request.get_json()

#     if data is None:
#         return jsonify({"status": "error", "message": "No data received"}), 400

#     print(f"Received data: {data}")

#     # Extract relevant fields
#     user_id = data.get('userId')
#     time_spent = data.get('timeSpent', 0)
#     session_duration = data.get('sessionDuration', 0)  # New field for session duration
#     event = data.get('event')

#     # Additional data points
#     user_agent = request.headers.get('User-Agent')   # Browser details
#     referrer = request.referrer                      # Referrer URL
#     ip_address = request.remote_addr                 # IP address
#     clicks = data.get('clicks', 0)                  # Clicks
#     submissions = data.get('submissions', 0)        # Form submissions
#     scrolls = data.get('scrolls', 0)                # Scrolls
#     video_plays = data.get('video_plays', 0)        # Video plays
#     hovers = data.get('hovers', 0)                  # Hovers

#     # Get location based on IP address
#     country, city = get_location(ip_address)

#     # Additional data points
#     screen_resolution = data.get('screenResolution', 'Unknown')  # Screen resolution
#     scroll_depth = data.get('scrollDepth', 0)       # Scroll depth
#     session_id = data.get('sessionId', None)        # Session ID
#     page_url = data.get('page_url', 'Unknown')      # Page URL
#     device_type = data.get('device_type', 'Unknown')  # Device type
#     operating_system = data.get('operating_system', 'Unknown')  # Operating system
#     browser_info = data.get('browser_info', 'Unknown')  # Browser info
#     referring_domain = data.get('referring_domain', 'Unknown')  # Referring domain
#     utm_source = data.get('utm_source', 'Unknown')    # UTM source
#     utm_medium = data.get('utm_medium', 'Unknown')    # UTM medium
#     utm_campaign = data.get('utm_campaign', 'Unknown')  # UTM campaign
#     click_path = ','.join(data.get('click_path', []))  # Click path
#     error_logs = data.get('error_logs', '')  # Error logs

#     # Current timestamp
#     timestamp = datetime.now()

#     # Insert user tracking information as a new entry
#     insert_user_tracking(
#         user_id, time_spent, session_duration, event, user_agent, referrer,
#         ip_address, clicks, submissions, scrolls, video_plays, hovers,
#         country, city, screen_resolution, scroll_depth, session_id,
#         timestamp, page_url, device_type, operating_system,
#         browser_info, referring_domain, utm_source, utm_medium,
#         utm_campaign, click_path, error_logs
#     )

#     return jsonify({"status": "success", "received_data": data}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
