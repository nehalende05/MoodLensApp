"""
MoodLens Agentic AI System
Core agent logic for perception, reasoning, and autonomous action
"""

import json
import time
from datetime import datetime
from collections import deque
from typing import Dict, List, Tuple, Optional
import numpy as np

class EmotionBuffer:
    """Maintains a rolling buffer of emotional states for pattern detection"""
    def __init__(self, window_size=30):
        self.emotions = deque(maxlen=window_size)
        self.timestamps = deque(maxlen=window_size)
        
    def add(self, emotion_data: Dict):
        self.emotions.append(emotion_data)
        self.timestamps.append(datetime.now())
        
    def get_trend(self) -> Dict:
        """Analyze trend in emotions"""
        if len(self.emotions) < 5:
            return {"status": "insufficient_data"}
        
        emotions_list = list(self.emotions)
        emotions_array = np.array([list(e.values()) for e in emotions_list])
        
        trend = {
            "stress_trend": float(np.mean([e.get("stress", 0) for e in emotions_list])),
            "fatigue_trend": float(np.mean([e.get("fatigue", 0) for e in emotions_list])),
            "mood_trend": float(np.mean([e.get("mood", 0) for e in emotions_list])),
            "sample_count": len(self.emotions)
        }
        
        return trend

class MoodLensAgent:
    """
    Agentic AI system for mental wellness monitoring
    Implements perception → reasoning → action loop
    """
    
    def __init__(self):
        self.emotion_buffer = EmotionBuffer(window_size=30)
        self.session_start = datetime.now()
        self.recommendations_history = deque(maxlen=10)
        self.user_feedback_log = []
        
        # Agent state
        self.current_state = {
            "perceiving": False,
            "reasoning": False,
            "acting": False,
            "last_action": None,
            "last_action_time": None
        }
        
        # Reasoning rules
        self.action_thresholds = {
            "stress_high": 0.7,
            "fatigue_high": 0.6,
            "mood_low": 0.4,
            "critical_threshold": 0.8
        }
        
    def perceive(self, facial_data: Dict, voice_data: Dict) -> Dict:
        """
        PERCEPTION PHASE: Gather and interpret emotional signals
        """
        self.current_state["perceiving"] = True
        
        perception_result = {
            "facial": self._analyze_facial(facial_data),
            "voice": self._analyze_voice(voice_data),
            "timestamp": datetime.now().isoformat()
        }
        
        # Combine signals
        combined_emotion = self._fuse_signals(
            perception_result["facial"],
            perception_result["voice"]
        )
        
        self.emotion_buffer.add(combined_emotion)
        
        self.current_state["perceiving"] = False
        return perception_result
    
    def _analyze_facial(self, facial_data: Dict) -> Dict:
        """Analyze facial expressions"""
        emotions_map = facial_data.get("dominant_emotion", "neutral").lower()
        emotion_probs = facial_data.get("emotion", {})
        
        # Map emotions to mental health indicators
        analysis = {
            "primary_emotion": emotions_map,
            "stress": float(emotion_probs.get("angry", 0) + emotion_probs.get("fear", 0)) / 2,
            "fatigue": float(emotion_probs.get("sad", 0) * 0.6 + emotion_probs.get("neutral", 0) * 0.4),
            "mood": float(emotion_probs.get("happy", 0) * 0.8 + emotion_probs.get("surprise", 0) * 0.2),
            "confidence": float(facial_data.get("confidence", 0))
        }
        
        return analysis
    
    def _analyze_voice(self, voice_data: Dict) -> Dict:
        """Analyze voice characteristics"""
        analysis = {
            "intensity": float(voice_data.get("intensity", 0.5)),
            "pace": float(voice_data.get("pace", 0.5)),  # 0 = slow, 1 = fast
            "stress_indicators": self._detect_voice_stress(voice_data)
        }
        
        # Derive mental state from voice
        analysis["fatigue"] = 1 - analysis["intensity"]  # Lower intensity = more fatigue
        analysis["stress"] = min(1.0, (analysis["pace"] + voice_data.get("tremor", 0)) / 2)
        
        return analysis
    
    def _detect_voice_stress(self, voice_data: Dict) -> float:
        """Detect stress from voice characteristics"""
        tremor = voice_data.get("tremor", 0)  # Voice trembling
        pace = voice_data.get("pace", 0.5)
        
        # Fast pace + tremor = stress indicator
        stress = (tremor * 0.6 + abs(pace - 0.5) * 0.4)
        return float(min(1.0, stress))
    
    def _fuse_signals(self, facial: Dict, voice: Dict) -> Dict:
        """Fuse facial and voice signals for holistic emotion detection"""
        fused = {
            "stress": (facial["stress"] * 0.5 + voice["stress"] * 0.5),
            "fatigue": (facial["fatigue"] * 0.4 + voice["fatigue"] * 0.6),
            "mood": facial["mood"],
            "overall_confidence": (facial["confidence"] + voice.get("confidence", 0.5)) / 2
        }
        
        return fused
    
    def reason(self, perception: Dict) -> Dict:
        """
        REASONING PHASE: Interpret emotional state and decide on action
        Implements rule-based and contextual reasoning
        """
        self.current_state["reasoning"] = True
        
        # Get emotional trends
        trends = self.emotion_buffer.get_trend()
        
        if trends.get("status") == "insufficient_data":
            return {"decision": "monitor", "confidence": 0.0}
        
        # Contextual reasoning
        reasoning_output = {
            "detected_patterns": self._detect_patterns(trends),
            "severity_level": self._assess_severity(trends),
            "recommended_action_type": None,
            "reasoning": []
        }
        
        # Decision logic
        stress = trends.get("stress_trend", 0)
        fatigue = trends.get("fatigue_trend", 0)
        mood = trends.get("mood_trend", 0)
        
        # Rule-based reasoning
        if stress > self.action_thresholds["critical_threshold"]:
            reasoning_output["recommended_action_type"] = "emergency_support"
            reasoning_output["reasoning"].append("Critical stress levels detected - immediate support needed")
        elif stress > self.action_thresholds["stress_high"]:
            reasoning_output["recommended_action_type"] = "stress_relief"
            reasoning_output["reasoning"].append("High stress detected - recommend calming interventions")
        elif fatigue > self.action_thresholds["fatigue_high"]:
            reasoning_output["recommended_action_type"] = "energy_boost"
            reasoning_output["reasoning"].append("Fatigue detected - recommend energizing activities")
        elif mood < self.action_thresholds["mood_low"]:
            reasoning_output["recommended_action_type"] = "mood_lifting"
            reasoning_output["reasoning"].append("Low mood detected - recommend mood-lifting interventions")
        else:
            reasoning_output["recommended_action_type"] = "maintain"
            reasoning_output["reasoning"].append("Emotional state stable - continue monitoring")
        
        self.current_state["reasoning"] = False
        return reasoning_output
    
    def _detect_patterns(self, trends: Dict) -> List[str]:
        """Detect patterns in emotional data"""
        patterns = []
        
        if trends.get("stress_trend", 0) > 0.65:
            patterns.append("sustained_high_stress")
        if trends.get("fatigue_trend", 0) > 0.55:
            patterns.append("progressive_fatigue")
        if trends.get("mood_trend", 0) < 0.45:
            patterns.append("declining_mood")
        
        if len(self.emotion_buffer.emotions) > 10:
            recent_stress = [e.get("stress", 0) for e in list(self.emotion_buffer.emotions)[-5:]]
            if all(s > 0.6 for s in recent_stress):
                patterns.append("consistent_stress_spike")
        
        return patterns
    
    def _assess_severity(self, trends: Dict) -> str:
        """Assess severity level"""
        stress = trends.get("stress_trend", 0)
        fatigue = trends.get("fatigue_trend", 0)
        mood = trends.get("mood_trend", 0)
        
        # Weighted severity score
        severity_score = (stress * 0.4 + fatigue * 0.3 + (1 - mood) * 0.3)
        
        if severity_score > 0.75:
            return "critical"
        elif severity_score > 0.6:
            return "high"
        elif severity_score > 0.4:
            return "moderate"
        else:
            return "low"
    
    def act(self, reasoning: Dict) -> Dict:
        """
        ACTION PHASE: Autonomously recommend and execute support actions
        """
        self.current_state["acting"] = True
        
        action_type = reasoning.get("recommended_action_type")
        severity = reasoning.get("severity_level")
        
        actions = self._generate_actions(action_type, severity)
        
        action_result = {
            "action_type": action_type,
            "actions": actions,
            "priority": self._get_priority(severity),
            "timestamp": datetime.now().isoformat()
        }
        
        # Log action
        self.current_state["last_action"] = action_type
        self.current_state["last_action_time"] = datetime.now()
        self.recommendations_history.append(action_result)
        
        self.current_state["acting"] = False
        return action_result
    
    def _generate_actions(self, action_type: str, severity: str) -> List[Dict]:
        """Generate context-aware recommendations"""
        
        action_library = {
            "stress_relief": [
                {
                    "name": "Box Breathing Exercise",
                    "description": "Breathe in for 4, hold for 4, exhale for 4, hold for 4",
                    "duration": 120,
                    "category": "breathing",
                    "priority": "high"
                },
                {
                    "name": "Calming Music",
                    "description": "Listen to lo-fi beats or ambient sounds",
                    "duration": 300,
                    "category": "music",
                    "priority": "high"
                },
                {
                    "name": "Progressive Muscle Relaxation",
                    "description": "Tense and relax muscle groups sequentially",
                    "duration": 600,
                    "category": "relaxation",
                    "priority": "medium"
                }
            ],
            "energy_boost": [
                {
                    "name": "Quick Stretch Break",
                    "description": "Stand up and do 10 full-body stretches",
                    "duration": 300,
                    "category": "movement",
                    "priority": "high"
                },
                {
                    "name": "Energizing Music",
                    "description": "Play upbeat motivational music",
                    "duration": 300,
                    "category": "music",
                    "priority": "high"
                },
                {
                    "name": "Brief Walk",
                    "description": "Take a 5-minute walk to refresh",
                    "duration": 300,
                    "category": "movement",
                    "priority": "medium"
                }
            ],
            "mood_lifting": [
                {
                    "name": "Positive Affirmation",
                    "description": "Read personalized positive messages",
                    "duration": 120,
                    "category": "mindfulness",
                    "priority": "high"
                },
                {
                    "name": "Gratitude Reflection",
                    "description": "Think of 3 things you're grateful for",
                    "duration": 180,
                    "category": "mindfulness",
                    "priority": "high"
                },
                {
                    "name": "Uplifting Video",
                    "description": "Watch an inspirational or funny video",
                    "duration": 600,
                    "category": "media",
                    "priority": "medium"
                }
            ],
            "emergency_support": [
                {
                    "name": "Crisis Breathing",
                    "description": "Follow guided crisis breathing technique",
                    "duration": 300,
                    "category": "breathing",
                    "priority": "critical"
                },
                {
                    "name": "Grounding Technique",
                    "description": "Practice 5-4-3-2-1 sensory awareness exercise",
                    "duration": 600,
                    "category": "mindfulness",
                    "priority": "critical"
                },
                {
                    "name": "Professional Help",
                    "description": "Consider reaching out to a mental health professional",
                    "duration": 0,
                    "category": "professional",
                    "priority": "critical"
                }
            ],
            "maintain": [
                {
                    "name": "Daily Gratitude",
                    "description": "Maintain emotional balance with gratitude",
                    "duration": 300,
                    "category": "mindfulness",
                    "priority": "low"
                }
            ]
        }
        
        actions = action_library.get(action_type, action_library["maintain"])
        
        # Filter by severity
        severity_filter = {
            "critical": ["critical", "high"],
            "high": ["high", "medium"],
            "moderate": ["medium", "low"],
            "low": ["low"]
        }
        
        allowed_priorities = severity_filter.get(severity, ["low"])
        filtered_actions = [a for a in actions if a["priority"] in allowed_priorities]
        
        return filtered_actions[:3]  # Return top 3 recommendations
    
    def _get_priority(self, severity: str) -> int:
        """Convert severity to priority level"""
        priority_map = {
            "critical": 1,
            "high": 2,
            "moderate": 3,
            "low": 4
        }
        return priority_map.get(severity, 4)
    
    def learn_from_feedback(self, action_id: str, user_feedback: Dict):
        """
        LEARNING PHASE: Adapt based on user feedback
        """
        feedback_entry = {
            "action_id": action_id,
            "feedback": user_feedback,
            "timestamp": datetime.now().isoformat()
        }
        self.user_feedback_log.append(feedback_entry)
        
        # Implement learning (could adjust thresholds or weights)
        effectiveness = user_feedback.get("effectiveness", 0)  # 0-1 scale
        if effectiveness > 0.7:
            # Action was effective, could increase its priority in future
            pass
        elif effectiveness < 0.3:
            # Action was not effective, could deprioritize
            pass
    
    def get_session_summary(self) -> Dict:
        """Generate session summary and insights"""
        if not self.emotion_buffer.emotions:
            return {"status": "no_data"}
        
        trends = self.emotion_buffer.get_trend()
        
        summary = {
            "session_duration": (datetime.now() - self.session_start).total_seconds(),
            "emotional_trends": trends,
            "interventions_provided": len(self.recommendations_history),
            "average_effectiveness": self._calculate_avg_effectiveness(),
            "key_patterns": self._detect_patterns(trends),
            "recommendations_for_next_session": self._generate_future_recommendations()
        }
        
        return summary
    
    def _calculate_avg_effectiveness(self) -> float:
        """Calculate average effectiveness of interventions"""
        if not self.user_feedback_log:
            return 0.5
        
        effectiveness_scores = [f.get("feedback", {}).get("effectiveness", 0.5) 
                               for f in self.user_feedback_log]
        return sum(effectiveness_scores) / len(effectiveness_scores)
    
    def _generate_future_recommendations(self) -> List[str]:
        """Generate recommendations for future sessions"""
        trends = self.emotion_buffer.get_trend()
        recommendations = []
        
        if trends.get("stress_trend", 0) > 0.6:
            recommendations.append("Consider regular stress-management practices")
        if trends.get("fatigue_trend", 0) > 0.5:
            recommendations.append("Ensure adequate rest and sleep")
        if trends.get("mood_trend", 0) < 0.5:
            recommendations.append("Consider social interaction or professional support")
        
        return recommendations
    
    def process_cycle(self, facial_data: Dict, voice_data: Dict) -> Dict:
        """
        Complete perception → reasoning → action cycle
        """
        # Phase 1: PERCEIVE
        perception = self.perceive(facial_data, voice_data)
        
        # Phase 2: REASON
        reasoning = self.reason(perception)
        
        # Phase 3: ACT
        action = self.act(reasoning)
        
        # Return complete agent state
        return {
            "perception": perception,
            "reasoning": reasoning,
            "action": action,
            "agent_state": self.current_state.copy(),
            "timestamp": datetime.now().isoformat()
        }
