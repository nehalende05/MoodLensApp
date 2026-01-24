"""
Flask API server for MoodLens
Handles emotion detection and agent communication
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image
import json
import threading
import time
from datetime import datetime

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except:
    DEEPFACE_AVAILABLE = False

from agent import MoodLensAgent

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/assets')
CORS(app)

# Global agent instance
agent = MoodLensAgent()
current_session = None

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.current_session_id = None
    
    def create_session(self, user_id: str):
        self.current_session_id = user_id
        self.sessions[user_id] = {
            "agent": MoodLensAgent(),
            "start_time": datetime.now(),
            "emotion_log": [],
            "action_log": []
        }
        return self.sessions[user_id]
    
    def get_session(self, user_id: str):
        return self.sessions.get(user_id)

session_manager = SessionManager()

@app.route('/')
def home():
    """Serve the main dashboard"""
    return render_template('index.html')

@app.route('/api/detect-emotion', methods=['POST'])
def detect_emotion():
    """
    Detect emotion from image and voice data
    """
    try:
        data = request.json
        
        # Get image from base64
        image_data = data.get('image')
        voice_data = data.get('voice', {})
        user_id = data.get('user_id', 'default')
        
        # Initialize session if needed
        if user_id not in session_manager.sessions:
            session_manager.create_session(user_id)
        
        session_agent = session_manager.sessions[user_id]['agent']
        
        # Decode image
        if image_data:
            image_data = image_data.replace('data:image/jpeg;base64,', '')
            img_array = np.frombuffer(base64.b64decode(image_data), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            # Detect emotions using DeepFace or mock data
            facial_data = detect_face_emotion(img)
        else:
            facial_data = {
                "dominant_emotion": "neutral",
                "emotion": {
                    "angry": 0.1,
                    "fear": 0.1,
                    "sad": 0.2,
                    "neutral": 0.4,
                    "happy": 0.2,
                    "surprise": 0.0
                },
                "confidence": 0.7
            }
        
        # Mock voice data if not provided
        if not voice_data:
            voice_data = {
                "intensity": 0.6,
                "pace": 0.5,
                "tremor": 0.1,
                "confidence": 0.7
            }
        
        # Run agent cycle
        agent_response = session_agent.process_cycle(facial_data, voice_data)
        
        # Log emotion
        session_manager.sessions[user_id]['emotion_log'].append({
            "facial": facial_data,
            "voice": voice_data,
            "timestamp": datetime.now().isoformat()
        })
        
        session_manager.sessions[user_id]['action_log'].append(agent_response)
        
        return jsonify({
            "success": True,
            "emotion_detection": facial_data,
            "voice_analysis": voice_data,
            "agent_decision": agent_response,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def detect_face_emotion(image):
    """
    Detect emotions from face using DeepFace
    Falls back to mock data if DeepFace not available
    """
    try:
        if not DEEPFACE_AVAILABLE:
            # Return mock emotion data
            return {
                "dominant_emotion": "neutral",
                "emotion": {
                    "angry": 0.05,
                    "fear": 0.05,
                    "sad": 0.15,
                    "neutral": 0.50,
                    "happy": 0.20,
                    "surprise": 0.05
                },
                "confidence": 0.85
            }
        
        # Use DeepFace for actual emotion detection
        result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
        
        if isinstance(result, list):
            result = result[0]
        
        emotions = result.get('emotion', {})
        dominant = result.get('dominant_emotion', 'neutral')
        
        # Normalize emotions to 0-1 range
        max_val = max(emotions.values()) if emotions else 1
        normalized_emotions = {k: v/max_val for k, v in emotions.items()}
        
        return {
            "dominant_emotion": dominant,
            "emotion": normalized_emotions,
            "confidence": 0.85
        }
    
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        # Return default emotion
        return {
            "dominant_emotion": "neutral",
            "emotion": {
                "angry": 0.1,
                "fear": 0.1,
                "sad": 0.2,
                "neutral": 0.4,
                "happy": 0.2,
                "surprise": 0.0
            },
            "confidence": 0.5
        }

@app.route('/api/feedback', methods=['POST'])
def provide_feedback():
    """
    Collect user feedback on recommendations
    Used for agent learning
    """
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        action_id = data.get('action_id')
        feedback = data.get('feedback', {})
        
        session = session_manager.get_session(user_id)
        if session:
            session['agent'].learn_from_feedback(action_id, feedback)
        
        return jsonify({
            "success": True,
            "message": "Feedback recorded for agent learning"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/session-summary', methods=['GET'])
def get_session_summary():
    """Get summary of current session"""
    try:
        user_id = request.args.get('user_id', 'default')
        
        session = session_manager.get_session(user_id)
        if not session:
            return jsonify({"success": False, "error": "No active session"}), 404
        
        summary = session['agent'].get_session_summary()
        session_duration = (datetime.now() - session['start_time']).total_seconds()
        
        return jsonify({
            "success": True,
            "summary": summary,
            "session_duration": session_duration,
            "total_emotions_logged": len(session['emotion_log']),
            "total_actions_triggered": len(session['action_log'])
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "deepface_available": DEEPFACE_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
