# MoodLens - AI Mental Wellness Monitoring System

Welcome to **MoodLens**, an advanced Agentic AI system for real-time mental wellness monitoring and autonomous support.

## 🧠 Project Overview

MoodLens is an intelligent companion that continuously monitors your emotional state through facial expressions and voice analysis. Using a sophisticated agentic workflow, it detects early signs of stress, fatigue, and low mood, then autonomously recommends personalized interventions.

### Key Features

✨ **Real-time Emotion Detection**
- Webcam-based facial expression analysis using DeepFace
- Voice tone and speech pattern analysis
- Multi-modal emotion fusion for accurate assessment

🤖 **Agentic AI Workflow**
- **Perception**: Continuous sensing of emotional signals
- **Reasoning**: Intelligent interpretation and pattern detection
- **Action**: Autonomous, context-aware recommendations
- **Learning**: Adaptation based on user feedback

💪 **Intelligent Interventions**
- Breathing exercises for stress relief
- Mood-lifting activities and affirmations
- Energy-boosting recommendations
- Personalized suggestions based on your patterns

📊 **Session Insights**
- Emotional trend tracking
- Pattern recognition
- Effectiveness analysis
- Session summaries and recommendations

## 🏗️ Architecture

```
MoodLens/
├── backend/
│   ├── agent.py           # Core agentic AI system
│   ├── app.py             # Flask API server
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── index.html         # Beautiful UI dashboard
│   ├── styles.css         # Modern styling
│   └── script.js          # Interactive functionality
│
└── models/                # Pre-trained models (optional)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js (optional, for frontend development)
- Webcam and microphone
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nehalende05/MoodLens.git
   cd MoodLens
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   python app.py
   ```
   
   The server will start at `http://localhost:5000`

5. **Open the frontend**
   - Navigate to `http://localhost:5000` in your browser
   - Or open `frontend/index.html` directly (limited functionality without backend)

## 📖 How It Works

### The Agentic Loop

```
┌─────────────────────────────────────────────┐
│           MOODLENS AGENTIC CYCLE             │
└─────────────────────────────────────────────┘

1️⃣  PERCEIVE
   ├─ Facial Expression Detection
   │  └─ Uses DeepFace to detect emotions from webcam
   ├─ Voice Tone Analysis
   │  └─ Analyzes speech patterns and voice characteristics
   └─ Signal Fusion
      └─ Combines facial and voice data for comprehensive assessment

2️⃣  REASON
   ├─ Pattern Detection
   │  └─ Identifies sustained stress, fatigue, mood patterns
   ├─ Severity Assessment
   │  └─ Calculates overall emotional strain (critical/high/moderate/low)
   └─ Decision Making
      └─ Determines appropriate intervention type

3️⃣  ACT
   ├─ Action Generation
   │  └─ Selects 1-3 best recommendations from action library
   ├─ Priority Assignment
   │  └─ Ranks by severity and relevance
   └─ User Notification
      └─ Presents intervention to user

4️⃣  LEARN
   ├─ Feedback Collection
   │  └─ User rates intervention effectiveness
   └─ Adaptation
      └─ System learns which interventions work best
```

### Emotional State Detection

The system detects:

- **Stress**: Angry + Fear emotions + voice tremor
- **Fatigue**: Sad + Neutral emotions + low voice intensity
- **Mood**: Happy emotion level
- **Overall Confidence**: Weighted average of detection confidence

### Smart Interventions

Based on detected patterns:

| Pattern | Intervention | Duration |
|---------|-------------|----------|
| High Stress | Box breathing, calming music | 2-5 min |
| Fatigue | Stretching, walk, energizing music | 5-10 min |
| Low Mood | Affirmations, gratitude, uplifting video | 2-10 min |
| Critical Stress | Crisis breathing, grounding, professional help | Immediate |

## 🎨 UI Features

### Dashboard
- Current emotional state with animated wheel
- Stress, Fatigue, and Mood metrics
- Quick action buttons
- Real-time status indicator

### Monitor
- Live webcam feed with emotion overlay
- Real-time emotion breakdown chart
- FPS and confidence metrics
- Voice analysis integration

### Recommendations
- Context-aware intervention suggestions
- Severity level indicator
- Detailed intervention descriptions
- Quick-start functionality

### Insights
- Session duration and statistics
- Emotional trend visualization
- Pattern detection and insights
- Effectiveness tracking

## 🔧 Configuration

### Emotion Detection Thresholds

Edit these in `backend/agent.py`:

```python
self.action_thresholds = {
    "stress_high": 0.7,        # Trigger at 70% stress
    "fatigue_high": 0.6,       # Trigger at 60% fatigue
    "mood_low": 0.4,           # Trigger at 40% mood
    "critical_threshold": 0.8  # Critical at 80% stress
}
```

### Emotion Buffer Size

Adjust rolling window for pattern detection:

```python
self.emotion_buffer = EmotionBuffer(window_size=30)  # Last 30 readings
```

## 🧪 Testing

### Without DeepFace (Demo Mode)

The system works in demo mode without DeepFace installed:
- Mock emotion data is generated
- All UI features are functional
- Useful for frontend testing and presentations

### With DeepFace

1. Install additional dependencies:
   ```bash
   pip install tensorflow
   ```

2. First run will download pre-trained models (~300MB)

3. Enable in `backend/app.py`:
   ```python
   DEEPFACE_AVAILABLE = True
   ```

## 📊 API Endpoints

### Emotion Detection
```
POST /api/detect-emotion
Body: {
  "image": "base64_encoded_image",
  "voice": {"intensity": 0.5, "pace": 0.5, "tremor": 0.1},
  "user_id": "user_123"
}
```

### Feedback
```
POST /api/feedback
Body: {
  "user_id": "user_123",
  "action_id": "action_name",
  "feedback": {"effectiveness": 0.8, "comment": "..."}
}
```

### Session Summary
```
GET /api/session-summary?user_id=user_123
```

### Health Check
```
GET /api/health
```

## 🎯 Use Cases

### For Students
- Monitor stress during exam preparation
- Detect fatigue and recommend breaks
- Track mood patterns and mental health

### For Professionals
- Prevent burnout through early detection
- Manage workplace stress
- Improve work-life balance

### For Mental Health Support
- Complement therapeutic interventions
- Provide continuous monitoring
- Enable self-awareness and reflection

## 🔐 Privacy & Security

- ✅ No data transmitted without consent
- ✅ Local processing option available
- ✅ Encrypted communication (HTTPS ready)
- ✅ No biometric data stored
- ✅ Session data can be cleared anytime

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Wearable device integration (smartwatch)
- [ ] Social sharing of achievements
- [ ] Integration with meditation apps
- [ ] Advanced ML model optimization
- [ ] Cloud-based analytics dashboard
- [ ] Mobile app version
- [ ] Team/group monitoring for HR

## 📚 Technologies

### Backend
- **Flask**: Lightweight web framework
- **DeepFace**: Facial emotion recognition
- **NumPy**: Numerical computing
- **OpenCV**: Computer vision

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript**: Interactive functionality
- **Web APIs**: Camera, Audio, Fetch

### AI/ML
- **Agentic Architecture**: Perception → Reasoning → Action → Learning
- **Rule-based Reasoning**: Pattern detection and severity assessment
- **Multi-modal Fusion**: Combining facial and voice signals

## 📝 License

This project is part of the Pune Hackathon - MoodLens Initiative.

## 👥 Team

**MoodLens Development Team**
- Neha Lende (@nehalende05)
- AI & Mental Wellness Focus

## 💬 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Submit an issue on GitHub
4. Contact the team

## 🙏 Acknowledgments

- DeepFace for emotion detection models
- Flask community
- Hackathon organizers
- Mental health advocates

---

**Made with ❤️ for mental wellness and emotional health**

Transform how you understand and manage your emotions. Let MoodLens be your intelligent companion on the journey to better mental health.
