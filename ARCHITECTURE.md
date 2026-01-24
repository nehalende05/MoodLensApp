# MoodLens - Complete Technical Documentation

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Agentic AI Workflow](#agentic-ai-workflow)
3. [API Documentation](#api-documentation)
4. [Frontend Components](#frontend-components)
5. [Configuration Guide](#configuration-guide)
6. [Deployment Guide](#deployment-guide)

---

## System Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MoodLens System                           │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐        ┌──────────────────────┐
│   FRONTEND (Browser) │◄──────►│   BACKEND (Flask)    │
│                      │        │                      │
│ • HTML5 Dashboard   │        │ • Emotion Detection  │
│ • CSS3 Styling      │        │ • Agent Logic        │
│ • JavaScript Logic  │        │ • Session Manager    │
│ • Camera Access     │        │ • API Endpoints      │
│ • Voice Input       │        │ • Model Integration  │
└──────────────────────┘        └──────────────────────┘
           │                              │
           └──────────────┬───────────────┘
                          │
                    ┌─────▼─────┐
                    │  DeepFace │
                    │  Models   │
                    └───────────┘
```

### File Structure

```
MoodLens/
├── backend/
│   ├── agent.py              # Core agentic AI system
│   ├── app.py                # Flask API server
│   ├── config.py             # Configuration settings
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── index.html            # Main HTML dashboard
│   ├── styles.css            # CSS3 styling
│   ├── script.js             # JavaScript functionality
│   └── assets/               # Images, fonts, etc.
│
├── models/                   # Pre-trained models (optional)
│
├── launch.py                 # Quick start launcher
├── README.md                 # Project overview
├── QUICKSTART.md             # Quick start guide
└── ARCHITECTURE.md           # This file
```

---

## Agentic AI Workflow

### Overview

MoodLens implements a sophisticated agentic AI system with four main phases:

```
┌──────────────┐
│  PERCEIVE    │  Sense emotional signals
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  REASON      │  Interpret and decide
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  ACT         │  Recommend actions
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  LEARN       │  Adapt from feedback
└──────────────┘
```

### Phase 1: PERCEIVE

**Input**: Webcam (facial) + Microphone (voice)

**Process**:
1. Capture image from webcam
2. Detect face using face detection model
3. Analyze emotions using DeepFace
4. Extract emotion probabilities (happy, sad, angry, etc.)
5. Analyze voice characteristics (intensity, pace, tremor)

**Output**:
```json
{
  "facial": {
    "dominant_emotion": "sad",
    "emotion": {
      "happy": 0.2,
      "neutral": 0.35,
      "sad": 0.3,
      "angry": 0.1,
      "fear": 0.05,
      "surprise": 0.0
    },
    "confidence": 0.85
  },
  "voice": {
    "intensity": 0.4,
    "pace": 0.45,
    "stress_indicators": 0.15
  }
}
```

### Phase 2: REASON

**Input**: Perception data + Historical emotion buffer

**Process**:
1. Fuse facial and voice signals using weighted average
2. Store in emotion buffer (rolling window of 30 samples)
3. Detect patterns:
   - Sustained high stress (>65% for 5+ samples)
   - Progressive fatigue (>55% trend)
   - Declining mood (<45% trend)
4. Calculate severity score:
   ```
   severity = (stress × 0.4) + (fatigue × 0.3) + ((1 - mood) × 0.3)
   ```
5. Make decision:
   - If severity > 0.75: Critical
   - If severity > 0.6: High
   - If severity > 0.4: Moderate
   - Otherwise: Low

**Output**:
```json
{
  "detected_patterns": [
    "sustained_high_stress",
    "progressive_fatigue"
  ],
  "severity_level": "high",
  "recommended_action_type": "stress_relief",
  "reasoning": [
    "High stress detected - recommend calming interventions"
  ]
}
```

### Phase 3: ACT

**Input**: Reasoning decision + Action library

**Process**:
1. Select appropriate action category based on severity
2. Filter actions by severity level
3. Select top 3 most relevant actions
4. Assign priorities
5. Generate user-facing recommendations
6. Track action in history

**Output**:
```json
{
  "action_type": "stress_relief",
  "actions": [
    {
      "name": "Box Breathing Exercise",
      "description": "Breathe in for 4, hold for 4, exhale for 4, hold for 4",
      "duration": 120,
      "category": "breathing",
      "priority": "high"
    }
  ],
  "priority": 2,
  "timestamp": "2026-01-24T13:51:00"
}
```

### Phase 4: LEARN

**Input**: User feedback on action effectiveness

**Process**:
1. Collect rating (1-5 stars) and comments
2. Calculate effectiveness score
3. Store in feedback log
4. Could optionally:
   - Increase priority of effective actions
   - Deprioritize ineffective ones
   - Adjust thresholds for user

**Example Feedback**:
```json
{
  "action_id": "Box Breathing Exercise",
  "effectiveness": 0.85,
  "comment": "Really helped me calm down quickly"
}
```

---

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### 1. Emotion Detection

**Endpoint**: `POST /api/detect-emotion`

**Purpose**: Detect emotion from image and voice data

**Request Body**:
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "voice": {
    "intensity": 0.6,
    "pace": 0.5,
    "tremor": 0.1,
    "confidence": 0.7
  },
  "user_id": "user_123"
}
```

**Response Success**:
```json
{
  "success": true,
  "emotion_detection": {
    "dominant_emotion": "neutral",
    "emotion": {
      "happy": 0.4,
      "neutral": 0.5,
      "sad": 0.05,
      "angry": 0.03,
      "fear": 0.02,
      "surprise": 0.0
    },
    "confidence": 0.85
  },
  "voice_analysis": {
    "intensity": 0.6,
    "pace": 0.5,
    "stress_indicators": 0.15
  },
  "agent_decision": {
    "perception": {...},
    "reasoning": {...},
    "action": {...},
    "agent_state": {...}
  },
  "timestamp": "2026-01-24T13:51:23.456Z"
}
```

**Response Error**:
```json
{
  "success": false,
  "error": "Error message"
}
```

**Status Codes**:
- `200`: Success
- `400`: Bad request
- `500`: Server error

---

### 2. Feedback

**Endpoint**: `POST /api/feedback`

**Purpose**: Submit feedback on intervention effectiveness

**Request Body**:
```json
{
  "user_id": "user_123",
  "action_id": "Box Breathing Exercise",
  "feedback": {
    "effectiveness": 0.8,
    "comment": "Helped me relax"
  }
}
```

**Response**:
```json
{
  "success": true,
  "message": "Feedback recorded for agent learning"
}
```

---

### 3. Session Summary

**Endpoint**: `GET /api/session-summary?user_id=user_123`

**Purpose**: Get summary of current session

**Response**:
```json
{
  "success": true,
  "summary": {
    "session_duration": 1800,
    "emotional_trends": {
      "stress_trend": 0.55,
      "fatigue_trend": 0.45,
      "mood_trend": 0.65,
      "sample_count": 18
    },
    "interventions_provided": 4,
    "average_effectiveness": 0.75,
    "key_patterns": [
      "sustained_high_stress",
      "progressive_fatigue"
    ],
    "recommendations_for_next_session": [
      "Consider regular stress-management practices",
      "Ensure adequate rest and sleep"
    ]
  },
  "session_duration": 1800,
  "total_emotions_logged": 18,
  "total_actions_triggered": 4
}
```

---

### 4. Health Check

**Endpoint**: `GET /api/health`

**Purpose**: Check server status

**Response**:
```json
{
  "status": "healthy",
  "deepface_available": true,
  "timestamp": "2026-01-24T13:51:00Z"
}
```

---

## Frontend Components

### HTML Structure

```html
<body>
  <nav>          <!-- Navigation bar -->
  <main>         <!-- Main dashboard -->
    <section id="dashboard">     <!-- Current emotion state -->
    <section id="monitor">       <!-- Real-time monitoring -->
    <section id="recommendations"> <!-- AI suggestions -->
    <section id="insights">      <!-- Session analysis -->
  </main>
  <div id="modals">  <!-- Recommendation & feedback modals -->
</body>
```

### Key CSS Classes

| Class | Purpose |
|-------|---------|
| `.card` | Container for content |
| `.emotion-wheel` | Animated emotion visualization |
| `.metric-bar` | Progress bar for metrics |
| `.recommendation-card` | Single recommendation display |
| `.modal` | Modal dialog overlay |
| `.btn` | Button styling |

### JavaScript Functions

**Initialization**:
- `initializeApp()` - Set up the application
- `checkBackendHealth()` - Verify backend is running

**Monitoring**:
- `startMonitoring()` - Begin webcam monitoring
- `stopMonitoring()` - Stop webcam access
- `startMicrophone()` - Start voice recording

**Interaction**:
- `viewRecommendations()` - Show recommendation cards
- `selectRecommendation()` - Choose an intervention
- `startIntervention()` - Begin selected intervention

**Feedback**:
- `setRating()` - Set feedback rating
- `submitFeedback()` - Send feedback to backend

**Analytics**:
- `viewInsights()` - Show session analytics
- `fetchSessionSummary()` - Get session data
- `updateInsightsUI()` - Display insights

---

## Configuration Guide

### Backend Configuration

**File**: `backend/config.py`

#### Emotion Thresholds
```python
EMOTION_THRESHOLDS = {
    "stress_high": 0.7,           # 70% = high stress
    "stress_very_high": 0.8,      # 80% = very high
    "fatigue_high": 0.6,          # 60% = high fatigue
    "mood_low": 0.4,              # 40% = low mood
}
```

#### Buffer Settings
```python
BUFFER_SETTINGS = {
    "window_size": 30,            # Keep 30 readings
    "min_samples": 5,             # Min before decision
    "pattern_lookback": 10,       # Pattern analysis window
}
```

#### Detection Settings
```python
DETECTION_SETTINGS = {
    "confidence_threshold": 0.6,  # Only >60% confidence
    "fps_target": 2,              # 2 detections/sec
    "frame_interval": 500,        # 500ms between analysis
}
```

### Frontend Configuration

**File**: `frontend/script.js`

#### Update API URL
```javascript
const API_URL = 'http://localhost:5000/api';
```

#### Adjust Detection Loop
```javascript
// Change detection interval (milliseconds)
setTimeout(detectFrame, 500);  // Currently 500ms
```

#### Customize Mock Data
```javascript
function generateMockVoiceData() {
    return {
        intensity: 0.5 + Math.random() * 0.3,
        pace: 0.4 + Math.random() * 0.3,
        tremor: Math.random() * 0.2,
    };
}
```

---

## Deployment Guide

### Local Development

1. **Clone repository**
   ```bash
   git clone https://github.com/nehalende05/MoodLens.git
   cd MoodLens
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run development server**
   ```bash
   python app.py
   ```

### Docker Deployment

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "backend/app.py"]
```

**Build & Run**:
```bash
docker build -t moodlens .
docker run -p 5000:5000 moodlens
```

### Production Deployment

1. **Use Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
   ```

2. **Enable HTTPS**
   - Get SSL certificate
   - Configure Flask for HTTPS

3. **Environment Variables**
   ```bash
   FLASK_ENV=production
   FLASK_DEBUG=0
   DEEPFACE_CACHE_DIR=/path/to/cache
   ```

4. **Database Setup** (if adding persistence)
   ```bash
   pip install flask-sqlalchemy
   python manage.py db init
   ```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 5000 in use | `netstat -ano \| findstr :5000` (Windows) |
| No camera access | Check browser permissions |
| Slow detection | Reduce detection frequency or resolution |
| DeepFace not working | Install TensorFlow: `pip install tensorflow` |

### Debug Mode

Enable debug logging in `config.py`:
```python
LOGGING_SETTINGS = {
    "log_level": "DEBUG",
    "log_emotion_updates": True,
    "log_agent_decisions": True,
}
```

---

## Performance Optimization

### Detection Loop
- Current: 2 detections/second (500ms interval)
- For faster: Reduce `frame_interval` to 333ms (3 fps)
- For slower: Increase to 1000ms (1 fps)

### Model Optimization
- Use lighter face detector: `cascade` instead of `retinaface`
- Reduce image resolution before analysis
- Batch process multiple frames

### Memory Usage
- Emotion buffer: 30 samples = minimal memory
- Session data: Cleared on server restart
- Feedback log: Limited to last 100 items

---

## Future Enhancements

### Planned Features
- [ ] Multi-user support with authentication
- [ ] Cloud sync for cross-device access
- [ ] Mobile app (React Native)
- [ ] Wearable integration (smartwatch)
- [ ] Advanced ML model (custom CNN)
- [ ] Real-time collaboration
- [ ] Integration with calendar/tasks
- [ ] Export session reports

### Research Directions
- Emotion prediction (what's next)
- Personality trait detection
- Social sentiment analysis
- Contextual recommendations
- Personalized intervention generation

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## License

This project is part of the Pune Hackathon - MoodLens Initiative.

---

**Last Updated**: January 24, 2026  
**Version**: 1.0.0  
**Status**: Production Ready
