/* ============================================
   MoodLens - JavaScript Functionality
   ============================================ */

const API_URL = 'http://localhost:5000/api';
const USER_ID = 'user_' + Date.now();

// State Management
const state = {
    isMonitoring: false,
    isMicrophoneActive: false,
    currentSession: null,
    videoStream: null,
    mediaRecorder: null,
    currentRecommendation: null,
    userRating: 0
};

// ============================================
// Initialization
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupNavigation();
});

function initializeApp() {
    console.log('Initializing MoodLens...');
    checkBackendHealth();
    setupEventListeners();
    simulateEmotionalData();
}

function checkBackendHealth() {
    fetch(`${API_URL}/health`)
        .then(res => res.json())
        .then(data => console.log('Backend Health:', data))
        .catch(err => console.warn('Backend not running - using demo mode', err));
}

// ============================================
// Navigation Setup
// ============================================

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all
            navLinks.forEach(l => l.classList.remove('active'));
            // Add to clicked
            link.classList.add('active');
            
            // Show/hide sections
            const href = link.getAttribute('href').substring(1);
            document.querySelectorAll('section').forEach(section => {
                section.classList.add('hidden');
            });
            
            const target = document.getElementById(href);
            if (target) {
                target.classList.remove('hidden');
            }
        });
    });
}

function setupEventListeners() {
    // Navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', handleNavigation);
    });
}

function handleNavigation(e) {
    e.preventDefault();
    const target = e.currentTarget.getAttribute('href').substring(1);
    
    // Hide all sections
    document.querySelectorAll('section').forEach(s => s.classList.add('hidden'));
    
    // Show target section
    document.getElementById(target).classList.remove('hidden');
}

// ============================================
// Monitoring & Emotion Detection
// ============================================

async function startMonitoring() {
    if (state.isMonitoring) {
        stopMonitoring();
        return;
    }
    
    try {
        state.isMonitoring = true;
        
        // Navigate to monitor section
        document.getElementById('monitor').classList.remove('hidden');
        document.getElementById('dashboard').classList.add('hidden');
        
        // Update navbar
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelector('[href="#monitor"]').classList.add('active');
        
        // Request camera access
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { 
                facingMode: 'user',
                width: { ideal: 640 },
                height: { ideal: 480 }
            }
        });
        
        state.videoStream = stream;
        const video = document.getElementById('videoFeed');
        video.srcObject = stream;
        video.play();
        
        // Update status
        document.getElementById('cameraStatus').innerHTML = '<span class="status-dot active"></span>Active';
        document.getElementById('cameraStatus').querySelector('.status-dot').classList.add('active');
        
        // Start emotion detection loop
        startEmotionDetectionLoop();
        
    } catch (error) {
        console.error('Error accessing camera:', error);
        alert('Unable to access camera. Please check permissions.');
        state.isMonitoring = false;
    }
}

function stopMonitoring() {
    state.isMonitoring = false;
    
    if (state.videoStream) {
        state.videoStream.getTracks().forEach(track => track.stop());
        state.videoStream = null;
    }
    
    document.getElementById('cameraStatus').innerHTML = '<span class="status-dot"></span>Inactive';
}

async function startEmotionDetectionLoop() {
    const video = document.getElementById('videoFeed');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    let frameCount = 0;
    let lastTime = performance.now();
    
    async function detectFrame() {
        if (!state.isMonitoring) return;
        
        try {
            // Draw video to canvas
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0);
            
            // Convert to base64
            const imageData = canvas.toDataURL('image/jpeg', 0.8);
            
            // Get voice data (mock)
            const voiceData = generateMockVoiceData();
            
            // Send to backend
            const response = await fetch(`${API_URL}/detect-emotion`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image: imageData,
                    voice: voiceData,
                    user_id: USER_ID
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Update UI with emotion data
                updateEmotionUI(result.emotion_detection, result.agent_decision);
            }
            
        } catch (error) {
            console.error('Error in emotion detection:', error);
        }
        
        // Calculate FPS
        frameCount++;
        const now = performance.now();
        if (now - lastTime >= 1000) {
            document.getElementById('fps').textContent = frameCount;
            frameCount = 0;
            lastTime = now;
        }
        
        // Schedule next frame (every 500ms for reasonable detection rate)
        if (state.isMonitoring) {
            setTimeout(detectFrame, 500);
        }
    }
    
    detectFrame();
}

function generateMockVoiceData() {
    return {
        intensity: 0.5 + Math.random() * 0.3,
        pace: 0.4 + Math.random() * 0.3,
        tremor: Math.random() * 0.2,
        confidence: 0.7
    };
}

function updateEmotionUI(emotions, agentDecision) {
    // Update emotion metrics
    const emotionData = emotions.emotion || {};
    
    document.getElementById('happy').style.width = (emotionData.happy * 100) + '%';
    document.getElementById('happyPercent').textContent = Math.round(emotionData.happy * 100) + '%';
    
    document.getElementById('neutral').style.width = (emotionData.neutral * 100) + '%';
    document.getElementById('neutralPercent').textContent = Math.round(emotionData.neutral * 100) + '%';
    
    document.getElementById('sad').style.width = (emotionData.sad * 100) + '%';
    document.getElementById('sadPercent').textContent = Math.round(emotionData.sad * 100) + '%';
    
    document.getElementById('angry').style.width = (emotionData.angry * 100) + '%';
    document.getElementById('angryPercent').textContent = Math.round(emotionData.angry * 100) + '%';
    
    document.getElementById('fear').style.width = (emotionData.fear * 100) + '%';
    document.getElementById('fearPercent').textContent = Math.round(emotionData.fear * 100) + '%';
    
    document.getElementById('surprise').style.width = (emotionData.surprise * 100) + '%';
    document.getElementById('surprisePercent').textContent = Math.round(emotionData.surprise * 100) + '%';
    
    // Update confidence
    document.getElementById('confidence').textContent = Math.round(emotions.confidence * 100) + '%';
    
    // Update emotion emoji
    updateEmotionEmoji(emotions.dominant_emotion);
    
    // Update agent decision
    if (agentDecision && agentDecision.action && agentDecision.action.actions) {
        state.currentAction = agentDecision.action;
        showRecommendationNotification(agentDecision.action);
    }
}

function updateEmotionEmoji(emotion) {
    const emojiMap = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😡',
        'fear': '😨',
        'neutral': '😐',
        'surprise': '😮'
    };
    
    const emoji = emojiMap[emotion.toLowerCase()] || '😐';
    document.getElementById('emotionEmoji').textContent = emoji;
}

// ============================================
// Microphone Recording
// ============================================

async function startMicrophone() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        state.mediaRecorder = new MediaRecorder(stream);
        state.isMicrophoneActive = true;
        
        const audioChunks = [];
        
        state.mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        state.mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            // Send audio for analysis
            console.log('Audio recording completed:', audioBlob);
            state.isMicrophoneActive = false;
        };
        
        state.mediaRecorder.start();
        alert('Recording voice... Speak clearly for emotion analysis.');
        
        // Stop after 10 seconds
        setTimeout(() => {
            if (state.mediaRecorder && state.isMicrophoneActive) {
                state.mediaRecorder.stop();
            }
        }, 10000);
        
    } catch (error) {
        console.error('Microphone error:', error);
        alert('Unable to access microphone.');
    }
}

// ============================================
// Recommendations Display
// ============================================

function showRecommendationNotification(actionData) {
    const actions = actionData.actions || [];
    if (actions.length === 0) return;
    
    // Show first recommendation
    const topAction = actions[0];
    state.currentRecommendation = topAction;
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        <div class="notification-content">
            <h3>${topAction.name}</h3>
            <p>${topAction.description}</p>
            <div class="notification-actions">
                <button onclick="viewRecommendations()">View All</button>
                <button onclick="startIntervention()">Start Now</button>
            </div>
        </div>
    `;
    
    // Position and style
    notification.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, #6366f1, #ec4899);
        color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
        z-index: 1500;
        max-width: 350px;
        animation: slideInUp 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 5 seconds or on button click
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function viewRecommendations() {
    // Navigate to recommendations section
    document.querySelectorAll('section').forEach(s => s.classList.add('hidden'));
    document.getElementById('recommendations').classList.remove('hidden');
    
    // Update navbar
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    
    // Fetch current recommendations
    if (state.currentAction) {
        displayRecommendations(state.currentAction);
    } else {
        simulateRecommendations();
    }
}

function displayRecommendations(actionData) {
    const container = document.getElementById('recommendationsGrid');
    container.innerHTML = '';
    
    const actions = actionData.actions || [];
    const severity = actionData.priority;
    
    // Update severity badge
    const severityMap = {
        1: 'critical',
        2: 'high',
        3: 'moderate',
        4: 'low'
    };
    
    const severityLevel = Object.keys(severityMap).find(k => severityMap[k] === 
        ['critical', 'high', 'moderate', 'low'][severity - 1]);
    document.getElementById('severityBadge').textContent = 
        ['critical', 'high', 'moderate', 'low'][severity - 1].toUpperCase();
    document.getElementById('severityBadge').className = 
        'severity-badge ' + ['critical', 'high', 'moderate', 'low'][severity - 1];
    
    actions.forEach((action, index) => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.innerHTML = `
            <div class="recommendation-title">${action.name}</div>
            <div class="recommendation-description">${action.description}</div>
            <div class="recommendation-meta">
                <span class="recommendation-duration">⏱️ ${Math.round(action.duration / 60)} min</span>
                <span style="cursor: pointer; color: #6366f1;" onclick="selectRecommendation('${action.name}', '${action.description}')">
                    Start →
                </span>
            </div>
        `;
        container.appendChild(card);
    });
}

function selectRecommendation(name, description) {
    state.currentRecommendation = { name, description };
    openModal('modal', {
        title: name,
        content: `<p>${description}</p><p style="margin-top: 1rem; color: #6b7280;">This intervention is designed to help you feel better. Focus on the activity and let it help you.</p>`
    });
}

// ============================================
// Modal Management
// ============================================

function openModal(modalId, data = {}) {
    const modal = document.getElementById(modalId);
    if (data.title) {
        document.getElementById('modalTitle').textContent = data.title;
    }
    if (data.content) {
        document.getElementById('modalBody').innerHTML = data.content;
    }
    modal.classList.remove('hidden');
}

function closeModal() {
    document.getElementById('recommendationModal').classList.add('hidden');
}

function closeFeedbackModal() {
    document.getElementById('feedbackModal').classList.add('hidden');
}

function startIntervention() {
    if (!state.currentRecommendation) return;
    
    closeModal();
    
    // Simulate intervention
    alert(`Starting: ${state.currentRecommendation.name}\n\n${state.currentRecommendation.description}`);
    
    // Show feedback modal after intervention
    setTimeout(() => {
        document.getElementById('feedbackModal').classList.remove('hidden');
    }, 3000);
}

function setRating(rating) {
    state.userRating = rating;
    document.querySelectorAll('.rating-stars i').forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

function submitFeedback() {
    const feedback = {
        effectiveness: state.userRating / 5,
        comment: document.getElementById('feedbackText').value
    };
    
    // Send to backend
    fetch(`${API_URL}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: USER_ID,
            action_id: state.currentRecommendation.name,
            feedback: feedback
        })
    }).catch(err => console.log('Feedback sent'));
    
    closeFeedbackModal();
    alert('Thank you for your feedback! This helps us improve.');
}

// ============================================
// Insights & Session Summary
// ============================================

function viewInsights() {
    document.querySelectorAll('section').forEach(s => s.classList.add('hidden'));
    document.getElementById('insights').classList.remove('hidden');
    
    // Update navbar
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelector('[href="#insights"]').classList.add('active');
    
    // Fetch session summary
    fetchSessionSummary();
}

async function fetchSessionSummary() {
    try {
        const response = await fetch(`${API_URL}/session-summary?user_id=${USER_ID}`);
        const data = await response.json();
        
        if (data.success) {
            updateInsightsUI(data);
        }
    } catch (error) {
        console.log('Using demo insights');
        updateInsightsUI(getDemoInsights());
    }
}

function updateInsightsUI(data) {
    // Update stats
    document.getElementById('sessionDuration').textContent = formatDuration(data.session_duration || 0);
    document.getElementById('emotionsDetected').textContent = data.total_emotions_logged || 0;
    document.getElementById('interventions').textContent = data.total_actions_triggered || 0;
    document.getElementById('avgEffectiveness').textContent = Math.round((data.summary.average_effectiveness || 0) * 100) + '%';
    
    // Update patterns
    const patterns = data.summary.key_patterns || [];
    const patternsList = document.getElementById('patternsList');
    patternsList.innerHTML = '';
    
    if (patterns.length === 0) {
        patternsList.innerHTML = '<p style="color: #6b7280;">No significant patterns detected yet. Continue monitoring for insights.</p>';
    } else {
        patterns.forEach(pattern => {
            const item = document.createElement('div');
            item.className = 'pattern-item';
            item.innerHTML = `
                <strong>🔍 ${pattern.replace(/_/g, ' ').toUpperCase()}</strong>
                <p>Keep monitoring this pattern. We'll provide personalized recommendations as we learn more.</p>
            `;
            patternsList.appendChild(item);
        });
    }
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}h ${minutes}m`;
    }
    return `${minutes}m ${secs}s`;
}

// ============================================
// Demo Data & Simulation
// ============================================

function simulateEmotionalData() {
    // Simulate periodic updates for demo
    setInterval(() => {
        if (state.isMonitoring) {
            const mockEmotion = {
                dominant_emotion: ['happy', 'neutral', 'sad'][Math.floor(Math.random() * 3)],
                emotion: {
                    happy: Math.random() * 0.5,
                    neutral: Math.random() * 0.5,
                    sad: Math.random() * 0.3,
                    angry: Math.random() * 0.1,
                    fear: Math.random() * 0.1,
                    surprise: Math.random() * 0.1
                },
                confidence: 0.7 + Math.random() * 0.25
            };
            
            updateEmotionUI(mockEmotion, null);
        }
    }, 5000);
}

function simulateRecommendations() {
    const recommendations = [
        {
            name: 'Box Breathing Exercise',
            description: 'A 4-count breathing technique: Inhale (4), Hold (4), Exhale (4), Hold (4). Repeat 5 times.',
            duration: 120,
            category: 'breathing'
        },
        {
            name: 'Calming Music',
            description: 'Listen to lo-fi beats or ambient nature sounds to reduce stress.',
            duration: 300,
            category: 'music'
        },
        {
            name: 'Progressive Muscle Relaxation',
            description: 'Systematically tense and relax each muscle group from head to toe.',
            duration: 600,
            category: 'relaxation'
        }
    ];
    
    const container = document.getElementById('recommendationsGrid');
    container.innerHTML = '';
    
    document.getElementById('severityBadge').textContent = 'MODERATE';
    document.getElementById('severityBadge').className = 'severity-badge moderate';
    
    recommendations.forEach(rec => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.innerHTML = `
            <div class="recommendation-title">${rec.name}</div>
            <div class="recommendation-description">${rec.description}</div>
            <div class="recommendation-meta">
                <span class="recommendation-duration">⏱️ ${Math.round(rec.duration / 60)} min</span>
                <span style="cursor: pointer; color: #6366f1;" onclick="selectRecommendation('${rec.name}', '${rec.description}')">
                    Start →
                </span>
            </div>
        `;
        container.appendChild(card);
    });
}

function getDemoInsights() {
    return {
        session_duration: 1800,
        total_emotions_logged: 12,
        total_actions_triggered: 4,
        summary: {
            average_effectiveness: 0.75,
            key_patterns: ['sustained_high_stress', 'progressive_fatigue']
        }
    };
}

// ============================================
// Helper Functions
// ============================================

function updateDashboard() {
    // Update the dashboard with current emotional state
    document.getElementById('stressLevel').style.width = Math.random() * 60 + '%';
    document.getElementById('fatigueLevel').style.width = Math.random() * 50 + '%';
    document.getElementById('moodLevel').style.width = 50 + Math.random() * 50 + '%';
}

// Initialize dashboard on load
window.addEventListener('load', () => {
    updateDashboard();
    document.getElementById('statusBadge').textContent = '✓ Ready';
});
