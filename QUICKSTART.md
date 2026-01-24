# MoodLens - Quick Start Guide

## 🎯 Start Using MoodLens in 5 Minutes

### Option 1: Quick Web Demo (No Installation)

1. **Open the UI directly**
   - Open `frontend/index.html` in your browser
   - All UI features work immediately
   - Emotion detection uses simulated data

2. **Features Available in Demo Mode**
   - ✅ Beautiful dashboard interface
   - ✅ Simulated emotional data
   - ✅ Recommendation display
   - ✅ Feedback collection
   - ✅ Session insights
   - ❌ Real webcam feed (requires backend)

---

### Option 2: Full Setup with Backend (5-10 minutes)

#### Step 1: Install Python Dependencies
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

#### Step 2: Start the Backend Server
```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

#### Step 3: Open the Application
- Go to `http://localhost:5000` in your browser
- Or open `frontend/index.html` for the full experience

---

## 📱 Using the Application

### Dashboard
1. Click "Start Monitoring" to begin emotion detection
2. Grant camera/microphone permissions when prompted
3. Your emotional metrics will update in real-time

### Real-time Monitoring
- **Webcam Feed**: Shows live video with emotion analysis
- **Emotion Breakdown**: See percentages for each emotion
- **Metrics**: Stress, Fatigue, and Mood levels

### Getting Recommendations
1. Emotional strain is detected automatically
2. Recommendations appear in a notification
3. Click "View All" or "Start Now" to see options
4. Choose an intervention and start

### Providing Feedback
1. After completing an intervention
2. Rate its effectiveness (1-5 stars)
3. Add optional comments
4. Submit feedback to help the AI learn

### Viewing Insights
1. Click "Insights" in the navigation
2. See your emotional trends
3. View detected patterns
4. Review session statistics

---

## 🎨 Demo Features

### Beautiful UI Components
- **Gradient backgrounds**: Modern, colorful design
- **Animated charts**: Smooth, interactive visualizations
- **Responsive layout**: Works on mobile and desktop
- **Real-time updates**: Live emotion metrics
- **Modal dialogs**: Clean interaction patterns

### Interactive Elements
- Start/Stop monitoring buttons
- Recommendation cards with quick actions
- Rating stars for feedback
- Responsive navigation menu
- Emoji indicators for emotions

---

## ⚙️ Configuration

### Demo Mode Settings

In `frontend/script.js`, adjust demo data:

```javascript
// Update demo emotion frequency (milliseconds)
setInterval(() => {
    // Demo emotion update
}, 5000);  // Change to 3000 for faster updates

// Adjust confidence level
confidence: 0.7 + Math.random() * 0.25
```

### Backend Settings

In `backend/agent.py`, configure emotion thresholds:

```python
# Stress detection threshold
"stress_high": 0.7,

# Fatigue detection threshold  
"fatigue_high": 0.6,

# Low mood detection threshold
"mood_low": 0.4,

# Critical stress level
"critical_threshold": 0.8
```

---

## 🎥 Using the Webcam

### Requirements
- Webcam must be connected
- Browser must have permission
- Good lighting recommended
- Face should be clearly visible

### Steps
1. Click "Start Monitoring" on dashboard
2. Grant camera access when prompted
3. Face the webcam
4. The system will analyze your expressions

### Tips for Best Results
- Ensure adequate lighting
- Position webcam at eye level
- Minimize head movement
- Use clear facial expressions

---

## 🔊 Voice Analysis

### Using Microphone
1. Click "Voice Analysis" button
2. Grant microphone access
3. Speak clearly for 10 seconds
4. Voice characteristics are analyzed

### Voice Metrics
- **Intensity**: Speaking volume level
- **Pace**: Speed of speech
- **Tremor**: Voice shaking/quivering
- **Stress Indicators**: Combination of above

---

## 📊 Understanding Your Results

### Emotion Breakdown
- **Happy** (Yellow): Positive mood
- **Neutral** (Gray): Normal/baseline
- **Sad** (Blue): Down mood or fatigue
- **Angry** (Red): Stress or irritation
- **Fear** (Purple): Anxiety or worry
- **Surprise** (Pink): Unexpected emotion

### Severity Levels
- 🟢 **Low**: Continue with current activities
- 🟡 **Moderate**: Consider a break
- 🟠 **High**: Intervention recommended
- 🔴 **Critical**: Urgent support needed

### Recommendation Types
- 🌬️ **Breathing**: For immediate stress relief
- 🎵 **Music**: For mood and energy
- 🏃 **Movement**: For fatigue and energy
- 💭 **Mindfulness**: For mood and emotional awareness
- 🎬 **Media**: For distraction and mood lift

---

## 🐛 Troubleshooting

### Camera Not Working
```
Error: NotAllowedError: Permission denied
Solution: Check browser camera permissions in settings
```

### Microphone Issues
```
Error: NotFoundError: No audio input device found
Solution: Connect microphone and refresh browser
```

### Backend Not Responding
```
Error: Failed to fetch from API
Solution: 
1. Check if Flask server is running (port 5000)
2. Verify no other app is using port 5000
3. Restart the server
```

### Demo Mode Not Starting
```
Solution: 
1. Clear browser cache
2. Hard refresh (Ctrl+Shift+R)
3. Try a different browser
```

### Slow Emotion Detection
```
Solution:
1. Close other applications
2. Reduce browser tabs
3. Adjust detection frequency in settings
4. Update your camera drivers
```

---

## 🔄 Agent Workflow Explanation

### The Four Phases

**1. PERCEIVE** 
- Captures facial expressions from webcam
- Analyzes voice characteristics
- Fuses signals into emotional state

**2. REASON**
- Analyzes emotion trends
- Detects patterns (stress, fatigue, low mood)
- Assesses severity level
- Decides action type needed

**3. ACT**
- Selects best recommendations
- Prioritizes based on severity
- Presents to user
- Tracks intervention

**4. LEARN**
- Collects user feedback
- Rates intervention effectiveness
- Adapts future recommendations
- Builds user profile

---

## 💾 Data & Privacy

### What Data Is Collected?
- Emotional state (not stored permanently)
- Session duration
- Recommendation effectiveness ratings
- Feedback comments

### Where Is Data Stored?
- Session data: In browser memory
- Backend: In-memory (cleared on restart)
- Optional: Local browser storage (IndexedDB)

### Data Deletion
- Clear browser cache to remove local data
- Restart server to clear backend data
- No persistent storage by default

---

## 🎓 Learning Resources

### Understanding Emotions
- Happy: Positive experiences, contentment
- Sad: Loss, disappointment, low mood
- Angry: Frustration, irritation, anger
- Fear: Anxiety, worry, tension
- Neutral: Calm baseline state
- Surprise: Unexpected situations

### Stress Management Techniques
- **Breathing**: 4-4-4 box breathing
- **Relaxation**: Progressive muscle relaxation
- **Movement**: Stretching and walking
- **Mindfulness**: Meditation and gratitude
- **Music**: Calming or energizing playlists

### Mental Wellness Tips
1. Regular check-ins with yourself
2. Take breaks before stress builds
3. Combine multiple techniques
4. Track what works for you
5. Seek professional help when needed

---

## 🎉 Next Steps

1. **Explore the Dashboard**
   - Familiarize yourself with all sections
   - Try different interventions
   - Rate their effectiveness

2. **Build Your Profile**
   - Use the system regularly
   - Provide honest feedback
   - Let AI learn your patterns

3. **Track Improvements**
   - Monitor your emotional trends
   - Notice which interventions help
   - Build better coping strategies

4. **Share Your Experience**
   - Tell others about MoodLens
   - Provide feedback for improvements
   - Contribute to the project

---

## 📞 Support

**Need help?**
1. Check the main README.md
2. Review this Quick Start Guide
3. Check troubleshooting section
4. Submit an issue on GitHub

**Have suggestions?**
- Open a feature request
- Share your experience
- Help improve the system

---

## 🎊 Enjoy Your Mental Wellness Journey!

MoodLens is your companion for emotional awareness and mental health. Use it regularly, provide feedback, and watch as it learns to support you better over time.

**Remember**: If you experience severe mental health issues, always seek help from a professional.

---

**Version**: 1.0.0  
**Last Updated**: January 24, 2026  
**License**: Pune Hackathon - MoodLens Project
