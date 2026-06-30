"""
Vibe Coding Tutor - Scripts Package

This package contains the core logic for the Vibe Coding Tutor skill:
- state_manager: Persistent state in .vibe/ folder
- quiz_engine: MCQ generation with 4-option pattern
- curriculum: Elo-based adaptive difficulty
- feedback: Explanatory feedback generation
"""

from .state_manager import StateManager, VibeContext
from .quiz_engine import QuizEngine, MCQ, DecisionPoint, DecisionType
from .curriculum import CurriculumTracker, UserSkillModel
from .feedback import FeedbackGenerator, Feedback

__all__ = [
    "StateManager",
    "VibeContext",
    "QuizEngine",
    "MCQ",
    "DecisionPoint",
    "DecisionType",
    "CurriculumTracker",
    "UserSkillModel",
    "FeedbackGenerator",
    "Feedback",
]
