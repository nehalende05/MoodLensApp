"""
MoodLens Configuration
Customize agent behavior, thresholds, and intervention settings
"""

# ============================================
# EMOTION DETECTION THRESHOLDS
# ============================================

EMOTION_THRESHOLDS = {
    # Stress detection
    "stress_high": 0.7,            # Trigger stress intervention at 70%
    "stress_very_high": 0.8,       # Trigger emergency at 80%
    
    # Fatigue detection
    "fatigue_high": 0.6,           # Trigger fatigue intervention at 60%
    "fatigue_critical": 0.85,      # Critical fatigue level
    
    # Mood detection
    "mood_low": 0.4,               # Trigger mood lift at 40%
    "mood_critical": 0.2,          # Critical low mood
    
    # Overall thresholds
    "critical_threshold": 0.8,     # Any metric >80% = critical
    "emergency_threshold": 0.9,    # Immediate professional help needed
}

# ============================================
# EMOTION BUFFER & DETECTION SETTINGS
# ============================================

BUFFER_SETTINGS = {
    "window_size": 30,             # Keep last 30 readings
    "min_samples": 5,              # Minimum readings before making decisions
    "pattern_lookback": 10,        # Look back 10 samples for patterns
}

DETECTION_SETTINGS = {
    "confidence_threshold": 0.6,   # Only accept detections >60% confident
    "fps_target": 2,               # Target 2 emotion updates per second
    "frame_interval": 500,         # 500ms between analysis (milliseconds)
}

# ============================================
# INTERVENTION LIBRARY
# ============================================

INTERVENTIONS = {
    "stress_relief": {
        "primary_actions": [
            {
                "name": "Box Breathing Exercise",
                "description": "Breathe in for 4, hold for 4, exhale for 4, hold for 4. Repeat 5 times.",
                "duration": 120,
                "category": "breathing",
                "priority": "high",
                "effectiveness": 0.85,
            },
            {
                "name": "Calming Music",
                "description": "Listen to lo-fi beats, ambient sounds, or nature recordings.",
                "duration": 300,
                "category": "music",
                "priority": "high",
                "effectiveness": 0.75,
            },
            {
                "name": "Progressive Muscle Relaxation",
                "description": "Systematically tense and release each muscle group.",
                "duration": 600,
                "category": "relaxation",
                "priority": "medium",
                "effectiveness": 0.80,
            },
        ]
    },
    
    "energy_boost": {
        "primary_actions": [
            {
                "name": "Quick Stretch Break",
                "description": "Stand up and perform 10 full-body stretches.",
                "duration": 300,
                "category": "movement",
                "priority": "high",
                "effectiveness": 0.70,
            },
            {
                "name": "Energizing Music",
                "description": "Play upbeat, motivational, or favorite music.",
                "duration": 300,
                "category": "music",
                "priority": "high",
                "effectiveness": 0.72,
            },
            {
                "name": "Quick Walk",
                "description": "Take a 5-minute walk outside or around your space.",
                "duration": 300,
                "category": "movement",
                "priority": "medium",
                "effectiveness": 0.78,
            },
        ]
    },
    
    "mood_lifting": {
        "primary_actions": [
            {
                "name": "Positive Affirmation",
                "description": "Read personalized positive messages and affirmations.",
                "duration": 120,
                "category": "mindfulness",
                "priority": "high",
                "effectiveness": 0.68,
            },
            {
                "name": "Gratitude Reflection",
                "description": "Write down or think about 3-5 things you're grateful for.",
                "duration": 180,
                "category": "mindfulness",
                "priority": "high",
                "effectiveness": 0.82,
            },
            {
                "name": "Inspirational Video",
                "description": "Watch an uplifting, funny, or motivational video.",
                "duration": 600,
                "category": "media",
                "priority": "medium",
                "effectiveness": 0.70,
            },
        ]
    },
    
    "emergency_support": {
        "primary_actions": [
            {
                "name": "Crisis Breathing",
                "description": "Follow guided crisis breathing: Slow, deep, focused breathing.",
                "duration": 300,
                "category": "breathing",
                "priority": "critical",
                "effectiveness": 0.90,
            },
            {
                "name": "5-4-3-2-1 Grounding",
                "description": "Use all senses: 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste.",
                "duration": 600,
                "category": "mindfulness",
                "priority": "critical",
                "effectiveness": 0.88,
            },
            {
                "name": "Professional Support",
                "description": "Reach out to a mental health professional or crisis helpline.",
                "duration": 0,
                "category": "professional",
                "priority": "critical",
                "effectiveness": 1.0,
            },
        ]
    },
    
    "maintain": {
        "primary_actions": [
            {
                "name": "Daily Gratitude Check-in",
                "description": "Maintain balance with a quick gratitude moment.",
                "duration": 300,
                "category": "mindfulness",
                "priority": "low",
                "effectiveness": 0.65,
            },
        ]
    }
}

# ============================================
# SESSION SETTINGS
# ============================================

SESSION_SETTINGS = {
    "max_session_duration": 3600,      # Maximum 1 hour per session
    "auto_save_interval": 300,         # Save progress every 5 minutes
    "enable_persistent_storage": False, # Don't persist data by default
    "enable_analytics": True,          # Track usage patterns
}

# ============================================
# UI/UX SETTINGS
# ============================================

UI_SETTINGS = {
    # Notification settings
    "show_notifications": True,
    "notification_duration": 5000,     # Show for 5 seconds
    "notification_position": "bottom-right",
    
    # Update frequencies
    "emotion_update_interval": 1000,   # Update UI every 1 second
    "trend_update_interval": 5000,     # Update trends every 5 seconds
    "chart_animation_duration": 300,   # 300ms animations
    
    # Theme
    "theme": "light",                  # light or dark
    "enable_animations": True,
    "responsive_mobile": True,
}

# ============================================
# LOGGING & DEBUG
# ============================================

LOGGING_SETTINGS = {
    "log_level": "INFO",               # DEBUG, INFO, WARNING, ERROR
    "log_emotion_updates": False,      # Log every emotion detection
    "log_agent_decisions": True,       # Log reasoning and decisions
    "log_interventions": True,         # Log action recommendations
    "log_feedback": True,              # Log user feedback
}

# ============================================
# LEARNING & ADAPTATION
# ============================================

LEARNING_SETTINGS = {
    "enable_learning": True,
    "feedback_required_samples": 3,    # Need 3 feedback items before adaptation
    "effectiveness_threshold": 0.7,    # Only promote actions with >70% effectiveness
    "adaptation_strength": 0.1,        # Learning rate (0-1)
    "forget_old_feedback": True,
    "feedback_memory_size": 100,       # Remember last 100 feedback items
}

# ============================================
# MODEL SETTINGS
# ============================================

MODEL_SETTINGS = {
    # DeepFace settings
    "use_deepface": True,              # Use real emotion detection
    "deepface_detector": "retinaface", # Face detection model
    "deepface_enforce_detection": False, # Continue even if no face detected
    
    # Fallback to demo mode if DeepFace not available
    "demo_mode_fallback": True,
    "demo_emotion_variance": 0.15,     # Random variation in demo data
}

# ============================================
# API SETTINGS
# ============================================

API_SETTINGS = {
    "flask_host": "127.0.0.1",
    "flask_port": 5000,
    "flask_debug": True,
    "cors_origins": "*",               # Allow all origins (change for production)
    "request_timeout": 30,             # 30 second timeout
    "max_request_size": "16m",         # Max 16MB per request
}

# ============================================
# ADVANCED REASONING SETTINGS
# ============================================

REASONING_SETTINGS = {
    # Pattern detection
    "detect_sustained_stress": True,
    "sustained_stress_threshold": 5,   # 5+ consecutive high readings
    "detect_fatigue_patterns": True,
    "detect_mood_decline": True,
    "mood_decline_threshold": 3,       # 3 consecutive low readings
    
    # Contextual reasoning
    "use_time_context": True,          # Consider time of day
    "working_hours_start": 9,          # 9 AM
    "working_hours_end": 17,           # 5 PM
    
    # Multi-modal fusion
    "facial_weight": 0.5,              # Facial emotion weight
    "voice_weight": 0.5,               # Voice analysis weight
}

# ============================================
# EMERGENCY SETTINGS
# ============================================

EMERGENCY_SETTINGS = {
    "enable_emergency_detection": True,
    "emergency_threshold": 0.9,        # 90% stress/fatigue/mood
    
    # Contact information (customize)
    "emergency_contacts": {
        "crisis_line": "988",          # US crisis line
        "therapist_suggested": False,
        "family_contact": None,
    },
    
    "emergency_actions": [
        "Immediate grounding exercise",
        "Suggest professional help",
        "Provide crisis resources",
    ]
}

# ============================================
# PROFILE CUSTOMIZATION
# ============================================

def get_default_profile():
    """Return default user profile"""
    return {
        "name": "User",
        "age_group": "adult",  # teen, adult, senior
        "language": "en",
        "timezone": "UTC",
        
        # Preferences
        "preferred_interventions": ["breathing", "music", "movement"],
        "avoid_interventions": [],
        
        # Health considerations
        "anxiety_prone": False,
        "depression_history": False,
        "sleep_issues": False,
        
        # Goals
        "primary_goal": "stress_management",
        "secondary_goals": ["mood_improvement", "better_sleep"],
        
        # Sensitivity
        "notification_sensitivity": "medium",  # low, medium, high
        "intervention_detail_level": "medium", # brief, medium, detailed
    }

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_intervention_by_severity(severity: str) -> dict:
    """Get interventions appropriate for severity level"""
    severity_map = {
        "critical": INTERVENTIONS["emergency_support"],
        "high": INTERVENTIONS["stress_relief"],
        "moderate": INTERVENTIONS["energy_boost"],
        "low": INTERVENTIONS["maintain"],
    }
    return severity_map.get(severity, INTERVENTIONS["maintain"])

def get_effective_interventions(effectiveness_threshold: float = 0.75) -> dict:
    """Get interventions above effectiveness threshold"""
    effective = {}
    for category, data in INTERVENTIONS.items():
        effective[category] = [
            action for action in data["primary_actions"]
            if action["effectiveness"] >= effectiveness_threshold
        ]
    return effective

def customize_thresholds(stress=None, fatigue=None, mood=None):
    """Customize detection thresholds"""
    if stress:
        EMOTION_THRESHOLDS["stress_high"] = stress
    if fatigue:
        EMOTION_THRESHOLDS["fatigue_high"] = fatigue
    if mood:
        EMOTION_THRESHOLDS["mood_low"] = mood

# ============================================
# EXPORT
# ============================================

CONFIG = {
    "EMOTION_THRESHOLDS": EMOTION_THRESHOLDS,
    "BUFFER_SETTINGS": BUFFER_SETTINGS,
    "DETECTION_SETTINGS": DETECTION_SETTINGS,
    "INTERVENTIONS": INTERVENTIONS,
    "SESSION_SETTINGS": SESSION_SETTINGS,
    "UI_SETTINGS": UI_SETTINGS,
    "LOGGING_SETTINGS": LOGGING_SETTINGS,
    "LEARNING_SETTINGS": LEARNING_SETTINGS,
    "MODEL_SETTINGS": MODEL_SETTINGS,
    "API_SETTINGS": API_SETTINGS,
    "REASONING_SETTINGS": REASONING_SETTINGS,
    "EMERGENCY_SETTINGS": EMERGENCY_SETTINGS,
}
