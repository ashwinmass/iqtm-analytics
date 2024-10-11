from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/track": {"origins": "*"}})  # Explicitly allow all origins for /track route

# Get MongoDB connection URI from environment variable
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MongoDB URI not found in environment variables")

# Create a new MongoDB client and connect to the server
IQTM_CLIENT = MongoClient(MONGO_URI, server_api=ServerApi('1'))
IQTM_SITE_ANALYTICS = IQTM_CLIENT["IQTM_Site_Analytics"]
IQTM_USER_TRACKINGS_COLL = IQTM_SITE_ANALYTICS["User_Trackings"]

# Send a ping to confirm a successful connection
try:
    IQTM_CLIENT.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    raise ConnectionError(f"Couldn't connect to MongoDB: {e}")

# Route to check if the server is running
@app.route('/', methods=['GET'])
def server_info():
    return jsonify({"status": "Server is up and running"}), 200

# Function to insert a new tracking event
def insert_user_tracking(data):
    try:
        IQTM_USER_TRACKINGS_COLL.insert_one(data)
        print("Inserted user info successfully")
    except Exception as e:
        print(f"Couldn't insert record into the database: {e}")

# Route to track visitor activity and additional data points
@app.route('/track', methods=['POST'])
def track_visitor():
    try:
        # Check for correct content type
        if request.content_type != 'application/json':
            return jsonify({"status": "error", "message": "Invalid content type. Expected application/json"}), 415

        data = request.get_json()

        if data is None:
            return jsonify({"status": "error", "message": "No data received"}), 400

        print(f"Received data: {data}")

        # Extract relevant fields
        user_data = {
            "user_id": data.get('userId'),
            "time_spent": data.get('timeSpent', 0),
            "session_duration": data.get('sessionDuration', 0),
            "event": data.get('event'),
            "user_agent": request.headers.get('User-Agent'),
            "referrer": request.referrer,
            "ip_address": request.remote_addr,
            "clicks": data.get('clicks', 0),
            "submissions": data.get('submissions', 0),
            "scrolls": data.get('scrolls', 0),
            "video_plays": data.get('video_plays', 0),
            "hovers": data.get('hovers', 0),
            "country": data.get('country', 'Unknown'),
            "city": data.get('city', 'Unknown'),
            "screen_resolution": data.get('screenResolution', 'Unknown'),
            "scroll_depth": data.get('scrollDepth', 0),
            "session_id": data.get('sessionId', None),
            "page_url": data.get('page_url', 'Unknown'),
            "device_type": data.get('device_type', 'Unknown'),
            "operating_system": data.get('operating_system', 'Unknown'),
            "browser_info": data.get('browser_info', 'Unknown'),
            "referring_domain": data.get('referring_domain', 'Unknown'),
            "utm_source": data.get('utm_source', 'Unknown'),
            "utm_medium": data.get('utm_medium', 'Unknown'),
            "utm_campaign": data.get('utm_campaign', 'Unknown'),
            "click_path": ','.join(data.get('click_path', [])),
            "error_logs": data.get('error_logs', ''),
            "timestamp": datetime.now()
        }

        # Insert user tracking information as a new entry
        insert_user_tracking(user_data)

        return jsonify({"status": "success", "received_data": data}), 200
    except Exception as e:
        print(f"Error tracking visitor: {e}")
        return jsonify({"message": "INTERNAL SERVER ERROR"}), 500

@app.route('/trackings', methods=['GET'])
def get_Trackings():
    try:
        # Retrieve all documents from the "User_Trackings" collection
        trackings = IQTM_USER_TRACKINGS_COLL.find()

        # Convert the cursor to a list and manually convert BSON types to JSON-compatible types
        tracking_list = []
        for tracking in trackings:
            tracking['_id'] = str(tracking['_id'])  # Convert ObjectId to string
            tracking['timestamp'] = tracking['timestamp'].isoformat()  # Convert datetime to ISO format
            tracking_list.append(tracking)

        return jsonify({"status": "success", "data": tracking_list}), 200
    except Exception as e:
        print(f"Error retrieving trackings: {e}")
        return jsonify({"status": "error", "message": "Unable to retrieve trackings"}), 500
